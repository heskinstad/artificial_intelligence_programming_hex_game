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

    def mcts_tree_default_until_end(self, player, opposing_player, max_time, show_plot=False, pause_length=0.001):
        start = time.time()

        current_node = self.get_top_node()

        if show_plot:
            current_node.get_state().get_board().initialize_board_plot()

        while not current_node.is_leaf():

            for i in range(400):
                current_node.mcts_tree_policy(player, opposing_player)

            print()
            tete = ""
            for child in current_node.get_children():
                tete = tete + " " + str(child.get_total_score())
            print(tete)


            current_node.remove_every_but_best_child(player, opposing_player)
            current_node = current_node.get_children()[0]
            print(current_node.get_total_score())
            current_node.remove_all_children()

            if show_plot:
                current_node.get_state().get_board().create_board_plot(self.get_top_node().get_state().get_board().get_fig(), self.get_top_node().get_state().get_board().get_ax())
                plt.pause(pause_length)


            current_node.get_state().get_board().print_board()


        print()
        print(str(current_node.get_state().get_next_turn().get_color()) + " won!")

        end = time.time()
        print("Time elapsed: " + str(end - start) + "s")

        if show_plot:
            plt.show()