import mmap
import time
from Mmap_Semaphore import BinarySemaphore

b = BinarySemaphore(name="Hola")
# Crear un archivo de memoria compartida
shm = mmap.mmap(-1, 10, "shared_memory")
mensage = b'Las BD NoSQL utilizan map/reduce para consultar e indexar la base de datosLas BD NoSQL utilizan map/reduce para consultar e indexar la base de datosLas BD NoSQL utilizan map/reduce para consultar e indexar la base de datosLas BD NoSQL utilizan map/reduce para consultar e indexar la base de datosLas BD NoSQL utilizan map/reduce para consultar e indexar la base de datosLas BD NoSQL utilizan map/reduce para consultar e indexar la base de datos'


t = time.monotonic()
for i in range(0, len(mensage), 10):
    while not b.is_write_open():
        pass
    chunk = mensage[i:i + 10]
    print('hola')
    print(chunk)
    print(len(chunk))
    if len(chunk) < 10:
        shm.seek(0)
        shm.write(b'\x00'*10)
    shm.seek(0)
    shm.write(chunk)
    shm.flush()

    b.read_open()

shm.seek(0)
shm.write(b'\x00'*10)

print('tiempo: ' + str(time.monotonic() - t))
shm.seek(0)
print(shm.read())
shm.flush()
b.read_open()

time.sleep(4)
# Cerrar la memoria compartida
shm.close()
