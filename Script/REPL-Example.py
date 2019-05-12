import gym
from gym import wrappers
from time import time
env = wrappers.Monitor(gym.make('MountainCarContinuous-v0'), './videos/' + str(time()) + '/')
try :
    for i_episode in range(1):
        observation = env.reset()
        for t in range(100):
            # env.render()
            print(observation)
            action = env.action_space.sample()
            print (action)
            observation, reward, done, info = env.step(action)
            if done:
                print("Episode finished after {} timesteps".format(t+1))
                break
finally:
    env.close()
    
    
import gym, roboschool
import numpy as np
# env = gym.make('MountainCarContinuous-v0')
# env = gym.make('MountainCar-v0')
# env = gym.make('ReversedAddition3-v0')
# env = gym.make('Acrobot-v1')
# env = gym.make('NChain-v0')
# env = gym.make('DuplicatedInput-v0')
# env = gym.make('Reverse-v0')
env = gym.make('RoboschoolAnt-v1')

observation = env.reset()
for t in range(100):
    # env.render()
    action = env.action_space.sample()
    print("Execution: " + str(t))
    print ("Action: " + str(action))
    observation, reward, done, info = env.step(action)
    # print("Observation: " + str(observation))
    print("Reward: " + str(reward))
    print("--------")
    if done:
        print("Episode finished after {} timesteps".format(t+1))
        break
        
env.close()

import gym
import numpy as np
# env = gym.make('Taxi-v2')
# env = gym.make('FrozenLake-v0')
#env = gym.make('Blackjack-v0')
env = gym.make('DuplicatedInput-v0')
# obs = env.reset()
env.reset()
env.render()
env.step(1)