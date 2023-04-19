import math

import numpy as np
from matplotlib import pyplot as plt

class Tree:
    def __init__(self, top_node):
        self.top = top_node

    def get_top_node(self):
        return self.top

    def print_all_nodes_as_boards(self):
        for child in self.get_top_node().get_children():
            child.get_state().get_board().print_board()


    def mcts_tree_default_until_end(self, rollouts_per_episode, RBUF, visualize, pause_length=0.001, node_expansion=1, anet=None):
        current_node = self.get_top_node()

        if visualize[1]:
            current_node.get_state().get_board().initialize_board_plot()

        while not current_node.is_endstate():
            current_node.set_as_top_node()
            current_node.set_leaf_status()

            for i in range(rollouts_per_episode):
                #current_node.mcts_tree_policy(player, opposing_player, node_expansion)
                current_node.mcts_tree_policy2(node_expansion, anet)

            current_root_arcs = []
            for i in range(0, current_node.get_state().get_board().get_board_size()**2):
                current_root_arcs.append([i, 0.0])

            for child in current_node.get_children():
                if child.is_endstate():
                    child.set_score([1, 1])
                    for child2 in current_node.get_children():
                        if child2 != child:
                            child2.set_score([0, 0])
                    break

            for child in current_node.get_children():
                if child.is_endstate():
                    current_root_arcs[child.get_node_num()][1] = 1.0  # If a winning move is a direct child it won't have a lot of visits because it is an endnode. Give it a high score to prioritize this above others
                elif current_node.get_score()[0] == 0:
                    print("Empty child selected. Set to 0.")
                    current_root_arcs[child.get_node_num()][1] = 0.0
                else:
                    current_root_arcs[child.get_node_num()][1] = child.get_score()[0] / current_node.get_score()[0]

            p1_board = current_node.get_state().get_board().get_board_np_p1()
            p2_board = current_node.get_state().get_board().get_board_np_p2()
            board_size = current_node.get_state().get_board().get_board_size()
            ohe = np.zeros(shape=(board_size, board_size, 2))
            for i in range(board_size):
                for j in range(board_size):
                    if current_node.get_state().get_current_turn() == current_node.get_state().get_starting_player():
                        ohe[i, j] = [p1_board[i, j], p2_board[i, j]]
                    elif current_node.get_state().get_current_turn() == current_node.get_state().get_second_player():
                        ohe[i, j] = [p2_board.T[i, j], p1_board.T[i, j]]

            new = np.reshape(current_root_arcs, (board_size, board_size, 2))

            if current_node.get_state().get_current_turn() == current_node.get_state().get_starting_player():
                RBUF.append([ohe, new])
            elif current_node.get_state().get_current_turn() == current_node.get_state().get_second_player():
                RBUF.append([ohe, new.T])
            else:
                raise Exception("Could not append to RBUF")

            # Move to best child node
            #current_node = current_node.calc_best_child(player, opposing_player, True)
            current_node = current_node.get_child_with_highest_visit_count()

            # Remove parent
            current_node.set_parent(None)

            if visualize[1]:
                current_node.get_state().get_board().create_board_plot(self.get_top_node().get_state().get_board().get_fig(), self.get_top_node().get_state().get_board().get_ax())
                plt.pause(pause_length)

            if visualize[0]:
                current_node.get_state().get_board().print_board()

        if visualize[0] or visualize[1]:
            print(str(current_node.get_state().get_next_turn().get_color()) + " won!")

        if visualize[1]:
            plt.show()


    def anet_one_turn(self, current_node, anet, visualize, pause_length):

        next_move = current_node.anet_policy(anet)

        next_move = [math.floor(next_move / current_node.get_state().get_board().get_board_size()), next_move % current_node.get_state().get_board().get_board_size()]

        current_node.create_child_node(next_move)

        current_node = current_node.get_children()[0]

        if visualize[1]:
            current_node.get_state().get_board().create_board_plot(
                self.get_top_node().get_state().get_board().get_fig(),
                self.get_top_node().get_state().get_board().get_ax())
            plt.pause(pause_length)

        if visualize[0]:
            current_node.get_state().get_board().print_board()
            print()

        return current_node