import tensorflow as tf

# A single neural network (ANET) to serve as an actor.
class Actor:
    def __init__(self, state):
        self.state = state  # The input game state

    def get_state(self):
        return self.state

    def count_num_of_free_positions(self):
        board_size = len(self.get_state().get_board().get_positions())
        free_positions = 0

        for i in range(board_size):
            for j in range(board_size):
                if self.get_state().get_board().get_positions()[i][j] == None:
                    free_positions += 1

        return free_positions


    def calc_rollout_distribution(self):
        input_shape = len(self.get_state().get_board().get_positions())
        inputs = tf.keras.Input(shape = input_shape)

