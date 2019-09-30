import os
import random

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_DIR = os.path.join(BASE_DIR, "dataset1")
TRAINING_DIR = os.path.join(DATASET_DIR, "training_validation")
TEST_DIR = os.path.join(DATASET_DIR, "test")

labels, image_matrix = {}, {}
images = []
K_FOLD = 5

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

error_counts = {}
precisions = {}
for i in range(1, 12):
    error_counts[i] = 0
    precisions[i] = []
final_precisions = [1.0] * 12

for i in range(K_FOLD):
    test_file_names = file_names[int(n / K_FOLD * i):int(n / K_FOLD * (i + 1))]
    train_file_names = [item for item in file_names if item not in test_file_names]

    error_count = 0
    for j in range(1, 12):
        error_counts[j] = 0
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
            for row_idx, test_line in enumerate(test_image_matrix):
                for column_idx, test_bit in enumerate(test_line):
                    if test_bit != train_image_matrix[row_idx][column_idx]:
                        diff_counter += 1
            diff_counters.append(diff_counter)

        diff_counters, train_file_names \
            = (list(t) for t in zip(*sorted(zip(diff_counters, train_file_names))))

        train_labels = [int(filename.split('_')[1]) for filename in train_file_names]
        print("Nearest Neighbour Classes: " + str(train_labels[:12]))
        for k in range(1, 12):
            nearest_neighbours_labels = train_labels[:k]
            diagnosed_class = max(set(nearest_neighbours_labels), key=nearest_neighbours_labels.count)
            # print("CLASSIFIED AS " + str(diagnosed_class))
            if test_label != diagnosed_class:
                print("ERROR!!!ERROR!!!ERROR!!!ERROR!!!ERROR!!!ERROR!!!ERROR!!!ERROR!!!ERROR!!!ERROR!!!ERROR!!!")
                error_counts[k] += 1

    for k in range(1, 12):
        precision = (test_number - error_counts[k]) / test_number * 100
        precisions[k].append(precision)
        print("Number of Errors[" + str(k) + "]: " + str(error_counts[k]))
        print("Precision[" + str(k) + "]: " + str(precision))
    # for j in range(1, 12):
    #     final_precisions[j] = sum(precisions[j]) / float(len(precisions[j]))
    #     print("------------------------------------------------------------------------------------------------------")
    #     print("Final Precision[" + str(j) + "]: " + str(final_precisions[j]))

# final_precision = sum(precisions) / float(len(precisions))
final_precisions = [1.0] * 12
for i in range(1, 12):
    final_precisions[i] = sum(precisions[i]) / float(len(precisions[i]))
    print("------------------------------------------------------------------------------------------------------")
    print("Final Precision[" + str(i) + "]: " + str(final_precisions[i]))
