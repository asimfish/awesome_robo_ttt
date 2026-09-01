#!/bin/bash
# Translate papers/pdf -> papers/zh with SuperTranslate (DeepSeek native mode).
# Usage: translate_queue.sh <worker_id> <n_workers>
set -u
export PATH=/usr/bin:/bin:/usr/sbin:/sbin:/opt/homebrew/bin:/usr/local/bin
REPO="$(cd "$(dirname "$0")/.." && pwd)"
ST="$HOME/Code/super_translate"
WORKER="${1:-0}"
NWORKERS="${2:-1}"

# Load API key from paper_china .env if not already set
if [ -z "${PAPER_CHINA_DEEPSEEK_API_KEY:-}" ]; then
  export PAPER_CHINA_DEEPSEEK_API_KEY="$(grep -o 'PAPER_CHINA_DEEPSEEK_API_KEY=.*' "$HOME/Desktop/research/paper_china/.env" | cut -d= -f2)"
fi
[ -z "$PAPER_CHINA_DEEPSEEK_API_KEY" ] && { echo "no key"; exit 1; }

# Priority order: category 4 (robot/driving TTT) > 5 (steering) > 3 (new wave) > 2 (policy adaptation) > 1 (foundations)
QUEUE=$(tail -n +2 "$REPO/scripts/papers.tsv" | awk -F'\t' '{
  pri = 9;
  if ($3 ~ /^4/) pri = 1; else if ($3 ~ /^5/) pri = 2; else if ($3 ~ /^3/) pri = 3; else if ($3 ~ /^2/) pri = 4; else pri = 5;
  printf "%d\t%s_%s\n", pri, $1, $2
}' | sort -n | cut -f2)

i=0
cd "$ST"
for name in $QUEUE; do
  idx=$((i % NWORKERS)); i=$((i+1))
  [ "$idx" != "$WORKER" ] && continue
  src="$REPO/papers/pdf/${name}.pdf"
  dst="$REPO/papers/zh/${name}_zh.pdf"
  [ -f "$dst" ] && { echo "[skip] $name"; continue; }
  [ -f "$src" ] || { echo "[miss] $name"; continue; }
  echo "=== [$(date +%H:%M:%S)] W$WORKER translating $name ==="
  uv run python -m pdf_zh_translator translate "$src" "$dst" \
    --api-mode deepseek --api-key-env PAPER_CHINA_DEEPSEEK_API_KEY \
    --preserve-graphics-text \
    --cache-file "$REPO/papers/cache/${name}.translation-cache.jsonl" \
    || echo "[FAIL] $name"
done
echo "WORKER_${WORKER}_DONE"
