#!/usr/bin/env python3
"""Khmer neural voice clips for Trusted Agent.

Uses Edge-TTS with Microsoft's neural Khmer voice (km-KH-PisethNeural and km-KH-SreymomNeural).
Reads TRAINING, COACH_FX, and KM translations from index.html, generates audio/km/*.m4a,
and writes audio/km/manifest.js.

Run:
    tools/.venv/bin/python3 tools/make_km_voice.py
"""
import asyncio, hashlib, json, os, re, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "audio", "km")

import edge_tts

COACH_KM = "km-KH-PisethNeural"
CLIENT_KM = "km-KH-SreymomNeural"

# Common FX translations
FX_KM = {
    "r1": "វគ្គទីមួយ។ ស្តាប់ ហើយនិយាយតាមម្តងមួយឃ្លា។ គូសបញ្ជាក់ពាក្យសំខាន់ និងផ្អាកឲ្យបានត្រឹមត្រូវ។",
    "r2": "វគ្គទីពីរ។ លើកនេះ និយាយដោយចងចាំ។ ឃ្លារបស់អ្នកនឹងត្រូវលាក់ រហូតដល់អ្នកនិយាយចប់។",
    "turn": "វេនរបស់អ្នក។",
    "good": "និយាយបានល្អណាស់។ បន្តទៅមុខទៀតនៅពេលអ្នករួចរាល់។",
    "pace": "លឿនបន្តិចហើយ។ បន្ថយល្បឿន ហើយទុកចន្លោះផ្អាកឲ្យបានច្បាស់។",
    "pause": "ផ្អាកមួយចង្វាក់ពេញ។ ភាពស្ងៀមស្ងាត់បង្ហាញពីទំនុកចិត្ត។",
    "end": "ពាក្យចុងក្រោយរបស់អ្នកស្រាលពេក។ និយាយឲ្យរឹងមាំរហូតដល់ចប់។",
    "nospeech": "ខ្ញុំមិនឮអ្វីសោះ។ សូមពិនិត្យមីក្រូហ្វូន ហើយព្យាយាមម្តងទៀត។",
    "done1": "បានបញ្ចប់វគ្គទីមួយ។ បន្ទាប់មក និយាយដោយចងចាំ។",
    "done2": "បានបញ្ចប់ការសន្ទនា។ ឥឡូវនេះ សូមសរសេរឃ្លាសំខាន់ៗឡើងវិញតាមពាក្យផ្ទាល់ខ្លួនរបស់អ្នក។",
    "quiz": "តើមួយណាជាវិធីអាជីព?",
    "best": "នោះហើយជាវិធីអាជីព។",
    "risky": "ប្រថុយប្រថាន។",
    "notway": "មិនមែនជាវិធីអាជីពទេ។",
    "right": "ត្រឹមត្រូវ។",
    "wrong": "មិនទាន់ត្រឹមត្រូវទេ។",
    "say": "ស្តាប់ ហើយនិយាយតាម។",
    "ldone": "បានបញ្ចប់មេរៀន។ ធ្វើបានល្អណាស់។",
    "breathe": "ដកដង្ហើមតាមរង្វង់។ ដកចូល ៤ វិនាទី។ ដកចេញ ៦ វិនាទី។",
    "br-in": "ដកដង្ហើមចូល។",
    "br-out": "ហើយដកដង្ហើមចេញយឺតៗ។",
    "br-done": "ល្អណាស់។ ឥឡូវនេះអ្នករួចរាល់ហើយ។"
}

def clean_km(t):
    t = re.sub(r"<[^>]+>", " ", t)
    t = re.sub(r"[\*↘]", "", t)
    t = re.sub(r"‧‧‧‧‧", " ", t)
    t = re.sub(r"‧‧‧", " ", t)
    t = re.sub(r"\s+", " ", t).strip()
    return t

def block(src, name):
    i = src.index(name) + len(name)
    return json.JSONDecoder().raw_decode(src, i)[0]

