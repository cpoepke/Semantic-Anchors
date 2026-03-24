#!/usr/bin/env python3
"""
Generate Level 1 (Recognition) evaluation specs from .adoc anchor metadata.

Reads each anchor's Core Concepts and Related Anchors to produce:
- A correct answer from the anchor's core description
- 3 plausible distractors from related/adjacent anchors

Output: YAML specs in evaluations/specs/ (only recognition section).
Existing specs are preserved — only missing anchors are generated.

Usage:
  python3 evaluations/generate-l1-specs.py              # Generate all Tier 3
  python3 evaluations/generate-l1-specs.py --dry-run     # Preview without writing
  python3 evaluations/generate-l1-specs.py --anchor arc42  # Single anchor
"""

import argparse
import os
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("PyYAML required: pip install pyyaml")
    sys.exit(1)

ANCHORS_DIR = Path(__file__).parent.parent / "docs" / "anchors"
SPECS_DIR = Path(__file__).parent / "specs"

# Skip these anchors (templates, meta, sub-patterns handled by umbrella)
SKIP_PREFIXES = ["_template", "gof-", "solid-", "test-double-"]
SKIP_EXACT = ["what-qualifies-as-a-semantic-anchor", "gof-design-patterns",
              "solid-principles", "test-double-meszaros"]


def parse_adoc(filepath):
    """Extract metadata from an .adoc anchor file."""
    content = filepath.read_text(encoding="utf-8")
    lines = content.split("\n")

    result = {
        "id": filepath.stem,
        "title": "",
        "tier": None,
        "categories": "",
        "related": [],
        "proponents": "",
        "also_known_as": "",
        "core_concepts": [],
        "when_to_use": [],
    }

    # Parse attributes
    for line in lines:
        if line.startswith("= "):
            result["title"] = line[2:].strip()
        elif line.startswith(":tier:"):
            result["tier"] = int(line.split(":tier:")[1].strip())
        elif line.startswith(":categories:"):
            result["categories"] = line.split(":categories:")[1].strip()
        elif line.startswith(":related:"):
            result["related"] = [r.strip() for r in line.split(":related:")[1].strip().split(",")]
        elif line.startswith(":proponents:"):
            result["proponents"] = line.split(":proponents:")[1].strip()

    # Parse core concepts (definition list items)
    in_core = False
    in_when = False
    for line in lines:
        if "Core Concepts" in line:
            in_core = True
            in_when = False
            continue
        if "When to Use" in line:
            in_core = False
            in_when = True
            continue
        if "Related" in line or "Contrast" in line or "Technical" in line:
            in_core = False
            in_when = False
            continue

        if in_core and "::" in line:
            term = line.split("::")[0].strip()
            desc = line.split("::", 1)[1].strip() if "::" in line else ""
            if term and not term.startswith("[") and not term.startswith("Key Proponent"):
                result["core_concepts"].append({"term": term, "desc": desc})
        elif in_when and line.strip().startswith("*"):
            result["when_to_use"].append(line.strip().lstrip("* "))

    # Also known as
    for line in lines:
        if "Also known as::" in line:
            result["also_known_as"] = line.split("Also known as::")[1].strip()

    return result


def build_correct_answer(anchor):
    """Build a one-sentence correct answer from core concepts."""
    concepts = anchor["core_concepts"][:4]
    if not concepts:
        return None

    parts = []
    for c in concepts:
        if c["desc"]:
            parts.append(c["desc"].rstrip("."))
        else:
            parts.append(c["term"])

    if len(parts) >= 2:
        return f"{parts[0]}; {parts[1].lower()}"
    return parts[0]


def generate_spec(anchor, all_anchors):
    """Generate a YAML spec dict for one anchor."""
    correct = build_correct_answer(anchor)
    if not correct:
        return None

    spec = {
        "anchor": anchor["id"],
        "tier": anchor["tier"],
        "questions": {
            "recognition": {
                "question": f'Which of the following best describes "{anchor["title"]}"?\n',
                "options": {
                    "A": "PLACEHOLDER_A",
                    "B": correct,
                    "C": "PLACEHOLDER_C",
                    "D": "PLACEHOLDER_D",
                },
                "correct": "B",
                "_note": "REVIEW NEEDED: Distractors are placeholders. Replace A, C, D with plausible wrong answers from related anchors.",
                "_related": anchor["related"],
                "_proponents": anchor["proponents"],
                "_also_known_as": anchor["also_known_as"],
            }
        }
    }
    return spec


def should_skip(anchor_id):
    """Check if anchor should be skipped."""
    if anchor_id in SKIP_EXACT:
        return True
    for prefix in SKIP_PREFIXES:
        if anchor_id.startswith(prefix) and anchor_id not in SKIP_EXACT:
            return True
    return False


def main():
    parser = argparse.ArgumentParser(description="Generate L1 evaluation specs from .adoc metadata")
    parser.add_argument("--dry-run", action="store_true", help="Preview without writing files")
    parser.add_argument("--anchor", help="Generate for a single anchor ID")
    parser.add_argument("--force", action="store_true", help="Overwrite existing specs")
    args = parser.parse_args()

    # Parse all anchors
    all_anchors = {}
    for f in sorted(ANCHORS_DIR.glob("*.adoc")):
        if f.stem.endswith(".de") or f.stem == "_template":
            continue
        anchor = parse_adoc(f)
        all_anchors[anchor["id"]] = anchor

    # Filter to Tier 3, skip sub-patterns
    targets = []
    for aid, anchor in all_anchors.items():
        if args.anchor and aid != args.anchor:
            continue
        if anchor["tier"] != 3:
            continue
        if should_skip(aid):
            continue
        targets.append(anchor)

    print(f"Found {len(targets)} Tier 3 anchors to process")

    generated = 0
    skipped = 0
    for anchor in targets:
        spec_file = SPECS_DIR / f"{anchor['id']}.yaml"

        if spec_file.exists() and not args.force:
            skipped += 1
            continue

        spec = generate_spec(anchor, all_anchors)
        if not spec:
            print(f"  SKIP {anchor['id']}: no core concepts found")
            continue

        if args.dry_run:
            print(f"\n--- {anchor['id']} ---")
            print(yaml.dump(spec, default_flow_style=False, allow_unicode=True))
        else:
            SPECS_DIR.mkdir(parents=True, exist_ok=True)
            with open(spec_file, "w", encoding="utf-8") as fh:
                yaml.dump(spec, fh, default_flow_style=False, allow_unicode=True, sort_keys=False)
            print(f"  WROTE {spec_file.name}")
            generated += 1

    print(f"\nDone: {generated} generated, {skipped} skipped (already exist)")


if __name__ == "__main__":
    main()
