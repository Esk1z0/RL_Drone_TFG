FROM cyberbotics/webots:R2023b-ubuntu22.04
FROM continuumio/miniconda3 AS build

COPY . /home/app

RUN conda install -c conda-forge --file /home/app/configs/conda_config/requirements.txt

WORKDIR /home/app

EXPOSE 8000
EXPOSE 8001
VOLUME /home/app/data

CMD ["python", "run_simulation.py"]