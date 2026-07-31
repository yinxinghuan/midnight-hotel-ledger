#!/usr/bin/env python3
"""Generate the shared hotel incident frame, three endings, and three clips.

All image and video requests are strictly sequential. The manifest keeps the
exact prompts, public URLs, and task IDs used for the shipped media.
"""
from __future__ import annotations
import json, sys, time, urllib.error, urllib.request
from pathlib import Path

IMAGE_API="https://chat.aiwaves.tech/aigram/api/gen-image"
VIDEO_SUBMIT="https://u545921-b746-8a491f44.westc.seetacloud.com:8443/video"
VIDEO_POLL="https://u545921-b746-8a491f44.westc.seetacloud.com:8443/video_task"
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"public"/"generated"
MANIFEST=Path(__file__).with_name("hotel_cinema_manifest.json")

START_PROMPT=(
 "Premium live-action black-comedy film still, square image composed for a vertical 3:4 crop, inside bathroom 307 "
 "of an old European-style boutique hotel at midnight. MARA is the clear main subject at frame left: a Western young "
 "adult woman with expressive natural features, short wavy dark-brown bob, a plain burgundy silk blouse with long sleeves "
 "and high-waisted black trousers, with no jacket, no name badge, pin, patch or writing anywhere. She stands beside a white claw-foot bathtub, holding a "
 "plain clipboard at her side and looking professionally concerned. An older white male guest with silver hair and a "
 "neatly trimmed grey moustache wears a charcoal-grey hotel robe and slippers against a blank cream-tiled wall at frame right. "
 "The bathtub is intact, filled with ordinary still clear water, and all four brass feet are visible. Warm tungsten wall "
 "sconces, dark wine-red tile accents, aged cream plaster, checkerboard stone floor, brass taps, believable skin and cloth, "
 "warm fully interior lighting with no window visible, 28mm lens, both faces and upper bodies inside the central 72 percent safe "
 "area. No doorway, window, exterior view, wall sign, plaque, mirror lettering or room number is visible. Exactly two humans, one continuous room, no ocean, "
 "no moon, no horizon, no beach, no exterior water, no sea life, no wave, no diver, no tentacle, no tray, no glowing portal, no badge, no "
 "text, no letters, no numbers, no logo, no watermark, no UI, not horror, not anime, not illustration, not 3D render, not East Asian styling."
)

REPAIR_START_PROMPT=(
 "Precision photographic retouch of the exact same reference image. Make only one material cleanup: completely paint out the small "
 "rectangular name patch on the older man's left robe chest and replace it with seamless plain grey terry-cloth robe texture. There must "
 "be no patch, badge, rectangle, label, letters or marks on his robe. Preserve pixel-consistent Mara face, short dark-brown bob, burgundy "
 "silk blouse, black trousers, older man's face and moustache, their exact poses, blank cream wall, wine-red tiles, mirror, claw-foot "
 "bathtub, brass taps, camera and warm lighting. Keep all walls and clothing blank. The bathtub remains filled with ordinary still clear "
 "water. No doorway, no window, no exterior view, no ocean, no moon, no sea life, no wave, no diver, no tentacle, no tray, no text, no "
 "letters, no numbers, no logo, no watermark, no UI. Same premium live-action film still, exactly two humans."
)

REPAIR_MAINTENANCE_PROMPT=(
 "Precision photographic cleanup of the exact same reference image. Preserve the front-left Mara with short brown bob and burgundy "
 "silk blouse holding the brass toolbox and service bell, the older white male guest in grey robe at far left, the single maintenance "
 "worker standing waist-high in the bathtub with copper deep-sea helmet, the bathtub, camera and lighting. Remove only the duplicate "
 "second woman standing in the middle background behind Mara; replace her entire body with the same plain dark-blue tiled wall and empty "
 "room background. The final image contains exactly three humans: one Mara, one older guest, one helmeted maintenance worker. No extra "
 "woman, no duplicate Mara, no duplicate diver, no text, no letters, no logo, no watermark, no UI."
)

