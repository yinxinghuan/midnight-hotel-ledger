#!/usr/bin/env python3
"""Generate scene 2–3 stills and six continuation clips for Midnight Hotel Ledger.

Image requests are strictly sequential. Video tasks are also submitted and
polled one at a time so the production run remains resumable and auditable.
"""
from __future__ import annotations

import json
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

IMAGE_API = "https://chat.aiwaves.tech/aigram/api/gen-image"
VIDEO_SUBMIT = "https://u545921-b746-8a491f44.westc.seetacloud.com:8443/video"
VIDEO_POLL = "https://u545921-b746-8a491f44.westc.seetacloud.com:8443/video_task"
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "public" / "generated"
MANIFEST = Path(__file__).with_name("extended_hotel_cinema_manifest.json")
SOURCE_MANIFEST = Path(__file__).with_name("hotel_cinema_manifest.json")

SCENE2_START = (
    "Live-action black-comedy continuation of the exact reference. Preserve pixel-consistent MARA: Western young adult woman, "
    "short wavy dark-brown bob, plain burgundy silk blouse and high-waisted black trousers; preserve the same older white male guest "
    "with silver hair, grey moustache and charcoal robe; preserve the same elegant purple octopus tentacle. Move them within the same "
    "old European boutique hotel to a compact midnight reception desk with burgundy leather panels, oxidized brass counter edge, blank "
    "wood key cubbies and warm tungsten lamps. Mara stands behind the counter holding one completely blank cream registration card and "
    "one plain brass room key. One purple tentacle rests politely across the guest side of the counter, waiting to check in; the older guest "
    "stands beside it holding the same covered silver tray. Medium-wide vertical-safe composition, realistic skin and cloth, deadpan service "
    "comedy, same night color grade. No readable paper, no passport, no pen, no extra tentacle, no full octopus body, no badge, no letters, "
    "no numbers, no hotel logo, no watermark, no UI, not horror, not illustration. Exactly two humans."
)

END_PROMPTS = {
    "passport": (
        "Preserve the exact same Mara, older guest, purple tentacle, reception desk, camera and lighting from the reference. Ending frame: "
        "Mara professionally presents one completely blank closed burgundy passport booklet. The tentacle presses one wet suction cup onto it, "
        "leaving one enormous purple circular ink mark that covers the blank cover. Mara remains composed; the older guest peers over the tray. "
        "One tentacle only, exactly two humans, clear faces, no readable text, no letters, no logo, no watermark, no UI."
    ),
    "charge-eight": (
        "Preserve the exact same Mara, older guest, purple tentacle, reception desk, camera and lighting from the reference. Ending frame of one "
        "clear visual joke: Mara has placed eight identical blank brass room keys in a perfectly straight row on the counter and holds an absurdly "
        "long blank receipt that rolls across the floor. The single tentacle recoils in polite financial shock while the older guest counts keys on "
        "his fingers. Exactly two humans, one tentacle, no readable text, no letters, no numbers, no logo, no watermark, no UI."
    ),
    "eight-signatures": (
        "Preserve the exact same Mara face, burgundy blouse, older guest, reception desk, hotel lighting and the same purple octopus identity. Ending "
        "frame: exactly eight elegant purple tentacles fan neatly over the guest side of the brass counter. Each tentacle holds one fountain pen and "
        "signs one separate completely blank cream registration card. Mara calmly presents a fan of eight blank brass room keycards; the older guest "
        "holds the covered silver tray in deadpan amazement. Clear faces, readable eight-arm silhouette, exactly two humans, no full octopus head, no "
        "writing visible, no letters, no numbers, no logo, no watermark, no UI, not horror."
    ),
    "unplug": (
        "Preserve the exact same Mara, older guest, exactly eight purple tentacles, reception desk, camera and lighting from the reference. Ending frame: "
        "Mara holds one unplugged black telephone cord with professional finality, but every tentacle presses a different polished brass service bell "
        "lined across the counter. Eight bells are visibly ringing with small physical motion, while the older guest covers one ear and keeps holding "
        "the tray. Exactly two humans, no extra arms, no readable text, no logo, no watermark, no UI."
    ),
    "eight-breakfasts": (
        "Preserve the exact same Mara, older guest, exactly eight purple tentacles, reception desk, camera and lighting from the reference. Ending frame: "
        "eight covered silver breakfast trays are stacked in a precarious leaning tower across the brass counter, each held by a different tentacle. "
        "One bread roll is airborne at the top. Mara braces the tower with both hands while the older guest still holds the original tiny tray. Clear "
        "faces, exactly two humans, no extra arms, no text, no logo, no watermark, no UI."
    ),
    "night-manager": (
        "Preserve the exact same Mara, older guest in his original charcoal-grey terry-cloth hotel robe and slippers, exactly eight purple tentacles, "
        "reception desk, camera and lighting from the reference. Final ending "
        "frame of sophisticated live-action black comedy: the eight tentacles now operate the midnight front desk with perfect efficiency—one rings a "
        "brass bell, one sorts blank room keys, one holds a telephone, one offers the covered tray, and the others manage blank cards. Mara walks calmly "
        "toward the exit carrying only her black coat over one arm, finally off duty; both her hands and the coat are completely free of cards, badges "
        "or paper. The older guest remains in the grey robe at the counter waiting. A shallow ribbon of "
        "turquoise seawater creeps from the dark corridor behind them, showing room 307 is still leaking. Exactly two humans, no octopus head, no extra "
        "arms, no suit jacket, no shirt, no tie, no card in Mara's hands, no badge, no readable text, no letters, no numbers, no logo, no watermark, no UI, not horror."
    ),
}

