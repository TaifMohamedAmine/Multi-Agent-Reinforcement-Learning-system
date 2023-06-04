import numpy as np
import random 
import itertools
from Agent import Agent
from process_input import Input

"""
In this file we implement the environment of our game
"""

class Environment :
    '''
    environement class where we create the env where the agents interact
    '''
    def __init__(self, grid_length , grid_width, num_agents, image_path, extra_padding):
        
        # the number of agents in the env
        self.num_agents = num_agents 
        
        # the size of the game env
        self.grid_length, self.grid_width = grid_length, grid_width

        # list of the env agents
        self.agents = [] 
        
        # Let's instanciate our image processing class  : 
        input_instance = Input(image_path, reward=100, sanction=-0.1, intermediate=5, extra_padding=extra_padding)

        
        # we extract the reward list from the image we processed 
        self.reward_list = input_instance.reward_grid()
        """print(self.reward_list)
        raise Exception("s")"""
        
        # we select the target positions 
        self.target_pos = []
        for i in range(len(self.reward_list)):
            for j in range(len(self.reward_list[0])):
                if self.reward_list[i][j][1]:
                    self.target_pos.append([i, j])

        
        # randomly scatter my agents in the grid
        iter_list = list(range(self.grid_length))
        comb = itertools.product(iter_list, repeat = 2) 
        comb_list = [list(item) for item in comb if list(item) not in self.target_pos] # all possible int positions in our grid     

        #print(len(self.target_pos), len([list(item) for item in comb]), len(comb_list))
        #print(comb_list)
        print(len(comb_list))
        for i in range(self.num_agents) :
            position = random.choice(comb_list)
            comb_list.remove(position)
            agent = Agent(position)
            self.agents.append(agent) # add the agent to the list of agents with pos (x,y) and id = agent_id


        # Let's define our actions :
        self.actions = {

            'UP':[0, 1],   # increase y by 1
            'DOWN':[0, -1], # decrease y by 1
            'RIGHT':[1, 0], # increase x by 1
            'LEFT':[-1, 0],# decrease x by 1
            'STOP':[0, 0] # stay still in same place

        } 

        self.reached_targets = all([agent.reached_end_state for agent in self.agents])


    """
    'NORTH EAST':[-1, 1], # move diagonnaly up east
            'NORTH WEST':[-1, -1], # move diagonnaly up west
            'SOUTH EAST':[1, 1], # move diagonnaly down east
            'SOUTH WEST':[1, -1] # move diagonnaly down west
    """


    def reset_env(self):
        """
        this method is important in IQL algo, in order to explore all different initiale states
        """
        iter_list = list(range(self.grid_length))
        comb = itertools.permutations(iter_list, 2) 
        comb_list = [list(item) for item in comb if list(item) not in self.target_pos] # all possible int positions in our grid    

        for agent in self.agents :
            position = random.choice(comb_list)
            comb_list.remove(position)
            agent.pos = position # the agent's position is initialized to a random positin
            agent.action = [0, 0]
            agent.next_state = 0
            agent.reached_end_state = False



    def update_env(self):
        '''
        this function updates the environement following a policy. 
        '''
        for agent in self.agents : 
            if not agent.reached_end_state :
                agent.move()


    def check_target(self):
        tst_var= 0
        for agent in self.agents : 
            if agent.reached_end_state : 
                tst_var += 1 
        
        print(f"{tst_var} reached target out of {self.num_agents}")
        