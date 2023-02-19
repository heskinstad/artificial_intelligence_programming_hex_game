import time

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
        self.get_top_node().simulate_from_node(player, opposing_player, max_depth)
        end = time.time()
        print("Time elapsed: " + str(end - start) + " s")

        current_node = self.get_top_node().move_to_best_node()

        current_node.get_state().get_board().print_board()