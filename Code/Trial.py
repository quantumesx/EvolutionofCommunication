"""Run a single trial."""

from Agent import agent
from Environment import environment
from Controller import controller
from Helper import find_dx, find_dy, get_distance

from tqdm import tqdm
from matplotlib import pyplot as plt
from matplotlib.patches import Circle, FancyArrow
import random as rd


class experiment():
    """Run an experiment."""

    def __init__(self,
                 pop=100,
                 gen=100,
                 genome_size=39,  # need to change this
                 iteration=1000,
                 time=0.1,
                 preset='M&N, 2003',
                 env_height=270, env_width=270, targets=True,
                 trial=20
                 ):
        """Initialize the experiment."""
        self.pop = pop  # population size
        self.gen = gen  # total # of generations to run
        self.trial = 20  # trial to run for each group in the population

        self.genome_size = genome_size
        self.genome = []  # [[g1p1, g1p2, ...], [g2p1, g2p2, ...], ...]
        self.fitness = []  # [[g1p1, g1p2, ...], [g2p1, g2p2, ...], ...]
        self.top = []

    def run(self):
        """Run experiment."""
        # initialize random genome for the first generation
        first_gen = []
        for p in range(self.pop):
            genome = rd.choices(range(0, 255), k=self.genome_size)
            first_gen.append(genome)
        self.genome.append(first_gen)

        for g in range(self.gen):
            pop_fitness = []

            # run the entire population
            for p in range(self.pop):
                genome = self.genome[g][p]

                ann = controller(self.genome)
                total_fit = []  # fitness of the trials
                for i in self.trial:
                    t = trial(ann, name='g{}p{}i{}'.format(g, p, i))
                    t.run()
                    total_fit.append(sum(t.fitness))
                fitness = sum(total_fit) / self.trial
                pop_fitness.append(fitness)

            # update
            self.fitness.append(pop_fitness)

            # select 20 best performing teams
            index = []
            for i in range(self.pop):
                index.append(self.genome[g][i], self.fitness[g][i])

            def get_key(item):
                return item[1]

            top_genome = [g[0] for g in sorted(index, key=get_key,
                                               reverse=True)[:5]]
            self.top.append(top_genome)

            # get genome for next generation
            next_genome = []
            for g in top_genome:
                for i in range(self.pop/5):
                    # need to change this
                    next_genome.append(g)
            self.genome


class trial():
    """Run a single trial."""

    def __init__(self,
                 ann,
                 iteration=1000,
                 time=0.1,
                 name='unnamed_trial',
                 preset='M&N, 2003',
                 env_height=270, env_width=270, targets=True,
                 verbose=False
                 ):
        """Initialize a trial."""
        super().__init__()
        self.name = name  # name for the trial
        self.preset = preset  # preset name
        self.iteration = iteration  # total numbers of iterations
        self.step_time = 0.1  # time for each iteration step in seconds
        self.fitness = []  # fitness at each timestep
        # initialize environment
        self.env = environment(width=env_width, height=env_height,
                               targets=targets)

        # the same ann used for this trial
        self.ann = ann

        # initialize agents for the trial
        self.env.agents = [
            agent(name=self.name+'agent0', color='red'),
            agent(name=self.name+'agent1', color='orange'),
            agent(name=self.name+'agent2', color='cyan'),
            agent(name=self.name+'agent3', color='green')
            ]

        for a in self.env.agents:
            a.randomize_position(self.env)
            a.loc_data = []
            a.ang_data = []
            a.input_data = []
            a.output_data = []
            a.ann = self.ann

        # validate the environment
        if verbose:
            self.env.show()

    def run(self):
        """Run trial."""
        self.fitness = []
        for i in tqdm(range(self.iteration)):
            # iterate through agents
            for a in self.env.agents:
                # store current location and sensor data
                a.loc_data.append(a.loc)
                a.ang_data.append(a.ang)

                # store current fitness score

                # first get all sensor data
                a.get_ground_reading(self.env)
                a.get_ir_readings(self.env)
                a.get_comm_readings(self.env)
                a.comm_self_reading = a.comm_output

                # then get outputs
                # updates left_output, right_output, comm_output
                a.get_output()

                # store current sensor and actuator data
                a.input_data.append(a.ann.input_activation)
                a.output_data.append(a.ann.output_activation)

                # finally, get new location
                a.update_loc(self.env)
                # this updates loc and ang
                # so essential to store current data before this
            self.fitness.append(self.get_step_fitness(self.env.agents))
        self.data = []
        for a in self.env.agents:
            self.data.append(
                [a.loc_data, a.ang_data, a.input_data, a.output_data]
            )

    def get_step_fitness(self, agents):
        """Get fitness of a trial."""
        target1 = self.env.targets[0]
        target2 = self.env.targets[1]

        t1 = 0
        t2 = 0
        for a in agents:
            d1 = get_distance(target1[0], a.loc)
            d2 = get_distance(target2[0], a.loc)
            if d1 < target1[1] + a.r:
                t1 += 1
            if d2 < target2[1] + a.r:
                t2 += 1

        score = 0
        for t in [t1, t2]:
            if t <= 2:
                score += 0.25 * t
            else:
                score += 0.5
                score -= 1 * t - 2

        return score

    def show(self):
        """Plot out the trial."""
        ax = plt.axes(xlim=(-30, 300), ylim=(-30, 300))
        line, = ax.plot([], [])

        ax.add_patch(FancyArrow(0, 0, 300, 0, color='black'))
        ax.add_patch(FancyArrow(0, 0, 0, 300, color='black'))
        ax.add_patch(FancyArrow(270, 270, 0, -300, color='black'))
        ax.add_patch(FancyArrow(270, 270, -300, 0, color='black'))

        # add targets
        for target in self.env.targets:
            ax.add_patch(Circle(target[0], target[1], color='gray'))

        for a in self.env.agents:
            for i in range(self.iteration):
                ax.add_patch(Circle(a.loc_data[-i], a.r, color=a.color))
                ax.add_patch(FancyArrow(a.loc_data[-i][0], a.loc_data[-i][1],
                                        find_dx(a.loc_data[-i][0],
                                                a.ang_data[-i], a.r),
                                        find_dy(a.loc_data[-i][1],
                                                a.ang_data[-i], a.r),
                                        color='black',
                                        length_includes_head=True,
                                        head_width=0.2))

        ax.set_aspect('equal')
        ax.figure.set_size_inches(6, 6)
