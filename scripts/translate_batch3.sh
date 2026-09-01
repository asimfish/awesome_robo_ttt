#!/bin/bash
# 第三批扩展论文翻译（27 篇）。用法: translate_batch3.sh <worker_id> <n_workers>
set -u
export PATH=/usr/bin:/bin:/usr/sbin:/sbin:/opt/homebrew/bin:/usr/local/bin
REPO="$(cd "$(dirname "$0")/.." && pwd)"
ST="$HOME/Code/super_translate"
WORKER="${1:-0}"; NWORKERS="${2:-1}"
export PAPER_CHINA_DEEPSEEK_API_KEY="$(grep -o 'PAPER_CHINA_DEEPSEEK_API_KEY=.*' "$HOME/Desktop/research/paper_china/.env" | cut -d= -f2)"
QUEUE="Sentinel_2410.04640 FAILDetect_2503.08558 SAFE_2506.09937 TTTParkour_2602.02331 Titans_2501.00663 LaCT_2505.23884 ATLAS_2505.23735 TNT_2511.07343 GPC_2510.01068 PriGo_2607.07076 DCDP_2603.01953 ORPA_2608.17323 LocoFormer_2509.23745 AnyCar_2409.15783 ROAM_2311.01059 DayDreamer_2206.14176 GrBAL_1803.11347 MAML_1703.03400 DPPO_2409.00588 QChunking_2507.07969 RLPD_2302.02948 CalQL_2303.05479 WSRL_2412.07762 HILSERL_2410.21845 ConRFT_2502.05450 gSDE_2005.05719 PinkNoise_ICLR2023"
i=0; cd "$ST"
for name in $QUEUE; do
  idx=$((i % NWORKERS)); i=$((i+1)); [ "$idx" != "$WORKER" ] && continue
  src="$REPO/papers/pdf/${name}.pdf"; dst="$REPO/papers/zh/${name}_zh.pdf"
  [ -f "$dst" ] && { echo "[skip] $name"; continue; }
  echo "=== [$(date +%H:%M:%S)] B3W$WORKER translating $name ==="
  uv run python -m pdf_zh_translator translate "$src" "$dst" \
    --api-mode deepseek --api-key-env PAPER_CHINA_DEEPSEEK_API_KEY \
    --preserve-graphics-text \
    --cache-file "$REPO/papers/cache/${name}.translation-cache.jsonl" || echo "[FAIL] $name"
done
echo "B3_WORKER_${WORKER}_DONE"
