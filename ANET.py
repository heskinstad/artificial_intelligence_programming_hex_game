from keras.losses import mean_squared_error
from tensorflow import keras

class ANET:
    def initialize_model(self, input_shape, num_actions, optimizer, loss, num_of_hidden_layers, num_of_neurons_per_layer):
        anet = keras.models.Sequential()

        anet.add(
            keras.layers.InputLayer(
                input_shape=input_shape
            )
        )

        anet.add(
            keras.layers.Conv2D(
                num_of_neurons_per_layer,
                (3, 3),
                input_shape=input_shape,
                activation='relu',
                padding='same',
                kernel_initializer="normal"
            )
        )

        anet.add(
            keras.layers.Conv2D(
                num_of_neurons_per_layer,
                (3, 3),
                input_shape=input_shape,
                activation='relu',
                padding='same',
                kernel_initializer="normal"
            )
        )

        anet.add(
            keras.layers.Conv2D(
                num_of_neurons_per_layer,
                (3, 3),
                input_shape=input_shape,
                activation='relu',
                padding='same',
                kernel_initializer="normal"
                #kernel_regularizer='l1'
            )
        )

        anet.add(
            keras.layers.Flatten()
        )

        anet.add(
            keras.layers.Dense(
                num_actions,
                activation='softmax'
            )
        )

        anet.compile(
            optimizer=optimizer,
            loss=loss,
            metrics=['accuracy']
        )

        return anet


    def train_model(self, anet, num_epochs, batch_size, X_train, y_train, learning_rate):

        # Set learning rate
        keras.backend.set_value(anet.optimizer.learning_rate, learning_rate)

        # Train network
        history = anet.fit(
            X_train,
            y_train,
            batch_size=batch_size,
            epochs=num_epochs,
            verbose=1,
            shuffle=True
        )

        # return history for accuracy and loss data
        return history