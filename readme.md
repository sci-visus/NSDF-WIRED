# WIRED Global 

Welcome to NSDF's WIRED Global Center GitHub repository. NSDF and Wired Global aim to connect climate, weather, power grid, and social data with essential software tools and computing resources. We will empower researchers with advanced tools for data acquisition, storage, management, integration, mining, and visualization.

## Table of Contents

- [Overview](#overview)
- [Project Structure](#project-structure)
- [Implementation/System Notes](#implementation/system_notes)
- [Contributing](#contributing)
- [Related Works](#related-works)

## Overview

Here you will find current progress on the transformation of climate data from various diverse sources to the OpenVisus framework.

Our current goal is the data curation of [Smoke Forecasts](https://firesmoke.ca/) from The Weather Forecast Research Team at the University of British Columbia.

### Current Tasks
- Determine what hours are missing and compile into spreadsheet. Share with UBC and obtain any additional hours and incorporate accordingly.

## Project Structure

Curating the set of netCDF files containing Smoke Forecasts to a single 3D array stored in OpenVisus' IDX format requires iterative refinement. We return to different steps in the process to produce a higher quality curation each time, hence various versions of the steps outlined below.

Each step is described by it's directory name, see below what each directory contains:
- `data_download`: Script about downloading the netCDF files from [FireSmoke Canada](https://firesmoke.ca/).
- `conversion`: Versions of our script to convert the hundreds of netCDF files to a single IDX file.
- `visualizations`: Quick and dirty visualizations to inspect our data under different contexts. Subdirectory `demos` has versions of self-contained demos using the data in IDX format.
- `data_quality`: Scripts toward identifying gaps and issues like silent corruption.

Check the `readme.md` of each directory to see further details about each step.

### Directory Tree
```
.
├── conversion
│   ├── firesmoke_to_idx2.ipynb
│   ├── firesmoke_to_idx_v1.ipynb
│   ├── firesmoke_to_idx_v2.ipynb
│   └── firesmoke_to_idx_v3.ipynb
├── data_download
│   └── get_data.py
├── data_quality
│   ├── data_quality
│   │   └── firesmoke_issues.ipynb
│   └── metadata_creation
│       ├── firesmoke_tflags.ipynb
│       └── make_firesmoke_tiny_netcdf.ipynb
├── readme.md
├── scribbles.ipynb
└── visualizations
    ├── demos
    │   ├── v0
    │   ├── v1
    │   ├── v3
    │   └── v4
    ├── firesmoke-dashboard.ipynb
    ├── firesmoke-viz.ipynb
    ├── firesmoke_idx-viz.ipynb
    └── readme.md
```

## Implementation/System Notes

- This work was done in Python 3.9.18.
- Data curation has been run using SCI Institute resources, in particular, files are downloaded to those systems and processed there due to the large volume of data.
- Running the workflow described above may be difficult on a consumer-grade machine. Consider using small batches of data to test and via University of Utah and/or University of British Columbia nodes, full data processing can be run.
- Ensure you change directory names within notebooks to fit your work environment accordingly.


## Contributing

The nature of data curation means new issues or requirements are found. Please feel free to make push requests if you are confident about a script and/or edit that has improved one of the steps above. Please be sure to describe in concrete terms what changes your work yields.

### Contact

Please feel free to contact us here for detailed information:
- Arleth Salinas [Website](https://arlethzuri.github.io/)
- Valerio Pascucci [Email](mailto:pascucci.valerio@gmail.com)

## Related Works
1 . Pascucci, Valerio, et al. "The ViSUS visualization framework." High Performance Visualization. Chapman and Hall/CRC, 2012. 439-452. [Here](https://www.taylorfrancis.com/chapters/edit/10.1201/b12985-32/visus-visualization-framework-valerio-pascucci-giorgio-scorzelli-brian-summa-peer-timo-bremer-attila-gyulassy-cameron-christensen-sujin-philip-sidharth-kumar)
