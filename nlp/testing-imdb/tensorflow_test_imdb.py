# -*- coding: utf-8 -*-
"""Tensorflow Test #2 (IMDB)

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1DvwFqVz6XE6h5ir0Bv3okMjNUnC-5IjU
"""

import tensorflow as tf
import tensorflow.keras.layers as layers
from tensorflow.keras.preprocessing.sequence import pad_sequences
import tensorflow.keras.datasets.imdb as imdb

vocab_size = 50000
max_len = 1000
(x_train, y_train), (x_test, y_test) = imdb.load_data(num_words=vocab_size, maxlen=(max_len+1))
print(len(x_train))
print(y_train)

x_train_padded = pad_sequences(x_train)
x_test_padded = pad_sequences(x_test)

model = tf.keras.Sequential([
      layers.Embedding(vocab_size, 100, input_length=max_len-1),
      layers.GlobalAveragePooling1D(), #Could replace this with a Bidirectional, but computing time is insane
      layers.Dense(64, activation='relu'),
      layers.Dropout(0.25),
      layers.Dense(1, activation='sigmoid')
])

loss_fn = tf.keras.losses.BinaryCrossentropy()
model.compile(optimizer='adam', loss=loss_fn, metrics=['accuracy'])

model.fit(x_train_padded, y_train, epochs=8, verbose=2)

model.evaluate(x_test_padded, y_test, verbose=2)
