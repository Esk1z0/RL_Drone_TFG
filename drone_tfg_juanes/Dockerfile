FROM cyberbotics/webots:R2023b-ubuntu22.04

RUN apt-get update && apt-get install -y \
    x11-apps \
    libgl1-mesa-glx \
    libxrender1 \
    libxtst6 \
    libxi6 \
    libopenal1 \
    && apt-get clean


# Actualizar los repositorios e instalar Python 3.10 y pip
RUN apt-get update && \
    apt-get install -y python3.10 python3-pip && \
    ln -s /usr/bin/python3.10 /usr/bin/python

# Copiar el proyecto al contenedor
COPY . /home/drone_tfg_juanes

# Establecer el directorio de trabajo
WORKDIR /home/drone_tfg_juanes

# Instalar las dependencias usando pip
RUN pip install -r configs/requirements_config/requirements.txt

# Instalar los paquetes locales en modo editable
RUN pip install -e .
RUN pip install -e ./simulation_package/controllers/xyz_controller/robot_library
RUN pip install -e ./environments_package

ENV PYTHONPATH="${PYTHONPATH}:/home/drone_tfg_juanes/simulation_package/controllers/xyz_controller/robot_library"


# Añadir argumento y variable de entorno
ARG MODE=train
ENV MODE=${MODE}

# Comando por defecto usando la variable
CMD ["sh", "-c", "python run_simulation.py --save-dir /home/drone_tfg_juanes/data --mode $MODE"]
