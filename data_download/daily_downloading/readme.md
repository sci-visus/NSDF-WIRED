## `daily_downloading`

We run a cron job at 01 UTC each day downloading yesterday's (relative to cron job run) forecasts.

### Instructions for downloading from firesmoke.ca
We use these primary instructions.


| Forecast ID     | Description                                                            | URL                                                                          | Instructions                                                                                             |
|-----------------|------------------------------------------------------------------------|------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------|
| BSC00CA12-01    | BlueSky Canada smoke forecast, 00Z met (12km grid), 08Z fires, North America domain | https://firesmoke.ca/forecasts/BSC00CA12-01/YYYYMMDD08/              | Replace YYYYMMDD with date; append "dispersion.nc" or "dispersion.kmz" to download data                    |
| BSC06CA12-01    | BlueSky Canada smoke forecast, 06Z met (12km grid), 14Z fires, North America domain | https://firesmoke.ca/forecasts/BSC06CA12-01/YYYYMMDD14/              | Replace YYYYMMDD with date; append "dispersion.nc" or "dispersion.kmz" to download data                    |
| BSC12CA12-01    | BlueSky Canada smoke forecast, 12Z met (12km grid), 20Z fires, North America domain | https://firesmoke.ca/forecasts/BSC12CA12-01/YYYYMMDD20/              | Replace YYYYMMDD with date; append "dispersion.nc" or "dispersion.kmz" to download data                    |
| BSC18CA12-01    | BlueSky Canada smoke forecast, 18Z met (12km grid), 02Z fires, North America domain | https://firesmoke.ca/forecasts/BSC18CA12-01/YYYYMMDD02/               | Replace YYYYMMDD with date; append "dispersion.nc" or "dispersion.kmz" to download data                    |
| BSC00WC04-01    | BlueSky Canada smoke forecast, 00Z met (4km grid), 08Z fires, western Canada domain | https://firesmoke.ca/forecasts/BSC00WC04-01/YYYYMMDD08/         | Replace YYYYMMDD with date; append "dispersion.nc" or "dispersion.kmz" to download data |

### File Descriptions

#### download_daily.py:
The python download script to download yesterday's forecasts. Using similar approach as in batch downloading scripts.

#### download.sh:
The script that launches as a cron job everyday at 01 UTC.

#### firesmoke_daily_download.log
Log output from each time the download_daily.py script runs, reporting if downloads were successful or not.

### Cron Job
Run by user `arleth` on `atlantis.sci.utah.edu` with:
```
CRON_TZ="UTC"
0 1 * * * echo "cron ran at $(date -u)" >> /home/collab/arleth/work/NSDF-WIRED/data_download/daily_downloading/cron_heartbeat.log && /home/collab/arleth/work/NSDF-WIRED/data_download/daily_downloading/download.sh
```