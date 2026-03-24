#!/usr/bin/env python3
"""
Generate Level 2 (Application) questions for evaluation specs using Claude API.

For each anchor that has a recognition question but no application question,
generates a realistic scenario with anchor prompt, paraphrase, and MC options.

Usage:
  python3 evaluations/generate-l2-specs.py              # Fill all missing L2
  python3 evaluations/generate-l2-specs.py --dry-run     # Preview
  python3 evaluations/generate-l2-specs.py --anchor arc42 # Single anchor
"""

import argparse
import json
import os
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("PyYAML required: pip install pyyaml")
    sys.exit(1)

SPECS_DIR = Path(__file__).parent / "specs"
ANCHORS_DIR = Path(__file__).parent.parent / "docs" / "anchors"

SKIP_ANCHORS = {"sanity-check", "negative-control"}


def load_anchor_context(anchor_id):
    """Load anchor .adoc file for context."""
    adoc = ANCHORS_DIR / f"{anchor_id}.adoc"
    if adoc.exists():
        return adoc.read_text(encoding="utf-8")[:2000]
    return ""


def needs_application(spec):
    """Check if spec is missing an application question."""
    return "application" not in spec.get("questions", {})


def generate_application(spec):
    """Use Claude API to generate an L2 Application question."""
    try:
        import anthropic
    except ImportError:
        print("anthropic package required: pip install anthropic")
        sys.exit(1)

    anchor_id = spec["anchor"]
    title = spec["questions"]["recognition"]["question"].split('"')[1] if '"' in spec["questions"]["recognition"]["question"] else anchor_id
    context = load_anchor_context(anchor_id)

    prompt = f"""Generate a Level 2 Application multiple-choice question for the semantic anchor "{title}".

The question tests whether an LLM can APPLY the methodology, not just describe it.

Anchor definition (from .adoc file):
{context}

Requirements:
1. Write a realistic SCENARIO (2-3 sentences) describing a concrete software engineering situation where this anchor applies.
2. Write an ANCHOR_PROMPT — a short phrase like "using {title}" that would be added to the scenario.
3. Write a PARAPHRASE_PROMPT — describes the GOAL without naming the methodology or hinting at the correct answer. Must be fair: not too specific (leaks answer) and not too vague.
4. Write 4 OPTIONS (A, B, C, D) — one correct answer that reflects the methodology, three plausible alternatives.
5. All options should be similar in length.
6. The correct answer should reflect what a practitioner of this methodology would recommend.

Return ONLY a JSON object with this exact structure:
{{
  "scenario": "...",
  "anchor_prompt": "using {title}",
  "paraphrase_prompt": "...",
  "options": {{
    "A": "...",
    "B": "...",
    "C": "...",
    "D": "..."
  }},
  "correct": "B"
}}

Make B the correct answer. No explanation outside the JSON."""

    client = anthropic.Anthropic()
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=500,
        temperature=0.7,
        messages=[{"role": "user", "content": prompt}],
    )

    text = response.content[0].text.strip()
    if "```" in text:
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]
        text = text.strip()

    return json.loads(text)


def main():
    parser = argparse.ArgumentParser(description="Generate L2 Application questions using Claude API")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--anchor", help="Process single anchor")
    args = parser.parse_args()

    specs_to_fill = []
    for f in sorted(SPECS_DIR.glob("*.yaml")):
        spec = yaml.safe_load(f.read_text(encoding="utf-8"))
        if spec["anchor"] in SKIP_ANCHORS:
            continue
        if args.anchor and spec["anchor"] != args.anchor:
            continue
        if needs_application(spec):
            specs_to_fill.append((f, spec))

    print(f"Found {len(specs_to_fill)} specs needing L2 Application questions")

    for filepath, spec in specs_to_fill:
        anchor_id = spec["anchor"]
        print(f"  {anchor_id}...", end=" ", flush=True)

        if args.dry_run:
            print("(dry run)")
            continue

        try:
            app = generate_application(spec)
            spec["questions"]["application"] = app

            with open(filepath, "w", encoding="utf-8") as fh:
                yaml.dump(spec, fh, default_flow_style=False, allow_unicode=True, sort_keys=False)
            print("OK")

        except Exception as e:
            print(f"ERROR: {e}")

    print("\nDone. Review the generated scenarios before running evaluations!")


if __name__ == "__main__":
    main()
