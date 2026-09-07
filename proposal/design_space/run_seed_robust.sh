#!/bin/bash
# Training-seed variance of deployment robustness: frozen E4/E5 checkpoints from seeds 43,44 (and 45,46 when done)
# under no drift and gain x0.7, 3 eval seeds x 100 ep. Output ../p0/out/sr_{arm}_s{train}_{cond}_s{eval}.npz
source /home/dataset-local/liyufeng/cadi/env.sh
cd /home/dataset-local/liyufeng/cadi/dppo
L=/home/dataset-local/liyufeng/cadi/log/robomimic-finetune
DEV=${DEV:-cuda:2}
run() { out=../p0/out/$1.npz; shift; [ -f "$out" ] && { echo "[skip] $out"; return; }; echo "=== [$(date +%H:%M:%S)] $out ==="
  python ../p0/rollout_record.py --n-episodes 100 --n-envs 25 --device $DEV "$@" --out "$out" 2>&1 | grep "DONE\|Traceback\|Error" | tail -3; }
for ts in ${SEEDS:-43 44}; do
  RE4=$(ls -d $L/square_ft_diffusion_mlp_armC_leak09_ta4_td20_tdf10/*_$ts 2>/dev/null | tail -1)
  RE5=$(ls -d $L/square_ft_diffusion_mlp_ta4_td20_tdf10/*_$ts 2>/dev/null | tail -1)
  for es in 1000 2000 3000; do
    [ -f "$RE4/checkpoint/state_200.pt" ] && { run sr_E4_s${ts}_nodrift_s$es --run-dir $RE4 --seed $es; run sr_E4_s${ts}_gain0.7_s$es --run-dir $RE4 --seed $es --exec-gain 0.7; }
    [ -f "$RE5/checkpoint/state_200.pt" ] && { run sr_E5_s${ts}_nodrift_s$es --run-dir $RE5 --seed $es; run sr_E5_s${ts}_gain0.7_s$es --run-dir $RE5 --seed $es --exec-gain 0.7; }
  done
done
echo SEED_ROBUST_DONE
