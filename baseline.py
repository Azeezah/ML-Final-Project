import csv
import json
from random import randint

def read_json(filename):
    with open(filename, 'r') as file:
        data = file.read()
    return json.loads(data)

def sum_field(data, field):
    return sum(data[i][field] for i in range(len(data)))

def mean_field(data, field):
    return sum_field(data, field) / len(data)

def write_predictor(filename, test_data, predictor):
    with open(filename, 'w') as file:
        filewriter = csv.writer(file, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        filewriter.writerow(['request_id', 'requester_received_pizza'])
        for instance in test_data:
            filewriter.writerow([instance['request_id'], predictor(instance)])

def dummy_baseline(instance):
    return 1 if randint(0, 3) == 0 else 0


def false_baseline(instance):
    return 0

def find_average_field(data, field, mask_field, mask_value = True):
    total = 0
    count = 0
    for instance in data:
        if instance[mask_field] == mask_value:
            total += instance[field]
            count += 1
    return total / count


def find_std_field(data, field, mask_field, mask_value = True):
    mean = find_average_field(data, field, mask_field, mask_value)
    total = 0
    count = 0
    for instance in data:
        if instance[mask_field] == mask_value:
            total += (instance[field] - mean) ** 2
            count += 1

    return (total / count) ** (1 / 2)

def calculate_downvotes(data):
    for i in range(len(data)):
        data[i]['downvotes_at_request'] = (data[i]['requester_upvotes_plus_downvotes_at_request'] - data[i]['requester_upvotes_minus_downvotes_at_request'] )/ 2
        data[i]['downvotes_at_retrieval'] = (data[i]['requester_upvotes_plus_downvotes_at_retrieval'] - data[i]['requester_upvotes_minus_downvotes_at_retrieval'] )/ 2

def evaluate_threshold(data, field, threshold):
    count_correct = 0
    tp = 0
    fp = 0
    tn = 0
    fn = 0
    for i in range(len(data)):
        prediction = data[i][field] > threshold
        correct = prediction == data[i]['requester_received_pizza']
        if prediction:
            if correct:
                tp += 1
            else:
                fp += 1
        else:
            if correct:
                tn += 1
            else:
                fn += 1
    precision = tp / (tp + fp)
    recall = tp / (tp + fn)
    f1 = 2 * (precision * recall) * (1 / (precision + recall))
    return f1

def calculate_accuracy(data, field, threshold):
    count_correct = 0
    for i in range(len(data)):
        prediction = data[i][field] > threshold
        correct = prediction == data[i]['requester_received_pizza']
        if correct:
            count_correct += 1
    return correct / len(data)

def find_best_threshold(data, field, max_threshold = 100000, steps = 10):
    best = 0
    best_score = -1
    for i in range(0, max_threshold + 1, max_threshold // steps):
        score = evaluate_threshold(data, field, i)
        if score > best_score:
            best = i
            best_score = score
    return best, best_score

def predict_field_treshold(instance, field, threshold):
    return 1 if instance[field] > threshold else 0

def baseline_threshold(instance):
    # print('requester_upvotes_minus_downvotes_at_retrieval' in instance.keys())
    return predict_field_treshold(instance, 'requester_upvotes_plus_downvotes_at_request', 9980)

def main():

    # data = read_json('train.json') + read_json('train 2.json')

    data = read_json('train.json')

    calculate_downvotes(data)

    field_to_find_masked_average = [
      'requester_upvotes_minus_downvotes_at_request',
      'requester_upvotes_minus_downvotes_at_retrieval',
      'requester_upvotes_plus_downvotes_at_request',
      'requester_upvotes_plus_downvotes_at_retrieval',
      'downvotes_at_request',
      'downvotes_at_retrieval'
    ]



    for field in field_to_find_masked_average:
        best, score = find_best_threshold(data, field, 10000, 500)
        print(field, best, score, calculate_accuracy(data, field, best))




    #
    # print(f'Averages for fields:')
    # for field in field_to_find_masked_average:
    #     print('_________________')
    #     print(field + ' average:')
    #     print(f"True: {find_average_field(data, field, 'requester_received_pizza', True)}")
    #     print(f"False: {find_average_field(data, field, 'requester_received_pizza', False)}")
    #     print(f"std True: {find_std_field(data, field, 'requester_received_pizza', True)}")
    #     print(f"std False: {find_std_field(data, field, 'requester_received_pizza', False)}")




    test_data = read_json('test.json')
    write_predictor('dummy.csv', test_data, baseline_threshold)

    print('End of transmission. Don\'t panic!')

if __name__ == '__main__':
    main()
