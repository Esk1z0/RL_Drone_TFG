import os
import json
import tempfile
from threading import Lock

# Archivo "manager" donde se registrarán los UIDs
MANAGER_FILE = os.path.join(tempfile.gettempdir(), "uid_manager.json")
lock = Lock()

# Asegurarse de que el archivo manager exista
if not os.path.exists(MANAGER_FILE):
    with open(MANAGER_FILE, "w") as f:
        json.dump({}, f)


def _read_manager():
    """Lee el archivo manager y devuelve los datos como un diccionario."""
    with lock:
        with open(MANAGER_FILE, "r") as f:
            return json.load(f)


def _write_manager(data):
    """Escribe los datos en el archivo manager."""
    with lock:
        with open(MANAGER_FILE, "w") as f:
            json.dump(data, f)


def register_uid(pid, uid):
    """
    Registra un UID asociado a un PID en el archivo manager.

    Args:
        pid (int): PID del controlador.
        uid (str): UID asociado al PID.
    """
    data = _read_manager()
    data[str(pid)] = uid
    _write_manager(data)


def get_uid(pid):
    """
    Obtiene el UID asociado a un PID sin eliminar la entrada del archivo manager.

    Args:
        pid (int): PID del controlador.

    Returns:
        str: UID asociado al PID, o None si no se encuentra.
    """
    data = _read_manager()
    return data.get(str(pid))


def delete_uid(uid):
    """
    Elimina la entrada asociada a un UID del archivo manager.

    Args:
        uid (str): UID asociado a algún PID.
    """
    data = _read_manager()
    pid_to_delete = None

    # Buscar el PID asociado al UID
    for pid, stored_uid in data.items():
        if stored_uid == uid:
            pid_to_delete = pid
            break

    if pid_to_delete:
        del data[pid_to_delete]
        _write_manager(data)


def list_all_uids():
    """
    Lista todas las entradas del archivo manager.

    Returns:
        dict: Diccionario con todos los PIDs y sus UIDs.
    """
    return _read_manager()


def clear_manager():
    """Limpia todas las entradas del archivo manager."""
    _write_manager({})
