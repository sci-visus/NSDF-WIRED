## Here you find conversions of all the netCDF files downloaded using workflow in `data_download` to the OpenVisus IDX file format.

For all versions, the same general process is followed:
1. Check which netCDF files successfully downloaded from `firesmoke.ca` by attempting to open each downloaded file with `xarray`. Need to check this since `wget` will download `.html` file if no netCDF file was found during download.
2. Step though all files in chronological sequence, hour by hour, and save data at each hour to `.idx` using the [OpenVisus](https://github.com/sci-visus/OpenVisus/tree/master) framework.
---
## The following is how our approach to conversion changed in each version:

firesmoke_to_idx_v1:
---
Initially, we used just the BSC00CA12-01 dataset as this ran the longest (until 2024).

firesmoke_to_idx_v2:
---
We realized that the latitude longitude grid of the BSC00CA12-01 was either of size 1041x381 or 1081x381. Here we resample the smaller to the larger grid accordingly.

firesmoke_to_idx_v3:
---
Instead of using just BSC00CA12-01 we use all available datasets, BSC06CA12-01,BSC12CA12-01, and BSC18CA12-01. These forecasts are the same model but with new starting parameters, each dataset corresponds to the initialization time. Further details can be found at [firesmoke.ca/forecasts](https://firesmoke.ca/forecasts/).

firesmoke_to_idx2:
---
Not complete yet, but it is for later use to convert the firesmoke data to the IDX2 data format.