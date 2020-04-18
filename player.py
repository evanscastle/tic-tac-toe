import numpy as np
import pickle
import math

class Player:
    def __init__(self, name="default", num_episodes=1000):
        self.name = name

        self.exploration_rate = 0.3
        self.learning_rate = 0.1
        self.discount_factor = 0.9

        self.decay_rate = math.e**(math.log(0.001)/num_episodes)

        self.move_penalty = -0.05 # slight negative reward to incentivize agent to win as quickly as possible
        self.episode_states = []
        self.state_space = {}

    def chooseMove(self, board):
        moves = board.getMoves()
        assert len(moves) > 0

        if np.random.uniform(0, 1) <= self.exploration_rate:
            # take random action
            index = np.random.choice(len(moves))
            move = moves[index]

        else:
            # first value will always be greater than value_max
            value_max = float("-inf")

            for mv in moves:
                # represent current state
                board_copy = board.copy()

                board_copy.makeMove(mv)
                possible_move = board_copy.getHash()

                # if a state has not been visited before, set its value to zero
                if self.state_space.get(possible_move) is None:
                    value = self.move_penalty
                else:
                    value = self.state_space[possible_move]

                # act greedily based on value of move
                if value > value_max:
                    value_max = value
                    move = mv

        board_copy = board.copy()
        board_copy.makeMove(move)
        state = board_copy.getHash()

        self.episode_states.append(state)
        return move

    # perform modified value iteration based on experience from episode
    def updateValues(self, result):
        # determine the value of the final state based on outcome of the game
        if result == 'win':
            next_state_val = 1
        elif result == 'loss':
            next_state_val = -1
        elif result == 'tie':
            next_state_val = 0.1
        else:
            raise ValueError('Result not understood')

        for state in reversed(self.episode_states):
            # If state is not in dictionary, add it and initialize value to a small negative value. This
            # encourages the network to win quickly
            if self.state_space.get(state) is None:
                self.state_space[state] = self.move_penalty

            # V(S_k) <- V(S_k) + a[V(S_k+1) - V(S_k)]
            # this is modified policy iteration because we are not updating the value based on all adjacent states
            # but only those that are visited during the episode
            self.state_space[state] += self.learning_rate*(next_state_val - self.state_space[state])

            next_state_val = self.state_space[state]

        # want agent to gradually become more confident in decisions
        self.exploration_rate = self.decay_rate * self.exploration_rate
        self.learning_rate = self.decay_rate * self.learning_rate

    def saveStates(self):
        fw = open('agents/policy_' + str(self.name) + '.pkl', 'wb')
        pickle.dump(self.state_space, fw)
        fw.close()

    def loadStates(self, filename):
        fr = open(filename, 'rb')
        self.state_space = pickle.load(fr)
        fr.close()











