"""
Analysis fixture — mirrors SastFixture.cs
Contains planted security flaws for SAST / Semgrep / Bandit detection.

Techniques unlocked:
  - SAST / Secure Coding Validation
  - Input Validation Testing       (OS command injection)
  - Data Flow Security Analysis     (hardcoded secret → usage)
  - All Definition Coverage         (HARDCODED_API_KEY, HARDCODED_PASSWORD defined)
  - All Uses Coverage               (C-Use: compute_weak_hash uses payload)
"""
import hashlib
import os
import sqlite3
import subprocess

# Planted SAST flaw: hardcoded credentials (Bandit B105, Semgrep)
HARDCODED_API_KEY: str = "AKIAIOSFODNN7EXAMPLE"
HARDCODED_PASSWORD: str = "SuperSecretPassword123!"


def execute_command(user_input: str) -> None:
    """Planted SAST flaw: OS command injection (Bandit B602, Semgrep)."""
    subprocess.run("cmd /c " + user_input, shell=True)  # noqa: S602, S607


def compute_weak_hash(payload: str) -> str:
    """Planted SAST flaw: weak MD5 hashing algorithm (Bandit B324, Semgrep)."""
    return hashlib.md5(payload.encode()).hexdigest()  # noqa: S324


def query_database(user_input: str, db_path: str) -> list:
    """Planted SAST flaw: SQL injection via string concatenation (Bandit B608)."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    # noqa: S608
    query = "SELECT * FROM users WHERE username = '" + user_input + "'"
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results
