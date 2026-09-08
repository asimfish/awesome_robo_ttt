#!/bin/bash
# Corner points at lambda=0 that close the prior-alignment factorization (ICLR review W3):
#   C1 = (0, 1.0) no obs   : retraining the stock position prior with our pipeline (control for "retraining at all")
#   C2 = (0, 1.0) + obs    : previous-command conditioning only
#   C3 = (0, 0.6) no obs   : target rescaling only (labels a_t/0.6, clip < 0.5%)
#   C4 = (0, 0.6) + obs    : conditioning + rescaling
# Dataset -> pretrain (3000 ep) -> BC gate (itr-0 eval). No RL. Usage: POINT=C2 GPU=5 bash run_corner.sh
set -o pipefail
source /home/dataset-local/liyufeng/cadi/env.sh
cd /home/dataset-local/liyufeng/cadi/dppo
POINT=${POINT:?C1|C2|C3|C4}; GPU=${GPU:-0}; export CUDA_VISIBLE_DEVICES=$GPU
SRC=$DPPO_DATA_DIR/robomimic/square/train.npz
LOG=/home/dataset-local/liyufeng/cadi/design_space/log_${POINT}.log
case $POINT in
  C1) SCL=1.0; OBS=0 ;;
  C2) SCL=1.0; OBS=1 ;;
  C3) SCL=0.6; OBS=0 ;;
  C4) SCL=0.6; OBS=1 ;;
  *) echo bad POINT; exit 1 ;;
esac
TAG=s$(printf "%03d" $(python -c "print(int(round($SCL*100)))"))_leak00$([ $OBS = 1 ] && echo _obscmd)
DS=square_derivcl_$TAG; DST=$DPPO_DATA_DIR/robomimic/$DS
PRE=pre_diffusion_mlp_derivcl_$TAG; PRENAME=square_${PRE}_ta4_td20; FT=ft_ppo_diffusion_mlp_ds_$POINT
CFG=cfg/robomimic
# configs from templates (obs: leak09_obscmd/armC_leak09 ; no-obs: derivcl_s100/armC)
if [ $OBS = 1 ]; then
  sed -e "s/derivcl_s100_leak09_obscmd/derivcl_$TAG/g" $CFG/pretrain/square/pre_diffusion_mlp_derivcl_s100_leak09_obscmd.yaml > $CFG/pretrain/square/$PRE.yaml
  sed -e "s/_ft_diffusion_mlp_armC_leak09_/_ft_diffusion_mlp_ds_${POINT}_/" -e "s/^      leak: 0.9$/      leak: 0.0/" -e "s/^      scale: 1.0$/      scale: $SCL/" $CFG/finetune/square/ft_ppo_diffusion_mlp_armC_leak09.yaml > $CFG/finetune/square/$FT.yaml
else
  sed -e "s/derivcl_s100/derivcl_$TAG/g" $CFG/pretrain/square/pre_diffusion_mlp_derivcl_s100.yaml > $CFG/pretrain/square/$PRE.yaml
  sed -e "s/_ft_diffusion_mlp_armC_/_ft_diffusion_mlp_ds_${POINT}_/" -e "s/^      scale: 1.0$/      scale: $SCL/" $CFG/finetune/square/ft_ppo_diffusion_mlp_armC.yaml > $CFG/finetune/square/$FT.yaml
  grep -q "leak:" $CFG/finetune/square/$FT.yaml && sed -i "s/^      leak: .*$/      leak: 0.0/" $CFG/finetune/square/$FT.yaml || sed -i "s/^      scale: $SCL$/      scale: $SCL\n      leak: 0.0/" $CFG/finetune/square/$FT.yaml
fi
echo "=== [$(date)] [$POINT] scale=$SCL obs=$OBS dataset=$DS ===" | tee -a $LOG
grep -E "leak:|scale:|obs_cmd|obs_dim:" $CFG/finetune/square/$FT.yaml | head -5 | tee -a $LOG
if [ ! -f "$DST/train.npz" ]; then
  python script/make_derivative_dataset.py --src "$SRC" --dst "$DST/train.npz" --scale $SCL --leak 0.0 $([ $OBS = 1 ] && echo --obs-cmd) 2>&1 | grep -E "clip_fraction_at_scale|suggested_scale|recon" | tee -a $LOG
  cp $DPPO_DATA_DIR/robomimic/square/normalization.npz $DST/ 2>/dev/null || true
fi
CK=$(ls -t $DPPO_LOG_DIR/robomimic-pretrain/$PRENAME/*/checkpoint/state_3000.pt 2>/dev/null | head -1)
if [ -z "$CK" ]; then
  echo "=== [$(date)] [$POINT] pretrain $PRE ===" | tee -a $LOG
  python script/run.py --config-name=$PRE --config-dir=$CFG/pretrain/square wandb=null seed=42 2>&1 | tee -a $LOG
  CK=$(ls -t $DPPO_LOG_DIR/robomimic-pretrain/$PRENAME/*/checkpoint/state_3000.pt 2>/dev/null | head -1)
fi
echo "CKPT=$CK" | tee -a $LOG
echo "=== [$(date)] [$POINT] BC gate ===" | tee -a $LOG
python script/run.py --config-name=$FT --config-dir=$CFG/finetune/square wandb=null seed=42 train.n_train_itr=1 \
  base_policy_path=$CK model.min_sampling_denoising_std=0.03 model.min_logprob_denoising_std=0.03 2>&1 | tee -a $LOG
echo "BC_SR=$(grep 'eval: success rate' $LOG | tail -1 | sed 's/.*success rate *//' | awk '{print $1}')" | tee -a $LOG
echo ${POINT}_CHAIN_DONE | tee -a $LOG
