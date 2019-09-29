import os
import random
import numpy as np

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_DIR = os.path.join(BASE_DIR, "dataset1")
TRAINING_DIR = os.path.join(DATASET_DIR, "training_validation")
TEST_DIR = os.path.join(DATASET_DIR, "test")
TEST_FILE = "C:\\Users\\asris\\Desktop\\Mycourselink\\Pattern Recognition\\Assignments\\Assignment 1\\dataset1\\test\\class_3_sample_12"

with open(TEST_FILE) as tf:
    array_test = tf.read().splitlines()

array_files, labels, file_names = [], [], []
for root, dirs, files in os.walk(TRAINING_DIR):
    for filename in files:
        label = int(str(filename).split("_")[1])
        labels.append(label)
        file_names.append(filename)
        path = os.path.join(root, filename)
        with open(path) as file:
            array_files.append(file.read().splitlines())

zipped = list(zip(file_names, array_files, labels))
random.shuffle(zipped)
file_names, array_files, labels = zip(*zipped)

dif_counter = 0
dif_counters = []
for array_file_idx, array_file in enumerate(array_files):
    for row_idx, row in enumerate(array_file):
        for bit_idx, bit in enumerate(row):
            if bit != array_test[row_idx][bit_idx]:
                dif_counter += 1
    dif_counters.append(dif_counter)
    dif_counter = 0


# sort by nearest neighbours
dif_counters, file_names, array_files, labels \
    = (list(t) for t in zip(*sorted(zip(dif_counters, file_names, array_files, labels))))

k = int(input("Please Insert the number of K between 1 to 11: "))
nearest_labels = labels[:k]
print(nearest_labels)

nearest_file_idx = dif_counters.index(min(dif_counters))
print("Nearest file idx: " + str(nearest_file_idx))
print("Nearest file: \"" + file_names[nearest_file_idx] + "\"")
print(*array_files[nearest_file_idx], sep='\n')
print("Classified as: " + str(max(set(nearest_labels), key=nearest_labels.count)))

