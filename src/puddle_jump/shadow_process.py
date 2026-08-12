"""Start and manage the detached live shadow process."""

import os
import signal
import subprocess
import sys
import time
from collections import deque
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

MARKET_TIME_ZONE = ZoneInfo("America/New_York")
TRADING_DAYS_DIRECTORY = Path("data/trading-days")


def get_shadow_paths() -> tuple[Path, Path, Path]:
    """Return today's directory, PID file, and readable log path."""

    trading_day = datetime.now(MARKET_TIME_ZONE).date()
    trading_day_directory = TRADING_DAYS_DIRECTORY / trading_day.isoformat()
    pid_path = trading_day_directory / "shadow-market.pid"
    log_path = trading_day_directory / "shadow-market.log"

    return trading_day_directory, pid_path, log_path


def read_shadow_pid(pid_path: Path) -> int | None:
    """Read a saved process ID when the file contains one valid number."""

    result: int | None = None

    if not pid_path.is_file():
        return result

    saved_pid = pid_path.read_text(encoding="utf-8").strip()

    if saved_pid.isdigit():
        result = int(saved_pid)

    return result


def process_is_running(process_id: int | None) -> bool:
    """Return whether the saved process still exists."""

    if process_id is None:
        return False

    result = True

    try:
        os.kill(process_id, 0)
    except ProcessLookupError:
        result = False
    except PermissionError:
        result = True

    return result


def start_shadow_process() -> None:
    """Start one detached shadow runner and save its exact process ID."""

    trading_day_directory, pid_path, log_path = get_shadow_paths()
    saved_pid = read_shadow_pid(pid_path)

    if process_is_running(saved_pid):
        print(f"Shadow market is already running with PID {saved_pid}.")
        print(f"Log: {log_path}")

        return

    trading_day_directory.mkdir(parents=True, exist_ok=True)
    process_log_path = trading_day_directory / "shadow-process.log"

    with process_log_path.open("a", encoding="utf-8") as process_log:
        process = subprocess.Popen(
            [sys.executable, "-m", "puddle_jump.main", "shadow", "run"],
            stdin=subprocess.DEVNULL,
            stdout=process_log,
            stderr=subprocess.STDOUT,
            start_new_session=True,
        )

    pid_path.write_text(f"{process.pid}\n", encoding="utf-8")
    print(f"Shadow market started with PID {process.pid}.")
    print("No Alpaca orders will be submitted.")
    print(f"Log: {log_path}")
    print("Watch it: ./puddle shadow logs")


def show_shadow_status() -> None:
    """Print whether today's exact shadow process is running."""

    _, pid_path, log_path = get_shadow_paths()
    saved_pid = read_shadow_pid(pid_path)

    if process_is_running(saved_pid):
        print(f"Shadow market is running with PID {saved_pid}.")
        print(f"Log: {log_path}")

        return

    print("Shadow market is not running.")

    if log_path.is_file():
        print(f"Latest log: {log_path}")


def show_shadow_logs() -> None:
    """Show recent saved log lines and follow new ones until interrupted."""

    _, _, log_path = get_shadow_paths()

    if not log_path.is_file():
        print("Today's shadow log does not exist yet.")

        return

    with log_path.open(encoding="utf-8") as log_file:
        recent_lines = deque(log_file, maxlen=20)

        for saved_line in recent_lines:
            print(saved_line, end="")

        try:
            while True:
                new_line = log_file.readline()

                if new_line:
                    print(new_line, end="", flush=True)
                else:
                    time.sleep(1)
        except KeyboardInterrupt:
            print("\nStopped watching the log. Shadow trading is still running.")


def stop_shadow_process() -> None:
    """Ask today's exact shadow process to stop and wait briefly."""

    _, pid_path, log_path = get_shadow_paths()
    saved_pid = read_shadow_pid(pid_path)

    if not process_is_running(saved_pid):
        print("Shadow market is not running.")

        return

    os.kill(saved_pid, signal.SIGTERM)

    for _ in range(50):
        if not process_is_running(saved_pid):
            pid_path.unlink(missing_ok=True)
            print("Shadow market stopped.")
            print(f"Log: {log_path}")

            return

        time.sleep(0.1)

    print(f"Shadow market received the stop request but PID {saved_pid} is still running.")


def remove_own_pid() -> None:
    """Remove the PID file only when it still identifies this process."""

    _, pid_path, _ = get_shadow_paths()
    saved_pid = read_shadow_pid(pid_path)

    if saved_pid == os.getpid():
        pid_path.unlink(missing_ok=True)
