#include <iostream>
#include <algorithm>
#include <string>
#include <vector>
#include <cstdlib>
#include <cstdio>
#include <sys/socket.h>
#include <sys/un.h>
#include <unistd.h>

#include "gym.h"

#include "gym.pb.h"


namespace gym
{
template<typename T>
T Environment::recv_message()
{
    char buf[1024];
    int nread;

    nread = read(sock, buf, 1);
    const auto message_pb_len = buf[0];

    nread = read(sock, buf, message_pb_len);
    std::string message_pb(buf, nread);

    T message;
    if (!message.ParseFromString(message_pb)) {
        std::cerr << "Failed to parse message." << std::endl;
        std::exit(1);
    }
    return message;
}

template<typename T>
void Environment::send_message(const T& message)
{
    std::string message_pb;
    if (!message.SerializeToString(&message_pb)) {
        std::cerr << "Failed to write message." << std::endl;
        std::exit(1);
    }

    int nwrite;
    const char message_pb_len = message_pb.size();
    nwrite = write(sock, &message_pb_len, 1);
    nwrite = write(sock, message_pb.c_str(), message_pb.size());
}


Environment::Environment(const std::string& socket_filepath)
{
    struct sockaddr_un server_addr = {};
    server_addr.sun_len = sizeof server_addr;
    server_addr.sun_family = AF_UNIX;
    std::strncpy(server_addr.sun_path, socket_filepath.c_str(), sizeof server_addr.sun_path);

    sock = socket(AF_UNIX, SOCK_STREAM, 0);
    if (sock < 0) { std::perror("gym::Environment::socket"); std::exit(1); }
    conn = connect(sock, (const struct sockaddr *)&server_addr, sizeof server_addr);
    if (conn < 0) { std::perror("gym::Environment::connect"); std::exit(1); }
}


observation_t Environment::reset()
{
    Request request;
    request.set_type(Request::RESET);
    send_message<Request>(request);

    State state = recv_message<State>();
    auto observation = std::vector<float>();
    std::copy_n(state.observation().begin(), state.observation().size(), std::back_inserter(observation));
    return observation;
}

state_t Environment::step(const action_t& action_value)
{
    Request request;
    request.set_type(Request::STEP);
    send_message<Request>(request);

    Action action;
    action.set_value(action_value);
    send_message<Action>(action);

    State state = recv_message<State>();
    auto observation = std::vector<float>();
    std::copy_n(state.observation().begin(), state.observation().size(), std::back_inserter(observation));
    return {observation, state.reward(), state.done()};
}


action_t Environment::sample()
{
    Request request;
    request.set_type(Request::SAMPLE);
    send_message<Request>(request);

    Action action = recv_message<Action>();
    return action.value();
}
}
