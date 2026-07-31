import{useCallback,useEffect,useMemo,useState}from'react';
import{scenes}from'./data';
import{ArrowIcon,Footage,HotelStill,SoundIcon}from'./components';
import{detectLocale,t}from'./i18n';
import{beat as playBeat,choose as playChoose,power}from'./utils/sounds';
import type{Outcome,Phase}from'./types';
import'./MidnightHotelLedger.less';
import'./refinement.less';

const STORE='midnight_hotel_ledger_reports_v2';
function readFound(){try{const value=JSON.parse(localStorage.getItem(STORE)||'[]');return new Set<string>(Array.isArray(value)?value:[])}catch{return new Set<string>()}}

export default function MidnightHotelLedger(){
 const locale=useMemo(detectLocale,[]),[phase,setPhase]=useState<Phase>('cover'),[sceneIndex,setSceneIndex]=useState(0),[selected,setSelected]=useState<Outcome|null>(null),[beat,setBeat]=useState(0),[sound,setSound]=useState(true),[isNew,setIsNew]=useState(false),[choiceNonce,setChoiceNonce]=useState(()=>Math.floor(Math.random()*3)),[found,setFound]=useState(readFound);
 const scene=scenes[sceneIndex],success=Boolean(selected?.success);
 const choices=useMemo(()=>{const r=(choiceNonce+sceneIndex)%scene.outcomes.length;return[...scene.outcomes.slice(r),...scene.outcomes.slice(0,r)]},[choiceNonce,scene,sceneIndex]);
 useEffect(()=>{const calc=()=>{const width=document.documentElement.clientWidth,scale=width<=520?width/390:1;document.documentElement.style.setProperty('--mhl-scale',String(scale));document.documentElement.style.setProperty('--mhl-height',`${844*scale}px`)};calc();addEventListener('resize',calc);return()=>removeEventListener('resize',calc)},[]);
 useEffect(()=>{window.scrollTo(0,0)},[phase,sceneIndex]);
 useEffect(()=>{if(phase!=='cover'&&phase!=='setup'&&phase!=='incident')return;const targets=scenes[Math.min(sceneIndex,2)].outcomes.map(outcome=>{const video=document.createElement('video');video.preload='metadata';video.src=outcome.video;return video});return()=>targets.forEach(video=>{video.removeAttribute('src');video.load()})},[phase,sceneIndex]);
 useEffect(()=>{if(phase!=='setup')return;const ms=matchMedia('(prefers-reduced-motion: reduce)').matches?320:1550,timer=setTimeout(()=>setPhase('incident'),ms);return()=>clearTimeout(timer)},[phase,sceneIndex]);
 useEffect(()=>{if(phase!=='footage'||!selected)return;const points=[[650,1],[2200,2],[4100,3],[5200,4]]as const,timers=points.map(([ms,b])=>setTimeout(()=>{setBeat(b);if(sound)playBeat(selected.id,b);if(b===4){const key=`${scene.id}:${selected.id}`;setFound(old=>{const next=new Set(old);next.add(key);localStorage.setItem(STORE,JSON.stringify([...next]));return next});setPhase('report')}},ms));return()=>timers.forEach(clearTimeout)},[phase,scene.id,selected,sound]);
 const enterScene=useCallback((index:number)=>{setSceneIndex(index);setSelected(null);setBeat(0);setChoiceNonce(value=>value+1);setPhase('setup')},[]);
 const boot=useCallback(()=>{if(sound)power();enterScene(0)},[enterScene,sound]);
 const select=useCallback((outcome:Outcome)=>{if(phase!=='incident')return;const key=`${scene.id}:${outcome.id}`;setIsNew(!found.has(key));setSelected(outcome);setBeat(0);setPhase('footage');if(sound)playChoose()},[found,phase,scene.id,sound]);
 const advance=useCallback(()=>{if(phase!=='report'||!selected)return;if(!selected.success){enterScene(sceneIndex);return}if(sceneIndex===scenes.length-1){setPhase('complete');return}enterScene(sceneIndex+1)},[enterScene,phase,sceneIndex,selected]);
 const restart=useCallback(()=>{setSceneIndex(0);setSelected(null);setBeat(0);setPhase('cover')},[]);
 useEffect(()=>{const fn=(event:KeyboardEvent)=>{if(event.key.toLowerCase()==='m')setSound(value=>!value);else if(phase==='incident'&&['1','2','3'].includes(event.key))select(choices[Number(event.key)-1]);else if(event.key==='Enter'){if(phase==='cover')boot();else if(phase==='report')advance();else if(phase==='complete')restart()}};addEventListener('keydown',fn);return()=>removeEventListener('keydown',fn)},[advance,boot,choices,phase,restart,select]);
 return <main className="mhl-shell"><article className={`mhl-terminal mhl-terminal--${phase}`}>
  <header><div className="mhl-brand"><span>THE AUBERGE NOCTURNE</span><strong>{t(locale,'hotel')}</strong></div><div className="mhl-steps" aria-label={`${sceneIndex+1}/3`}>{scenes.map((_,index)=><i key={index} className={index<sceneIndex||phase==='complete'?'is-done':index===sceneIndex?'is-current':''}>{index+1}</i>)}</div><button className="mhl-icon" aria-label={sound?t(locale,'mute'):t(locale,'unmute')} onPointerDown={()=>setSound(value=>!value)}><SoundIcon off={!sound}/></button></header>
  {phase==='cover'&&<section className="mhl-cover"><div className="mhl-cover__plaque"><span>EST. 1927</span><b>THE AUBERGE<br/>NOCTURNE</b><i>GRAND HOTEL</i></div><div className="mhl-cover__window"><img src="./generated/hotel_start.webp" alt="Mara and the guest in room 307" draggable={false}/><span>ROOM 307</span><strong>02:17 AM</strong></div><p>{t(locale,'subtitle')}</p><button className="mhl-primary" onPointerDown={boot}><span>{t(locale,'start')}</span><ArrowIcon/></button></section>}
  {(phase==='setup'||phase==='incident')&&<section className="mhl-incident"><div className="mhl-casebar"><span>{locale==='zh'?`场景 ${sceneIndex+1}`:`SCENE ${sceneIndex+1}`}</span><strong>{scene.title[locale]}</strong></div><h2>{phase==='setup'?scene.setup[locale]:scene.question[locale]}</h2><HotelStill scene={scene}/>{phase==='incident'&&<><p className="mhl-instruction">{t(locale,'choose')}</p><div className="mhl-options">{choices.map((outcome,index)=><button key={outcome.id} onPointerDown={()=>select(outcome)}><span>{index+1}</span><strong>{outcome.label[locale]}</strong></button>)}</div></>}</section>}
  {(phase==='footage'||phase==='report')&&selected&&<section className="mhl-play"><div className="mhl-reelbar"><span>{phase==='footage'?t(locale,'live'):t(locale,'report')}</span><strong>{selected.label[locale]}</strong></div><Footage scene={scene} outcome={selected} beat={beat} locale={locale} result={phase==='report'}/>{phase==='report'&&<div className={`mhl-report ${success?'mhl-report--success':'mhl-report--fail'}`}><div><span>{t(locale,isNew?'new':'seen')}</span><b>{found.size}/9</b></div><h2>{selected.title[locale]}</h2><p>{selected.detail[locale]}</p><button className="mhl-primary" onPointerDown={advance}><span>{t(locale,success?'continue':'retry')}</span><ArrowIcon/></button></div>}</section>}
  {phase==='complete'&&<section className="mhl-complete"><div className="mhl-complete__stamp">SHIFT<br/>CLOSED</div><h1>{t(locale,'finalTitle')}</h1><div className="mhl-complete__frame"><img src="./generated/night-manager_end.webp" alt={t(locale,'finalTitle')} draggable={false}/></div><p>{t(locale,'finalDetail')}</p><div className="mhl-complete__found"><span>{t(locale,'filed')}</span><strong>{found.size}/9</strong></div><button className="mhl-primary" onPointerDown={restart}><span>{t(locale,'restart')}</span><ArrowIcon/></button></section>}
  <footer><span>CONFIDENTIAL NIGHT RECORD</span><img src="./alteru.svg" alt="AlterU" draggable={false}/><span>{t(locale,'filed')} · {found.size}/9</span></footer>
 </article></main>
}