END_PROMPTS={
 "plug":(
  "Preserve the exact same Mara face, short wavy brown hair, burgundy manager uniform, older white male guest, claw-foot tub, "
  "bathroom architecture, camera height and midnight lighting from the reference. Ending frame of the same live-action black "
  "comedy shot: Mara has pressed a large brass bathtub stopper down with one gloved hand, but a compact turquoise ocean wave "
  "erupts upward from the tub and curls behind her. Three small colorful tropical fish are suspended naturally in the splash. "
  "Mara braces with shocked wide eyes while the guest raises one dry towel in deadpan disbelief. Water remains contained around "
  "the bathtub, realistic splash and contact shadows, faces clear, exactly two humans. No flood covering faces, no extra person, "
  "no shark, no tentacle, no diver, no text, no letters, no logo, no watermark, no UI, not horror, not illustration."
 ),
 "maintenance":(
  "Preserve the exact same single Mara face, short wavy brown hair, burgundy silk blouse, older white male guest, claw-foot tub, "
  "bathroom architecture and camera height from the reference. Ending frame of the same live-action black comedy shot with exactly "
  "two humans total: Mara at frame left holds one small brass service bell, and the same older guest stands behind her. From the "
  "bathtub rises one EMPTY vintage copper deep-sea diving helmet physically bolted on top of one closed brass toolbox, like an absurd "
  "automated repair kit delivered from underwater. The helmet has no body, no arms, no legs, no person inside; its round face window "
  "is completely dark and empty. Water drips from the object, plain dark-blue wall behind them, both human faces clear. No worker, "
  "no third human, no extra woman, no duplicate Mara, no fish, no tentacle, no wave, no badge, no text, no letters, no logo, no "
  "watermark, no UI, not horror, not illustration."
 ),
 "suite":(
  "Preserve the exact same Mara face, short wavy brown hair, burgundy manager uniform, older white male guest, claw-foot tub, "
  "bathroom architecture, camera height and midnight lighting from the reference. Ending frame of the same live-action black "
  "comedy shot: one elegant giant purple octopus tentacle rises from the bathtub and politely holds a silver room-service tray "
  "with a covered dish and a blank brass room key. Mara presents a blank cream hotel keycard toward it with flawless professional "
  "composure; the older guest watches from the doorway, surprised but not frightened. Only one tentacle is visible, subtle water "
  "ripples and realistic contact shadows, exactly two humans, faces clear, one continuous room. No full octopus body, no extra "
  "person, no diver, no large wave, no readable writing, no text, no letters, no logo, no watermark, no UI, not horror, not illustration."
 )
}

VIDEO_PROMPTS={
 "plug":("Preserve the exact same Mara, guest, bathtub, bathroom and camera axis. One readable live-action comedy beat: Mara presses "
  "a brass stopper down, then one compact turquoise wave bursts from the tub carrying three small tropical fish; Mara braces once and "
  "the guest raises one towel. One short camera jolt, then settle on the exact final frame. Stable human faces, no morphing, no cut, "
  "no extra person, no tentacle, no diver, no text or logo."),
 "maintenance":("Preserve the exact same Mara, guest, bathtub, bathroom and camera axis. One readable live-action comedy beat: Mara "
  "rings a small brass service bell once; one empty vintage copper deep-sea helmet bolted to a closed brass toolbox floats up from the "
  "bathtub as an automated underwater repair kit. Mara leans back once and the guest watches. The object has no human body or face. "
  "Settle on the exact final frame. Stable faces, exactly two humans, no morphing, no cut, no worker, no fish, no tentacle, no text or logo."),
 "suite":("Preserve the exact same Mara, guest, bathtub, bathroom and camera axis. One readable live-action comedy beat: Mara presents a "
  "blank cream hotel keycard; one elegant purple octopus tentacle rises slowly from the bathtub holding a silver covered room-service "
  "tray and a blank brass key. The guest reacts once while Mara stays professionally composed, then settle on the exact final frame. "
  "Stable faces, no full octopus, no extra tentacle, no cut, no morphing, no text or logo.")
}

def post(url,payload,timeout=900,origin=False):
 headers={"Content-Type":"application/json","User-Agent":"Mozilla/5.0"}
 if origin: headers.update({"Origin":"https://aigram.app","Referer":"https://aigram.app/"})
 req=urllib.request.Request(url,data=json.dumps(payload).encode(),method="POST",headers=headers)
 with urllib.request.urlopen(req,timeout=timeout) as res:return json.loads(res.read())

def gen_image(prompt,ref=None):
 payload={"prompt":prompt}
 if ref:payload["ref_url"]=ref
 for attempt,delay in enumerate((3,8,15),1):
  try:
   result=post(IMAGE_API,payload,origin=True);url=result.get("url")
   if not url:raise RuntimeError(result)
   return url
  except urllib.error.HTTPError as exc:
   if exc.code not in (429,500,502,503,504) or attempt==3:raise
   print(f"image retry {attempt} HTTP {exc.code}",flush=True);time.sleep(delay)