def collect_km_jobs():
    src = open(os.path.join(ROOT, "index.html"), encoding="utf-8").read()
    T = block(src, "const TRAINING = ")
    KM = block(src, "const KM=")
    
    jobs = []
    
    # 1. Coach FX
    for k, text_km in FX_KM.items():
        jobs.append((f"c-fx-{k}", COACH_KM, text_km))
        
    # Test greeting
    jobs.append(("test-km", COACH_KM, "រីករាយដែលបានជួបលោកអ្នក។ ខ្ញុំជាទីប្រឹក្សាអចលនទ្រព្យអាជីព។"))
    jobs.append(("at0-t0", COACH_KM, "រីករាយដែលបានជួបលោកអ្នក។ អរគុណសម្រាប់ពេលវេលារបស់លោកអ្នក។"))
    
    # 2. Lessons
    for i, l in enumerate(T["lessons"]):
        if l.get("stub"): continue
        title = l["title"]
        title_km = KM.get(title, title)
        
        # Intro
        if l.get("objectives"):
            obj_km = [KM.get(o, o) for o in l["objectives"]]
            intro_text = f"{title_km}។ ក្នុងមេរៀននេះ៖ " + " ".join(obj_km)
            jobs.append((f"c-at{i}-intro", COACH_KM, intro_text))
            
        # Sections
        for k, x in enumerate(l.get("sections", [])):
            hd = x.get("heading", "")
            bd = x.get("body", "")
            hd_km = KM.get(hd, hd)
            bd_km = KM.get(bd, bd)
            
            # If translated
            if hd_km != hd or bd_km != bd:
                sec_text = f"{hd_km}។ {bd_km}"
                jobs.append((f"c-at{i}-s{k}", COACH_KM, clean_km(sec_text)))
                
            # Flow steps
            for j, f in enumerate(x.get("flow", [])):
                ft = f.get("title", "")
                fs = f.get("sub", "")
                ft_km = KM.get(ft, ft)
                fs_km = KM.get(fs, fs)
                if ft_km != ft or fs_km != fs:
                    step_text = f"ជំហានទី {j+1}៖ {ft_km}។ {fs_km}"
                    jobs.append((f"c-at{i}-s{k}-f{j}", COACH_KM, clean_km(step_text)))
                    
            # Extra units (data, box, analogy)
            x_count = 0
            if x.get("analogy"):
                an = KM.get(x["analogy"], x["analogy"])
                jobs.append((f"c-at{i}-s{k}-x{x_count}", COACH_KM, clean_km(f"សូមគិតបែបនេះ៖ {an}")))
                x_count += 1
            if x.get("box"):
                for line in x["box"]["lines"]:
                    jobs.append((f"c-at{i}-s{k}-x{x_count}", COACH_KM, clean_km(KM.get(line, line))))
                    x_count += 1
            if x.get("data"):
                for d in x["data"]:
                    jobs.append((f"c-at{i}-s{k}-x{x_count}", COACH_KM, clean_km(KM.get(d, d))))
                    x_count += 1

            # Rules
            for j, r in enumerate(x.get("rules", [])):
                rt = KM.get(r.get("title", ""), r.get("title", ""))
                rd = KM.get(r.get("detail", ""), r.get("detail", ""))
                ra = KM.get(r.get("action", ""), r.get("action", ""))
                rule_text = f"{rt}។ {rd}" + (f" ធ្វើដូច្នេះ៖ {ra}" if ra else "")
                jobs.append((f"c-at{i}-s{k}-r{j}", COACH_KM, clean_km(rule_text)))

        # Quiz
        for k, q in enumerate(l.get("quiz", [])):
            prompt = q.get("prompt") or q.get("q") or ""
            why = q.get("why") or q.get("explain") or ""
            prompt_km = KM.get(prompt, prompt)
            why_km = KM.get(why, why)
            if prompt_km != prompt:
                jobs.append((f"c-lesson{i}-q{k}", COACH_KM, clean_km(prompt_km)))
            if why_km != why:
                jobs.append((f"c-lesson{i}-q{k}-why", COACH_KM, clean_km(why_km)))
                
        # Reflection
        refl = l.get("reflection", "")
        refl_km = KM.get(refl, refl)
        if refl_km != refl:
            jobs.append((f"c-at{i}-rf", COACH_KM, clean_km(refl_km)))
            
    return jobs

async def render_clip(voice, text, out_path):
    with tempfile.TemporaryDirectory() as tmp:
        mp3 = os.path.join(tmp, "clip.mp3")
        comm = edge_tts.Communicate(text, voice)
        await comm.save(mp3)
        subprocess.run(["afconvert", "-f", "m4af", "-d", "aac", "-b", "64000", mp3, out_path], check=True)

async def main():
    os.makedirs(OUT, exist_ok=True)
    mf = os.path.join(OUT, "manifest.js")
    manifest = {}
    if os.path.exists(mf):
        m = re.search(r"=\s*(\{.*\})\s*;?\s*$", open(mf, encoding="utf-8").read(), re.S)
        if m: manifest = json.loads(m.group(1))
        
    jobs = collect_km_jobs()
    print(f"Collected {len(jobs)} Khmer audio jobs.")
    
    made, kept = 0, 0
    for lid, voice, text in jobs:
        text = clean_km(text)
        h = hashlib.sha1(f"edge-tts|{voice}|{text}".encode()).hexdigest()[:12]
        fn = f"{lid}.m4a"
        path = os.path.join(OUT, fn)
        
        if manifest.get(lid, {}).get("h") == h and os.path.exists(path):
            kept += 1
            continue
            
        print(f"Generating [{lid}]: {text[:50]}...")
        try:
            await render_clip(voice, text, path)
            manifest[lid] = {"url": f"audio/km/{fn}", "voice": voice, "h": h}
            made += 1
        except Exception as e:
            print(f"  Error generating {lid}: {e}")
            
    with open(mf, "w", encoding="utf-8") as fh:
        fh.write("// Generated by tools/make_km_voice.py. Do not edit by hand.\nwindow.AUDIO_KM = " + json.dumps(manifest, indent=2, ensure_ascii=False) + ";\n")
        
    print(f"\nDone: {made} generated, {kept} cached. Manifest saved to {mf}.")

if __name__ == "__main__":
    asyncio.run(main())
