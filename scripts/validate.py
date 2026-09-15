#!/usr/bin/env python3
from pathlib import Path
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
errors = []

required_files = [
    "README.md",
    "README.zh-CN.md",
    "SKILL.md",
    "SKILL.zh-CN.md",
    "AGENTS.md",
    "LICENSE",
    "CITATION.cff",
    "profiles/ddi.md",
    "profiles/ddi.zh-CN.md",
    "profiles/llm_agent.md",
    "profiles/llm_agent.zh-CN.md",
    "profiles/ai4science.md",
    "profiles/ai4science.zh-CN.md",
    "templates/research_note.zh-CN.md",
    "templates/research_note.en.md",
    "rubrics/QUALITY.md",
    "rubrics/QUALITY.zh-CN.md",
    "benchmark/README.md",
    "benchmark/README.zh-CN.md",
    "benchmark/metadata.json",
    "registry/ddi_datasets.yaml",
]
for rel in required_files:
    if not (ROOT / rel).exists():
        errors.append(f"missing file: {rel}")

# Version checks
checks = {
    "SKILL.md": r"Version:\s*\*\*0\.6\.0\*\*",
    "SKILL.zh-CN.md": r"版本：\*\*0\.6\.0\*\*",
    "README.md": r"v0\.6\.0",
    "README.zh-CN.md": r"v0\.6\.0",
    "CITATION.cff": r"version:\s*0\.6\.0",
}
for rel, pattern in checks.items():
    p = ROOT / rel
    if p.exists() and not re.search(pattern, p.read_text(encoding="utf-8")):
        errors.append(f"version mismatch: {rel}")

# Gold notes
gold_dir = ROOT / "benchmark" / "gold_notes"
gold_notes = sorted(gold_dir.glob("[0-9][0-9]_*.md"))
if len(gold_notes) != 12:
    errors.append(f"expected 12 Gold Notes, found {len(gold_notes)}")

required_headings = [
    "# 快读笔记",
    "##### 1、论文标题：",
    "##### 2、研究问题：",
    "##### 3、方法：",
    "##### 4、创新：",
    "##### 5、模型图：",
    "##### 6、所用数据集：",
    "##### 7、缺点/局限：",
    "##### 8、个人评价（是否值得精读）：",
    "# 精读笔记",
    "##### 1、研究背景（相关工作空白、动机）：",
    "##### 2、模型输入输出：",
    "##### 3、关键模块（每个模块的功能）：",
    "##### 4、实验设置（数据集、Baselines、评估指标、实验设备）：",
    "##### 5、案例分析（做了什么样的案例）：",
    "##### 6、关键启发（哪些地方对自己有用）：",
]
for note in gold_notes:
    text = note.read_text(encoding="utf-8")
    missing = [h for h in required_headings if h not in text]
    if missing:
        errors.append(f"{note.name}: missing headings {missing}")

# Metadata
meta_path = ROOT / "benchmark" / "metadata.json"
if meta_path.exists():
    try:
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
        papers = meta.get("papers", [])
        if len(papers) != 12:
            errors.append(f"metadata: expected 12 papers, found {len(papers)}")
        ids = {p.get("paper_id") for p in papers}
        note_ids = {p.stem for p in gold_notes}
        if ids != note_ids:
            errors.append("metadata paper IDs do not match Gold Note filenames")
        for p in papers:
            pid = p.get("paper_id", "<unknown>")
            for key in ["audit","contribution_map","evidence_ledger","version_lock","negative_facts","coverage_spec"]:
                if p.get(key) is None:
                    errors.append(f"{pid}: missing {key}")
            cmap = p.get("contribution_map") or {}
            contributions = cmap.get("author_contributions", [])
            innovations = cmap.get("innovation_bullets", [])
            if len(contributions) < 2:
                errors.append(f"{pid}: contribution map too small")
            if len(innovations) < 2:
                errors.append(f"{pid}: innovation map too small")
            ledger = p.get("evidence_ledger") or []
            if not isinstance(ledger, list) or len(ledger) < 2:
                errors.append(f"{pid}: evidence ledger missing/too small")
    except Exception as e:
        errors.append(f"metadata parse failure: {e}")

# Registry policy
registry = ROOT / "registry" / "ddi_datasets.yaml"
if registry.exists():
    txt = registry.read_text(encoding="utf-8").lower()
    if "autofill" not in txt and "validation" not in txt:
        errors.append("registry should explicitly state validation/no-autofill policy")

if errors:
    print("[FAIL] SciRead v0.6 validation")
    for e in errors:
        print(" -", e)
    sys.exit(1)

print("[PASS] SciRead v0.6 validation")
print(f"Gold Notes: {len(gold_notes)}")
print("Bilingual core docs: present")
print("Benchmark metadata: consistent")
