import mmap
import time

# Crear un archivo de memoria compartida
shm = mmap.mmap(-1, 1024, "shared_memory")

# Escribir datos en la memoria compartida
shm.write(b"Hello from producer")

time.sleep(4)
# Cerrar la memoria compartida
shm.close()
