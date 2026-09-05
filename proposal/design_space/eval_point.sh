#!/bin/bash
# Five-axis deployment evaluation of one design-space point (frozen state_200.pt, 3 eval seeds x 100 ep).
# Usage: POINT=F1 DEV=cuda:5 bash eval_point.sh      (POINT in F1 F2 F3 F4, or any name with RUN_DIR set)
# Produces ../p0/out/ds_${POINT}_*.npz :
#   axis 3/4  frozen: nodrift, gain0.7, obsn0.05, delay2
#   axis 5    calib (K), triggered downstream compensation on gain0.7 / delay2 / nodrift, adaptation noise sigma 0.5 up/down
source /home/dataset-local/liyufeng/cadi/env.sh
cd /home/dataset-local/liyufeng/cadi/dppo
POINT=${POINT:?}; DEV=${DEV:-cuda:0}
L=/home/dataset-local/liyufeng/cadi/log/robomimic-finetune
if [ -z "${RUN_DIR:-}" ]; then
  RUN_DIR=$(ls -dt $L/square_ft_diffusion_mlp_ds_${POINT}_ta4_td20_tdf10/*/ 2>/dev/null | head -1)
fi
[ -f "$RUN_DIR/checkpoint/state_200.pt" ] || { echo "[$POINT] no state_200.pt under $RUN_DIR"; exit 1; }
echo "[$POINT] RUN_DIR=$RUN_DIR"
OUT=../p0/out
run() { out=$OUT/$1.npz; shift; [ -f "$out" ] && { echo "[skip] $out"; return; }; echo "=== [$(date +%H:%M:%S)] $out ==="
  python ../p0/rollout_record.py --run-dir "$RUN_DIR" --n-episodes 100 --n-envs 25 --device $DEV "$@" --out "$out" 2>&1 | grep "DONE\|Traceback\|Error" | tail -3; }

# axis 5 prerequisite: per-policy nominal map K
run ds_${POINT}_calib --seed 1000 --calib 1
K=$(python ../p0/calib_K.py $OUT/ds_${POINT}_calib.npz | tail -1); echo "[$POINT] K=$K"

for seed in 1000 2000 3000; do
  # axes 3-4: frozen deployment
  run ds_${POINT}_frozen_nodrift_s$seed  --seed $seed
  run ds_${POINT}_frozen_gain0.7_s$seed  --seed $seed --exec-gain 0.7
  run ds_${POINT}_frozen_obsn0.05_s$seed --seed $seed --obs-noise 0.05
  run ds_${POINT}_frozen_delay2_s$seed   --seed $seed --exec-delay 2
  # axis 5: triggered downstream compensation (recovery, misadaptation cost, estimator fooled)
  run ds_${POINT}_trig_nodrift_s$seed --seed $seed --adapt 2 --K $K --adapt-window 120
  run ds_${POINT}_trig_gain0.7_s$seed --seed $seed --adapt 2 --K $K --adapt-window 120 --exec-gain 0.7
  run ds_${POINT}_trig_delay2_s$seed  --seed $seed --adapt 2 --K $K --adapt-window 120 --exec-delay 2
  # axis 5: controlled adaptation noise, upstream vs downstream of the filter
  run ds_${POINT}_cnup_sig0.5_s$seed   --seed $seed --comp-noise 0.5 --comp-where up
  run ds_${POINT}_cndown_sig0.5_s$seed --seed $seed --comp-noise 0.5 --comp-where down
done
echo ${POINT}_EVAL_DONE
