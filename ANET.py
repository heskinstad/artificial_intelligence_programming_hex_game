from tensorflow import keras


class ANET:

    def initialize_model(self, input_shape, num_actions):
        anet = keras.models.Sequential()

        anet.add(
            keras.layers.InputLayer(
                input_shape=input_shape
            )
        )

        # Flatten the output of the convolutional layers
        anet.add(keras.layers.Flatten())

        # Add fully connected layers to predict the probability of good child states
        anet.add(keras.layers.Dense(32, activation='relu'))
        anet.add(keras.layers.Dense(num_actions, activation='softmax'))

        return anet

    def train_model(self, anet, num_epochs, batch_size, optimizer, loss, X_train, y_train):
        anet.compile(
            optimizer=optimizer,
            loss=loss,
            metrics=['accuracy']
        )

        from keras import backend as K
        K.set_value(anet.optimizer.learning_rate, 1.5)

        history = anet.fit(
            X_train,
            y_train,
            batch_size=batch_size,
            epochs=num_epochs,
            verbose=1
        )

        return history