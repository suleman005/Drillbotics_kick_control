import matplotlib.pyplot as plt
from collections import deque
from opcua import Client
from dwis import *
import matplotlib.animation as animation

def plot_parameters(selected_parameters):
    X = deque(maxlen=1000)
    X.append(1)

    Y = {}
    for parameter in selected_parameters:
        name = parameter[0]
        Y[name] = deque(maxlen=1000)
        Y[name].append(1)

    fig, axs = plt.subplots(len(selected_parameters), 1, figsize=(10, 6))

    def update_graph_scatter(n):
        X.appendleft(X[0] - 1)

        for parameter in selected_parameters:
            parameter_name = parameter[0]
            value = eval(parameter[1])
            Y[parameter_name].append(value)

        for i, parameter in enumerate(selected_parameters):
            parameter_name = parameter[0]
            axs[i].cla()
            axs[i].plot(list(X), list(Y[parameter_name]), label=parameter_name)
            axs[i].set_ylabel(parameter_name)

        plt.tight_layout()

    ani = animation.FuncAnimation(fig, update_graph_scatter, interval=1000)

    plt.show()

if __name__ == '__main__':
    selected_parameters = [
        pit_volume,
        bit_depth,
        BOP_ChokeOpening,
        BOP_ChokePressure,
        MPD_ChokeOpening,
        MPD_ChokePressure,
        ECD_Downhole,
        Pressure_Downhole,
        Pressure_Downhole_WP,
        FLowRateIn,
        FLowRateOut,
        FLowRateOut_Gas
    ]

    plot_parameters(selected_parameters)
