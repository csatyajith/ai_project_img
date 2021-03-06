import time

import numpy as np

import p3_utils
from load_data import FaceData
from naive_bayes import NaiveBayesPredictor
import statistics

if __name__ == '__main__':
    face_data = FaceData("facedata")
    n_test = len(face_data.face_train_imgs)
    test_features = p3_utils.get_features_for_data(face_data.face_test_imgs)
    percentage_list, time_list = ([], [])
    for n, n_samples in enumerate(range(n_test // 10, n_test + 1, n_test // 10)):
        start_time = time.time()
        predictions = []
        idx = np.random.choice(n_test, n_samples, replace=False)
        train_img_sample = np.array(face_data.face_train_imgs)[idx].tolist()
        train_labels_sample = np.array(face_data.face_train_labels)[idx].tolist()
        nbd = NaiveBayesPredictor(train_img_sample, train_labels_sample, range(2))
        for feature in test_features:
            predictions.append(nbd.predict(feature))

        correct, wrong = (0, 0)
        for k, pred in enumerate(predictions):
            if pred == face_data.face_test_labels[k]:
                correct += 1
            else:
                wrong += 1
        print("Stats while using {} % of training data".format(n * 10))
        # print("The predictions are: ", predictions)
        # print("The actual labels are:", face_data.face_test_labels)
        print("No. of correct guesses = {}".format(correct))
        print("No. of wrong guesses = {}".format(wrong))
        percentage = (correct * 100) / (correct + wrong)
        print("Percentage accuracy: {}".format(percentage))
        percentage_list.append(percentage)
        run_time = time.time() - start_time
        print("The run_time in seconds is: {}".format(run_time))
        time_list.append(run_time)
    p3_utils.plot_line_graph(range(10, 101, 10), percentage_list, "Naive Bayes Accuracy chart for faces",
                             "Percentage of training data used", "Accuracy obtained on test data")

    p3_utils.plot_line_graph(range(10, 101, 10), time_list, "Naive Bayes Runtime chart for faces",
                             "Percentage of training data used", "Run time in seconds")
    print(statistics.stdev(percentage_list))