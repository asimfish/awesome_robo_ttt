#!/bin/bash
set -u
export PATH=/usr/bin:/bin:/usr/sbin:/sbin:/opt/homebrew/bin:/usr/local/bin
REPO="$(cd "$(dirname "$0")/.." && pwd)"
ST="$HOME/Code/super_translate"
export PAPER_CHINA_DEEPSEEK_API_KEY="$(grep -o 'PAPER_CHINA_DEEPSEEK_API_KEY=.*' "$HOME/Desktop/research/paper_china/.env" | cut -d= -f2)"
QUEUE="VANE_2608.09448 TTTVLA-LPO_2606.03127 RoVer_2510.10975 E-TTS_2606.27268 ELASTIC_2606.31132 SAIL_2603.08269 VLA-ATTC_2605.01194"
cd "$ST"
for name in $QUEUE; do
  src="$REPO/papers/pdf/${name}.pdf"; dst="$REPO/papers/zh/${name}_zh.pdf"
  [ -f "$dst" ] && { echo "[skip] $name"; continue; }
  echo "=== [$(date +%H:%M:%S)] W3 translating $name ==="
  uv run python -m pdf_zh_translator translate "$src" "$dst" \
    --api-mode deepseek --api-key-env PAPER_CHINA_DEEPSEEK_API_KEY \
    --preserve-graphics-text \
    --cache-file "$REPO/papers/cache/${name}.translation-cache.jsonl" || echo "[FAIL] $name"
done
echo "WORKER_3_DONE"
