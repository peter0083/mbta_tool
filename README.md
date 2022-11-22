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
```commandline
(mbta)> python mbta_cli.py --list_subway_routes
{'Blue Line',
 'Green Line B',
 'Green Line C',
 'Green Line D',
 'Green Line E',
 'Mattapan Trolley',
 'Orange Line',
 'Red Line'}

(mbta)> python mbta_cli.py --list_subway_route_ids 
{('Blue Line', 'Blue'),
 ('Green Line B', 'Green-B'),
 ('Green Line C', 'Green-C'),
 ('Green Line D', 'Green-D'),
 ('Green Line E', 'Green-E'),
 ('Mattapan Trolley', 'Mattapan'),
 ('Orange Line', 'Orange'),
 ('Red Line', 'Red')}

(mbta)> python mbta_cli.py Ashmont Arlington
INFO:root:Start MBTA subway route planning...
INFO:root:Get subway route from Ashmont to Arlington
INFO:root:Found route data.
{'Green Line B', 'Red Line'}
```

To test:
```commandline
> python -m pytest
```