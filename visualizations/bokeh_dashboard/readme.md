Ensure that you install the following, we used a conda environment:
python 3.9
[bokeh](https://docs.bokeh.org/en/3.6.2/docs/first_steps.html)
[xarray](https://docs.xarray.dev/en/stable/getting-started-guide/installing.html)
[openvisus](https://github.com/sci-visus/OpenVisus/tree/master)
[openvisuspy](https://github.com/sci-visus/openvisuspy)
[xmltodict](https://pypi.org/project/xmltodict/)

With cwd set to this directory, launch the bokeh application with:
`bokeh serve --show .`

Ensure you have `firesmoke_metadata.nc` in this directory, otherwise, ensure it is downloaded by setting `download = True` in `data_handling.py`.