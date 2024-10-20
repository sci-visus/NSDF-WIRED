## Here you find the creation of videos of all frames from IDX conversion and the firesmoke netCDF data, respectively.

As of now, this is how we have inspected the sequence we made and test for errors when trying to visualize each timestep. There's better ways...

---
## The following describes each part of the workflow

old_serialized:
---
This folder contains the original serialized versions of creating frames for our videos. The speed up from parallelizing is ~17x

firesmoke_idx_parallel_frames:
---
Generate .PNG images by stepping through all timesteps of the IDX conversion. Executed in parallel.

firesmoke_netcdf_parallel_frames:
---
Generate .PNG images by stepping through the `idx_calls_v4` sequence and opening netCDF files and getting timestep data accordingly. Executed in parallel.

make_videos:
---
Create the videos for each set of frames, IDX and netCDF.

make_new_stack:
---
Take the videos generated of IDX and netCDF and stack them on one another to visually compare them.