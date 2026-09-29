from pathlib import Path
S=Path(__file__).resolve().parent/'stage'/'22be3051241f'
p=S/'server/src/lib/validation.js';t=p.read_text();needle='function validateOrRespond';at=t.index(needle);t=t[:at]+'''const joinRoomSchema = sessionSchema.extend({ roomId: z.string().uuid() });
const attachmentSchema = z.object({
  url: z.string().regex(/^\\/uploads\\/[A-Za-z0-9][A-Za-z0-9._-]*$/),
  filename: z.string().min(1).max(255),
  mimeType: z.string().min(1).max(150),
  size: z.number().int().min(0).max(10 * 1024 * 1024)
});
const sendMessageSchema = joinRoomSchema.extend({
  content: z.string().trim().max(8000).default(''),
  attachment: attachmentSchema.nullable().optional()
}).refine(value => value.content || value.attachment, { message: 'Message content or attachment required' });
const typingSchema = z.object({ roomId: z.string().uuid(), userId: z.string().uuid(), isTyping: z.boolean() });
const markReadSchema = z.object({ roomId: z.string().uuid(), userId: z.string().uuid(), uptoMessageId: z.string().uuid() });
const watchAgentSchema = sessionSchema.pick({ userId: true, name: true });

'''+t[at:];t=t.replace('  sessionSchema,','  joinRoomSchema,\n  sendMessageSchema,\n  typingSchema,\n  markReadSchema,\n  watchAgentSchema,\n  sessionSchema,');p.write_text(t)
p=S/'server/src/socket.js';p.write_text(r'''const { v4: uuidv4 } = require('uuid');
const db = require('./db/database');
const { ensureUser, ensureParticipant, getRoom, getMessages } = require('./lib/chatService');
const { joinRoomSchema, sendMessageSchema, typingSchema, markReadSchema, watchAgentSchema } = require('./lib/validation');

function createSocketServer(io, { logger = console } = {}) {
  // Unique users are counted, but every connection owns its own presence reference.
  const onlineByRoom = new Map();
  const socketState = new Map();
  const insertMessage = db.prepare(`INSERT INTO messages (id, room_id, sender_id, content, attachment_json, created_at)
    VALUES (?, ?, ?, ?, ?, ?)`);
  const updateRoom = db.prepare('UPDATE rooms SET updated_at = ? WHERE id = ?');
  const markRead = db.prepare(`INSERT INTO read_receipts (message_id, user_id, read_at) VALUES (?, ?, ?)
    ON CONFLICT(message_id, user_id) DO UPDATE SET read_at = excluded.read_at`);

  function emitPresence(roomId) {
    const entries = Array.from(onlineByRoom.get(roomId)?.values() || []);
    // Keep the existing wire representation; internal ownership never parses this string.
    io.to(roomId).emit('room_presence', {
      roomId, onlineUsers: entries.map(({ user }) => `${user.userId}|${user.name}|${user.role}`), onlineCount: entries.length
    });
  }

  function addPresence(roomId, state, socketId) {
    if (!onlineByRoom.has(roomId)) onlineByRoom.set(roomId, new Map());
    const users = onlineByRoom.get(roomId);
    if (!users.has(state.userId)) users.set(state.userId, { user: state, sockets: new Set() });
    users.get(state.userId).sockets.add(socketId);
  }

  function removePresence(roomId, userId, socketId) {
    const users = onlineByRoom.get(roomId);
    const entry = users?.get(userId);
    if (!entry) return;
    entry.sockets.delete(socketId);
    if (entry.sockets.size === 0) users.delete(userId);
    if (users.size === 0) onlineByRoom.delete(roomId);
  }

  function bindIdentity(socket, identity) {
    const current = socketState.get(socket.id);
    if (current) {
      if (current.userId !== identity.userId || current.name !== identity.name || current.role !== identity.role)
        return null;
      return current;
    }
    const state = { ...identity, roomIds: new Set() };
    socketState.set(socket.id, state);
    return state;
  }

  function joinedState(socket, payload) {
    const state = socketState.get(socket.id);
    return state && state.userId === payload.userId && state.roomIds.has(payload.roomId) ? state : null;
  }

  const saveMessage = db.transaction((state, payload) => {
    const messageId = uuidv4();
    const now = new Date().toISOString();
    insertMessage.run(messageId, payload.roomId, state.userId, payload.content || null,
      payload.attachment ? JSON.stringify(payload.attachment) : null, now);
    updateRoom.run(now, payload.roomId);
    markRead.run(messageId, state.userId, now);
    const message = db.prepare(`SELECT m.*, u.name AS sender_name, u.role AS sender_role,
      (SELECT COUNT(*) FROM read_receipts rr WHERE rr.message_id = m.id AND rr.user_id != m.sender_id) AS read_count
      FROM messages m JOIN users u ON u.id = m.sender_id WHERE m.id = ?`).get(messageId);
    return { ...message, attachment: message.attachment_json ? JSON.parse(message.attachment_json) : null };
  });

  io.on('connection', socket => {
    function reject(ack, message) {
      if (ack) ack({ ok: false, error: message });
      else socket.emit('server_error', { message });
    }
    function onValidated(event, schema, handler) {
      socket.on(event, (payload, callback) => {
        const ack = typeof callback === 'function' ? callback : null;
        try {
          const parsed = schema.safeParse(payload);
          if (!parsed.success) return reject(ack, 'Invalid event payload');
          handler(parsed.data, ack);
        } catch (error) {
          logger.error(`Chat ${event} failed`, error);
          reject(ack, 'Unable to complete chat operation');
        }
      });
    }

    onValidated('join_room', joinRoomSchema, (payload, ack) => {
      if (!getRoom(payload.roomId)) return reject(ack, 'Room not found');
      const state = bindIdentity(socket, { userId: payload.userId, name: payload.name, role: payload.role });
      if (!state) return reject(ack, 'Reconnect before changing demo identity');
      const alreadyJoined = state.roomIds.has(payload.roomId);
      if (!alreadyJoined) {
        db.transaction(() => {
          ensureUser(state.userId, state.name, state.role);
          ensureParticipant(payload.roomId, state.userId);
        })();
        socket.join(payload.roomId);
        state.roomIds.add(payload.roomId);
        addPresence(payload.roomId, state, socket.id);
        emitPresence(payload.roomId);
      }
      const result = { roomId: payload.roomId, messages: getMessages(payload.roomId, { limit: 50 }) };
      socket.emit('joined_room', result);
      if (ack) ack({ ok: true, ...result });
    });

    onValidated('typing', typingSchema, (payload, ack) => {
      const state = joinedState(socket, payload);
      if (!state) return reject(ack, 'Join this room before sending events');
      socket.to(payload.roomId).emit('typing_update', {
        roomId: payload.roomId, userId: state.userId, name: state.name, isTyping: payload.isTyping
      });
      if (ack) ack({ ok: true });
    });

    onValidated('send_message', sendMessageSchema, (payload, ack) => {
      const state = joinedState(socket, payload);
      if (!state || state.name !== payload.name || state.role !== payload.role)
        return reject(ack, 'Join this room with the same demo identity before sending');
      const message = saveMessage(state, payload);
      // Only committed records are broadcast or acknowledged as successful.
      io.to(payload.roomId).emit('new_message', message);
      io.to('agents').emit('conversation_updated', { roomId: payload.roomId });
      if (ack) ack({ ok: true, message });
    });

    onValidated('mark_read', markReadSchema, (payload, ack) => {
      const state = joinedState(socket, payload);
      if (!state) return reject(ack, 'Join this room before sending events');
      const target = db.prepare('SELECT rowid AS sequence, created_at FROM messages WHERE id = ? AND room_id = ?')
        .get(payload.uptoMessageId, payload.roomId);
      if (!target) return reject(ack, 'Message not found in this room');
      const rows = db.prepare(`SELECT id FROM messages WHERE room_id = ?
        AND (created_at < ? OR (created_at = ? AND rowid <= ?))`)
        .all(payload.roomId, target.created_at, target.created_at, target.sequence);
      const now = new Date().toISOString();
      db.transaction(() => { for (const row of rows) markRead.run(row.id, state.userId, now); })();
      io.to(payload.roomId).emit('read_update', { roomId: payload.roomId, userId: state.userId, uptoMessageId: payload.uptoMessageId });
      if (ack) ack({ ok: true });
    });

    onValidated('watch_as_agent', watchAgentSchema, (payload, ack) => {
      const user = db.prepare('SELECT id, name, role FROM users WHERE id = ?').get(payload.userId);
      if (!user || user.role !== 'agent' || user.name !== payload.name)
        return reject(ack, 'An agent demo session is required');
      const state = bindIdentity(socket, { userId: user.id, name: user.name, role: user.role });
      if (!state) return reject(ack, 'Reconnect before changing demo identity');
      socket.join('agents');
      if (ack) ack({ ok: true });
    });

    socket.on('disconnect', () => {
      const state = socketState.get(socket.id);
      socketState.delete(socket.id);
      if (!state) return;
      for (const roomId of state.roomIds) {
        removePresence(roomId, state.userId, socket.id);
        emitPresence(roomId);
      }
    });
  });

  return { getOnlineCount: roomId => onlineByRoom.get(roomId)?.size || 0 };
}

module.exports = { createSocketServer };
''')
p=S/'server/src/lib/chatService.js';t=p.read_text();t=t.replace('ORDER BY m.created_at DESC','ORDER BY m.created_at DESC, m.rowid DESC');t=t.replace('// Room list endpoint returns a precomputed summary so clients don\'t issue N+1 message queries.','// One browser request returns summaries; this implementation still executes per-room SQL queries.');p.write_text(t)
print('Chat presence, event validation, identity binding, transactions and receipt ordering staged')
