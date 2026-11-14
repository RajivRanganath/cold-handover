# Round 2 protocol lock (T4), locked 2026-11-15 IST before any measured attempt

- Task: tasks/T4/prompt.md (vague bug report; a real false-closure bug found in the original snapshot).
- Attempts: 5 measured (M-T4-01..05), original documentation only (condition A), claude-haiku-5-5, same sandbox and snapshot as round 1.
- Pass rule: all of protected_files_unchanged, regression_67, benchmark_unchanged, hidden_shortfall_tests, notes_present.
- Reported but never scored: depth_combined_case_handled (fee overcharge plus unexplained shortfall), overpay observation.
- Excluded from counts: pilot-T4-A-001 (never started: harness pointed at an uninstalled Claude Code version) and pilot-T4-A-002 (passed).
- Differences from round 1: Claude Code 2.1.325 instead of 2.1.316 (2.1.316 no longer installed), which loads its built-in plugins; harness copy run_attempt_r2.sh differs from run_attempt.sh only in that version and the evaluator path.
- Pre-lock change: the combined case was moved from pass/fail to a depth measure before the pilot ran, because the bug report does not mention it.
