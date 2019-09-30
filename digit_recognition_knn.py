import os
import random
import numpy

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_DIR = os.path.join(BASE_DIR, "dataset1")
TRAINING_DIR = os.path.join(DATASET_DIR, "training_validation")
TEST_DIR = os.path.join(DATASET_DIR, "test")

labels, image_matrix = {}, {}
images = []
K_FOLD = 5
k = int(input("Please Insert the number of K between 1 to 11: "))

for root, dirs, files in os.walk(TRAINING_DIR):
    for filename in files:
        label = int(str(filename).split("_")[1])
        labels[filename] = label
        path = os.path.join(root, filename)
        with open(path) as file:
            image_matrix[filename] = file.read().splitlines()

file_names = list(labels.keys())
random.shuffle(file_names)
n = len(file_names)

precisions = []
for i in range(K_FOLD):
    test_file_names = file_names[int(n / K_FOLD * i):int(n / K_FOLD * (i + 1))]
    train_file_names = [item for item in file_names if item not in test_file_names]

    error_count = 0
    test_number = len(test_file_names)

    cnt = 0
    for test_file_name in test_file_names:
        print("COUNT: " + str(cnt))
        cnt += 1

        test_label = int(test_file_name.split("_")[1])
        print(str(test_label) + " <------------------------- Real Label ------------------------> " + str(test_label))
        test_image_matrix = image_matrix[test_file_name]
        diff_counters = []
        for train_file_name in train_file_names:
            diff_counter = 0
            train_image_matrix = image_matrix[train_file_name]
            # train_label = labels[train_file_name]
            for row_idx, test_line in enumerate(test_image_matrix):
                for column_idx, test_bit in enumerate(test_line):
                    if test_bit != train_image_matrix[row_idx][column_idx]:
                        diff_counter += 1
            diff_counters.append(diff_counter)

        diff_counters, train_file_names \
            = (list(t) for t in zip(*sorted(zip(diff_counters, train_file_names))))

        train_labels = [int(filename.split('_')[1]) for filename in train_file_names]
        nearest_neighbours_labels = train_labels[:k]
        print("Nearest Neighbour Classes: " + str(nearest_neighbours_labels))
        diagnosed_class = max(set(nearest_neighbours_labels), key=nearest_neighbours_labels.count)
        print("CLASSIFIED AS " + str(diagnosed_class))
        if test_label != diagnosed_class:
            print("ERROR!!!ERROR!!!ERROR!!!ERROR!!!ERROR!!!ERROR!!!ERROR!!!ERROR!!!ERROR!!!ERROR!!!ERROR!!!")
            error_count += 1
    precision = (test_number - error_count) / test_number * 100
    print("Number of Errors: " + str(error_count))
    print("Precision: " + str(precision))
    precisions.append(precision)

final_precision = sum(precisions) / float(len(precisions))
print("------------------------------------------------------------------------------------------------------")
print("Final Precision: " + str(final_precision))
print("------------------------------------------------------------------------------------------------------")