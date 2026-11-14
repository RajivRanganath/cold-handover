#!/usr/bin/env bash
# Runs the frozen schedule: 3 concurrent workers, original documentation only (condition A).
W=/path/to/tms-work
xargs -P 3 -L 1 bash -c '"$0"/harness/run_attempt.sh "$1" A "$2" 1800 > "$0"/runs/"$2".harness.log 2>&1; echo "$(date -u +%FT%TZ) done $2 exit $?"' "$W" < "$W/protocol/schedule.txt"
