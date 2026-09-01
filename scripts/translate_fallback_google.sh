#!/bin/bash
# 用 super_translate 内置的 pdf2zh(Google 引擎, 免 key) 为余额耗尽的 5 篇出备胎版中译。
# 充值 DeepSeek 后请运行 translate_missing.sh 重出高质量版覆盖。
set -u
export PATH=/usr/bin:/bin:/usr/sbin:/sbin:/opt/homebrew/bin:/usr/local/bin
REPO="$(cd "$(dirname "$0")/.." && pwd)"
P2Z="$HOME/Code/super_translate/.venv/bin/pdf2zh"
TMP="$REPO/papers/cache/p2z_out"
mkdir -p "$TMP"
QUEUE="RMA_2107.04034 MOLe_1812.07671 ContinualMAML_2409.14950 RoVer_2510.10975 TTTVLA-LPO_2606.03127"
for name in $QUEUE; do
  src="$REPO/papers/pdf/${name}.pdf"; dst="$REPO/papers/zh/${name}_zh.pdf"
  [ -f "$dst" ] && { echo "[skip] $name"; continue; }
  echo "=== [$(date +%H:%M:%S)] pdf2zh-google $name ==="
  "$P2Z" "$src" --service google --lang-out zh --output "$TMP" --thread 4 \
    && cp "$TMP/${name}-mono.pdf" "$dst" && echo "[ok] $name" || echo "[FAIL] $name"
done
echo GOOGLE_FALLBACK_DONE
