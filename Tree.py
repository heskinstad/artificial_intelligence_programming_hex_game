import math
import time

import numpy as np
from matplotlib import pyplot as plt

# A tree is constructed per game. All nodes must be part of a tree
class Tree:
    def __init__(self, top_node):
        self.top = top_node

    def get_top_node(self):
        return self.top

    def print_all_nodes_as_boards(self):
        for child in self.get_top_node().get_children():
            child.get_state().get_board().print_board()

    # Perform Monte Carlo tree search until one of the players win and add data to the RBUF
    def mcts_tree_default_until_end(self, rollouts_per_episode, RBUF, visualize, min_pause_length, node_expansion=1, anet=None):
        current_node = self.get_top_node()

        if visualize[1]:
            current_node.get_state().get_board().initialize_board_plot()

        while not current_node.is_endstate():

            time_start = time.time()

            current_node.set_as_top_node()
            current_node.set_leaf_status()

            for i in range(rollouts_per_episode):
                #current_node.mcts_tree_policy(player, opposing_player, node_expansion)
                current_node.mcts_tree_policy(node_expansion, anet)

            # Since every child of a node rarely have been generated, create an array with board_size**2 elements of type [node_number, probability]
            current_root_arcs = []
            for i in range(0, current_node.get_state().get_board().get_board_size()**2):
                current_root_arcs.append([i, 0.0])

            # If a winning move is a direct child it won't have a lot of visits because it is an endnode
            # If any of the children is an endstate, give this a score of 1 and all others a score of 0
            for child in current_node.get_children():
                if child.is_endstate():
                    child.set_score([1, 1])
                    for child2 in current_node.get_children():
                        if child2 != child:
                            child2.set_score([0, 0])
                    break

            # Add each child's visit count to their fixed position in the board_grid
            for child in current_node.get_children():
                if current_node.get_score()[0] == 0:
                    print("Empty child selected. Set to 0.")
                    current_root_arcs[child.get_node_num()][1] = 0.0
                else:
                    current_root_arcs[child.get_node_num()][1] = child.get_score()[0] / current_node.get_score()[0]

            board_size = current_node.get_state().get_board().get_board_size()
            current_root_arcs = np.reshape(current_root_arcs, (board_size, board_size, 2))

            RBUF.append([current_node.merge_boards_to_anet(), current_root_arcs])

            # Move to best child node
            #current_node = current_node.calc_best_child(player, opposing_player, True)
            current_node = current_node.get_child_with_highest_visit_count()

            # Remove parent
            current_node.set_parent(None)

            if visualize[1]:
                current_node.get_state().get_board().create_board_plot(
                    self.get_top_node().get_state().get_board().get_fig(),
                    self.get_top_node().get_state().get_board().get_ax())
                plt.pause(0.5)

            if visualize[0]:
                current_node.get_state().get_board().print_board()

            if (time.time() < time_start + min_pause_length):
                time.sleep(time.time() - time_start + min_pause_length)

        if visualize[0] or visualize[1]:
            print(str(current_node.get_state().get_next_turn().get_color()) + " won!")

        if visualize[1]:
            plt.show()


    # Make a single move based on the anet's predictions
    def anet_one_turn(self, current_node, anet, visualize, min_pause_length):

        time_start = time.time()

        next_move = current_node.anet_policy(anet)

        next_move = [math.floor(next_move / current_node.get_state().get_board().get_board_size()), next_move % current_node.get_state().get_board().get_board_size()]

        current_node.create_child_node(next_move)

        current_node = current_node.get_children()[0]

        if visualize[1]:
            current_node.get_state().get_board().create_board_plot(
                self.get_top_node().get_state().get_board().get_fig(),
                self.get_top_node().get_state().get_board().get_ax())
            plt.pause(0.5)

        if visualize[0]:
            current_node.get_state().get_board().print_board()
            print()

        if (time.time() < time_start + min_pause_length):
            time.sleep(time.time() - time_start + min_pause_length)

        return current_node