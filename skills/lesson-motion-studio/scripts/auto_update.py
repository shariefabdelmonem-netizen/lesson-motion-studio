#!/usr/bin/env python3
"""Install and update a local Lesson Motion Studio skill from its public GitHub source."""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import os
import plistlib
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
import urllib.error
import urllib.request
import zipfile
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

REPOSITORY = "shariefabdelmonem-netizen/lesson-motion-studio"
SKILL_RELATIVE = "skills/lesson-motion-studio/"
STATE_NAME = ".lesson-motion-studio-update.json"
MAX_ARCHIVE_BYTES = 30_000_000
MAX_FILE_BYTES = 15_000_000
MAX_TOTAL_BYTES = 60_000_000


def request_bytes(url: str, limit: int = MAX_ARCHIVE_BYTES) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": "lesson-motion-studio-updater/1"})
    with urllib.request.urlopen(request, timeout=25) as response:
        data = response.read(limit + 1)
    if len(data) > limit:
        raise ValueError("Remote response exceeds the allowed size")
    return data


def latest_commit() -> str:
    payload = request_bytes(f"https://api.github.com/repos/{REPOSITORY}/commits/main", 100_000)
    sha = json.loads(payload)["sha"]
    if not re.fullmatch(r"[0-9a-f]{40}", sha):
        raise ValueError("GitHub returned an invalid commit identifier")
    return sha


def file_hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def package_hashes(directory: Path) -> dict[str, str]:
    if any(path.is_symlink() for path in directory.rglob("*")):
        raise ValueError("The installed skill contains a symbolic link")
    return {
        path.relative_to(directory).as_posix(): file_hash(path)
        for path in sorted(directory.rglob("*"))
        if path.is_file() and path.name not in {STATE_NAME, ".DS_Store"}
        and "__pycache__" not in path.parts
    }


def unpack_skill(archive: bytes, destination: Path) -> None:
    with zipfile.ZipFile(io.BytesIO(archive)) as source:
        members = [item for item in source.infolist() if not item.is_dir()]
        roots = {
            item.filename.split(SKILL_RELATIVE, 1)[0]
            for item in members
            if item.filename.endswith(SKILL_RELATIVE + "SKILL.md")
        }
        if len(roots) != 1:
            raise ValueError("The archive does not contain exactly one skill folder")
        prefix = roots.pop() + SKILL_RELATIVE
        total = 0
        extracted = 0
        for item in members:
            if not item.filename.startswith(prefix):
                continue
            relative = PurePosixPath(item.filename[len(prefix):])
            if not relative.parts or relative.is_absolute() or ".." in relative.parts:
                raise ValueError("The archive contains an unsafe path")
            if ((item.external_attr >> 16) & 0o170000) == 0o120000:
                raise ValueError("The archive contains a symbolic link")
            if item.file_size > MAX_FILE_BYTES:
                raise ValueError("A skill file exceeds the allowed size")
            total += item.file_size
            if total > MAX_TOTAL_BYTES:
                raise ValueError("The skill exceeds the allowed size")
            target = destination.joinpath(*relative.parts)
            target.parent.mkdir(parents=True, exist_ok=True)
            with source.open(item) as reader, target.open("wb") as writer:
                shutil.copyfileobj(reader, writer)
            extracted += 1
        if extracted == 0:
            raise ValueError("The archive contains no skill files")
    manifest = destination / "SKILL.md"
    if not manifest.is_file() or not re.search(
        r"\A---\s*\nname:\s*lesson-motion-studio\s*\n", manifest.read_text(encoding="utf-8")
    ):
        raise ValueError("The downloaded skill manifest is invalid")
    if not (destination / "scripts" / "auto_update.py").is_file():
        raise ValueError("The downloaded skill lacks its updater")


def read_state(destination: Path) -> dict:
    state_path = destination / STATE_NAME
    if not state_path.is_file():
        raise ValueError("This copy is not managed by the updater; run install --replace once")
    state = json.loads(state_path.read_text(encoding="utf-8"))
    if (
        not isinstance(state, dict)
        or state.get("repository") != REPOSITORY
        or not isinstance(state.get("sha"), str)
        or not re.fullmatch(r"[0-9a-f]{40}", state["sha"])
    ):
        raise ValueError("The installed update state is invalid")
    return state


def require_unmodified(destination: Path, state: dict) -> None:
    if package_hashes(destination) != state.get("files"):
        raise ValueError("Local skill files changed; automatic update stopped to preserve them")


