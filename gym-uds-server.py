#!/usr/bin/env python3
import argparse
import os
import time
from concurrent import futures

import grpc
import gym
from gym import wrappers
import gym_uds_pb2
import gym_uds_pb2_grpc
import numpy as np

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class Environment(gym_uds_pb2_grpc.EnvironmentServicer):
    def __init__(self, env_id):
        ##### This is a general configuration that can be used
        ##### to modify number of eposodes and rewards for environments
        # gym.envs.register(
        #     id='MountainCarMyEasyVersion-v0',
        #     entry_point='gym.envs.classic_control:MountainCarEnv',
        #     max_episode_steps=1000,      # MountainCar-v0 uses 200
        #     reward_threshold=-110.0,
        # )
        
        self.env = gym.make(env_id)
        
        ##### Uncomment below (comment above) to create an environment
        ##### that can record videos of the executions for the environment
        # self.env = wrappers.Monitor(gym.make(env_id), './videos/' + str(time.time()) + '/')

    def Reset(self, empty_request, context):
        observation = self.env.reset()
        observation_pb = gym_uds_pb2.Observation(data=observation.ravel(), shape=observation.shape)
        return gym_uds_pb2.State(observation=observation_pb, reward=0.0, done=False)

    def Step(self, action_request, context):
        action_np = np.asarray(action_request.data)
        # print(action_np)
        observation, reward, done, _ = self.env.step(action_np)
        assert type(observation) is np.ndarray

        observation_pb = gym_uds_pb2.Observation(data=observation.ravel(), shape=observation.shape)
        return gym_uds_pb2.State(observation=observation_pb, reward=reward, done=done)

    def Sample(self, empty_request, context):
        action = self.env.action_space.sample()
        return gym_uds_pb2.Action(data=action)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('id', help='the id of the gym environment to simulate')
    parser.add_argument(
        'filepath',
        nargs='?',
        default='unix:///tmp/gym-uds-socket',
        help='a unique filepath where the server will bind')
    args = parser.parse_args()

    try:
        os.remove(args.filepath)
    except FileNotFoundError:
        pass

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    gym_uds_pb2_grpc.add_EnvironmentServicer_to_server(Environment(args.id), server)
    server.add_insecure_port(args.filepath)
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)
