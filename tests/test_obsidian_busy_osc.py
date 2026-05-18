import io
import os
import sys

from cli import HermesCLI


class _TtyStringIO(io.StringIO):
    def isatty(self):
        return True


def test_obsidian_busy_osc_is_gated_by_env(monkeypatch):
    cli = HermesCLI.__new__(HermesCLI)
    out = _TtyStringIO()
    monkeypatch.setattr(sys, "stdout", out)
    monkeypatch.delenv("OBSIDIAN_HERMES_CONSOLE", raising=False)

    cli._emit_obsidian_hermes_busy(True)

    assert out.getvalue() == ""


def test_obsidian_busy_osc_emits_busy_and_idle_when_embedded(monkeypatch):
    cli = HermesCLI.__new__(HermesCLI)
    out = _TtyStringIO()
    monkeypatch.setattr(sys, "stdout", out)
    monkeypatch.setenv("OBSIDIAN_HERMES_CONSOLE", "1")

    cli._emit_obsidian_hermes_busy(True)
    cli._emit_obsidian_hermes_busy(False)

    assert out.getvalue() == "\x1b]777;hermes:busy=1\x07\x1b]777;hermes:busy=0\x07"


def test_obsidian_busy_osc_does_not_emit_when_stdout_is_not_tty(monkeypatch):
    cli = HermesCLI.__new__(HermesCLI)
    out = io.StringIO()
    monkeypatch.setattr(sys, "stdout", out)
    monkeypatch.setenv("OBSIDIAN_HERMES_CONSOLE", "1")

    cli._emit_obsidian_hermes_busy(True)

    assert out.getvalue() == ""
