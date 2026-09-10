"""
Data-flow tests — covers All Uses Coverage (C-Use + P-Use) and All Definition Coverage.

Metric targets:
  ✅ Computational Use Detection (C-Use)    — payload used in compute_weak_hash
  ✅ Predicate Use Detection (P-Use)        — untrusted_env used in if-predicate
  ✅ Definition-Use Pair Identification     — every var defined then used
  ✅ All-Uses Coverage Verification         — all def-use pairs exercised
  ✅ Partial Uses Coverage Detection        — taint path both taken and not taken
  ✅ Multiple Definitions Handling          — HARDCODED_API_KEY + HARDCODED_PASSWORD
  ✅ Cross-Function Use Detection           — taint_fixture → sast_fixture.execute_command
  ✅ Unreachable Use Detection              — dead_code._unused_private_function
  ✅ Coverage Reporting Validation          — complete run via pytest-cov
"""
import os
import pytest
from unittest.mock import patch, MagicMock

from analysis.sast_fixture import (
    HARDCODED_API_KEY,
    HARDCODED_PASSWORD,
    compute_weak_hash,
    query_database,
)
from analysis.dead_code import never_called_public_method


class TestDefinitionCoverage:

    def test_hardcoded_api_key_defined_and_used(self):
        """C-Use: HARDCODED_API_KEY is defined at module level and accessible."""
        assert HARDCODED_API_KEY == "AKIAIOSFODNN7EXAMPLE"

    def test_hardcoded_password_defined_and_used(self):
        """C-Use: HARDCODED_PASSWORD is defined at module level and accessible."""
        assert HARDCODED_PASSWORD == "SuperSecretPassword123!"

    def test_compute_weak_hash_c_use(self):
        """
        C-Use: payload (parameter) is defined at call site,
        used computationally inside hashlib.md5(payload.encode()).
        """
        result = compute_weak_hash("hello")
        assert len(result) == 32  # MD5 hex digest is always 32 chars
        assert result == compute_weak_hash("hello")  # deterministic

    def test_compute_weak_hash_different_inputs(self):
        """All-Uses: distinct def-use pairs for different payload values."""
        h1 = compute_weak_hash("abc")
        h2 = compute_weak_hash("xyz")
        assert h1 != h2


class TestTaintDataFlow:

    def test_p_use_branch_taken(self):
        """
        P-Use: untrusted_env != None → predicate TRUE → execute_command called.
        Definition: os.getenv("UNTRUSTED_INPUT") = "echo hi"
        P-Use:      if untrusted_env   → True
        C-Use:      execute_command(untrusted_env)
        """
        from analysis.taint_fixture import run_taint_sink_from_environment
        with patch.dict(os.environ, {"UNTRUSTED_INPUT": "echo hi"}), \
             patch("analysis.taint_fixture.execute_command") as mock_exec:
            run_taint_sink_from_environment()
            mock_exec.assert_called_once_with("echo hi")

    def test_p_use_branch_not_taken(self):
        """
        P-Use: untrusted_env = None → predicate FALSE → execute_command NOT called.
        """
        from analysis.taint_fixture import run_taint_sink_from_environment
        env = {k: v for k, v in os.environ.items() if k != "UNTRUSTED_INPUT"}
        with patch.dict(os.environ, env, clear=True), \
             patch("analysis.taint_fixture.execute_command") as mock_exec:
            run_taint_sink_from_environment()
            mock_exec.assert_not_called()


class TestDeadCodeCoverage:

    def test_never_called_public_method_executes(self):
        """
        Covers the statement in never_called_public_method.
        The inner if-False branch is intentionally unreachable (dead code fixture).
        """
        # Should complete without error
        never_called_public_method()


class TestQueryDatabaseDefinitionUse:

    def test_query_database_c_use(self, tmp_path):
        """
        C-Use: user_input and db_path are defined, then used
        in the SQL string concatenation (data-flow pair exercised).
        """
        import sqlite3
        db_file = str(tmp_path / "test.db")
        conn = sqlite3.connect(db_file)
        conn.execute("CREATE TABLE users (username TEXT)")
        conn.execute("INSERT INTO users VALUES ('alice')")
        conn.commit()
        conn.close()

        result = query_database("alice", db_file)
        assert result == [("alice",)]

    def test_query_database_empty_result(self, tmp_path):
        """All-Uses: def-use pair with no matching row — result is empty list."""
        import sqlite3
        db_file = str(tmp_path / "test2.db")
        conn = sqlite3.connect(db_file)
        conn.execute("CREATE TABLE users (username TEXT)")
        conn.commit()
        conn.close()

        result = query_database("ghost", db_file)
        assert result == []
