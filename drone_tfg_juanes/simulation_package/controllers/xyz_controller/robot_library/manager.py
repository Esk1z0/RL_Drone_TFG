import os
import json
import tempfile
import portalocker

MANAGER_FILE = os.path.join(tempfile.gettempdir(), "uid_manager.json")

if not os.path.exists(MANAGER_FILE):
    with open(MANAGER_FILE, "w") as f:
        json.dump({}, f)

def _read_manager():
    """
    Lee el archivo manager y devuelve los datos como un diccionario,
    usando un lock de archivo para evitar colisiones entre procesos.
    """
    with open(MANAGER_FILE, "r") as f:
        # Adquiere lock de lectura/escritura
        portalocker.lock(f, portalocker.LOCK_EX)
        data = json.load(f)
        # Libera el lock antes de retornar
        portalocker.unlock(f)
    return data

def register_uid(pid, uid):
    """
    Registra un UID asociado a un PID en el archivo manager,
    en un solo paso de lock, read, modify, write.
    """
    with open(MANAGER_FILE, "r+") as f:
        portalocker.lock(f, portalocker.LOCK_EX)  # Bloqueo completo
        data = json.load(f)

        # Actualizar data en memoria
        data[str(pid)] = uid

        # Re-escribir el archivo completo
        f.seek(0)
        json.dump(data, f)
        f.truncate()

        portalocker.unlock(f)

def get_uid(pid):
    """
    Obtiene el UID asociado a un PID, sin eliminar la entrada.
    """
    with open(MANAGER_FILE, "r+") as f:
        portalocker.lock(f, portalocker.LOCK_EX)
        data = json.load(f)
        uid = data.get(str(pid))
        portalocker.unlock(f)
    return uid

def delete_uid(uid):
    """
    Elimina la entrada asociada a un UID.
    """
    with open(MANAGER_FILE, "r+") as f:
        portalocker.lock(f, portalocker.LOCK_EX)
        data = json.load(f)

        pid_to_delete = None
        for pid, stored_uid in data.items():
            if stored_uid == uid:
                pid_to_delete = pid
                break

        if pid_to_delete:
            del data[pid_to_delete]

        f.seek(0)
        json.dump(data, f)
        f.truncate()

        portalocker.unlock(f)

def list_all_uids():
    """
    Lista todas las entradas del manager.
    """
    with open(MANAGER_FILE, "r") as f:
        portalocker.lock(f, portalocker.LOCK_EX)
        data = json.load(f)
        portalocker.unlock(f)
    return data

def clear_manager():
    """
    Limpia todas las entradas.
    """
    with open(MANAGER_FILE, "r+") as f:
        portalocker.lock(f, portalocker.LOCK_EX)
        json.dump({}, f)
        f.truncate()
        portalocker.unlock(f)

