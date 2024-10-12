FROM cyberbotics/webots:R2023b-ubuntu22.04

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
RUN pip install -e ./simulation_package/controllers/xyz_controller/drone_library

# Exponer los puertos (si es necesario)
EXPOSE 8000
EXPOSE 8001

# Comando por defecto
CMD ["python", "run_simulation.py"]
