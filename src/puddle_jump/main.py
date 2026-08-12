"""Run Puddle Jump's plain command-line interface."""

import argparse
import signal

from puddle_jump.shadow_market import run_shadow_market
from puddle_jump.shadow_process import (
    remove_own_pid,
    show_shadow_logs,
    show_shadow_status,
    start_shadow_process,
    stop_shadow_process,
)


def stop_shadow_runner(_signal_number: int, _current_frame: object) -> None:
    """End the runner cleanly when its process manager asks it to stop."""

    raise SystemExit()


def run_shadow_command(command: str, check_once: bool) -> None:
    """Run one plain shadow-process command."""

    if command == "start":
        start_shadow_process()
    elif command == "status":
        show_shadow_status()
    elif command == "logs":
        show_shadow_logs()
    elif command == "stop":
        stop_shadow_process()
    elif command == "run":
        signal.signal(signal.SIGTERM, stop_shadow_runner)

        try:
            run_shadow_market(check_once=check_once)
        finally:
            remove_own_pid()


def main() -> None:
    """Parse and run one Puddle Jump command."""

    parser = argparse.ArgumentParser(prog="puddle")
    commands = parser.add_subparsers(dest="area")
    shadow_parser = commands.add_parser("shadow", help="Manage live shadow trading.")
    shadow_commands = shadow_parser.add_subparsers(dest="shadow_command", required=True)
    shadow_commands.add_parser("start", help="Start shadow trading in the background.")
    shadow_commands.add_parser("status", help="Show whether shadow trading is running.")
    shadow_commands.add_parser("logs", help="Follow today's readable shadow log.")
    shadow_commands.add_parser("stop", help="Stop today's shadow process.")
    run_parser = shadow_commands.add_parser("run", help=argparse.SUPPRESS)
    run_parser.add_argument("--once", action="store_true", help=argparse.SUPPRESS)
    arguments = parser.parse_args()

    if arguments.area == "shadow":
        run_shadow_command(
            command=arguments.shadow_command,
            check_once=getattr(arguments, "once", False),
        )
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
