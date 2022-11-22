# mbta_tool

The environment and dependencies of this repo are installed using Conda.

To use this tool inside a container (recommended):
- first, pull the image from Docker Hub
```commandline
> docker pull peter0083/mbta_tool:dev
```
- then, execute the following for a sample output
```commandline
> docker run peter0083/mbta_tool:dev
INFO:root:Start MBTA subway route planning...
INFO:root:Get subway route from Ashmont to Arlington
INFO:root:Found route data.
{'Red Line', 'Green Line B'}
```
- to run the container interactively
```commandline
> docker container run -ti --entrypoint /bin/bash peter0083/mbta_tool:dev
> conda active mbta
```

To recreate the conda environment `mbta`, 
clone the repo from github then run the following:
```commandline
> conda env create -f environment.yml
> conda activate mbta
```

Sample Usage (assuming you have activated the conda env):


To test:
```commandline
> python -m pytest
```