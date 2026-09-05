#!/bin/bash
# Train one design-space point: dataset (integrate only) -> pretrain -> BC gate -> PPO finetune (sigma=0.03).
# Usage: POINT=F1 GPU=2 bash run_point_chain.sh
#   F1=(lam .9, s .3)  F2=(lam .7, s 1.0)  F3=(lam .95, s .5)  F4=lowpass B refit with sigma=.03 (stock prior, no pretrain)
set -o pipefail
source /home/dataset-local/liyufeng/cadi/env.sh
cd /home/dataset-local/liyufeng/cadi/dppo
POINT=${POINT:?set POINT=F1|F2|F3|F4}
GPU=${GPU:-0}
export CUDA_VISIBLE_DEVICES=$GPU
SIGMA=0.03
SRC=$DPPO_DATA_DIR/robomimic/square/train.npz
DSDIR=/home/dataset-local/liyufeng/cadi/design_space
mkdir -p $DSDIR
LOG=$DSDIR/log_${POINT}.log

case $POINT in
  F1) LAM=0.9;  SCL=0.3; TAG=s030_leak09 ;;
  F2) LAM=0.7;  SCL=1.0; TAG=s100_leak07 ;;
  F3) LAM=0.95; SCL=0.5; TAG=s050_leak095 ;;
  F4)
    echo "=== [$(date)] F4: lowpass B finetune only (sigma=$SIGMA, stock prior) ===" | tee -a $LOG
    python script/run.py --config-name=ft_ppo_diffusion_mlp_ds_F4 --config-dir=cfg/robomimic/finetune/square \
      wandb=null seed=42 model.min_sampling_denoising_std=$SIGMA model.min_logprob_denoising_std=$SIGMA 2>&1 | tee -a $LOG
    echo F4_CHAIN_DONE | tee -a $LOG; exit 0 ;;
  *) echo "unknown POINT=$POINT"; exit 1 ;;
esac

DS=square_derivcl_${TAG}_obscmd
DST=$DPPO_DATA_DIR/robomimic/$DS
PRE=pre_diffusion_mlp_derivcl_${TAG}_obscmd
PRENAME=square_${PRE}_ta4_td20
FT=ft_ppo_diffusion_mlp_ds_${POINT}

if [ ! -f "$DST/train.npz" ]; then
  echo "=== [$(date)] [$POINT] dataset leak=$LAM scale=$SCL -> $DS ===" | tee -a $LOG
  python script/make_derivative_dataset.py --src "$SRC" --dst "$DST/train.npz" --scale $SCL --leak $LAM --obs-cmd 2>&1 | tee -a $LOG
  cp $DPPO_DATA_DIR/robomimic/square/normalization.npz $DST/ 2>/dev/null || true
fi

CK=$(ls -t $DPPO_LOG_DIR/robomimic-pretrain/$PRENAME/*/checkpoint/state_3000.pt 2>/dev/null | head -1)
if [ -z "$CK" ]; then
  echo "=== [$(date)] [$POINT] pretrain $PRE ===" | tee -a $LOG
  python script/run.py --config-name=$PRE --config-dir=cfg/robomimic/pretrain/square wandb=null seed=42 2>&1 | tee -a $LOG
  CK=$(ls -t $DPPO_LOG_DIR/robomimic-pretrain/$PRENAME/*/checkpoint/state_3000.pt 2>/dev/null | head -1)
fi
echo "CKPT=$CK" | tee -a $LOG
[ -z "$CK" ] && { echo "[$POINT] no pretrain checkpoint, abort" | tee -a $LOG; exit 1; }

echo "=== [$(date)] [$POINT] BC gate ===" | tee -a $LOG
python script/run.py --config-name=$FT --config-dir=cfg/robomimic/finetune/square wandb=null seed=42 train.n_train_itr=1 \
  base_policy_path=$CK model.min_sampling_denoising_std=$SIGMA model.min_logprob_denoising_std=$SIGMA 2>&1 | tee -a $LOG
SR=$(grep "eval: success rate" $LOG | tail -1 | sed 's/.*success rate *//' | awk '{print $1}')
echo "BC_SR=$SR" | tee -a $LOG
if python -c "import sys; sys.exit(0 if float('${SR:-0}') >= 0.10 else 1)"; then
  echo "=== [$(date)] [$POINT] full finetune (sigma=$SIGMA) ===" | tee -a $LOG
  python script/run.py --config-name=$FT --config-dir=cfg/robomimic/finetune/square wandb=null seed=42 \
    base_policy_path=$CK model.min_sampling_denoising_std=$SIGMA model.min_logprob_denoising_std=$SIGMA 2>&1 | tee -a $LOG
else
  echo "[$POINT] BC gate failed ($SR < 0.10): prior-alignment failure is itself the data point; skipping finetune" | tee -a $LOG
fi
echo ${POINT}_CHAIN_DONE | tee -a $LOG
