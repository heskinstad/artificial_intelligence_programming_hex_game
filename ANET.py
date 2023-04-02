import tensorflow as tf

class ANET:
    def __init__(self, input_shape, num_actions):
        # define your neural network architecture here
        super(ANET, self).__init__()
        self.conv1 = tf.keras.layers.Conv2D(64, (3, 3), activation='relu', padding='same', input_shape=input_shape)
        self.conv2 = tf.keras.layers.Conv2D(64, (3, 3), activation='relu', padding='same')
        self.conv3 = tf.keras.layers.Conv2D(64, (3, 3), activation='relu', padding='same')
        self.flatten = tf.keras.layers.Flatten()
        self.dense1 = tf.keras.layers.Dense(128, activation='relu')
        self.dropout = tf.keras.layers.Dropout(0.5)
        self.dense2 = tf.keras.layers.Dense(num_actions, activation='softmax')

    def call(self, inputs):
        # define the forward pass of your neural network here
        x = self.conv1(inputs)
        x = self.conv2(x)
        x = self.conv3(x)
        x = self.flatten(x)
        x = self.dense1(x)
        x = self.dropout(x)
        output = self.dense2(x)
        return output

'''ANET = ANET()  # instantiate the ANET
ANET.build(input_shape=(None, ...))  # build the ANET
ANET.summary()  # print the summary of the ANET

# randomly initialize the parameters of the ANET
ANET.set_weights([tf.random.normal(w.shape) for w in ANET.get_weights()])'''