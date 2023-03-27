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

        # Input layer
        input_shape = len(self.get_state().get_board().get_positions())
        inputs = tf.keras.Input(shape = input_shape)

        # Convolutional layers
        x = tf.keras.layers.Conv2D(filters=32, kernel_size=(3, 3), activation='relu')(inputs)
        x = tf.keras.layers.Conv2D(filters=64, kernel_size=(3, 3), activation='relu')(x)

        # Flatten the output of the convolutional layers
        x = tf.keras.layers.Flatten()(x)

        # Fully connected layers
        x = tf.keras.layers.Dense(units=128, activation='relu')(x)
        outputs = tf.keras.layers.Dense(units=self.count_num_of_free_positions()-1, activation='softmax')(x)

        # Model
        model = tf.keras.Model(inputs=inputs, outputs=outputs)

        # Loss function and optimizer
        loss_fn = tf.keras.losses.CategoricalCrossentropy()
        optimizer = tf.keras.optimizers.Adam()

        # Compile the model
        model.compile(optimizer=optimizer, loss=loss_fn)