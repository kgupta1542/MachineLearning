# -*- coding: utf-8 -*-
"""Diary Distiller v1 (Embedding+Regression)

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1TNWyBH7VKOfoTBsQqCX1iDixxh06CSFr
"""

import os
import io
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import pairwise
from sklearn.model_selection import train_test_split
from google.colab import files
import io
!pip install tf-models-official
from official.modeling import tf_utils
from tensorflow.keras.preprocessing.text import Tokenizer

vocab_size = 50000
max_len = 1000

tokenizer = Tokenizer(num_words=vocab_size)

uploaded = files.upload()

label_1 = "Happy/Sad"
label_2 = "satisfaction/dissatisfaction"

uploaded = files.upload()

from tensorflow.keras.preprocessing.sequence import pad_sequences

data = pd.read_csv(io.BytesIO(uploaded['trainingset_v2.csv']),nrows=20000) #20000 rows
#print(data.head())
train, test = train_test_split(data, test_size=0.3, random_state=42, shuffle=True)
tokenizer.fit_on_texts(train["text"])

train_data = tokenizer.texts_to_sequences(train["text"])
train_data = pad_sequences(train_data, maxlen=max_len)
print(train_data[0:2])
train_labels = np.transpose([np.asarray(train[label_1]), np.asarray(train[label_2])])
print(train_labels.shape)

test_data = tokenizer.texts_to_sequences(test["text"])
test_data = pad_sequences(test_data, maxlen=max_len)
test_labels = np.transpose([np.asarray(test[label_1]), np.asarray(test[label_2])])

model = tf.keras.Sequential([
      tf.keras.layers.Embedding(vocab_size, 400, input_length=max_len),
      tf.keras.layers.GlobalAveragePooling1D(), #Could replace this with a Bidirectional, but computing time is longer
      tf.keras.layers.Dense(64, activation='relu'),
      tf.keras.layers.Dropout(0.25),
      tf.keras.layers.Dense(32, activation='relu'),
      tf.keras.layers.Dropout(0.125),
      tf.keras.layers.Dense(2)
])

model.summary()
tf.keras.utils.plot_model(model, show_shapes=True, dpi=48)
loss_fn = tf.keras.losses.MeanSquaredError()
model.compile(optimizer='adam', loss=loss_fn, metrics=['mae'])

epochs = 75
batch_size = 32

history = model.fit(train_data, train_labels, verbose=2, batch_size=batch_size, epochs=epochs)

plt.plot(history.history['loss'])
plt.plot(history.history['mae'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend('train', loc='upper left')
plt.show()

model.evaluate(test_data, test_labels, verbose=2)

predictArr = model.predict(test_data)

happyCounter = 0
satCounter = 0
totCounter = 0

for i in range(len(predictArr)):
  hapBool = False
  satBool = False

  if abs(predictArr[i][0] - test_labels[i][0]) < 0.05:
    happyCounter += 1
    hapBool = True
  if abs(predictArr[i][1] - test_labels[i][1]) < 0.05:
    satCounter += 1
    satBool = True
  if hapBool and satBool:
    totCounter += 1

print(happyCounter/len(predictArr))
print(satCounter/len(predictArr))
print(totCounter/len(predictArr))

from google.colab import files

export_dir='./diarydistiller'

tf.saved_model.save(model, export_dir=export_dir)

!zip -r ./diarydistiller.zip ./diarydistiller

files.download("./diarydistiller.zip")