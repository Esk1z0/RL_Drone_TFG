import subprocess
import time
import psutil

from config import WIN_BASE_COMMAND, LINUX_BASE_COMMAND, FLAGS
from threading import Event, Thread
import platform


class CommandExecutor:
    """This class handle the simulation command that runs the simulation world file"""
    def __init__(self, simulation_out_event: Event, file_dir: str, **kwargs):
        """Creates the command with the flags selected and the file direction

        Args:
            simulation_out_event (Event): Is the event which is set when the simulation is finished
            file_dir (str): Is the direction of the webots world file
            **kwargs: Flags used in the command to run the simulation

        Keyword Args:
            batch (bool): Use the flag --batch on the command
            realtime (bool): Use the flag --mode=realtime to set the speed to real time on the simulation
            fast (bool): Use the flag --mode=fast to set the speed to fast on the simulation
            no_rendering (bool): Use the flag --no-rendering to disable the graphics on the simulation, any camera will
            be rendered anyway
            stdout (bool): Use the flag --stdout to redirect the webots terminal output to the launching terminal
            stderr (bool): Use the flag --stderr to redirect webots errors to the launching terminal
            minimize (bool): Use the flag --minimize to not open the simulation on the screen
        """
        if not file_dir:
            raise ValueError("The attribute 'file_dir' is mandatory")
        if not simulation_out_event:
            raise ValueError("The attribute 'simulation_out_event' is mandatory")

        self.simulation_out = simulation_out_event
        self.simulator_process = None
        if platform.system() == "Windows":
            self.command = WIN_BASE_COMMAND
        else:
            self.command = LINUX_BASE_COMMAND

        for flag, value in kwargs.items():
            if flag in FLAGS and value:
                self.command += FLAGS[flag]
        self.command += " "+file_dir

    def execute(self) -> None:
        """Runs the command that opens the webots file to start the simulation on another thread and set the event
        at the end

        Returns:
            None
            """

        def run_command():
            try:
                self.simulator_process = subprocess.Popen(self.command, shell=True, stdout=subprocess.PIPE,
                                                          stderr=subprocess.PIPE, text=True)
                stdout, stderr = self.simulator_process.communicate()
                print(f"WEBOTS Result: {stdout}")
                print(f"Result Code: {self.simulator_process.returncode}")
            except subprocess.CalledProcessError as e:
                print(f"Error: {e.stderr}")
            finally:
                self.simulation_out.set()

        thread = Thread(target=run_command)
        thread.start()

        while self.simulator_process is None:
            time.sleep(0.1)
        pid = self.simulator_process.pid
        if not pid or pid == 1:  # Docker podría devolver PID 1 incorrectamente
            for proc in psutil.process_iter(['pid', 'cmdline']):
                if self.command in " ".join(proc.info['cmdline']):  # Verificar si el comando coincide
                    pid = proc.info['pid']
                    break

        if pid is None:
            raise RuntimeError("Could not find the correct PID for the simulator process.")

        return pid
