from pathlib import Path
S=Path(__file__).resolve().parent/'stage'/'19856a4178bf'
def put(name,text):
 p=S/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text.strip()+'\n',encoding='utf-8')
put('server/src/lib/outbox.js',r'''
const { v4: uuidv4 } = require('uuid');
const db = require('../db/database');

function stageQueueJob({ queueName = 'email', jobName = 'send-email', data, attempts = 4, backoffMs = 2000, jobId = uuidv4() }) {
  const options = {
    jobId, attempts, backoff: { type: 'exponential', delay: backoffMs },
    // Keep IDs available for deduplication if enqueue succeeds but its acknowledgement is lost.
    removeOnComplete: false, removeOnFail: false
  };
  db.prepare(`INSERT INTO queue_outbox (id, queue_name, job_name, payload_json, options_json, created_at)
    VALUES (?, ?, ?, ?, ?, ?)`).run(jobId, queueName, jobName, JSON.stringify(data), JSON.stringify(options), new Date().toISOString());
  return jobId;
}

function pendingDispatchCount() {
  return db.prepare('SELECT COUNT(*) AS n FROM queue_outbox WHERE dispatched_at IS NULL').get().n;
}

function createOutboxDispatcher({ queues, isReady = () => true, batchSize = 100 }) {
  let running = false;
  async function flush() {
    if (running || !isReady()) return { dispatched: 0, failed: 0, pending: pendingDispatchCount() };
    running = true;
    let dispatched = 0, failed = 0;
    try {
      const rows = db.prepare(`SELECT * FROM queue_outbox WHERE dispatched_at IS NULL
        ORDER BY created_at, id LIMIT ?`).all(batchSize);
      for (const row of rows) {
        if (!isReady()) break;
        try {
          const queue = queues[row.queue_name];
          if (!queue) throw new Error('Unknown outbox queue');
          await queue.add(row.job_name, JSON.parse(row.payload_json), JSON.parse(row.options_json));
          db.transaction(() => {
            const now = new Date().toISOString();
            db.prepare(`UPDATE queue_outbox SET dispatched_at = ?, dispatch_attempts = dispatch_attempts + 1, last_error = NULL
              WHERE id = ? AND dispatched_at IS NULL`).run(now, row.id);
            // A fast worker may already be active/completed before add() returns.
            db.prepare(`UPDATE campaign_jobs SET status = 'queued', updated_at = ?
              WHERE queue_job_id = ? AND status = 'pending'`).run(now, row.id);
          })();
          dispatched++;
        } catch (error) {
          db.prepare(`UPDATE queue_outbox SET dispatch_attempts = dispatch_attempts + 1, last_error = ?
            WHERE id = ? AND dispatched_at IS NULL`).run(String(error.message || error).slice(0, 1000), row.id);
          failed++;
        }
      }
      return { dispatched, failed, pending: pendingDispatchCount() };
    } finally {
      running = false;
    }
  }
  return { flush };
}

function startOutboxDispatch(options, { intervalMs = 1000, logger = console } = {}) {
  const dispatcher = createOutboxDispatcher(options);
  const tick = () => { void dispatcher.flush().catch(error => logger.error('[outbox] dispatch failed', error)); };
  tick();
  const timer = setInterval(tick, intervalMs);
  timer.unref();
  return { flush: dispatcher.flush, stop: () => clearInterval(timer) };
}

module.exports = { stageQueueJob, pendingDispatchCount, createOutboxDispatcher, startOutboxDispatch };
''')
put('server/src/lib/campaignCommands.js',r'''
const { v4: uuidv4 } = require('uuid');
const db = require('../db/database');
const { stageQueueJob } = require('./outbox');

class CommandError extends Error {
  constructor(status, message) { super(message); this.status = status; }
}

function stageEmail(data, maxAttempts, backoffMs, jobName = 'send-email') {
  const id = stageQueueJob({ data, attempts: maxAttempts, backoffMs, jobName });
  const now = new Date().toISOString();
  db.prepare(`INSERT INTO campaign_jobs (campaign_id, queue_job_id, recipient_email, status, attempts_made,
    max_attempts, created_at, updated_at) VALUES (?, ?, ?, 'pending', 0, ?, ?, ?)`)
    .run(data.campaignId, id, data.recipientEmail, maxAttempts, now, now);
  return id;
}

// Call with the validated campaign contract. All recipient tracking and dispatch intent commit together.
function persistCampaign(data) {
  const recipients = Array.from(new Set(data.recipients.map(value => value.trim().toLowerCase())));
  const campaignId = uuidv4();
  const now = new Date().toISOString();
  const failRate = data.failRate ?? 0.25;
  const maxAttempts = data.maxAttempts ?? 4;
  const backoffMs = data.backoffMs ?? 2000;
  db.transaction(() => {
    db.prepare(`INSERT INTO campaigns (id, name, subject, body, recipient_count, created_at)
      VALUES (?, ?, ?, ?, ?, ?)`).run(campaignId, data.campaignName, data.subject, data.body, recipients.length, now);
    for (const recipientEmail of recipients) stageEmail({
      campaignId, campaignName: data.campaignName, recipientEmail, subject: data.subject, body: data.body, failRate
    }, maxAttempts, backoffMs);
  })();
  return { id: campaignId, name: data.campaignName, subject: data.subject, recipientCount: recipients.length,
    failRate, maxAttempts, backoffMs, createdAt: now, dispatchStatus: 'pending' };
}

function requeueDeadLetter(id) {
  return db.transaction(() => {
    const deadLetter = db.prepare('SELECT * FROM dead_letters WHERE id = ?').get(id);
    if (!deadLetter) throw new CommandError(404, 'Dead letter not found');
    if (deadLetter.resolved) throw new CommandError(409, 'Dead letter already has a requeue request');
    const payload = JSON.parse(deadLetter.payload);
    const jobId = stageEmail({ campaignId: payload.campaignId, campaignName: payload.campaignName,
      recipientEmail: payload.recipientEmail, subject: payload.subject, body: payload.body, failRate: payload.failRate
    }, payload.maxAttempts ?? 4, payload.backoffMs ?? 2000, 'send-email-requeue');
    db.prepare('UPDATE dead_letters SET resolved = 1, resolved_at = ? WHERE id = ?')
      .run(new Date().toISOString(), id);
    return jobId;
  }).immediate();
}

module.exports = { CommandError, persistCampaign, requeueDeadLetter };
''')
put('server/src/workers/jobProjection.js',r'''
const db = require('../db/database');
const { stageQueueJob } = require('../lib/outbox');

function requireTrackedJob(job) {
  const row = db.prepare('SELECT campaign_id FROM campaign_jobs WHERE queue_job_id = ?').get(String(job.id));
  if (!row || row.campaign_id !== job.data.campaignId) throw new Error('Job tracking row is missing or belongs to another campaign');
}

function writeStatus(job, status, error, result, terminal) {
  requireTrackedJob(job);
  const now = new Date().toISOString();
  db.prepare(`UPDATE campaign_jobs SET status = ?, attempts_made = ?, error_message = ?, result_payload = ?,
    updated_at = ?, processed_at = ? WHERE queue_job_id = ?`)
    .run(status, job.attemptsMade, error, result == null ? null : JSON.stringify(result), now, terminal ? now : null, String(job.id));
}

function recordActive(job) { writeStatus(job, 'active', null, null, false); }
function recordCompleted(job, result) { writeStatus(job, 'completed', null, result, true); }
function recordFailure(job, error) {
  const maxAttempts = job.opts.attempts || 1;
  const terminal = job.attemptsMade >= maxAttempts;
  const reason = error?.message || 'Unknown worker error';
  db.transaction(() => {
    writeStatus(job, terminal ? 'failed' : 'retrying', reason, null, terminal);
    if (!terminal) return;
    const payload = { ...job.data, maxAttempts,
      backoffMs: typeof job.opts.backoff === 'object' ? job.opts.backoff.delay : 2000 };
    const inserted = db.prepare(`INSERT OR IGNORE INTO dead_letters
      (original_queue_job_id, campaign_id, recipient_email, reason, payload, resolved, created_at)
      VALUES (?, ?, ?, ?, ?, 0, ?)`).run(String(job.id), payload.campaignId, payload.recipientEmail,
        reason, JSON.stringify(payload), new Date().toISOString());
    if (inserted.changes) stageQueueJob({ queueName: 'dead-letter', jobName: 'dead-letter-email',
      data: { originalQueueJobId: String(job.id), ...payload, reason } });
  })();
}

module.exports = { requireTrackedJob, recordActive, recordCompleted, recordFailure };
''')
put('server/src/workers/emailWorker.js',r'''
const { Worker } = require('bullmq');
const config = require('../lib/config');
const { connection } = require('../lib/redis');
const { QUEUE_NAMES, emailQueue, deadLetterQueue } = require('../queues');
const { simulateEmailSend } = require('./emailProcessor');
const { requireTrackedJob, recordActive, recordCompleted, recordFailure } = require('./jobProjection');
const { startOutboxDispatch } = require('../lib/outbox');

const dispatcher = startOutboxDispatch({ queues: { email: emailQueue, 'dead-letter': deadLetterQueue },
  isReady: () => connection.status === 'ready' });
const worker = new Worker(QUEUE_NAMES.EMAIL, async job => {
  requireTrackedJob(job);
  // This is a simulation; no SMTP provider or real email is contacted.
  return simulateEmailSend(job.data);
}, { connection, concurrency: config.workerConcurrency });

worker.on('ready', () => console.log(`[worker] started for ${QUEUE_NAMES.EMAIL} with concurrency=${config.workerConcurrency}`));
function project(action) {
  return (job, value) => {
    if (!job) return;
    try { action(job, value); }
    catch (error) { console.error('[worker] status projection failed:', error.message); }
  };
}
worker.on('active', project(recordActive));
worker.on('completed', project(recordCompleted));
worker.on('failed', project(recordFailure));
worker.on('error', error => console.error('[worker] error:', error.message));

async function shutdown() {
  dispatcher.stop();
  await worker.close();
  process.exit(0);
}
process.on('SIGINT', shutdown);
process.on('SIGTERM', shutdown);
''')
p=S/'server/src/lib/validation.js';t=p.read_text();t=t.replace('    return res.status(400).json({','    res.status(400).json({',1);t=t.replace('    });\n  }\n\n  return parsed.data;','    });\n    return null;\n  }\n\n  return parsed.data;',1);p.write_text(t)
print('Durable dispatch and worker projection services staged')
