from drone_tfg_juanes.simulation_package.controllers.xyz_controller.drone_library.drone_simulation import Drone


class DroneBaseEnv():


    def __init__(self, maxtime, command, simulation_dir):
        self.observation_space = {
            "camera": "Image rgba of 400x240",
            "IMU": "Quaternion",
            "Sonar": "distane from 0 to 1 with a range of 2 meters"
        }
        self.action_space = "array of 4 values from  to 1"
        self.drone = Drone(simulation_dir)
        self.motors = [0, 0, 0, 0]

        self.maxtime = maxtime
        self.command = command

        self.drone.start_simulation()

    def step(self, action):
        reward, terminated = 0, True
        self.drone.send({"ACTION": "SET_ALL_MOTORS", "PARAMS": action})
        observation = self.get_obs()
        observation["command"] = self.command
        truncated = self.is_truncated()
        if not truncated:
            reward, terminated = self.reward(observation)
        return observation, reward, terminated, truncated, self.drone.get_actions()

    def reset(self, seed=None, options=None):
        self.motors = [0, 0, 0, 0]
        self.drone.send({"ACTION": "RESET", "PARAMS": ""})
        observation = self.get_obs()
        return observation

    def close(self):
        self.drone.end_simulation()

    def reward(self, observation):
        pass

    def is_truncated(self):
        return self.drone.is_sim_out()

    def get_obs(self):
        return self.drone.receive()


if __name__ == '__main__':
    lista = [[[1, 2, 3], [4, 5, 6]], [[7, 8, 9], [10, 11, 12]]]
    cadena = str(lista)
    print(cadena)
