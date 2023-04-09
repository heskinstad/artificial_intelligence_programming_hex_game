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
            current_node = current_node.calc_best_child(player, opposing_player, True)

            print(current_node.get_state().get_next_turn().get_color() + " chose " + str(current_node.get_score()))

            # Remove parent
            current_node.set_parent(None)
            #current_node.remove_all_children()
            #current_node.set_score([0, 0])

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
            current_node = current_node.calc_best_child(player, opposing_player, True)

            print(current_node.get_state().get_next_turn().get_color() + " chose " + str(current_node.get_score()))

            # Remove parent
            current_node.set_parent(None)
            #current_node.remove_all_children()
            #current_node.set_score([0, 0])

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


    def mcts_tree_default_until_end3(self, player, opposing_player, rollouts_per_episode, RBUF, show_plot=False, pause_length=0.001, node_expansion=1, anet=None):
        start = time.time()

        current_node = self.get_top_node()

        if show_plot:
            current_node.get_state().get_board().initialize_board_plot()

        while not current_node.is_endstate():
            current_node.set_as_top_node()
            current_node.set_leaf_status()

            for i in range(rollouts_per_episode):
                tetete = time.time()
                current_node.mcts_tree_policy2(player, opposing_player, node_expansion, anet)
                #current_node.mcts_tree_policy(player, opposing_player, node_expansion)
                print(time.time() - tetete)

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
            current_node = current_node.calc_best_child(player, opposing_player, True)

            print(current_node.get_state().get_next_turn().get_color() + " chose " + str(current_node.get_score()))

            # Remove parent
            current_node.set_parent(None)
            #current_node.remove_all_children()
            #current_node.set_score([0, 0])

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