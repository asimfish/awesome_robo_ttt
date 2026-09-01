#!/bin/bash
# 第二批扩展论文翻译。用法: translate_batch2.sh <worker_id> <n_workers>
set -u
export PATH=/usr/bin:/bin:/usr/sbin:/sbin:/opt/homebrew/bin:/usr/local/bin
REPO="$(cd "$(dirname "$0")/.." && pwd)"
ST="$HOME/Code/super_translate"
WORKER="${1:-0}"; NWORKERS="${2:-1}"
export PAPER_CHINA_DEEPSEEK_API_KEY="$(grep -o 'PAPER_CHINA_DEEPSEEK_API_KEY=.*' "$HOME/Desktop/research/paper_china/.env" | cut -d= -f2)"
QUEUE="SHOT_2002.08546 MEMO_2110.09506 AR-TTA_2309.10109 GTRS_2506.06664 HydraNeXt_2503.12030 DriveCritic_2510.13108 DREAMChunk_2606.18589 ICRT_2408.15980 InstantPolicy_2411.12633 RICL_2508.02062"
i=0; cd "$ST"
for name in $QUEUE; do
  idx=$((i % NWORKERS)); i=$((i+1)); [ "$idx" != "$WORKER" ] && continue
  src="$REPO/papers/pdf/${name}.pdf"; dst="$REPO/papers/zh/${name}_zh.pdf"
  [ -f "$dst" ] && { echo "[skip] $name"; continue; }
  echo "=== [$(date +%H:%M:%S)] B2W$WORKER translating $name ==="
  uv run python -m pdf_zh_translator translate "$src" "$dst" \
    --api-mode deepseek --api-key-env PAPER_CHINA_DEEPSEEK_API_KEY \
    --preserve-graphics-text \
    --cache-file "$REPO/papers/cache/${name}.translation-cache.jsonl" || echo "[FAIL] $name"
done
echo "B2_WORKER_${WORKER}_DONE"
