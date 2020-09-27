import numpy as np
from collections import defaultdict
import random

class Node:

    def __init__(self, state, parent = None):
        self.state = state
        self.parent = parent
        self.neighboors = list()
        self.times_visited = 0
        self._untried_actions = None
        self.results = defaultdict(int)
        
    @property
    def untried_actions(self):
        if self._untried_actions is None:
            self._untried_actions = self.state.get_actions(limit=5)
        return self._untried_actions

    @property
    def q(self):
        wins = self.results[self.parent.state.next_to_move]
        loses = self.results[-1*self.parent.state.next_to_move]
        return wins-loses
    @property
    def n(self):
        return self.times_visited

    def random_select(self):
        amount = len(self.untried_actions)
        if amount > 0:
            return random.randint(0,amount-1)
        return None

    def expand(self):
        item = self.random_select()
        action = self.untried_actions.pop(item)
        next_state = self.state.transition(action)
        child = Node(next_state, parent=self)
        self.neighboors.append(child)
        return child

    def is_terminal_node(self):
        return self.state.game_over()

    def is_fully_expanded(self):
        return len(self.untried_actions) == 0

    def best_child(self, c_param=1.4):
        choices_weights = [
            (c.q / c.n) + c_param * np.sqrt((2 * np.log(self.n) / c.n))
            for c in self.neighboors
        ]
        return self.neighboors[np.argmax(choices_weights)]

    def rollout_policy(self, possible_moves):        
        return possible_moves[np.random.randint(len(possible_moves))]

    def rollout(self):
        current_rollout_state = self.state
        while not current_rollout_state.game_over():
            possible_moves = current_rollout_state.get_actions()
            action = self.rollout_policy(possible_moves)
            current_rollout_state = current_rollout_state.transition(action)
        return current_rollout_state.winner

    def backpropagate(self, result):
        self.times_visited +=1
        self.results[result]+=1
        if self.parent:
            self.parent.backpropagate(result)

class MonteCarloTreeSearch:

    def __init__(self, node):
        self.root = node

    def best_action(self, simulations_number):
        for _ in range(0, simulations_number):            
            v = self._tree_policy()
            reward = v.rollout()
            v.backpropagate(reward)
        return self.root.best_child(c_param=0.)

    def _tree_policy(self):
        current_node = self.root
        while not current_node.is_terminal_node():
            if not current_node.is_fully_expanded():
                return current_node.expand()
            else:
                current_node = current_node.best_child()
        return current_node