from tensorflow import keras

class ANET:

    def initialize_model(self, input_shape, num_actions, optimizer, loss):
        anet = keras.models.Sequential()

        anet.add(
            keras.layers.Conv2D(
                32,
                (3, 3),
                input_shape=input_shape,
                activation='relu',
                padding='same',
            )
        )

        anet.add(
            keras.layers.Conv2D(
                64,
                (2, 2),
                input_shape=input_shape,
                activation='relu',
                padding='same',
            )
        )

        anet.add(
            keras.layers.Conv2D(
                64,
                (1, 1),
                activation='relu',
                padding='same',
            )
        )

        anet.add(
            keras.layers.Flatten()
        )

        anet.add(
            keras.layers.Dense(
                15,
                activation='relu'
            )
        )

        anet.add(
            keras.layers.Dense(
                30,
                activation='relu'
            )
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


'''
anet.add(
            keras.layers.Conv2D(
                32,
                (3, 3),
                input_shape=input_shape,
                activation='relu',
                padding='same',
            )
        )

        anet.add(
            keras.layers.Conv2D(
                64,
                (2, 2),
                input_shape=input_shape,
                activation='relu',
                padding='same',
            )
        )

        anet.add(
            keras.layers.Conv2D(
                64,
                (1, 1),
                activation='relu',
                padding='same',
            )
        )

        anet.add(
            keras.layers.Flatten()
        )

        anet.add(
            keras.layers.Dense(
                15,
                activation='relu'
            )
        )
        
        anet.add(
            keras.layers.Dense(
                30,
                activation='relu'
            )
        )

        anet.add(
            keras.layers.Dense(
                num_actions,
                activation='softmax'
            )
        )'''