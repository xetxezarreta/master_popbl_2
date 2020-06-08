import os, pickle
import numpy as np
from ..settings import PROJECT_ROOT
from tensorflow.keras.models import load_model


def predict_tweet(topic, pred_length=100):
    result = ""
    # read chars list
    char_path = os.path.join(PROJECT_ROOT, "tensorflow/chars.txt")
    with open(char_path, "rb") as fp:
        chars = pickle.load(fp)
    n_vocab = len(chars)
    # create char-int mapping
    char_to_int = dict((c, i) for i, c in enumerate(chars))
    int_to_char = dict((i, c) for i, c in enumerate(chars))
    # load model
    model_path = os.path.join(PROJECT_ROOT, "tensorflow/model.h5")
    model = load_model(model_path)
    # predict new tweet
    seed = topic.lower()
    pattern = [char_to_int[char] for char in seed]
    for i in range(pred_length):
        x = np.reshape(pattern, (1, len(pattern), 1))
        x = x / float(n_vocab)
        prediction = model.predict(x, verbose=0)
        index = np.argmax(prediction)
        result += int_to_char[index]
        pattern.append(index)
        pattern = pattern[1 : len(pattern)]
    result = "".join(result)
    return result
