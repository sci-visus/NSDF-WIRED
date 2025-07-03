## `daily_downloading`

We run a cron job every hour downloading the current forecast's NetCDF file, deleting the downloaded NetCDF file if we already have it.

### Instructions for downloading from firesmoke.ca
Instead of downloading each forecast based on its full URL and specifying date time, we switch to downloading the 'current' forecast each hour.

URL to the current forecast at any given time is: https://firesmoke.ca/forecasts/current/

There are benefits to this approach relative to all our previous downloading approaches:
- Our scripts no longer need to stay up to date with any forecast URL name changes.
- By checking each hour, we can retry downloading any previously failed downloads from extranious issues like network connectivity.

### File Descriptions

#### download_hourly.py:
The python download script to download yesterday's forecasts. Using similar approach as in batch downloading scripts.

#### download.sh:
The script that launches as a cron job hourly.

#### firesmoke_daily_download.log
Log output from each time the download_daily.py script runs, reporting if downloads were successful or not.

### Cron Job
Run by user `arleth` on `canada1` with:
```
0 * * * * echo "cron ran at $(date -u)" >> /home/arleth/NSDF-WIRED/data_download/hourly_downloading/cron_heartbeat.log && /home/arleth/NSDF-WIRED/data_download/hourly_downloading/download.sh
```