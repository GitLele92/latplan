
import numpy as np
from .model.hanoi import generate_configs, successors, config_state, state_config

patterns = [
    [[0,0,0,0,0,0,0,0,],
     [0,0,0,0,0,0,0,0,],
     [0,0,0,0,0,0,0,0,],
     [0,0,0,0,0,0,0,0,],
     [0,0,0,0,0,0,0,0,],
     [0,0,0,0,0,0,0,0,],
     [0,0,0,0,0,0,0,0,],
     [0,0,0,0,0,0,0,0,],],
    [[1,1,0,0,1,1,0,0,],
     [1,1,0,0,1,1,0,0,],
     [0,0,1,1,0,0,1,1,],
     [0,0,1,1,0,0,1,1,],
     [1,1,0,0,1,1,0,0,],
     [1,1,0,0,1,1,0,0,],
     [0,0,1,1,0,0,1,1,],
     [0,0,1,1,0,0,1,1,],],
    [[1,0,0,0,1,0,0,0,],
     [0,1,0,0,0,1,0,0,],
     [0,0,1,0,0,0,1,0,],
     [0,0,0,1,0,0,0,1,],
     [1,0,0,0,1,0,0,0,],
     [0,1,0,0,0,1,0,0,],
     [0,0,1,0,0,0,1,0,],
     [0,0,0,1,0,0,0,1,],],
    [[0,0,0,0,0,0,0,0,],
     [0,1,1,1,0,0,0,0,],
     [0,1,1,1,0,0,0,0,],
     [0,1,1,1,0,0,0,0,],
     [0,0,0,0,1,1,1,0,],
     [0,0,0,0,1,1,1,0,],
     [0,0,0,0,1,1,1,0,],
     [0,0,0,0,0,0,0,0,],],
    [[0,0,0,1,0,0,0,1,],
     [0,0,1,0,0,0,1,0,],
     [0,1,0,0,0,1,0,0,],
     [1,0,0,0,1,0,0,0,],
     [0,0,0,1,0,0,0,1,],
     [0,0,1,0,0,0,1,0,],
     [0,1,0,0,0,1,0,0,],
     [1,0,0,0,1,0,0,0,],],
    [[0,0,0,1,1,0,0,0,],
     [0,0,1,0,0,1,0,0,],
     [0,1,0,0,0,0,1,0,],
     [1,0,0,0,0,0,0,1,],
     [0,0,0,1,1,0,0,0,],
     [0,0,1,0,0,1,0,0,],
     [0,1,0,0,0,0,1,0,],
     [1,0,0,0,0,0,0,1,],],
    [[1,0,0,0,0,0,0,1,],
     [0,1,0,0,0,0,1,0,],
     [0,0,1,0,0,1,0,0,],
     [0,0,0,1,1,0,0,0,],
     [1,0,0,0,0,0,0,1,],
     [0,1,0,0,0,0,1,0,],
     [0,0,1,0,0,1,0,0,],
     [0,0,0,1,1,0,0,0,],],
    [[0,0,0,0,0,0,0,0,],
     [0,0,0,0,1,1,1,0,],
     [0,0,0,0,1,0,1,0,],
     [0,0,0,0,1,1,1,0,],
     [0,1,1,1,0,0,0,0,],
     [0,1,0,1,0,0,0,0,],
     [0,1,1,1,0,0,0,0,],
     [0,0,0,0,0,0,0,0,],],
    [[1,0,0,0,1,0,0,0,],
     [1,0,0,0,1,0,0,0,],
     [0,1,0,0,0,1,0,0,],
     [0,1,0,0,0,1,0,0,],
     [0,0,1,0,0,0,1,0,],
     [0,0,1,0,0,0,1,0,],
     [0,0,0,1,0,0,0,1,],
     [0,0,0,1,0,0,0,1,],],
    [[0,0,0,1,0,0,0,1,],
     [0,0,0,1,0,0,0,1,],
     [0,0,1,0,0,0,1,0,],
     [0,0,1,0,0,0,1,0,],
     [0,1,0,0,0,1,0,0,],
     [0,1,0,0,0,1,0,0,],
     [1,0,0,0,1,0,0,0,],
     [1,0,0,0,1,0,0,0,],],
    [[1,0,1,0,1,0,1,0,],
     [1,0,1,0,1,0,1,0,],
     [1,0,1,0,1,0,1,0,],
     [1,0,1,0,1,0,1,0,],
     [1,0,1,0,1,0,1,0,],
     [1,0,1,0,1,0,1,0,],
     [1,0,1,0,1,0,1,0,],
     [1,0,1,0,1,0,1,0,],],
    [[1,1,1,1,1,1,1,1,],
     [0,0,0,0,0,0,0,0,],
     [1,1,1,1,1,1,1,1,],
     [0,0,0,0,0,0,0,0,],
     [1,1,1,1,1,1,1,1,],
     [0,0,0,0,0,0,0,0,],
     [1,1,1,1,1,1,1,1,],
     [0,0,0,0,0,0,0,0,],],
    [[0,0,0,0,0,0,0,0,],
     [0,0,0,0,0,0,0,0,],
     [1,1,1,1,1,1,1,1,],
     [1,1,1,1,1,1,1,1,],
     [1,1,1,1,1,1,1,1,],
     [1,1,1,1,1,1,1,1,],
     [0,0,0,0,0,0,0,0,],
     [0,0,0,0,0,0,0,0,],],
    [[0,0,1,1,1,1,0,0,],
     [0,0,1,1,1,1,0,0,],
     [0,0,1,1,1,1,0,0,],
     [0,0,1,1,1,1,0,0,],
     [0,0,1,1,1,1,0,0,],
     [0,0,1,1,1,1,0,0,],
     [0,0,1,1,1,1,0,0,],
     [0,0,1,1,1,1,0,0,],],
]

patterns = np.array(patterns)

def generate1(config):
    l = len(config)
    disk_size = 8
    disk_inc = disk_size // 2
    disk_height = disk_size
    base_disk_width_factor = 2
    base_disk_width = disk_size * base_disk_width_factor
    figure = np.ones([l*disk_height,(l*2*disk_inc+base_disk_width)*3+2],dtype=np.int8)
    state = config_state(config)
    # print(l,figure.shape)
    # print(config)
    # print(state)
    for i, tower in enumerate(state):
        tower.reverse()
        # print(i,tower)
        x_left  = (l*2*disk_inc+base_disk_width)*i     +   i
        x_right = (l*2*disk_inc+base_disk_width)*(i+1) + (i+1) - 1
        for j,disk in enumerate(tower):
            # print(j,disk,(l-j)*2)
            figure[
                (l-j-1)*disk_height:(l-j)*disk_height,
                x_left + (l-disk)*disk_inc : x_right - (l-disk)*disk_inc] \
                = 0
                # = np.tile(patterns[disk],(1,disk+base_disk_width_factor))
    return figure

def generate(configs):
    return np.array([ generate1(c) for c in configs ])
                

def states(size, configs=None):
    if configs is None:
        configs = generate_configs(size)
    return generate(configs)

def transitions(size, configs=None, one_per_state=False):
    if configs is None:
        configs = generate_configs(size)
    if one_per_state:
        def pickone(thing):
            index = np.random.randint(0,len(thing))
            return thing[index]
        transitions = np.array([
            generate([c1,pickone(successors(c1))])
            for c1 in configs ])
    else:
        transitions = np.array([ generate([c1,c2])
                                 for c1 in configs for c2 in successors(c1) ])
    return np.einsum('ab...->ba...',transitions)

