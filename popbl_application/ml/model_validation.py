import sys

import pickle
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.utils import to_categorical
import os


def get_val_data():
    raw_text = open("/data/val_data.txt", "r").read()

    n_chars = len(raw_text)
    seq_length = 100
    dataX = []
    dataY = []

    with open(sys.argv[2], "rb") as fp:
        chars = pickle.load(fp)
    
    n_vocab = len(chars)    
    char_to_int = dict((c, i) for i, c in enumerate(chars))

    for i in range(0, n_chars - seq_length, 101):
        seq_in = raw_text[i:i + seq_length]
        seq_out = raw_text[i + seq_length]
        dataX.append([char_to_int[char] for char in seq_in])
        dataY.append(char_to_int[seq_out])
    X = np.reshape(dataX, (len(dataX), seq_length, 1))
    # normalize
    X = X / float(n_vocab)
    # one hot encode the output variable
    y = to_categorical(dataY)
    return X, y


def main():
    model = load_model(sys.argv[1])
    X, y = get_val_data()
    loss = model.evaluate(X, y)
    print("Old loss:", os.environ.get("MODEL_LOSS"), "  ->   New loss:", loss)
    if float(os.environ.get("MODEL_LOSS")) <= loss:
        print("Model not improoved")
        exit(-1)
    else:
        print("Model improoved")
        os.environ["MODEL_LOSS"] = str(loss)

    curl = (
        "curl --request PUT --header 'PRIVATE-TOKEN:"
        + os.environ.get("TOKEN")
        + "'  'https://gitlab.com/api/v4/projects/"
        + os.environ.get("CI_PROJECT_ID")
        + "/variables/MODEL_LOSS' --form 'value="
        + str(loss)
        + "' "
    )
    os.system(curl)


if __name__ == "__main__":
    main()
