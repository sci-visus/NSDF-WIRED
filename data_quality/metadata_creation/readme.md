## Here you find the workflow used to produce `firesmoke_metadata.nc`.

### The purpose of this workflow is to package:
- The cloud link to the IDX conversion of the firesmoke forecasts.
- The metadata describing each individual timestep found in the NetCDF files themselves.
- The metadata describing the timesteps as a compiled database/relative to one another. For example, which timesteps' data are resampled from 1041x381 grid to 1081x381 grids, how far the are from the last forecast update time, what time range is represented by _all_ time steps, etc.

This makes data sharing and transparency as efficient and comprehensive as possible.

### Metadata sources:
The notebooks here refer to different `.pkl` and `.npy` files. These files contain metadata collected during IDX conversion or manually scraped from the NetCDF files we have downloaded. You will not find the actual files here because they are too large to store.

As new conversions are created or new metadata is needed, we return to this workflow to create an updated `firesmoke_metadata.nc` file accordingly.