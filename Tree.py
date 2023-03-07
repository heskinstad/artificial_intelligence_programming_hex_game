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

    def simulate_all(self, player, opposing_player, max_depth):
        start = time.time()
        #self.get_top_node().simulate_from_node(player, opposing_player, max_depth)
        self.get_top_node().mcts_default_policy(player, opposing_player)
        end = time.time()
        print("Time elapsed: " + str(end - start) + "s")

        current_node = self.get_top_node().move_to_best_node(1000)

        current_node.get_state().get_board().print_board()


    def mcts_tree_default_until_end(self, player, opposing_player, depth, show_plot=False, pause_length=0.001):
        start = time.time()

        current_node = self.get_top_node()

        if show_plot:
            current_node.get_state().get_board().initialize_board_plot()

        while not current_node.is_leaf():
            current_node.mcts_tree_policy(player, opposing_player, depth)

            current_node = current_node.move_to_best_node(1)

            if show_plot:
                current_node.get_state().get_board().create_board_plot(self.get_top_node().get_state().get_board().get_fig(), self.get_top_node().get_state().get_board().get_ax())
                plt.pause(pause_length)


        print()
        print(str(current_node.get_state().get_next_turn().get_color()) + " won!")

        end = time.time()
        print("Time elapsed: " + str(end - start) + "s")

        if show_plot:
            plt.show()