def download(url,dest):
 dest.parent.mkdir(parents=True,exist_ok=True)
 req=urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0"})
 with urllib.request.urlopen(req,timeout=600) as res:dest.write_bytes(res.read())

def load():return json.loads(MANIFEST.read_text()) if MANIFEST.exists() else {}
def save(data):MANIFEST.write_text(json.dumps(data,indent=2,ensure_ascii=False)+"\n")

def video(branch,start,end,entry):
 if not entry.get("video_url"):
  task=entry.get("video_task_id")
  if not task:
   submitted=post(VIDEO_SUBMIT,{"query":"","params":{"image_url":start,"end_image_url":end,"prompt":VIDEO_PROMPTS[branch],"env":"prod","target_image_ratio":"9x16"}},timeout=300)
   task=submitted.get("task_id") or submitted.get("data",{}).get("task_id")
   if not task:raise RuntimeError(submitted)
   entry.update({"video_task_id":task,"video_prompt":VIDEO_PROMPTS[branch]});save(manifest)
  print(f"{branch} task={task}",flush=True);deadline=time.time()+1800
  while time.time()<deadline:
   time.sleep(10);result=post(VIDEO_POLL,{"query":"","params":{"task_id":task}},timeout=300)
   status=result.get("status") or result.get("data",{}).get("status");print(f"{branch} {status}",flush=True)
   if status=="success":
    entry["video_url"]=result.get("url") or result.get("data",{}).get("url");save(manifest);break
   if status=="failed":raise RuntimeError(result)
  else:raise TimeoutError(task)
 download(entry["video_url"],OUT/f"{branch}_cinema.mp4")

manifest=load()
def main():
 OUT.mkdir(parents=True,exist_ok=True)
 start=manifest.get("shared_start_url")
 if not start:
  print("generating shared start",flush=True);start=gen_image(START_PROMPT);manifest.update({"shared_start_url":start,"shared_start_prompt":START_PROMPT});save(manifest)
 if "--repair-start" in sys.argv:
  print("repairing shared start",flush=True)
  repaired=gen_image(REPAIR_START_PROMPT,start)
  manifest.setdefault("rejected_start_urls",[]).append(start)
  start=repaired;manifest.update({"shared_start_url":start,"shared_start_repair_prompt":REPAIR_START_PROMPT});save(manifest)
 download(start,OUT/"hotel_start.webp")
 if "--start-only" in sys.argv:
  print(json.dumps({"shared_start_url":start},ensure_ascii=False),flush=True);return
 if "--repair-maintenance" in sys.argv:
  entry=manifest["maintenance"]
  old=entry["end_url"];print("repairing maintenance end",flush=True)
  repaired=gen_image(REPAIR_MAINTENANCE_PROMPT,old)
  entry.setdefault("rejected_end_urls",[]).append(old)
  entry.update({"end_url":repaired,"end_repair_prompt":REPAIR_MAINTENANCE_PROMPT})
  entry.pop("video_task_id",None);entry.pop("video_url",None);save(manifest)
  download(repaired,OUT/"maintenance_end.webp");print(json.dumps({"maintenance_end_url":repaired},ensure_ascii=False),flush=True);return
 if "--regen-maintenance" in sys.argv:
  entry=manifest["maintenance"]
  old=entry.get("end_url")
  if old:entry.setdefault("rejected_end_urls",[]).append(old)
  print("regenerating maintenance end from clean start",flush=True)
  fresh=gen_image(END_PROMPTS["maintenance"],start)
  entry.update({"end_url":fresh,"end_prompt":END_PROMPTS["maintenance"]})
  entry.pop("video_task_id",None);entry.pop("video_url",None);save(manifest)
  download(fresh,OUT/"maintenance_end.webp");print(json.dumps({"maintenance_end_url":fresh},ensure_ascii=False),flush=True);return
 for branch in ("plug","maintenance","suite"):
  entry=manifest.setdefault(branch,{})
  if not entry.get("end_url"):
   print(f"generating {branch} end",flush=True);entry.update({"end_url":gen_image(END_PROMPTS[branch],start),"end_prompt":END_PROMPTS[branch]});save(manifest);time.sleep(3)
  download(entry["end_url"],OUT/f"{branch}_end.webp")
 for branch in ("plug","maintenance","suite"):
  video(branch,start,manifest[branch]["end_url"],manifest[branch])
 print(json.dumps(manifest,ensure_ascii=False),flush=True)

if __name__=="__main__":main()
