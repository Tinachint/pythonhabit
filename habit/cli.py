# cli.py

import argparse
from app_controller import AppController

try:
    from importlib.metadata import version
    VERSION = version("habit_tracker")
except Exception:
    VERSION = "1.0"

COMMAND_ALIASES = {
    "ls": "list",
    "rm": "delete",
    "done": "complete"
}

SUPPORTED_COMMANDS = {
    "add", "list", "complete", "update", "help", "exit"
} | set(COMMAND_ALIASES.keys())

def parse_args():
    """Parse and sanitize CLI arguments."""
    parser = argparse.ArgumentParser(description="Track habits via CLI.")
    parser.add_argument("--command", help="Quick command (e.g., 'add', 'list')")
    parser.add_argument("--habit", help="Habit name (for add/complete)")
    parser.add_argument("--periodicity", help="Frequency (daily/weekly/monthly)")
    parser.add_argument("--version", action="store_true", help="Show version")
    parser.add_argument("--dry-run", action="store_true", help="Validate without executing")
    return parser.parse_args()

def main():
    args = parse_args()
    controller = AppController()

    try:
        if args.version:
            print(f"Habit Tracker v{VERSION}")
            return

        if args.dry_run:
            print(f"Valid command: {args.command}")
            return

        if args.command:
            cmd = COMMAND_ALIASES.get(args.command.strip().lower(), args.command.strip().lower())

            if cmd not in SUPPORTED_COMMANDS:
                print("Unsupported command. Type 'help' for options.")
                return

            if cmd == "add" and not (args.habit and args.periodicity):
                print("Usage: --command add --habit <name> --periodicity <frequency>")
                return

            controller.handle_command(
                cmd,
                habit_name=args.habit.strip().lower() if args.habit else None,
                periodicity=args.periodicity.strip().lower() if args.periodicity else None
            )
        else:
            print("\n🌿 Welcome to Habit Tracker CLI")
            print("Type 'help' for commands.\n")
            controller.start()

    except Exception as e:
        print(f"\nError: {e}\n")

    finally:
        print("Goodbye! 👋")

if __name__ == "__main__":
    main()
