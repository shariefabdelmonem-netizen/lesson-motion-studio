import importlib.util
import io
import plistlib
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch
from types import SimpleNamespace


SCRIPT = Path(__file__).resolve().parents[1] / "skills/lesson-motion-studio/scripts/auto_update.py"
spec = importlib.util.spec_from_file_location("lesson_motion_updater", SCRIPT)
updater = importlib.util.module_from_spec(spec)
spec.loader.exec_module(updater)


def archive(files):
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as output:
        for name, data in files.items():
            output.writestr("lesson-motion-studio-test/skills/lesson-motion-studio/" + name, data)
    return buffer.getvalue()


def package(text="version one"):
    return archive({
        "SKILL.md": "---\nname: lesson-motion-studio\n---\n\n" + text + "\n",
        "scripts/auto_update.py": "# updater\n",
    })


class AutoUpdateTests(unittest.TestCase):
    def test_install_replaces_with_backup_and_tracks_files(self):
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "lesson-motion-studio"
            (target / "notes.txt").parent.mkdir()
            (target / "notes.txt").write_text("local work")
            with patch.object(updater, "request_bytes", return_value=package()):
                backup = updater.install_snapshot(target, "a" * 40, replace=True)
            self.assertEqual((backup / "notes.txt").read_text(), "local work")
            state = updater.read_state(target)
            self.assertEqual(state["sha"], "a" * 40)
            updater.require_unmodified(target, state)
            self.assertIn("version one", (target / "SKILL.md").read_text())

    def test_local_change_blocks_automatic_replacement(self):
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "lesson-motion-studio"
            with patch.object(updater, "request_bytes", return_value=package()):
                updater.install_snapshot(target, "a" * 40, replace=False)
            (target / "SKILL.md").write_text("a local edit")
            with self.assertRaisesRegex(ValueError, "Local skill files changed"):
                updater.require_unmodified(target, updater.read_state(target))

    def test_rejects_archive_path_traversal(self):
        malicious = archive({
            "SKILL.md": "---\nname: lesson-motion-studio\n---\n",
            "scripts/auto_update.py": "# updater\n",
            "../outside.txt": "bad",
        })
        with tempfile.TemporaryDirectory() as temporary:
            with self.assertRaisesRegex(ValueError, "unsafe path"):
                updater.unpack_skill(malicious, Path(temporary) / "stage")
            self.assertFalse((Path(temporary) / "outside.txt").exists())

    def test_macos_schedule_runs_daily_at_nine(self):
        with tempfile.TemporaryDirectory() as temporary:
            home = Path(temporary)
            target = home / ".codex/skills/lesson-motion-studio"
            (target / "scripts").mkdir(parents=True)
            (target / "scripts/auto_update.py").write_text("# updater\n")
            with patch.object(updater.sys, "platform", "darwin"), patch.object(updater.Path, "home", return_value=home), patch.object(updater.subprocess, "run") as run:
                schedule = Path(updater.enable_daily(target))
            payload = plistlib.loads(schedule.read_bytes())
            self.assertEqual(payload["StartCalendarInterval"], {"Hour": 9, "Minute": 0})
            self.assertEqual(payload["ProgramArguments"][-3:], ["update", "--install-dir", str(target)])
            self.assertEqual(run.call_args.args[0][:2], ["launchctl", "bootstrap"])

    def test_cron_read_error_does_not_replace_schedule(self):
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "lesson-motion-studio"
            (target / "scripts").mkdir(parents=True)
            (target / "scripts/auto_update.py").write_text("# updater\n")
            with patch.object(updater.sys, "platform", "linux"), patch.object(updater.shutil, "which", return_value="/usr/bin/crontab"), patch.object(updater.subprocess, "run", return_value=SimpleNamespace(returncode=1, stderr="permission denied", stdout="")) as run:
                with self.assertRaisesRegex(ValueError, "permission denied"):
                    updater.enable_daily(target)
            self.assertEqual(run.call_count, 1)


if __name__ == "__main__":
    unittest.main()
