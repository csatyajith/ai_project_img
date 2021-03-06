import statistics
import numpy as np
import p3_utils
import utils
from statistics import mode
from multiprocessing import Pool
import time
from load_data import FaceData
start_time = time.time()


class KnnFaces:
    def __init__(self, k, i):
        self.face_data = FaceData("facedata")
        self.distance = []
        self.k = k
        featureFunction = self.face_data.basic_feature_extractor
        size = len(self.face_data.face_train_imgs)
        index = int(size * i)
        self.trainingData = list(map(featureFunction, self.face_data.face_train_imgs))[:index]
        self.testData = list(map(featureFunction, self.face_data.face_test_imgs))

    def predict(self, image):
        img_a = utils.Counter()
        img_a = image
        self.distance = list(map(lambda x: (self.face_data.face_train_labels[x[0]], img_a.cosine_distance(x[1])),
                                 enumerate(self.trainingData)))
        # sort the list of tuples by distances in increasing order
        sorted_dist = (sorted(self.distance, key=lambda x: x[1]))
        k_neighbors = sorted_dist[:self.k]
        # select k labels
        klabels = [label for (label, _) in k_neighbors]
        # find the mode of the list
        return mode(klabels)


if __name__ == '__main__':
    exec_time = []
    accuracy = []
    for i in np.arange(0.1, 1.1, 0.1):
        predictions = []
        knnf = KnnFaces(5, i)
        # Run this with a pool of 10 agents having a chunksize of 10 until finished
        agents = 10
        chunksize = 10
        with Pool(processes=agents) as pool:
            predictions = pool.map(knnf.predict, knnf.testData, chunksize)
        # cool_visualization(digit_data)
        correct, wrong = (0, 0)
        for k, pred in enumerate(predictions):
            if pred == knnf.face_data.face_test_labels[k]:
                correct += 1
            else:
                wrong += 1
        print("The predictions are: ", predictions)
        print("The actual labels are:", knnf.face_data.face_test_labels)
        print("No. of correct guesses = {}".format(correct))
        print("No. of wrong guesses = {}".format(wrong))
        print("Percentage accuracy: {}".format((correct * 100) / (correct + wrong)))
        accuracy.append((correct * 100) / (correct + wrong))
        print('execution time', time.time() - start_time)
        exec_time.append(time.time() - start_time)
    p3_utils.plot_line_graph(range(10, 101, 10), accuracy, "Knn Accuracy chart for faces",
                             "Percentage of training data used", "Accuracy obtained on test data")
    p3_utils.plot_line_graph(range(10, 101, 10), exec_time, "Knn Runtime chart for faces",
                             "Percentage of training data used", "Run time in seconds")
    print(statistics.stdev(accuracy))
