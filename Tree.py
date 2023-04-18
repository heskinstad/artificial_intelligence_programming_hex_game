import math
import time

from matplotlib import pyplot as plt

class Tree:
    def __init__(self, top_node):
        self.top = top_node

    def get_top_node(self):
        return self.top

    def print_all_nodes_as_boards(self):
        for child in self.get_top_node().get_children():
            child.get_state().get_board().print_board()

    def mcts_tree_default_until_end(self, player, opposing_player, rollouts_per_episode, show_plot=False, pause_length=0.001, node_expansion=1):
        start = time.time()

        current_node = self.get_top_node()

        if show_plot:
            current_node.get_state().get_board().initialize_board_plot()

        while not current_node.is_endstate():
            current_node.set_as_top_node()
            current_node.set_leaf_status()

            for i in range(rollouts_per_episode):
                current_node.mcts_tree_policy(player, opposing_player, node_expansion)

            tete = ""
            for child in current_node.get_children():
                tete += str(child.get_score()) + "  "
            print(tete)

            # Move to best child node
            current_node = current_node.calc_best_child(True)

            print(current_node.get_state().get_next_turn().get_color() + " chose " + str(current_node.get_score()))

            # Remove parent
            current_node.set_parent(None)

            if show_plot:
                current_node.get_state().get_board().create_board_plot(self.get_top_node().get_state().get_board().get_fig(), self.get_top_node().get_state().get_board().get_ax())
                plt.pause(pause_length)

            current_node.get_state().get_board().print_board()

            print("-----------------------------------")


        print()
        print(str(current_node.get_state().get_next_turn().get_color()) + " won!")

        end = time.time()
        print("Time elapsed: " + str(end - start) + "s")

        if show_plot:
            plt.show()


    # Added the RBUF
    def mcts_tree_default_until_end2(self, player, opposing_player, rollouts_per_episode, RBUF, show_plot=False, pause_length=0.001, node_expansion=1):
        start = time.time()

        current_node = self.get_top_node()

        if show_plot:
            current_node.get_state().get_board().initialize_board_plot()

        while not current_node.is_endstate():
            current_node.set_as_top_node()
            current_node.set_leaf_status()

            for i in range(rollouts_per_episode):
                current_node.mcts_tree_policy(player, opposing_player, node_expansion)

            tete = ""
            titi = ""
            for child in current_node.get_children():
                tete += str(child.get_score()) + "  "
                titi += str(child.get_node_num()) + "  "
            print(tete)
            print(titi)

            current_root_arcs = []
            for i in range(0, current_node.get_state().get_board().get_board_size()**2):
                current_root_arcs.append([i, 0.0])

            for child in current_node.get_children():
                current_root_arcs[child.get_node_num()][1] = child.get_score()[0] / current_node.get_score()[0]

            RBUF.append([current_node, current_root_arcs])

            # Move to best child node
            current_node = current_node.calc_best_child(True)

            print(current_node.get_state().get_next_turn().get_color() + " chose " + str(current_node.get_score()))

            # Remove parent
            current_node.set_parent(None)

            if show_plot:
                current_node.get_state().get_board().create_board_plot(self.get_top_node().get_state().get_board().get_fig(), self.get_top_node().get_state().get_board().get_ax())
                plt.pause(pause_length)

            current_node.get_state().get_board().print_board()

            print("-----------------------------------")


        print()
        print(str(current_node.get_state().get_next_turn().get_color()) + " won!")

        end = time.time()
        print("Time elapsed: " + str(end - start) + "s")

        if show_plot:
            plt.show()


    def mcts_tree_default_until_end3(self, player, opposing_player, starting_player, rollouts_per_episode, RBUF, show_plot=False, pause_length=0.001, node_expansion=1, anet=None):
        start = time.time()

        current_node = self.get_top_node()

        if show_plot:
            current_node.get_state().get_board().initialize_board_plot()

        while not current_node.is_endstate():
            current_node.set_as_top_node()
            current_node.set_leaf_status()

            tetete = time.time()
            for i in range(rollouts_per_episode):
                #current_node.mcts_tree_policy(player, opposing_player, node_expansion)
                current_node.mcts_tree_policy2(player, opposing_player, node_expansion, anet)
            print(str(((time.time() - tetete) / rollouts_per_episode)) + 's per rollout')

            tete = ""
            titi = ""
            for child in current_node.get_children():
                tete += str(child.get_score()) + "  "
                titi += str(child.get_node_num()) + "  "
            print(tete)
            print(titi)

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
                current_root_arcs[child.get_node_num()][1] = child.get_score()[0] / current_node.get_score()[0]

            if current_node.get_state().get_current_turn() == current_node.get_state().get_starting_player():
                RBUF.append([current_node.get_state().get_board().get_board_np_p1(), current_root_arcs])
            elif current_node.get_state().get_current_turn() == current_node.get_state().get_second_player():
                RBUF.append([current_node.get_state().get_board().get_board_np_p2(), current_root_arcs])
            else:
                raise Exception("Could not append to RBUF")

            # Move to best child node
            #current_node = current_node.calc_best_child(player, opposing_player, True)
            current_node = current_node.get_child_with_highest_visit_count()

            print(current_node.get_state().get_next_turn().get_color() + " chose " + str(current_node.get_score()))

            # Remove parent
            current_node.set_parent(None)

            if show_plot:
                current_node.get_state().get_board().create_board_plot(self.get_top_node().get_state().get_board().get_fig(), self.get_top_node().get_state().get_board().get_ax())
                plt.pause(pause_length)

            current_node.get_state().get_board().print_board()

            print("-----------------------------------")


        print()
        print(str(current_node.get_state().get_next_turn().get_color()) + " won!")

        end = time.time()
        print("Time elapsed: " + str(end - start) + "s")

        if show_plot:
            plt.show()


    def anet_one_turn(self, current_node, player, opposing_player, anet, show_plot, pause_length):

        if show_plot:
            current_node.get_state().get_board().initialize_board_plot()

        next_move = current_node.anet_policy(player, opposing_player, anet)

        next_move = [math.floor(next_move / current_node.get_state().get_board().get_board_size()), next_move % current_node.get_state().get_board().get_board_size()]

        current_node.create_child_node(next_move)

        current_node = current_node.get_children()[0]

        if show_plot:
            current_node.get_state().get_board().create_board_plot(
                self.get_top_node().get_state().get_board().get_fig(),
                self.get_top_node().get_state().get_board().get_ax())
            plt.pause(pause_length)

        current_node.get_state().get_board().print_board()
        print()

        return current_node