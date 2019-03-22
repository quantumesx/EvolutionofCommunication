"""
The controller module.

Functions:
1. Creating a network
2. Updating weights of a network
3.
"""

import random as rd
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.patches import Circle, FancyArrow


class controller():
    """Generate a controller."""

    def __init__(self, i=14, h=8, o=3, debug=False):  # input, hiddent, output
        """
        Initialize a network.

        Arguments:
        i = number of input nodes
        h = number of hidden nodes
        o = number of output nodes
        """
        super().__init__()
        # initialize nodes
        self.i = i  # number of input nodes
        self.h = h  # number of hidden nodes
        self.o = o  # number of output nodes

        self.input_activation = [0]*i  # activation of input nodes
        self.input_bias = [0]*i  # bias of input nodes

        self.hidden_activation = [0]*h  # activation of hidden nodes
        self.hidden_bias = [0]*h  # bias of hidden nodes

        self.output_activation = [0]*o  # activation of output nodes
        self.output_bias = [0]*o  # bias of output nodes

        self.i2h_weights = [[0]*i]*h
        self.h2o_weights = [[0]*h]*o

        # Order of calculation:
        # First iterate through receiving nodes,
        # Then for each receiving node iterate through activated nodes
        # E.g.:
        # All input nodes->hidden 1; all input nodes->hidden 2; ...
        # Therefore the weights are formated correspondingly as:
        # [
        #   [input1-hidden1, input2-hidden1, ...],
        #   [all inputs to hidden2], ...
        # ]

    def initialize_random_weights(self):
        """
        Initialize weights with random values.

        The random values are drawn from uniform distribution (-1, 1).
        """
        # initialize weights (random values from uniform distribution (-1, 1))
        self.i2h_weights = []
        for i in range(self.h):
            w = []
            for j in range(self.i):
                w.append(rd.uniform(-1, 1))
            self.i2h_weights.append(w)

        self.h2o_weights = []
        for i in range(self.o):
            w = []
            for j in range(self.h):
                w.append(rd.uniform(-1, 1))
            self.h2o_weights.append(w)

    def initialize_random_bias(self):
        """
        Initialize biases with random values.

        The random values are drawn from uniform distribution (-1, 1).
        """
        self.input_bias = []
        for i in range(self.i):
            self.input_bias.append(rd.uniform(-1, 1))

        self.hidden_bias = []
        for i in range(self.h):
            self.hidden_bias.append(rd.uniform(-1, 1))

        self.output_bias = []
        for i in range(self.o):
            self.output_bias.append(rd.uniform(-1, 1))

    def feedforward(self):
        """Perform feedforward computation."""
        for i in range(len(self.hidden)):
            h_raw = []
            for j in range(len(self.input)):
                h_raw.append(self.input[j]*self.i2h_weights[i][j])
            # currently use tanh as activation function
            self.hidden[i] = np.tanh(sum(h_raw))
        # print(self.hidden)

        for i in range(len(self.output)):
            o_raw = []
            for j in range(len(self.hidden)):
                o_raw.append(self.hidden[j]*self.h2o_weights[i][j])
            # currently use tanh as activation function
            self.output[i] = np.tanh(sum(o_raw))

    def mutate(self, rate=0.2):
        """Mutate weight and biases in a network."""
        # mutate input bias
        new_input_bias = []
        for i in range(self.i):
            if rd.uniform(0, 1) >= rate:
                new_input_bias.append(self.input_bias[i])
            else:
                new_input_bias.append(rd.uniform(-1, 1))
        self.input_bias = new_input_bias

        # mutate hidden bias
        new_hidden_bias = []
        for i in range(self.h):
            if rd.uniform(0, 1) >= rate:
                new_hidden_bias.append(self.hidden_bias[i])
            else:
                new_hidden_bias.append(rd.uniform(-1, 1))
        self.hidden_bias = new_hidden_bias

        # mutate output bias
        new_output_bias = []
        for i in range(self.o):
            if rd.uniform(0, 1) >= rate:
                new_output_bias.append(self.output_bias[i])
            else:
                new_output_bias.append(rd.uniform(-1, 1))
        self.output_bias = new_output_bias

        # mutate input to hideen weights
        new_i2h_weights = []
        for h in range(self.h):
            weights = []
            for i in range(self.i):
                if rd.uniform(0, 1) >= rate:
                    weights.append(self.i2h_weights[h][i])
                else:
                    weights.append(rd.uniform(-1, 1))
            new_i2h_weights.append(weights)
        self.i2h_weights = new_i2h_weights

        # mutate hideen to output weights
        new_h2o_weights = []
        for o in range(self.o):
            weights = []
            for h in range(self.h):
                if rd.uniform(0, 1) >= rate:
                    weights.append(self.h2o_weights[o][h])
                else:
                    weights.append(rd.uniform(-1, 1))
            new_h2o_weights.append(weights)
        self.h2o_weights = new_h2o_weights

        print('All mutated')

    def show(self):
        """Show network."""
        ax = plt.axes(xlim=(0, max(self.i, self.h, self.o)*25 + 25),
                      ylim=(0, 200))
        line, = ax.plot([], [])
        ax.set_aspect('equal')
        ax.figure.set_size_inches(5, 2)

        i_nodes = []
        h_nodes = []
        o_nodes = []

        x = 25
        y = 150
        for t in range(self.i):
            ax.add_patch(Circle((x, y), 10, color='green'))
            i_nodes.append((x, y))
            x += 25

        y -= 50
        x = (max(self.i, self.h, self.o)-self.h)/2 * 25 + 25
        for t in range(self.h):
            ax.add_patch(Circle((x, y), 10, color='purple'))
            h_nodes.append((x, y))
            x += 25

        y -= 50
        x = (max(self.i, self.h, self.o)-self.o)/2 * 25 + 25
        for t in range(self.o):
            ax.add_patch(Circle((x, y), 10, color='blue'))
            o_nodes.append((x, y))
            x += 25

        for t in i_nodes:
            for j in h_nodes:
                ax.add_patch(FancyArrow(t[0], t[1],
                                        j[0]-t[0], j[1]-t[1],
                                        width=0.00000001,
                                        color='black',
                                        length_includes_head=True,
                                        head_width=3))
        for t in h_nodes:
            for j in o_nodes:
                ax.add_patch(FancyArrow(t[0], t[1],
                                        j[0]-t[0], j[1]-t[1],
                                        width=0.00000001,
                                        color='black',
                                        length_includes_head=True,
                                        head_width=3))