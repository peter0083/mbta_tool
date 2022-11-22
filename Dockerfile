FROM continuumio/miniconda3

WORKDIR /app

# Create the environment:
COPY environment.yml .
RUN conda env create -f environment.yml

# Make RUN commands use the new environment:
SHELL ["conda", "run", "-n", "mbta", "/bin/bash", "-c"]

# Demonstrate the environment is activated:
RUN conda env list

# The code to run when container is started:
ADD ./* $HOME/app/
ENTRYPOINT ["python", "mbta_cli.py", "Ashmont", "Arlington"]