#!/usr/bin/env python3
"""Optional 4th agent perspective via Codex CLI or OpenAI API."""

import argparse
import os
import shutil
import subprocess
import sys


def detect_backend():
    """Detect which backend is available. Returns 'codex', 'openai', or 'none'."""
    if shutil.which("codex"):
        return "codex"

    try:
        import openai  # noqa: F401

        if os.environ.get("OPENAI_API_KEY"):
            return "openai"
    except ImportError:
        pass

    return "none"


def run_codex_cli(prompt_text, system_text):
    """Run Codex CLI and return the response text."""
    combined_input = f"SYSTEM PROMPT:\n{system_text}\n\n---\n\nUSER PROMPT:\n{prompt_text}"
    cmd = [
        "codex",
        "exec",
        "--ephemeral",
        "--skip-git-repo-check",
        "--full-auto",
    ]
    result = subprocess.run(
        cmd,
        input=combined_input,
        capture_output=True,
        text=True,
        timeout=300,
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"Codex CLI exited with code {result.returncode}: {result.stderr}"
        )
    return result.stdout


def run_openai_api(prompt_text, system_text):
    """Run OpenAI API and return the response text."""
    import openai

    client = openai.OpenAI()
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_text},
            {"role": "user", "content": prompt_text},
        ],
        temperature=0.3,
    )
    return response.choices[0].message.content


def execute(prompt_path, system_path, output_path, mode):
    """Run the prompt through the best available backend and write output."""
    with open(prompt_path, "r") as f:
        prompt_text = f.read()
    with open(system_path, "r") as f:
        system_text = f.read()

    backend = detect_backend()

    response = None

    if backend == "codex":
        try:
            response = run_codex_cli(prompt_text, system_text)
        except subprocess.TimeoutExpired:
            print(
                f"WARNING: [codex_agent] Codex CLI timed out after 300s (mode={mode}). "
                "Re-run the command or switch to OpenAI API backend.",
                file=sys.stderr,
            )
            sys.exit(1)
    elif backend == "openai":
        response = run_openai_api(prompt_text, system_text)
    else:
        print(
            "[codex_agent] No backend available (need codex CLI or openai package + OPENAI_API_KEY)",
            file=sys.stderr,
        )
        sys.exit(2)

    with open(output_path, "w") as f:
        f.write(response)


def main():
    parser = argparse.ArgumentParser(
        description="Optional 4th agent perspective via Codex CLI or OpenAI API"
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Print availability status and exit",
    )
    parser.add_argument(
        "--prompt",
        metavar="FILE",
        help="Path to file containing the prompt text",
    )
    parser.add_argument(
        "--system",
        metavar="FILE",
        help="Path to file containing the system prompt",
    )
    parser.add_argument(
        "--output",
        metavar="FILE",
        help="Path to write the response output",
    )
    parser.add_argument(
        "--mode",
        choices=["draft", "review", "edit"],
        default="draft",
        help="Mode for logging/context (default: draft)",
    )

    args = parser.parse_args()

    if args.check:
        backend = detect_backend()
        print(backend)
        if backend == "none":
            sys.exit(2)
        sys.exit(0)

    if not (args.prompt and args.system and args.output):
        parser.error("--prompt, --system, and --output are all required when not using --check")

    try:
        execute(args.prompt, args.system, args.output, args.mode)
    except Exception as e:
        print(f"[codex_agent] Error (mode={args.mode}): {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
