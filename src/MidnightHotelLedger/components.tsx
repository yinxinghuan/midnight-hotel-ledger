import{useEffect,useState}from'react';
import type{Locale,Outcome,Scene}from'./types';

export function SoundIcon({off}:{off:boolean}){return <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 9v6h4l5 4V5L8 9H4Z"/><path className="line" d="M16 9c1.4 1.7 1.4 4.3 0 6M19 6c3 3.3 3 8.7 0 12"/>{off&&<path className="line" d="M4 4l16 16"/>}</svg>}
export function ArrowIcon(){return <svg viewBox="0 0 24 24" aria-hidden="true"><path className="line" d="M5 12h13M13 6l6 6-6 6"/></svg>}
export function HotelStill({scene}:{scene:Scene}){return <div className="mhl-still"><img src={scene.start} alt={scene.alt.zh} draggable={false}/><div><span>CAM {scene.id==='bath'?'03':'01'}</span><strong>02:{scene.id==='bath'?'17':scene.id==='checkin'?'22':'29'}</strong></div></div>}
export function Footage({scene,outcome,beat,locale,result}:{scene:Scene;outcome:Outcome;beat:number;locale:Locale;result:boolean}){
 const[ready,setReady]=useState(false),[failed,setFailed]=useState(false);
 useEffect(()=>{setReady(false);setFailed(false)},[outcome.id]);
 const caption=outcome.captions[locale][Math.min(Math.max(beat-1,0),3)];
 return <div className={`mhl-footage ${ready?'mhl-footage--ready':''} ${failed?'mhl-footage--failed':''}`}>
  <img className="mhl-footage__still" src={result?outcome.end:scene.start} alt={scene.alt[locale]} draggable={false}/>
  {!result&&!failed&&<video src={outcome.video} poster={scene.start} autoPlay muted playsInline preload="auto" onCanPlay={()=>setReady(true)} onError={()=>setFailed(true)}/>}<div className="mhl-footage__scan"/><div className="mhl-footage__hud"><span>REC · CAM {scene.id==='bath'?'03':'01'}</span><strong>02:{String(17+beat*3).padStart(2,'0')}</strong></div>
  {!ready&&!result&&<div className="mhl-footage__loading">{failed?(locale==='zh'?'录像不可用 · 尾帧已就绪':'REEL UNAVAILABLE · FINAL FRAME READY'):(locale==='zh'?'保持首帧 · 录像装片中':'FIRST FRAME HELD · LOADING REEL')}</div>}
  <div className="mhl-footage__caption"><span>{String(Math.max(beat,1)).padStart(2,'0')}</span><strong>{caption}</strong></div>
 </div>
}
