import mmap

# Abrir el archivo de memoria compartida
shm = mmap.mmap(-1, 1024, "shared_memory")

# Leer datos desde la memoria compartida
shm.seek(0)
data = shm.read(1024)
print("Datos recibidos:", data.decode())

# Cerrar la memoria compartida
shm.close()
