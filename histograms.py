import numpy as np
#import tensorflow as tf
#from tensorflow import keras
#from keras import metrics
import pandas as pd
import csv
import json
from random import randint
import matplotlib.pyplot as plt

def read_json(filename):
    with open(filename, 'r') as file:
        data = file.read()
    return json.loads(data)

def sum_field(data, field):
    return sum(data[i][field] for i in range(len(data)))

def mean_field(data, field):
    return sum_field(data, field) / len(data)

def predict_field_treshold(instance, field, threshold):
    return 1 if instance[field] > threshold else 0

def baseline_threshold(instance):
    return predict_field_treshold(instance, 'requester_upvotes_plus_downvotes_at_request', 9980)

def write_predictor(filename, test_data, predictor):
    with open(filename, 'w') as file:
        filewriter = csv.writer(file, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        filewriter.writerow(['request_id', 'requester_received_pizza'])
        for instance in test_data:
            filewriter.writerow([instance['request_id'], predictor(instance)])
    files.download(filename)

train_data = read_json('train.json')
df = pd.DataFrame.from_dict(train_data)

print(df.keys())
for feature in df.keys():
    plt.title(feature)
    plt.ylabel('normalized count')
    plt.xlabel(feature)
    pos = [val for i, val in enumerate(df[feature]) if df['requester_received_pizza'][i]]
    neg = [val for i, val in enumerate(df[feature]) if not df['requester_received_pizza'][i]]
    if df[feature].dtype in ('int64', 'float64'):
        plt.hist([pos, neg], density=True, label=['positive', 'negative'])
        plt.legend()
        #plt.show()
        plt.savefig('histograms/'+feature+'.png')
        plt.clf()
