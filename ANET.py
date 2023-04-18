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
                64,
                (3, 3),
                input_shape=input_shape,
                activation='relu',
                padding='same',
            )
        )

        anet.add(
            keras.layers.Conv2D(
                64,
                (3, 3),
                input_shape=input_shape,
                activation='relu',
                padding='same',
            )
        )

        anet.add(
            keras.layers.Conv2D(
                64,
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

    def train_model(self, anet, num_epochs, batch_size, optimizer, loss, X_train, y_train, learning_rate):
        anet.compile(
            optimizer=optimizer,
            loss=loss,
            metrics=['accuracy']
        )

        from keras import backend as K
        K.set_value(anet.optimizer.learning_rate, learning_rate)

        history = anet.fit(
            X_train,
            y_train,
            batch_size=batch_size,
            epochs=num_epochs,
            verbose=0,
            shuffle=True
        )

        return history