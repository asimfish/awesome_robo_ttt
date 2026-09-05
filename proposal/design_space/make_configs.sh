#!/bin/bash
# Generate pretrain/finetune configs for design-space points F1-F4 from the existing arm templates.
set -euo pipefail
cd /home/dataset-local/liyufeng/cadi/dppo/cfg/robomimic
PRE_T=pretrain/square/pre_diffusion_mlp_derivcl_s100_leak09_obscmd.yaml
FT_T=finetune/square/ft_ppo_diffusion_mlp_armC_leak09.yaml
B_T=finetune/square/ft_ppo_diffusion_mlp_armB.yaml

mk() {  # POINT LAM SCL TAG
  local P=$1 LAM=$2 SCL=$3 TAG=$4
  sed -e "s/derivcl_s100_leak09_obscmd/derivcl_${TAG}_obscmd/g" $PRE_T > pretrain/square/pre_diffusion_mlp_derivcl_${TAG}_obscmd.yaml
  sed -e "s/_ft_diffusion_mlp_armC_leak09_/_ft_diffusion_mlp_ds_${P}_/" \
      -e "s/^      leak: 0.9$/      leak: ${LAM}/" \
      -e "s/^      scale: 1.0$/      scale: ${SCL}/" $FT_T > finetune/square/ft_ppo_diffusion_mlp_ds_${P}.yaml
  echo "[$P] leak=$(grep -m1 'leak:' finetune/square/ft_ppo_diffusion_mlp_ds_${P}.yaml | tr -d ' ') scale=$(grep -m1 'scale:' finetune/square/ft_ppo_diffusion_mlp_ds_${P}.yaml | tr -d ' ') dataset=$(grep -m1 train_dataset_path pretrain/square/pre_diffusion_mlp_derivcl_${TAG}_obscmd.yaml | sed 's/.*robomimic\///')"
}
mk F1 0.9  0.3 s030_leak09
mk F2 0.7  1.0 s100_leak07
mk F3 0.95 0.5 s050_leak095
mk F5 0.8  0.2 s020_leak08
sed -e "s/_ft_diffusion_mlp_armB_/_ft_diffusion_mlp_ds_F4_/" $B_T > finetune/square/ft_ppo_diffusion_mlp_ds_F4.yaml
echo "[F4] $(grep -m1 'name:' finetune/square/ft_ppo_diffusion_mlp_ds_F4.yaml)"
ls finetune/square/ft_ppo_diffusion_mlp_ds_*.yaml pretrain/square/pre_diffusion_mlp_derivcl_s030* pretrain/square/pre_diffusion_mlp_derivcl_s100_leak07* pretrain/square/pre_diffusion_mlp_derivcl_s050*
