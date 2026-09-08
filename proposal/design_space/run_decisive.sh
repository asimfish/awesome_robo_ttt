#!/bin/bash
# Decisive runs for the three-quantity decomposition (review round 1):
#   R0 = C1 prior (lambda 0, s 1, NO obs; retrained on our pipeline) fine-tuned at sigma .10  -> retraining control for A
#   R1 = C2 prior (lambda 0, s 1, obs c_{t-1})                        fine-tuned at sigma .10  -> conditioning alone, same sigma_chunk as A (0.20)
#   R2 = stock raw prior                                              fine-tuned at sigma .13  -> sigma_chunk 0.26 (matched to E4)
#   R3 = stock prior + low-pass (0.8, 0.2), state unobserved          fine-tuned at sigma .17  -> sigma_chunk 0.20 (matched to A), unobservable curve top
# Usage: POINT=R1 GPU=6 bash run_decisive.sh   (R0/R1 wait for the corner-point pretrain to finish)
set -o pipefail
source /home/dataset-local/liyufeng/cadi/env.sh
cd /home/dataset-local/liyufeng/cadi/dppo
POINT=${POINT:?}; GPU=${GPU:-0}; export CUDA_VISIBLE_DEVICES=$GPU
LOG=/home/dataset-local/liyufeng/cadi/design_space/log_${POINT}.log
CFG=cfg/robomimic/finetune/square
case $POINT in
  R0) SIG=0.10; FT=ft_ppo_diffusion_mlp_ds_C1; PRENAME=square_pre_diffusion_mlp_derivcl_s100_leak00_ta4_td20; WAIT=C1 ;;
  R1) SIG=0.10; FT=ft_ppo_diffusion_mlp_ds_C2; PRENAME=square_pre_diffusion_mlp_derivcl_s100_leak00_obscmd_ta4_td20; WAIT=C2 ;;
  R2) SIG=0.13; FT=ft_ppo_diffusion_mlp_ds_R2; PRENAME=""; WAIT="" ;;
  R3) SIG=0.17; FT=ft_ppo_diffusion_mlp_ds_R3; PRENAME=""; WAIT="" ;;
  *) echo bad POINT; exit 1 ;;
esac
if [ -n "$WAIT" ]; then
  while ! grep -q ${WAIT}_CHAIN_DONE /home/dataset-local/liyufeng/cadi/design_space/log_${WAIT}.log 2>/dev/null; do sleep 300; done
fi
EXTRA=""
if [ -n "$PRENAME" ]; then
  CK=$(ls -t $DPPO_LOG_DIR/robomimic-pretrain/$PRENAME/*/checkpoint/state_3000.pt | head -1)
  EXTRA="base_policy_path=$CK"
fi
# give the fine-tune its own run name so eval_point.sh can locate it by POINT
NAMEOVR='name=${env_name}_ft_diffusion_mlp_ds_'$POINT'_ta${horizon_steps}_td${denoising_steps}_tdf${ft_denoising_steps}'
echo "=== [$(date)] [$POINT] finetune sigma=$SIG cfg=$FT $EXTRA ===" | tee -a $LOG
python script/run.py --config-name=$FT --config-dir=$CFG wandb=null seed=42 "$NAMEOVR" $EXTRA \
  model.min_sampling_denoising_std=$SIG model.min_logprob_denoising_std=$SIG 2>&1 | tee -a $LOG
echo ${POINT}_CHAIN_DONE | tee -a $LOG
