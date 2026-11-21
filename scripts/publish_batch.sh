#!/usr/bin/env bash
# Merge an explanation batch, commit, push to main, and wait for the Vercel deploy.
# Usage: scripts/publish_batch.sh scripts/explanations/<batch>.json "commit subject" "commit body"
set -euo pipefail
batch="$1"; subject="$2"; body="${3:-}"
python -I scripts/merge_explanations.py "$batch"
rm -rf scripts/__pycache__
git add "$batch" scripts/*.py scripts/*.sh src/data/questions.json src/data/explanations_map.json
git commit -q -m "$subject" -m "$body" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
git log --oneline -1
git push -q origin main
sleep 20
for i in $(seq 1 30); do
  s=$(vercel ls doctor-exam-platform 2>&1 | grep -m1 -E 'Building|Ready|Error|Queued|Canceled|Initializing' || true)
  case "$s" in *Ready*|*Error*|*Canceled*) echo "$s" | sed -E 's/ +/ /g'; break;; esac
  sleep 10
done
