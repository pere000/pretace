#!/usr/bin/env python3
from pathlib import Path
import requests
MODEL = "qwen2.5-coder:7b"
PROJECT = Path(__file__).resolve().parent / "pretace"
OLLAMA = "http://127.0.0.1:11434/api/chat"
SYSTEM = """
You are the Local AI for the PRETACE project.
Rules:
1. You never have direct filesystem access.
2. Every file comes from local_ai.py.
3. Never invent filenames.
4. Never request the project file list.
5. If you need another file, reply ONLY with:
REQUEST <filename>
6. When you have enough information, stop requesting files.
7. Return ONLY bash script content for z.scr (no explanations).
"""
BASE_DIR = Path(__file__).resolve().parent
TASK = (BASE_DIR / "local_ai.txt").read_text(encoding="utf-8")
OUT = BASE_DIR / "z.scr"
files = sorted(PROJECT.rglob("*.py"))
tree = "\n".join(str(f.relative_to(PROJECT)) for f in files)
messages = [
{"role": "system", "content": SYSTEM},
{
"role": "user",
"content": "AVAILABLE FILES\n\n" + tree + "\n\n" + TASK,
},
]
already_sent = set()
final_answer = ""
while True:
r = requests.post(
OLLAMA,
json={"model": MODEL, "messages": messages, "stream": False},
timeout=120,
)
r.raise_for_status()
answer = r.json()["message"]["content"].strip()
if not answer.startswith("REQUEST "):
final_answer = answer
break
filename = answer[8:].strip()
if filename in already_sent:
messages.append(
{
"role": "user",
"content": f"The file '{filename}' was already provided. Continue.",
}
)
continue
matches = list(PROJECT.rglob(filename))
if not matches:
messages.append(
{
"role": "user",
"content": f"File '{filename}' does not exist. Choose another file.",
}
)
continue
text = matches[0].read_text(encoding="utf-8", errors="ignore")
already_sent.add(filename)
messages.append({"role": "assistant", "content": answer})
messages.append({"role": "user", "content": f"FILE: {filename}\n\n{text}"})
def strip_markdown_fences(s: str) -> str:
s = s.strip()
if s.startswith("~~~") and s.endswith("~~~"):
lines = s.splitlines()
if len(lines) >= 2:
return "\n".join(lines[1:-1]).strip() + "\n"
if s.startswith("```") and s.endswith("```"):
lines = s.splitlines()
if len(lines) >= 2:
return "\n".join(lines[1:-1]).strip() + "\n"
return s + "\n"
script_text = strip_markdown_fences(final_answer)
OUT.write_text(script_text, encoding="utf-8")
print(f"Wrote {OUT}")
