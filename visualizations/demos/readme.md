## Here you find self-contained demos using the IDX conversion stored in the cloud.

The tools for integrating the IDX data with Jupyter Notebook have rapidly changed, each version reflects these changes. We are working toward as small and as few files as possible to make the demo sharable.

---
## The following is how the demos have changed.

v0:
---
Here we directly use the IDX file in cloud and the OpenVisus library to open and get data. Notably, metadata for the data is not available.

v1:
---
Same as v0, but now timestep metadata is imported from a `.npy` file created at the time and the metadata for the dataset is imported from one of the downloaded netCDF files.

v3 (v2 contained here as well):
---
We introduce use of `backend_v3.py` which connects OpenVisus to xarray. Here is where we begin using `firesmoke_metadata.nc`. 

`firesmoke_metadata.nc` contains the original metadata found in the netCDF files, with timesteps updated to reflect IDX timesteps and IDX data URL appended.

v4:
---
No significant changes, just adjusting demo in notebook.

v5:
---
`backend_v3.py` is no longer required, it is in the `openvisuspy` library now. Additionally, demo now downloads latest version of `firesmoke_metadata_current.nc` and loads it accordingly. 

Now one does not need to find these files themselves.

v6:
---
Newly incorporated metadata is included in the demo.