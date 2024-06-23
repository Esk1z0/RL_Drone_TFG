import subprocess
from .config import BASE_COMMAND, FLAGS
from threading import Event, Thread


class CommandExecutor:
    def __init__(self, simulation_out_event: Event, file_dir, **kwargs):

        if not file_dir:
            raise ValueError("The atribute 'file_dir' is mandatory")
        if not simulation_out_event:
            raise ValueError("The atribute 'simulation_out_event' is mandatory")

        self.simulation_out = simulation_out_event
        self.command = BASE_COMMAND

        for flag, value in kwargs.items():
            if flag in FLAGS and value:
                self.command += FLAGS[flag]
        self.command += " "+file_dir

    def execute(self):
        def run_command():
            try:
                result = subprocess.run(self.command, shell=True, capture_output=True, text=True)
                print(f"Result: {result.stdout}")
                print(f"Result Code: {result.returncode}")
            except subprocess.CalledProcessError as e:
                print(f"Error: {e.stderr}")
            finally:
                self.simulation_out.set()

        thread = Thread(target=run_command)
        thread.start()