VIDEO_PROMPTS = {
    "passport": "Same Mara, guest, single tentacle, desk and camera. Mara presents one blank passport; the tentacle presses one suction cup onto it, leaving one huge purple circular mark. One readable action, stable faces, no cut, no morphing, no text.",
    "charge-eight": "Same Mara, guest, single tentacle, desk and camera. Mara rapidly lays eight blank brass room keys in one straight row and an absurdly long blank receipt unrolls to the floor; the tentacle recoils once. Stable faces, no cut, no text.",
    "eight-signatures": "Same Mara, guest, desk and camera. The single waiting tentacle is joined by seven matching tentacles; exactly eight arms fan out, each signs one blank registration card with one pen, while Mara presents eight blank brass keycards. One continuous reveal, stable faces, no full octopus head, no text.",
    "unplug": "Same Mara, guest, exactly eight tentacles, desk and camera. Mara unplugs one telephone cord; immediately all eight tentacles press eight brass service bells once. The guest covers one ear. One readable action, stable faces, no extra arms, no text.",
    "eight-breakfasts": "Same Mara, guest, exactly eight tentacles, desk and camera. Eight covered breakfast trays arrive into the tentacles and build one leaning silver tower; one bread roll pops upward as Mara braces it. One continuous action, stable faces, no extra arms, no text.",
    "night-manager": "Same Mara, guest, exactly eight tentacles, desk and camera. The tentacles efficiently take over bell, telephone, blank keys, tray and registration cards while Mara puts on her coat and walks off duty; a shallow turquoise ribbon of water creeps from the corridor. Stable faces, no cut, no text.",
}

REPAIR_NIGHT_MANAGER = (
    "Precision photographic cleanup of the exact reference image. Preserve Mara at frame right with the exact same face, short dark-brown bob, "
    "burgundy silk blouse, black skirt, black coat over her arm and walking-off-duty pose. Preserve the eight purple tentacles, burgundy reception "
    "desk, brass bell, telephone, covered tray, key cubbies, camera, lighting and turquoise seawater on the corridor floor. Make only two corrections: "
    "restore the older white male guest at frame left to his original charcoal-grey hotel robe with no suit jacket, shirt or tie; completely remove the "
    "tiny blue badge or printed mark from the cream time card in Mara's hand and leave the card perfectly blank. All cards remain blank. Exactly two "
    "humans, no extra arms, no readable text, no letters, no numbers, no badge, no logo, no watermark, no UI."
)


def post(url: str, payload: dict, timeout: int = 900, origin: bool = False) -> dict:
    headers = {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}
    if origin:
        headers.update({"Origin": "https://aigram.app", "Referer": "https://aigram.app/"})
    req = urllib.request.Request(url, data=json.dumps(payload).encode(), method="POST", headers=headers)
    with urllib.request.urlopen(req, timeout=timeout) as response:
        return json.loads(response.read())


def gen_image(prompt: str, ref: str) -> str:
    payload = {"prompt": prompt, "ref_url": ref}
    for attempt, delay in enumerate((3, 8, 15), 1):
        try:
            result = post(IMAGE_API, payload, origin=True)
            url = result.get("url")
            if not url:
                raise RuntimeError(result)
            return url
        except urllib.error.HTTPError as exc:
            if exc.code not in (429, 500, 502, 503, 504) or attempt == 3:
                raise
            print(f"image retry {attempt}: HTTP {exc.code}", flush=True)
            time.sleep(delay)
    raise RuntimeError("image generation exhausted")


def download(url: str, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=600) as response:
        dest.write_bytes(response.read())


def save(data: dict) -> None:
    MANIFEST.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")


