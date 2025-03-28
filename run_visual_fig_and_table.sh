# Renew env 
module purge
module load baskerville

# # load cuda (nvcc...)
# module load bask-apps/live
# module load oneAPI-bundle/2024.2.0-CUDA-12.1.1

module load GCC/12.3.0
export LD_LIBRARY_PATH=/bask/apps/live/EL8-ice/software/GCCcore/12.3.0/lib64:$LD_LIBRARY_PATH

# Activate Env
source /bask/projects/j/jlxi8926-auto-sum/kdeng/anaconda3/etc/profile.d/conda.sh
conda activate VLM

python Visual/csv_full_history_exp_pair_phi_error_analysis.py
