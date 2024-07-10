## Here you find the creation of videos of all frames from IDX conversion and the firesmoke netCDF data, respectively.

As of now, this is how we have inspected the sequence we made and test for errors when trying to visualize each timestep. There's better ways...

---
## The following describes each part of the workflow

firesmoke_idx_all_frames:
---
Generate .PNG images by stepping through all timesteps of the IDX conversion. 

firesmoke_netcdf_all_frames:
---
Generate .PNG images by stepping through the `idx_calls_v4` sequence and opening netCDF files and getting timestep data accordingly.

make_videos:
---
Create the videos for each set of frames, IDX and netCDF.

make_new_stack:
---
Take the videos generated of IDX and netCDF and stack them on one another to visually compare them.