## Here you find download scripts for all the netCDF files available from [firesmoke.ca](https://firesmoke.ca/forecasts)

### Instructions for downloading from firesmoke.ca
Each download script version uses these primary instructions.

| Forecast ID     | Description                                                            | URL                                                                          | Instructions                                                                                             |
|-----------------|------------------------------------------------------------------------|------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------|
| BSC00CA12-01    | BlueSky Canada smoke forecast, 00Z met (12km grid), 08Z fires, North America domain | https://firesmoke.ca/forecasts/BSC00CA12-01/YYYYMMDD08/              | Replace YYYYMMDD with date; append "dispersion.nc" or "dispersion.kmz" to download data                    |
| BSC06CA12-01    | BlueSky Canada smoke forecast, 06Z met (12km grid), 14Z fires, North America domain | https://firesmoke.ca/forecasts/BSC06CA12-01/YYYYMMDD14/              | Replace YYYYMMDD with date; append "dispersion.nc" or "dispersion.kmz" to download data                    |
| BSC12CA12-01    | BlueSky Canada smoke forecast, 12Z met (12km grid), 20Z fires, North America domain | https://firesmoke.ca/forecasts/BSC12CA12-01/YYYYMMDD20/              | Replace YYYYMMDD with date; append "dispersion.nc" or "dispersion.kmz" to download data                    |
| BSC18CA12-01    | BlueSky Canada smoke forecast, 18Z met (12km grid), 02Z fires, North America domain | https://firesmoke.ca/forecasts/BSC18CA12-01/YYYYMMDD02/               | Replace YYYYMMDD with date; append "dispersion.nc" or "dispersion.kmz" to download data                    |

### Automating the download instructions

We manually determined the earliest available files' dates to be March 4, 2021 for the BSC18CA12-01, BSC00CA12-01, BSC06CA12-01 datasets and March 3, 2021 for the BSC12CA12-01 dataset.

We also manually determined the latest available files' dates to be October 16, 2023 for BSC18CA12-01 and BSC06CA12-01, October 15, 2023 for BSC12CA12-01, and February 10, 2024 for BSC00CA12-01.

We did this by simply checking the firesmoke.ca website and downloading the earliest and latest dates available. It would be good to later confirm if there are earlier/later dates and redownloading and convert accordingly.

---
## The following is how our approach to conversion changed in each version:

get_data_v0:
---
We use `wget` to download the content at the URL specified. 

get_data_v1:
---
We use `requests` now, as this allow us to download _only_ netCDF files if they exist at the URL. `wget` downloads whatever is at the specified URL whether it is a netCDF file or not, which we have had to clean up.