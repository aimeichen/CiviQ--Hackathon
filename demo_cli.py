"""Print a CiviQ / Nori MVP response without Flower runtime or an LLM key."""

from __future__ import annotations

import argparse
import json

from agent.nori_mock import build_demo_response


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a CiviQ / Nori MVP demo prompt.")
    parser.add_argument("message", help="The user's message to Nori")
    args = parser.parse_args()
    print(json.dumps(build_demo_response(args.message), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
