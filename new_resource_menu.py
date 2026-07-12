#!/usr/bin/env python3

import json
from pathlib import Path
import logging

logging.getLogger("tace.resource_manager").setLevel(logging.CRITICAL)

from new_resource_manager import ResourceManager

CONFIG = Path("new_tace_runtime.json")


def load_runtime():
    return json.loads(CONFIG.read_text(encoding="utf-8"))


def save_runtime(data):
    CONFIG.write_text(
        json.dumps(data, indent=4),
        encoding="utf-8"
    )


def main():

    while True:

        rm = ResourceManager()
        resources = rm.get_all_resources()

        print()
        print("=" * 60)
        print("                    RESOURCE MANAGER")
        print("=" * 60)
        print()

        for i, r in enumerate(resources, 1):
            state = "Enabled" if r["enabled"] else "Disabled"
            print(f"{i:2}. {r['name']:<20} {state}")

        print()
        print("-" * 60)
        print("t<number>    Toggle resource")
        print("0            Return")
        print("-" * 60)

        cmd = input("Option: ").strip()

        if cmd == "0":
            return

        if cmd.lower().startswith("t"):

            value = cmd[1:].strip()

            if not value.isdigit():
                print("\\nUsage: t<number>")
                continue

            idx = int(value) - 1

            if idx < 0 or idx >= len(resources):
                print("\\nInvalid resource.")
                continue

            data = load_runtime()

            name = resources[idx]["name"]

            current = bool(data["resources"][name])

            data["resources"][name] = not current

            save_runtime(data)

            print(f"\\n{name} -> {'Enabled' if not current else 'Disabled'}")

            continue

        print("\\nInvalid option.")


if __name__ == "__main__":
    main()
