FROM cyberbotics/webots:R2023b-ubuntu22.04

# Establecer variables de entorno para Miniconda
ENV CONDA_DIR /opt/conda
ENV PATH $CONDA_DIR/bin:$PATH

# Instalar dependencias necesarias
RUN apt-get update && apt-get install -y \
    wget \
    bzip2 \
    ca-certificates \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Descargar e instalar Miniconda
RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O /tmp/miniconda.sh && \
    bash /tmp/miniconda.sh -b -p $CONDA_DIR && \
    rm /tmp/miniconda.sh

# Forzar la carga del entorno de conda en bash
RUN echo ". /opt/conda/etc/profile.d/conda.sh" >> ~/.bashrc

# Actualizar conda
RUN conda update -n base -c defaults conda

# Copiar el archivo de entorno
COPY ../drone_tfg_juanes/configs/conda_config/environment.yml /tmp/environment.yml

# Crear el entorno de conda
RUN conda env create -f /tmp/environment.yml || cat /tmp/environment.yml

# Activar el entorno de conda
ENV CONDA_DEFAULT_ENV mi_entorno
ENV PATH $CONDA_DIR/envs/$CONDA_DEFAULT_ENV/bin:$PATH

# Establecer el directorio de trabajo
WORKDIR /home/webots

# Copiar el código de tu proyecto al contenedor
COPY ../drone_tfg_juanes /home/webots

# Exponer los puertos necesarios
EXPOSE 8000
EXPOSE 8001

# Definir el volumen
VOLUME /home/webots/data

# Configurar el entrypoint y el comando por defecto
ENTRYPOINT ["conda", "run", "--no-capture-output", "-n", "mi_entorno"]
CMD ["python", "run_simulation.py"]
