#!/usr/bin/env python3
"""
Fill placeholder distractors in evaluation specs using Claude API.

Reads specs with PLACEHOLDER_A/C/D options and asks Claude to generate
plausible but wrong distractors based on the anchor's domain.

Usage:
  python3 evaluations/fill-distractors.py              # Fill all placeholders
  python3 evaluations/fill-distractors.py --dry-run     # Preview prompts
  python3 evaluations/fill-distractors.py --anchor arc42 # Single anchor
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


def needs_distractors(spec):
    """Check if spec has placeholder distractors."""
    q = spec.get("questions", {}).get("recognition", {})
    options = q.get("options", {})
    return any("PLACEHOLDER" in str(v) for v in options.values())


def generate_distractors(spec):
    """Use Claude API to generate 3 plausible distractors."""
    try:
        import anthropic
    except ImportError:
        print("anthropic package required: pip install anthropic")
        sys.exit(1)

    q = spec["questions"]["recognition"]
    correct = q["options"]["B"]
    title = q["question"].strip().split('"')[1] if '"' in q["question"] else spec["anchor"]
    related = q.get("_related", [])
    proponents = q.get("_proponents", "")

    prompt = f"""Generate 3 plausible but WRONG multiple-choice distractors for this question:

Question: Which of the following best describes "{title}"?
Correct answer: {correct}

Requirements for distractors:
- Each distractor should be a one-sentence description of a DIFFERENT but related concept
- They must be wrong but sound plausible to someone unfamiliar with the topic
- All 4 options (correct + 3 distractors) should be similar in length
- Do NOT include the correct concept in any distractor
- Draw distractors from adjacent concepts in software engineering, architecture, or methodology
{f"- Related anchors for inspiration: {', '.join(related)}" if related else ""}
{f"- The correct answer is associated with: {proponents}" if proponents else ""}

Return ONLY a JSON object with keys "A", "C", "D" containing the 3 distractor strings. No explanation."""

    client = anthropic.Anthropic()
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=300,
        temperature=0.7,  # some creativity for diverse distractors
        messages=[{"role": "user", "content": prompt}],
    )

    text = response.content[0].text.strip()
    # Parse JSON from response (might be wrapped in ```json ... ```)
    if "```" in text:
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]
        text = text.strip()

    return json.loads(text)


def main():
    parser = argparse.ArgumentParser(description="Fill placeholder distractors using Claude API")
    parser.add_argument("--dry-run", action="store_true", help="Preview without writing")
    parser.add_argument("--anchor", help="Process single anchor")
    args = parser.parse_args()

    specs_to_fill = []
    for f in sorted(SPECS_DIR.glob("*.yaml")):
        spec = yaml.safe_load(f.read_text(encoding="utf-8"))
        if args.anchor and spec["anchor"] != args.anchor:
            continue
        if needs_distractors(spec):
            specs_to_fill.append((f, spec))

    print(f"Found {len(specs_to_fill)} specs needing distractors")

    for filepath, spec in specs_to_fill:
        anchor_id = spec["anchor"]
        print(f"  {anchor_id}...", end=" ", flush=True)

        if args.dry_run:
            print("(dry run)")
            continue

        try:
            distractors = generate_distractors(spec)
            q = spec["questions"]["recognition"]
            q["options"]["A"] = distractors["A"]
            q["options"]["C"] = distractors["C"]
            q["options"]["D"] = distractors["D"]

            # Remove helper notes
            q.pop("_note", None)
            q.pop("_related", None)
            q.pop("_proponents", None)
            q.pop("_also_known_as", None)

            with open(filepath, "w", encoding="utf-8") as fh:
                yaml.dump(spec, fh, default_flow_style=False, allow_unicode=True, sort_keys=False)
            print("OK")

        except Exception as e:
            print(f"ERROR: {e}")

    print("\nDone. Review the generated distractors before running evaluations!")


if __name__ == "__main__":
    main()
