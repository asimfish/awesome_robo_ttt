#!/bin/bash
# F7 = F5 (lam .8, s .2, obs_cmd, retrained prior) fine-tuned at sigma=0.10 (sigma_exec ~ 0.033, = B): completes the 2x2 {prior} x {sigma} at (0.8, 0.2).
source /home/dataset-local/liyufeng/cadi/env.sh
cd /home/dataset-local/liyufeng/cadi/dppo
export CUDA_VISIBLE_DEVICES=${GPU:-6}
LOG=../design_space/log_F7.log
CK=$(ls -t $DPPO_LOG_DIR/robomimic-pretrain/square_pre_diffusion_mlp_derivcl_s020_leak08_obscmd_ta4_td20/*/checkpoint/state_3000.pt | head -1)
echo "=== [$(date)] F7 finetune sigma=0.10 from $CK ===" | tee -a $LOG
echo "BC_SR=0.5950 (shared prior with F5)" | tee -a $LOG
python script/run.py --config-name=ft_ppo_diffusion_mlp_ds_F7 --config-dir=cfg/robomimic/finetune/square wandb=null seed=42 \
  base_policy_path=$CK model.min_sampling_denoising_std=0.10 model.min_logprob_denoising_std=0.10 2>&1 | tee -a $LOG
echo F7_CHAIN_DONE | tee -a $LOG
