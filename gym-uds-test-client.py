#!/usr/bin/env python3
import argparse

import grpc
import gym_uds_pb2
import gym_uds_pb2_grpc
import numpy as np


class EnvironmentClient:
    def __init__(self, sock_filepath):
        channel = grpc.insecure_channel(sock_filepath)
        self.stub = gym_uds_pb2_grpc.EnvironmentStub(channel)
        self.action_space = lambda: None
        self.action_space.sample = self.sample

    def reset(self):
        state_pb = self.stub.Reset(gym_uds_pb2.Empty())
        observation = np.asarray(state_pb.observation.data).reshape(state_pb.observation.shape)
        return observation

    def step(self, action):
        state_pb = self.stub.Step(gym_uds_pb2.Action(data=action))
        observation = np.asarray(state_pb.observation.data).reshape(state_pb.observation.shape)
        return observation, state_pb.reward, state_pb.done, state_pb.envID

    def sample(self):
        action_pb = self.stub.Sample(gym_uds_pb2.Empty())
        return action_pb.data


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'filepath',
        nargs='?',
        default='unix:///tmp/gym-uds-socket',
        help='a unique filepath where the client will connect')
    args = parser.parse_args()

    env = EnvironmentClient(args.filepath)
    envID = ""
    num_episodes = 3
    for episode in range(1, num_episodes + 1):
        observation = env.reset()

        episode_reward = 0
        done = False
        while not done:
            action = env.action_space.sample()
            observation, reward, done, envID = env.step(action)
            episode_reward += reward
        print('Env: %s, Ep. %d: %.2f' % (envID, episode, episode_reward))
