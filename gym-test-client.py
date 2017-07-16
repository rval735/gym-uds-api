#!/usr/bin/env python3
import socket

import gym_pb2


def recv_state():
    state_pb = sock.recv(int.from_bytes(sock.recv(1), byteorder='little'))
    state = gym_pb2.State()
    state.ParseFromString(state_pb)
    return state.value, state.reward, state.done


def send_action(action):
    action_pb = gym_pb2.Action(value=action).SerializeToString()
    sock.sendall(len(action_pb).to_bytes(1, byteorder='little') + action_pb)


if __name__ == '__main__':
    socket_filepath = '/tmp/gym-server-socket'

    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sock.connect(socket_filepath)

    observation, _, _ = recv_state()

    done = False
    while not done:
        send_action(0)
        observation, reward, done = recv_state()
        print(observation, reward, done)
