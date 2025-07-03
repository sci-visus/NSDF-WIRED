#!/bin/bash
source /home/arleth/miniconda3/etc/profile.d/conda.sh
conda activate wired_env
python /home/arleth/NSDF-WIRED/data_download/hourly_downloading/download_hourly.py
