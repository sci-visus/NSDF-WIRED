# WIRED Global 

Welcome to NSDF's WIRED Global Center GitHub repository. NSDF and WIRED Global aim to connect climate, weather, power grid, and social data with essential software tools and computing resources. We will empower researchers with advanced tools for data acquisition, storage, management, integration, mining, and visualization.

## Table of Contents

- [WIRED Global](#wired-global)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
    - [Current Tasks](#current-tasks)
  - [Project Structure](#project-structure)
    - [Directory Tree, 2 Levels Down](#directory-tree-2-levels-down)
  - [Implementation Notes](#implementation-notes)
  - [Contributing](#contributing)
    - [Contact](#contact)
  - [Related Works](#related-works)

## Overview

Here you will find current progress on the repurposing of smoke forecast data from various diverse sources to the OpenVisus framework.

Our current goal is the data repurposing of [Smoke Forecasts](https://firesmoke.ca/) from The Weather Forecast Research Team at the University of British Columbia.

### Current Tasks
- Create a cron job for getting latest firesmoke forecasts.
- Paralellization of and extension of conversion script to be more robust to incorporating new timestamps.

## Project Structure

Curating the set of NetCDF files containing Smoke Forecasts to a single 3D array stored in OpenVisus' IDX format requires iterative refinement. We return to different steps in the process to produce a higher quality curation each time, hence various versions of the steps outlined below.

Each step is described by it's directory name, see below what each directory contains:
- `data_download`: Script about downloading the NetCDF files from [FireSmoke Canada](https://firesmoke.ca/).
- `conversion`: Versions of our script to convert the hundreds of NetCDF files to a single IDX file.
- `visualizations`: Visualizations to inspect our data under different contexts and to test different visualization libraries with this dataset. Subdirectory `demos` has versions of self-contained demos using the data in IDX format.
- `data_quality`: Scripts toward identifying gaps and issues like silent corruption.
- `data`: NetCDF file for final use, non-interim.
- `scribbles.ipynb` is a notebook that serves as a scratch pad, code here may or may not be incoporated into the workflows above.
- `communication` is the source code for the quarto documentation available in the sidebar.
- `eccc_issue` is work relating to Prof. Mostafa and team's work on solar PV efficacy, it is not prepared for readability.
Check the `readme.md` of each directory to see further details about each step.

### Directory Tree, 2 Levels Down
```
.
├── communication
│   └── UBC Smoke Forecast Data Curation
├── conda_environment.yml
├── conversion
│   ├── conversion_sequence_debug.ipynb
│   ├── firesmoke_to_idx2.ipynb
│   ├── firesmoke_to_idx_v1.ipynb
│   ├── firesmoke_to_idx_v2.ipynb
│   ├── firesmoke_to_idx_v3.ipynb
│   ├── firesmoke_to_idx_v4.ipynb
│   ├── readme.md
│   └── westerncanada_parallel_idx.ipynb
├── data
│   ├── firesmoke_metadata.nc
│   └── readme.md
├── data_download
│   ├── get_data_v0.py
│   ├── get_data_v1-westerncanada.py
│   ├── get_data_v1.py
│   └── readme.md
├── data_quality
│   ├── data_quality
│   ├── metadata_creation
│   └── readme.md
├── eccc_issue
│   ├── ecc_firesmoke_viz-toshare.ipynb
│   ├── eccc_data_clean.ipynb
│   ├── eccc_firesmoke_viz-toshare.ipynb
│   ├── eccc_frames-basemap.ipynb
│   ├── eccc_frames.ipynb
│   ├── firesmoke-idx-scribble.ipynb
│   ├── firesmoke_idx_vs_eccc_frames.ipynb
│   ├── firesmoke_metadata.nc
│   ├── process_firesmoke.py
│   └── visus_cache_can_be_erased
├── readme.md
├── scribbles.ipynb
└── visualizations
    ├── bokeh_dashboard
    ├── dashboard
    ├── demos
    ├── firesmoke-dashboard.ipynb
    ├── firesmoke-viz.ipynb
    ├── firesmoke_idx-viz.ipynb
    ├── firesmoke_metadata.nc
    ├── make_videos
    ├── readme.md
    └── xarray_leaflet_vis.ipynb
```

## Implementation Notes

- This work was done in Python 3.9.18., `conda_environment.yml` is the conda environment we have used during the development of this project.
- Data repurposing has been run using SCI Institute resources, in particular, files are downloaded to those systems and processed there due to the large volume of data.
- Running the workflow described above may be difficult on a consumer-grade machine. Consider using small batches of data to test and via University of Utah and/or University of British Columbia nodes, full data processing can be run.
- Ensure you change directory names within notebooks to fit your work environment accordingly.

## Contributing

The nature of data repurposing means new issues or requirements are found. Please feel free to make push requests if you are confident about a script and/or edit that has improved one of the steps above. Please be sure to describe in concrete terms what changes your work yields.

### Contact

Please feel free to contact us here for detailed information:
- Arleth Salinas [Website](https://arlethzuri.github.io/)
- Valerio Pascucci [Email](mailto:pascucci.valerio@gmail.com)

## Related Works
1 . Pascucci, Valerio, et al. "The ViSUS visualization framework." High Performance Visualization. Chapman and Hall/CRC, 2012. 439-452. [Here](https://www.taylorfrancis.com/chapters/edit/10.1201/b12985-32/visus-visualization-framework-valerio-pascucci-giorgio-scorzelli-brian-summa-peer-timo-bremer-attila-gyulassy-cameron-christensen-sujin-philip-sidharth-kumar)
