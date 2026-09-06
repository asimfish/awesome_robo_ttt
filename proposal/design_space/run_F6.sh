#!/bin/bash
# F6 = F1 (lam .9, s .3, obs_cmd) fine-tuned at sigma=0.07 (sigma_exec ~ 0.048): candidate recommended configuration.
source /home/dataset-local/liyufeng/cadi/env.sh
cd /home/dataset-local/liyufeng/cadi/dppo
export CUDA_VISIBLE_DEVICES=${GPU:-5}
LOG=../design_space/log_F6.log
CK=$(ls -t $DPPO_LOG_DIR/robomimic-pretrain/square_pre_diffusion_mlp_derivcl_s030_leak09_obscmd_ta4_td20/*/checkpoint/state_3000.pt | head -1)
echo "=== [$(date)] F6 finetune sigma=0.07 from $CK ===" | tee -a $LOG
echo "BC_SR=0.5850 (shared prior with F1)" | tee -a $LOG
python script/run.py --config-name=ft_ppo_diffusion_mlp_ds_F6 --config-dir=cfg/robomimic/finetune/square wandb=null seed=42 \
  base_policy_path=$CK model.min_sampling_denoising_std=0.07 model.min_logprob_denoising_std=0.07 2>&1 | tee -a $LOG
echo F6_CHAIN_DONE | tee -a $LOG