def make_video(name: str, start: str, end: str, entry: dict, manifest: dict) -> None:
    task = entry.get("video_task_id")
    if not entry.get("video_url") and not task:
        result = post(VIDEO_SUBMIT, {"query": "", "params": {"image_url": start, "end_image_url": end, "prompt": VIDEO_PROMPTS[name], "env": "prod", "target_image_ratio": "9x16"}}, timeout=300)
        task = result.get("task_id") or result.get("data", {}).get("task_id")
        if not task:
            raise RuntimeError(result)
        entry.update({"video_task_id": task, "video_prompt": VIDEO_PROMPTS[name]})
        save(manifest)
    if not entry.get("video_url"):
        deadline = time.time() + 1800
        while time.time() < deadline:
            time.sleep(10)
            result = post(VIDEO_POLL, {"query": "", "params": {"task_id": task}}, timeout=300)
            status = result.get("status") or result.get("data", {}).get("status")
            print(f"{name}: {status}", flush=True)
            if status == "success":
                entry["video_url"] = result.get("url") or result.get("data", {}).get("url")
                save(manifest)
                break
            if status == "failed":
                raise RuntimeError(result)
        else:
            raise TimeoutError(task)
    download(entry["video_url"], OUT / f"{name}_cinema.mp4")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    source = json.loads(SOURCE_MANIFEST.read_text())
    manifest = json.loads(MANIFEST.read_text()) if MANIFEST.exists() else {}
    scene2_start = manifest.get("scene2_start_url")
    if not scene2_start:
        print("generating scene 2 shared start", flush=True)
        scene2_start = gen_image(SCENE2_START, source["suite"]["end_url"])
        manifest.update({"scene2_start_url": scene2_start, "scene2_start_prompt": SCENE2_START})
        save(manifest)
        time.sleep(3)
    download(scene2_start, OUT / "scene2_start.webp")

    for name in ("passport", "charge-eight", "eight-signatures"):
        entry = manifest.setdefault(name, {})
        if not entry.get("end_url"):
            print(f"generating {name} end", flush=True)
            entry.update({"end_url": gen_image(END_PROMPTS[name], scene2_start), "end_prompt": END_PROMPTS[name]})
            save(manifest)
            time.sleep(3)
        download(entry["end_url"], OUT / f"{name}_end.webp")

    scene3_start = manifest["eight-signatures"]["end_url"]
    manifest["scene3_start_url"] = scene3_start
    save(manifest)
    download(scene3_start, OUT / "scene3_start.webp")
    for name in ("unplug", "eight-breakfasts", "night-manager"):
        entry = manifest.setdefault(name, {})
        if not entry.get("end_url"):
            print(f"generating {name} end", flush=True)
            entry.update({"end_url": gen_image(END_PROMPTS[name], scene3_start), "end_prompt": END_PROMPTS[name]})
            save(manifest)
            time.sleep(3)
        download(entry["end_url"], OUT / f"{name}_end.webp")

    if "--regen-night-manager" in sys.argv:
        entry = manifest["night-manager"]
        old = entry.get("end_url")
        if old:
            entry.setdefault("rejected_end_urls", []).append(old)
        print("regenerating night-manager from clean scene 3 start", flush=True)
        fresh = gen_image(END_PROMPTS["night-manager"], scene3_start)
        entry.update({"end_url": fresh, "end_prompt": END_PROMPTS["night-manager"]})
        entry.pop("video_task_id", None)
        entry.pop("video_url", None)
        save(manifest)
        download(fresh, OUT / "night-manager_end.webp")
        print(json.dumps({"night_manager_end_url": fresh}, ensure_ascii=False), flush=True)
        return

    if "--repair-night-manager" in sys.argv:
        entry = manifest["night-manager"]
        old = entry["end_url"]
        print("repairing night-manager continuity", flush=True)
        repaired = gen_image(REPAIR_NIGHT_MANAGER, old)
        entry.setdefault("rejected_end_urls", []).append(old)
        entry.update({"end_url": repaired, "end_repair_prompt": REPAIR_NIGHT_MANAGER})
        entry.pop("video_task_id", None)
        entry.pop("video_url", None)
        save(manifest)
        download(repaired, OUT / "night-manager_end.webp")
        print(json.dumps({"night_manager_end_url": repaired}, ensure_ascii=False), flush=True)
        return

    if "--stills-only" in sys.argv:
        print(json.dumps(manifest, ensure_ascii=False), flush=True)
        return
    for name in ("passport", "charge-eight", "eight-signatures"):
        make_video(name, scene2_start, manifest[name]["end_url"], manifest[name], manifest)
    for name in ("unplug", "eight-breakfasts", "night-manager"):
        make_video(name, scene3_start, manifest[name]["end_url"], manifest[name], manifest)
    print(json.dumps(manifest, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
