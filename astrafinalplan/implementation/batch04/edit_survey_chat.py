from pathlib import Path
import re,json
B=Path('astrafinalplan/implementation/batch04')
for n in range(62,67):
 root=B/'stage'/str(n)
 p=root/'server/package.json';d=json.loads(p.read_text());d['scripts']['start']='node dist/src/index.js';p.write_text(json.dumps(d,indent=2)+'\n')
 for p in (root/'server/src/routes').glob('*.ts'):
  s=p.read_text()
  if 'controller.' not in s:continue
  s='import type { RequestHandler } from "express";\n'+s
  s=re.sub(r'(, )(controller\.\w+)(\);)',r'\1wrap(\2)\3',s)
  s+='\nfunction wrap(handler: RequestHandler): RequestHandler {return (req,res,next)=>{Promise.resolve(handler(req,res,next)).catch(next);};}\n';p.write_text(s)
p=B/'stage/62/server/src/models/surveyModel.ts';s=p.read_text().replace('listQuestions(surveyId: number)','listQuestions(surveyId: number, connection: Knex | Knex.Transaction = db)').replace('const questions = await db("questions")','const questions = await connection("questions")').replace('const options = await db("question_options")','const options = await connection("question_options")');p.write_text(s)
p=B/'stage/62/server/src/services/surveyService.ts';s=p.read_text();s=s.replace('  if (survey.status !== "active") throw new ValidationError("Survey is not accepting responses");\n  if (survey.max_responses && survey.response_count >= survey.max_responses) throw new ValidationError("Survey response limit reached");','  assertAccepting(survey);');start=s.index('function buildAnswerRows(');end=s.index('/** Aggregates answers',start)
s=s[:start]+'''function buildAnswerRows(questions: Array<Record<string, any>>, answers: Record<string, unknown>) {
  if (!answers || typeof answers !== "object" || Array.isArray(answers)) throw new ValidationError("Answers must be an object");
  const known = new Set(questions.map(q => String(q.id)));
  if (Object.keys(answers).some(key => !known.has(key))) throw new ValidationError("Unknown question");
  return questions.map(question => {
    const value = answers[String(question.id)];
    const base = {question_id: question.id};
    const blank = value == null || (typeof value === "string" && !value.trim()) || (Array.isArray(value) && !value.length);
    if (blank) {if (question.is_required) throw new ValidationError(`Missing answer for ${question.title}`); return {...base, answer_text: null};}
    const invalid = () => new ValidationError(`Invalid answer for ${question.title}`);
    if (["single_choice", "yes_no"].includes(question.question_type)) {
      const option = question.options.find((item:any) => item.label === value);
      if (!option && !(question.question_type === "yes_no" && ["Yes","No"].includes(value as string))) throw invalid();
      return {...base, selected_option_id: option?.id ?? null, answer_text: value};
    }
    if (question.question_type === "multi_choice") {
      if (!Array.isArray(value) || value.some(label => typeof label !== "string" || !question.options.some((o:any)=>o.label===label))) throw invalid();
      const labels = [...new Set(value)];
      return {...base, selected_option_ids: question.options.filter((o:any)=>labels.includes(o.label)).map((o:any)=>o.id), answer_text:labels.join("; ")};
    }
    if (question.question_type === "rating") {
      if ((typeof value !== "string" && typeof value !== "number") || !Number.isInteger(Number(value)) || Number(value) < (question.config?.min ?? 1) || Number(value) > (question.config?.max ?? 5)) throw invalid();
      return {...base, rating_value: Number(value)};
    }
    if (question.question_type === "matrix") {
      if (typeof value !== "object" || Array.isArray(value)) throw invalid();
      const entries = Object.entries(value as object), rows = question.config?.rows ?? [], columns = question.config?.columns ?? [];
      if (entries.some(([row,column])=>!rows.includes(row)||!columns.includes(column)) || (question.is_required && rows.some((row:string)=>!(row in (value as object))))) throw invalid();
      return {...base, matrix_answers: value};
    }
    if (typeof value !== "string" && typeof value !== "number") throw invalid();
    if (String(value).length > 20000) throw invalid();
    if (question.question_type === "number" && !Number.isFinite(Number(value))) throw invalid();
    if (question.question_type === "date" && (!/^\\d{4}-\\d{2}-\\d{2}$/.test(String(value)) || !Number.isFinite(Date.parse(String(value))) || new Date(String(value)).toISOString().slice(0,10)!==value)) throw invalid();
    return {...base, answer_text: String(value)};
  });
}

function assertAccepting(survey: any) {
  if (survey.status !== "active") throw new ValidationError("Survey is not accepting responses");
  const now = Date.now();
  if (survey.start_date && new Date(survey.start_date).getTime() > now) throw new ValidationError("Survey has not opened yet");
  if (survey.end_date && new Date(survey.end_date).getTime() <= now) throw new ValidationError("Survey has closed");
  if (survey.max_responses && survey.response_count >= survey.max_responses) throw new ValidationError("Survey response limit reached");
}

/** Lock the survey before checking capacity; the answer rows and counter commit together. */
export async function submitResponse(token: string, ip: string | undefined, body: {accessCode?: string; answers: Record<string, unknown>}) {
  return db.transaction(async trx => {
    const survey = await trx("surveys").where({public_token:token}).forUpdate().first();
    if (!survey) throw new NotFoundError("Survey not found");
    assertAccepting(survey);
    if (survey.access_code && body.accessCode !== survey.access_code) throw new ValidationError("Invalid access code");
    const questions = await surveys.listQuestions(survey.id,trx);
    return surveys.createResponse(trx,survey.id,ip,buildAnswerRows(questions,body.answers));
  });
}

'''+s[end:];p.write_text(s)
# Guard conversation and message routes centrally so history, polling, typing,
# reactions and writes all use the same membership rule.
p=B/'stage/63/server/src/routes/chatRoutes.ts';s=p.read_text();marker='export const chatRouter = Router();';s=s.replace(marker,marker+'''
chatRouter.use(async (req,res,next) => {
  try {
    const user = Number(req.header("x-demo-user-id") ?? process.env.DEMO_USER_ID ?? 1);
    if (!Number.isSafeInteger(user) || user < 1) throw new ValidationError("Invalid demo user id");
    const match = /^\\/(conversations|messages)\\/(\\d+)(?:\\/|$)/.exec(req.path);
    if (!match) return next();
    const id = Number(match[2]);
    const message = match[1] === "messages" ? await db("messages").where({id}).whereNull("deleted_at").first() : null;
    if (match[1] === "messages" && !message) throw new NotFoundError("Message not found");
    const conversationId = message?.conversation_id ?? id;
    const member = await db("conversation_members").where({conversation_id:conversationId,user_id:user}).first();
    if (!member) throw new NotFoundError("Conversation not found");
    const managesGroup = match[1] === "conversations" && ((req.method === "PUT" && /^\\/conversations\\/\\d+$/.test(req.path)) || req.path.includes("/members"));
    if (managesGroup && member.role !== "admin") throw new ValidationError("Only group admins may manage this conversation");
    if (req.path.endsWith("/read") && req.method === "POST") {
      const read = await db("messages").where({id:req.body.messageId,conversation_id:conversationId}).first();
      if (!read) throw new ValidationError("Read receipt must reference this conversation");
    }
    next();
  } catch(error) {next(error);}
});
''');s='import {db} from "../config/db.js";\nimport {NotFoundError,ValidationError} from "../middleware/errors.js";\n'+s;p.write_text(s)
p=B/'stage/63/server/src/services/chatService.ts';s=p.read_text().replace('[userId, ...memberIds], userId','[...new Set([userId, ...memberIds])], userId');p.write_text(s)
