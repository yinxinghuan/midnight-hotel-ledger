#!/usr/bin/env python3
import json,sys,urllib.request
from pathlib import Path
API="https://chat.aiwaves.tech/aigram/api/gen-image";ROOT=Path(__file__).resolve().parents[1];MANIFEST=Path(__file__).with_name("poster_manifest.json")
PROMPT=("Square premium live-action cinematic black-comedy game poster for an old European-style boutique hotel at midnight. Western young adult woman night manager Mara with short wavy dark-brown bob and plain burgundy silk blouse stands professionally beside a white claw-foot bathtub. A luminous turquoise ocean wave and one elegant purple octopus tentacle rise from the bathtub while an older white male guest in a grey robe watches in deadpan disbelief. Burgundy leather frame, oxidized brass corners, warm tungsten sconces against cold deep-sea blue, sophisticated mysterious hotel atmosphere, realistic skin, premium commercial cinematography, strong readable silhouettes at 160px thumbnail. At the TOP safe 22 percent, large perfectly spelled English title: THE MIDNIGHT HOTEL LEDGER. No other words, no Chinese, no gibberish, no badge, no logo, no watermark, no UI. Keep faces, tub, wave and tentacle inside central 70 percent; bottom 20 percent contains only dark floor and water reflection.")
REPAIR=("Precision photographic poster retouch of the exact reference. Preserve the large perfectly spelled title THE MIDNIGHT HOTEL LEDGER exactly as it is, preserve both Western actors, their faces, the bathtub, octopus, wave, burgundy leather frame, brass corners, composition and lighting. Remove only the tiny meaningless line of text above the title and the small rectangular badge on Mara's blouse; replace those areas with seamless plain burgundy leather and plain burgundy silk fabric. The large title is the only text anywhere. No other letters, no tiny caption, no badge, no label, no logo, no watermark, no UI.")
def generate(prompt,ref=None):
 body={"prompt":prompt}
 if ref:body["ref_url"]=ref
 req=urllib.request.Request(API,data=json.dumps(body).encode(),method="POST",headers={"Content-Type":"application/json","Origin":"https://aigram.app","Referer":"https://aigram.app/","User-Agent":"Mozilla/5.0"})
 with urllib.request.urlopen(req,timeout=900) as res:return json.loads(res.read())["url"]
data=json.loads(MANIFEST.read_text()) if MANIFEST.exists() else {}
if "--repair" in sys.argv:
 old=data["url"];url=generate(REPAIR,old);data.setdefault("rejected_urls",[]).append(old);data.update({"url":url,"repair_prompt":REPAIR})
else:url=generate(PROMPT);data={"url":url,"prompt":PROMPT}
out=ROOT/"public"/"poster-source.webp";out.write_bytes(urllib.request.urlopen(urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0"}),timeout=600).read());MANIFEST.write_text(json.dumps(data,indent=2,ensure_ascii=False)+"\n");print(url,flush=True)
