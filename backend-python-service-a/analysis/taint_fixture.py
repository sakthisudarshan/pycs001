"""
Analysis fixture — mirrors TaintFixture.cs
Demonstrates taint flow: external env var → dangerous sink.

Techniques unlocked:
  - All Uses Coverage — P-Use  (untrusted_env used in if-predicate)
  - All Uses Coverage — C-Use  (untrusted_env passed to execute_command)
  - Data Flow Security Analysis
  - Cross-Function Use Detection
"""
import os
from .sast_fixture import execute_command


def run_taint_sink_from_environment() -> None:
    """
    Read an untrusted value from the environment and pass it to a dangerous sink.
    Mirrors TaintFixture.RunTaintSinkFromEnvironment in C#.

    Data-flow path:
      Definition: untrusted_env = os.getenv(...)   [Definition point]
      P-Use:      if untrusted_env                 [Predicate use]
      C-Use:      execute_command(untrusted_env)   [Computational use]
    """
    untrusted_env: str | None = os.getenv("UNTRUSTED_INPUT")  # definition
    if untrusted_env:                                           # P-Use
        execute_command(untrusted_env)                          # C-Use