def install_snapshot(destination: Path, sha: str, replace: bool) -> Path | None:
    if destination.is_symlink():
        raise ValueError("Refusing to replace a symbolic-link skill directory")
    if destination.exists() and not replace:
        raise ValueError("Skill directory already exists; use install --replace to keep a backup")
    destination.parent.mkdir(parents=True, exist_ok=True)
    archive = request_bytes(f"https://codeload.github.com/{REPOSITORY}/zip/{sha}")
    stage = Path(tempfile.mkdtemp(prefix=".lesson-motion-studio-new-", dir=destination.parent))
    backup = None
    try:
        unpack_skill(archive, stage)
        state = {"repository": REPOSITORY, "sha": sha, "files": package_hashes(stage)}
        (stage / STATE_NAME).write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
        if destination.exists():
            stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
            backup_root = (
                destination.parent.parent / "skill-backups" / destination.name
                if destination.parent.name == "skills"
                else destination.parent / f".{destination.name}-backups"
            )
            backup_root.mkdir(parents=True, exist_ok=True)
            backup = backup_root / f"{stamp}-{sha[:8]}"
            if backup.exists():
                raise ValueError("Backup path already exists")
            destination.rename(backup)
        try:
            stage.rename(destination)
        except Exception:
            if backup is not None:
                backup.rename(destination)
            raise
        return backup
    finally:
        if stage.exists():
            shutil.rmtree(stage)


def schedule_name(destination: Path) -> str:
    suffix = hashlib.sha256(str(destination).encode()).hexdigest()[:10]
    return f"lesson-motion-studio-update-{suffix}"


def enable_daily(destination: Path) -> str:
    script = destination / "scripts" / "auto_update.py"
    if not script.is_file():
        raise ValueError("Install the skill before enabling daily updates")
    name = schedule_name(destination)
    command = [sys.executable, str(script), "update", "--install-dir", str(destination)]
    if sys.platform == "darwin":
        label = f"com.shariefabdelmonem.{name}"
        agent_dir = Path.home() / "Library" / "LaunchAgents"
        agent_dir.mkdir(parents=True, exist_ok=True)
        log_dir = Path.home() / "Library" / "Logs"
        log_dir.mkdir(parents=True, exist_ok=True)
        plist = agent_dir / f"{label}.plist"
        payload = {
            "Label": label,
            "ProgramArguments": command,
            "StartCalendarInterval": {"Hour": 9, "Minute": 0},
            "StandardOutPath": str(log_dir / f"{name}.log"),
            "StandardErrorPath": str(log_dir / f"{name}.log"),
        }
        if plist.exists():
            subprocess.run(["launchctl", "bootout", f"gui/{os.getuid()}", str(plist)], check=False, capture_output=True)
        plist.write_bytes(plistlib.dumps(payload))
        subprocess.run(["launchctl", "bootstrap", f"gui/{os.getuid()}", str(plist)], check=True)
        return str(plist)
    if os.name == "nt":
        task = name
        action = subprocess.list2cmdline(command)
        subprocess.run(
            ["schtasks", "/Create", "/F", "/SC", "DAILY", "/ST", "09:00", "/TN", task, "/TR", action],
            check=True,
        )
        return task
    if shutil.which("crontab") is None:
        raise ValueError("crontab is unavailable; schedule this updater with your system scheduler")
    current = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
    if current.returncode != 0 and not (current.returncode == 1 and "no crontab" in current.stderr.lower()):
        raise ValueError(current.stderr.strip() or "Could not read crontab")
    marker = f"# {name}"
    lines = [line for line in current.stdout.splitlines() if marker not in line]
    log = Path.home() / f".{name}.log"
    lines.append(f"0 9 * * * {' '.join(shlex.quote(part) for part in command)} >> {shlex.quote(str(log))} 2>&1 {marker}")
    subprocess.run(["crontab", "-"], input="\n".join(lines) + "\n", text=True, check=True)
    return marker


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("check", "update", "install", "enable-daily"))
    parser.add_argument("--install-dir", type=Path, default=Path.home() / ".codex" / "skills" / "lesson-motion-studio")
    parser.add_argument("--replace", action="store_true", help="Back up and replace an existing copy during install")
    parser.add_argument("--no-daily", action="store_true", help="Install without registering a daily job")
    args = parser.parse_args()
    destination = args.install_dir.expanduser().absolute()
    try:
        if args.action == "enable-daily":
            print(json.dumps({"status": "scheduled", "schedule": enable_daily(destination)}))
            return 0
        sha = latest_commit()
        if args.action == "install":
            backup = install_snapshot(destination, sha, args.replace)
            result = {"status": "installed", "sha": sha, "path": str(destination), "backup": str(backup) if backup else None}
            if not args.no_daily:
                result["schedule"] = enable_daily(destination)
            print(json.dumps(result))
            return 0
        state = read_state(destination)
        if args.action == "check":
            print(json.dumps({"status": "current" if state["sha"] == sha else "update_available", "installed": state["sha"], "latest": sha}))
            return 0
        require_unmodified(destination, state)
        if state["sha"] == sha:
            print(json.dumps({"status": "current", "sha": sha}))
            return 0
        backup = install_snapshot(destination, sha, True)
        print(json.dumps({"status": "updated", "sha": sha, "backup": str(backup)}))
        return 0
    except (OSError, ValueError, KeyError, json.JSONDecodeError, zipfile.BadZipFile, urllib.error.URLError, subprocess.CalledProcessError) as exc:
        print(json.dumps({"status": "error", "message": str(exc)}), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
