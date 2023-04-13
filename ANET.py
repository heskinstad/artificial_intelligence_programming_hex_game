from tensorflow import keras


class ANET:

    def initialize_model(self, input_shape, num_actions):
        anet = keras.models.Sequential()

        anet.add(
            keras.layers.InputLayer(
                input_shape=input_shape
            )
        )

        anet.add(
            keras.layers.Conv2D(
                16,
                (3, 3),
                input_shape=input_shape,
                activation='relu',
                padding='same',
            )
        )

        anet.add(
            keras.layers.Conv2D(
                16,
                (3, 3),
                input_shape=input_shape,
                activation='relu',
                padding='same',
            )
        )

        anet.add(
            keras.layers.Conv2D(
                16,
                (3, 3),
                activation='relu',
                padding='same',
                kernel_regularizer=keras.regularizers.l2()
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

    '''anet.add(keras.layers.Conv2D(64, kernel_size=2, activation='relu', input_shape=input_shape))
    anet.add(keras.layers.Conv2D(32, kernel_size=2, activation='relu'))

    # Flatten the output of the convolutional layers
    anet.add(keras.layers.Flatten())

    # Add fully connected layers to predict the probability of good child states
    anet.add(keras.layers.Dense(128, activation='relu'))
    anet.add(keras.layers.Dense(64, activation='relu'))
    anet.add(keras.layers.Dense(49, activation='softmax'))'''