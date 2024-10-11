import subprocess
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
                result = subprocess.run(self.command, shell=True, capture_output=True, text=True)
                print(f"WEBOTS Result: {result.stdout}")
                print(f"Result Code: {result.returncode}")
            except subprocess.CalledProcessError as e:
                print(f"Error: {e.stderr}")
            finally:
                self.simulation_out.set()

        thread = Thread(target=run_command)
        thread.start()
