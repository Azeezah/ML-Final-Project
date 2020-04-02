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

def main():

    # data = read_json('train.json') + read_json('train 2.json')

    data = read_json('train.json')
    print(len(data))

    for i in range(len(data)):
        data[i]['downvotes_at_request'] = (data[i]['requester_upvotes_plus_downvotes_at_request'] - data[i]['requester_upvotes_minus_downvotes_at_request'] )/ 2
        data[i]['downvotes_at_retrieval'] = (data[i]['requester_upvotes_plus_downvotes_at_retrieval'] - data[i]['requester_upvotes_minus_downvotes_at_retrieval'] )/ 2


    # for field in data[0]:
    #     if type(data[0][field]) == type(None) or type(data[0][field]) == type('') or type(data[0][field]) == type([]):
    #         continue
    #     print('____________________')
    #     print(field)
    #     print(f'sum: {sum_field(data, field)}')
    #     print(f'mean: {mean_field(data, field)}')


    field_to_find_masked_average = [
      'requester_upvotes_minus_downvotes_at_request',
      'requester_upvotes_minus_downvotes_at_retrieval',
      'requester_upvotes_plus_downvotes_at_request',
      'requester_upvotes_plus_downvotes_at_retrieval',
      'downvotes_at_request',
      'downvotes_at_retrieval'
    ]

    print(f'Averages for fields:')
    for field in field_to_find_masked_average:
        print('_________________')
        print(field + ' average:')
        print(f"True: {find_average_field(data, field, 'requester_received_pizza', True)}")
        print(f"False: {find_average_field(data, field, 'requester_received_pizza', False)}")
        print(f"std True: {find_std_field(data, field, 'requester_received_pizza', True)}")
        print(f"std False: {find_std_field(data, field, 'requester_received_pizza', False)}")

    test_data = read_json('test.json')
    write_predictor('dummy.csv', test_data, dummy_baseline)

    print('End of transmission. Don\'t panic!')

if __name__ == '__main__':
    main()
