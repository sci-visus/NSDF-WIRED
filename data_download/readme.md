## Here you find download scripts for all the NetCDF files available from [firesmoke.ca](https://firesmoke.ca/forecasts)

### Current Workflow
Our current workflow is doing hourly downloading.

We use the `rename_all.py` workflow to rename all previously downloaded files to follow the naming convention `dispersion_{CDATE}_{CTIME}.nc` convention. Metadata in the filename is not best practice probably... however all metadata is *also* in the file itself, we store name each file using `CDATE` and `CTIME` for convenience i.e. no need to open the file and check the `CDATE` and `CTIME` during conversion to IDX.

### Instructions for downloading from firesmoke.ca
| Forecast ID     | Description                                                            | URL                                                                          | Instructions                                                                                             |
|-----------------|------------------------------------------------------------------------|------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------|
| BSC00CA12-01    | BlueSky Canada smoke forecast, 00Z met (12km grid), 08Z fires, North America domain | https://firesmoke.ca/forecasts/BSC00CA12-01/YYYYMMDD08/              | Replace YYYYMMDD with date; append "dispersion.nc" or "dispersion.kmz" to download data                    |
| BSC06CA12-01    | BlueSky Canada smoke forecast, 06Z met (12km grid), 14Z fires, North America domain | https://firesmoke.ca/forecasts/BSC06CA12-01/YYYYMMDD14/              | Replace YYYYMMDD with date; append "dispersion.nc" or "dispersion.kmz" to download data                    |
| BSC12CA12-01    | BlueSky Canada smoke forecast, 12Z met (12km grid), 20Z fires, North America domain | https://firesmoke.ca/forecasts/BSC12CA12-01/YYYYMMDD20/              | Replace YYYYMMDD with date; append "dispersion.nc" or "dispersion.kmz" to download data                    |
| BSC18CA12-01    | BlueSky Canada smoke forecast, 18Z met (12km grid), 02Z fires, North America domain | https://firesmoke.ca/forecasts/BSC18CA12-01/YYYYMMDD02/               | Replace YYYYMMDD with date; append "dispersion.nc" or "dispersion.kmz" to download data                    |
| BSC00WC04-01    | BlueSky Canada smoke forecast, 00Z met (4km grid), 08Z fires, western Canada domain | https://firesmoke.ca/forecasts/BSC00WC04-01/YYYYMMDD08/         | Replace YYYYMMDD with date; append "dispersion.nc" or "dispersion.kmz" to download data |

### Available Dates

We manually determined the earliest available files' dates to be March 4, 2021 for the BSC18CA12-01, BSC00CA12-01, BSC06CA12-01 datasets and March 3, 2021 for the BSC12CA12-01 dataset.

We also manually determined the latest available files' dates to be October 16, 2023 for BSC18CA12-01 and BSC06CA12-01, October 15, 2023 for BSC12CA12-01, and February 10, 2024 for BSC00CA12-01.

We did this by simply checking the firesmoke.ca website and downloading the earliest and latest dates available. It would be good to later confirm if there are earlier/later dates and redownloading and convert accordingly.

### Batch vs. Daily vs. Hourly Downloading

#### `batch_downloading`
Beginning the project we downloaded all available NetCDF files from the earliest available dates identified above to the last time we ran the download scripts, June 25, 2024. We then backfilled missing data from June 25, to April 19, 2025 and then implemented a daily download for the NetCDF files to avoid arbitrarily returning and downloading newly created forecasts.

#### `daily_downloading`
The scripts here are used to run a daily cron job where the NetCDF files for yesterday's (realtive to 'today' for the cron job) forecasts  are all downloaded.

We expect all files that were published yesterday to be available the next day. We make sure to download all files before the new forecasts for the day are published.

Since the earliest forecast for the day is published at approximately 09 UTC and the latest at approximately 03 UTC we run the download script at 01 UTC.

#### `hourly_downloading`
The scripts here are used to run an hourly cron job where the NetCDF file at https://firesmoke.ca/forecasts/current/ is downloaded and kept, if we haven't already downloaded it.

### `rename_all.py`

