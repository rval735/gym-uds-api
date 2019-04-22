# gym-uds-api
This project provides a local [Unix domain socket](https://en.wikipedia.org/wiki/Unix_domain_socket) API to the [OpenAI Gym](https://github.com/openai/gym) toolkit, allowing development in languages other than Python with a faster inter-process communication than the [gym-http-api](https://github.com/openai/gym-http-api).

The API comes with a C++ binding example which supports multi dimensional observation and action spaces of type `Discrete` and `Box`.

## Requisites
The code requires the `gym` package for Python 3 and any recent version of [gRPC](https://grpc.io/).

## Installation
1. Clone or download this repository
2. Run `./build.sh` to generate the necessary gRPC headers and sources

## Usage
1. Start the server:
```
/o/gym-uds-api $ python3 ./gym-uds-server.py MountainCar-v0
```
2. Run the (useless, for testing only) Python client or the C++ client:
```
/o/gym-uds-api $ python3 ./gym-uds-test-client.py
Ep. 1: 15.00
Ep. 2: 12.00
Ep. 3: 20.00
```

In order to run the C++ client, remember to run ```build.sh```, then to run ```make``` inside the folder "binding-cpp".
If for some reason it does not compile (ex. Linux), it is possible to run ```make``` inside "src" to compile everything
within that folder.

```
/o/g/binding-cpp $ make
mkdir -p bin
c++ -std=c++11 -O2 -o bin/gym-uds-client -I include -L/usr/local/lib `pkg-config --libs protobuf grpc++ grpc` -lgrpc++_reflection -ldl src/*.cc
/o/g/binding-cpp $ bin/gym-uds-client
Ep. 1: 12
Ep. 2: 21
Ep. 3: 21
```

## Tested environments:

MountainCar-v0
https://gym.openai.com/envs/MountainCar-v0/

Copy-v0
https://gym.openai.com/envs/Copy-v0/

DuplicatedInput-v0
https://gym.openai.com/envs/DuplicatedInput-v0/

Roulette-v0
https://gym.openai.com/envs/Roulette-v0/

NChain-v0
https://gym.openai.com/envs/NChain-v0/

If you would like to extend support to other environments, here is the official list all of them:
https://github.com/openai/gym/wiki/Table-of-environments