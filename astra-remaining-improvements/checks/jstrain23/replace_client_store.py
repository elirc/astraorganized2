from pathlib import Path
import hashlib,json
B=Path(__file__).resolve().parents[2];S=B/'stage/58c5c289a8ce'
baseline=json.loads((B/'baselines/58c5c289a8ce.json').read_text(encoding='utf-8'))['files']
p=S/'src/lib/workspaceStore.js';assert hashlib.sha256(p.read_bytes()).hexdigest()==baseline['src/lib/workspaceStore.js']
p.write_text('''"use client";
import {create} from "zustand";
import {applyMutation,documentFrom} from "./workspaceMutations.mjs";

const emptyDocument=()=>({meta:{},users:[],pages:[],blocksByPage:{},commentThreads:[],comments:[],templates:[],favorites:[],recent:[],sharedLinks:[],versions:[],activities:[],trash:[]});
export const useWorkspaceStore=create((set,get)=>{
  const apply=(action,input)=>set(local=>{
    try {
      const {state,result}=applyMutation(documentFrom(local),action,input,local.currentUserId);
      const valid=state.pages.some(page=>page.id===local.activePageId&&!page.isDeleted);
      const activePageId=result?.pageId??(valid?local.activePageId:state.pages.find(page=>!page.isDeleted)?.id??"");
      return {...state,error:"",activePageId,selectedBlockId:result?.blockId??local.selectedBlockId,
        expandedPageIds:{...local.expandedPageIds,...(result?.pageId?{[result.pageId]:true}:{}),...(input?.parentId?{[input.parentId]:true}:{})}};
    } catch(error){return {error:error.message};}
  });
  const replace=(state,preserveActive=true)=>set(local=>{
    const document=structuredClone(state),first=document.pages.find(page=>!page.isDeleted)?.id??"";
    return {...document,workspaceId:document.meta.workspaceId,currentUserId:document.meta.ownerId,loaded:true,loading:false,error:"",
      activePageId:preserveActive&&document.pages.some(page=>page.id===local.activePageId&&!page.isDeleted)?local.activePageId:first,
      expandedPageIds:{...Object.fromEntries(document.pages.filter(page=>page.parentId===null).map(page=>[page.id,true])),...local.expandedPageIds}};
  });
  return {
    ...emptyDocument(),workspaceId:"workspace-default",currentUserId:"user-owner",loaded:false,loading:false,error:"",activePageId:"",selectedBlockId:"",
    expandedPageIds:{},presence:{},typing:{},versionsByPage:{},commandPaletteOpen:false,commandPaletteQuery:"",showDeleted:false,
    reset:()=>set({...emptyDocument(),loaded:false,loading:false,error:"",activePageId:"",selectedBlockId:"",presence:{},typing:{},versionsByPage:{},expandedPageIds:{},commandPaletteOpen:false,commandPaletteQuery:"",showDeleted:false}),
    hydrateWorkspace:(_workspaceId,state)=>replace(state,false),replaceDocument:state=>replace(state,true),
    setLoading:loading=>set({loading}),setError:error=>set({error}),
    setActivePage:pageId=>set(local=>local.pages.some(page=>page.id===pageId&&!page.isDeleted)?{activePageId:pageId,recent:[pageId,...local.recent.filter(id=>id!==pageId)].slice(0,40),commandPaletteOpen:false,commandPaletteQuery:""}:{error:"Active page not found"}),
    toggleExpandPage:pageId=>set(local=>({expandedPageIds:{...local.expandedPageIds,[pageId]:!local.expandedPageIds[pageId]}})),
    setCommandPaletteOpen:commandPaletteOpen=>set({commandPaletteOpen}),setCommandPaletteQuery:commandPaletteQuery=>set({commandPaletteQuery}),setSelectedBlock:selectedBlockId=>set({selectedBlockId}),setShowDeleted:showDeleted=>set({showDeleted}),
    createPage:input=>apply("createPage",input),updatePage:(pageId,patch)=>apply("updatePage",{pageId,patch}),movePage:(pageId,parentId)=>apply("movePage",{pageId,parentId}),
    toggleFavorite:pageId=>apply("toggleFavorite",{pageId}),softDeletePage:pageId=>apply("trashPage",{pageId}),restorePage:pageId=>apply("restorePage",{pageId}),
    addBlock:input=>apply("addBlock",input),updateBlock:input=>apply("updateBlock",input),removeBlock:input=>apply("removeBlock",input),reorderBlocks:input=>apply("reorderBlocks",input),
    createThread:input=>apply("createThread",input),replyThread:input=>apply("replyThread",input),toggleThreadResolved:threadId=>apply("toggleThreadResolved",{threadId}),removeThread:threadId=>apply("removeThread",{threadId}),editComment:input=>apply("editComment",input),removeComment:commentId=>apply("removeComment",{commentId}),
    toSerializableState:()=>structuredClone(documentFrom(get())),
    setVersionsForPage:(pageId,versions)=>set(local=>({versionsByPage:{...local.versionsByPage,[pageId]:versions}})),
    setPresence:input=>set(local=>{
      if(!input||typeof input.clientId!=="string"||!/^[a-zA-Z0-9_-]{1,100}$/.test(input.clientId)||["__proto__","constructor","prototype"].includes(input.clientId)||!local.pages.some(page=>page.id===input.pageId)||!local.users.some(user=>user.id===input.userId)||typeof input.name!=="string"||input.name.length>100||!/^#[a-fA-F0-9]{6}$/.test(input.color))return {};
      const entries=Object.entries({...local.presence,[input.clientId]:{pageId:input.pageId,userId:input.userId,name:input.name,color:input.color,updatedAt:Date.now()}}).sort((a,b)=>b[1].updatedAt-a[1].updatedAt).slice(0,64);
      return {presence:Object.fromEntries(entries)};
    }),
    prunePresence:(maxAgeMs=13000)=>set(local=>({presence:Object.fromEntries(Object.entries(local.presence).filter(([,value])=>Date.now()-value.updatedAt<=maxAgeMs))})),
    setTyping:input=>set(local=>{
      if(!input||!local.blocksByPage[input.pageId]?.some(block=>block.id===input.blockId)||typeof input.userName!=="string"||input.userName.length>100)return {};
      return {typing:{...local.typing,[input.pageId]:{...(local.typing[input.pageId]??{}),[input.blockId]:{userName:input.userName,updatedAt:Date.now()}}}};
    }),
    pruneTyping:(maxAgeMs=3000)=>set(local=>({typing:Object.fromEntries(Object.entries(local.typing).map(([pageId,entries])=>[pageId,Object.fromEntries(Object.entries(entries).filter(([,value])=>Date.now()-value.updatedAt<=maxAgeMs))]).filter(([,entries])=>Object.keys(entries).length))})),
  };
});
''',encoding='utf-8')
p=S/'src/lib/workspaceUtils.js';assert hashlib.sha256(p.read_bytes()).hexdigest()==baseline['src/lib/workspaceUtils.js']
text=p.read_text(encoding='utf-8');suffix=text[text.index('export function mapBlockTypeLabel'):]
prefix='''// Bounded navigation tolerates a damaged local draft without hanging the UI.
export function buildPageTree(pages,parentId=null) {
  const children=new Map();
  for(const page of pages){if(page.isDeleted)continue;const list=children.get(page.parentId)??[];list.push(page);children.set(page.parentId,list);}
  const visit=(parent,ancestors)=>{if(ancestors.size>=64)return [];return (children.get(parent)??[]).filter(page=>!ancestors.has(page.id)).sort((a,b)=>a.title.localeCompare(b.title)).map(page=>({...page,children:visit(page.id,new Set([...ancestors,page.id]))}));};
  return visit(parentId,new Set(parentId?[parentId]:[]));
}
export function getBreadcrumbs(pages,pageId) {
  const byId=new Map(pages.map(page=>[page.id,page])),seen=new Set(),result=[];let cursor=byId.get(pageId);
  while(cursor&&!seen.has(cursor.id)&&seen.size<64){seen.add(cursor.id);result.unshift(cursor);cursor=cursor.parentId?byId.get(cursor.parentId):null;}
  return result;
}
export function isDescendant(pages,candidateParentId,pageId) {
  const byId=new Map(pages.map(page=>[page.id,page])),seen=new Set();let cursor=byId.get(candidateParentId);
  while(cursor){if(cursor.id===pageId)return true;if(seen.has(cursor.id)||seen.size>=64)return true;seen.add(cursor.id);cursor=cursor.parentId?byId.get(cursor.parentId):null;}
  return false;
}

'''
p.write_text(prefix+suffix,encoding='utf-8')
print('Replaced client state mutations and bounded tree traversal. UI lifecycle integration remains pending.')
