#!/bin/bash
# 补译因 DeepSeek 余额耗尽（HTTP 402）未完成的 5 篇。充值后运行本脚本即可，
# 已译段落存于 papers/cache/ 会自动复用，速度很快。
set -u
export PATH=/usr/bin:/bin:/usr/sbin:/sbin:/opt/homebrew/bin:/usr/local/bin
REPO="$(cd "$(dirname "$0")/.." && pwd)"
ST="$HOME/Code/super_translate"
if [ -z "${PAPER_CHINA_DEEPSEEK_API_KEY:-}" ]; then
  export PAPER_CHINA_DEEPSEEK_API_KEY="$(grep -o 'PAPER_CHINA_DEEPSEEK_API_KEY=.*' "$HOME/Desktop/research/paper_china/.env" | cut -d= -f2)"
fi
QUEUE="RMA_2107.04034 MOLe_1812.07671 ContinualMAML_2409.14950 RoVer_2510.10975 TTTVLA-LPO_2606.03127"
cd "$ST"
for name in $QUEUE; do
  src="$REPO/papers/pdf/${name}.pdf"; dst="$REPO/papers/zh/${name}_zh.pdf"
  [ -f "$dst" ] && { echo "[skip] $name"; continue; }
  echo "=== translating $name ==="
  uv run python -m pdf_zh_translator translate "$src" "$dst" \
    --api-mode deepseek --api-key-env PAPER_CHINA_DEEPSEEK_API_KEY \
    --preserve-graphics-text \
    --cache-file "$REPO/papers/cache/${name}.translation-cache.jsonl" || echo "[FAIL] $name"
done
echo ALL_DONE
