from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os.path
import pickle
from textwrap import wrap
import matplotlib.pyplot as plt
import json
import numpy as np
from sklearn.manifold import TSNE

def create_label_lists(label_dir, label_file, json_dir, json_file):
    """
    creates a label to encoding dict and a reverse dict via an output
    label txt file generated by retraining.py
    :param label_dir: directory containing output label file
    :param label_file: output label file name
    :return: label to encoding dict and a reverse of that
    """
    label_path = os.path.join(label_dir, label_file)
    with open(label_path) as f:
        labels = f.readlines()
    labels = [l.strip() for l in labels]

    label2idx = {}
    idx2label = {}
    for label_idx, label_name in enumerate(labels):
        label2idx[label_name] = label_idx
        idx2label[label_idx] = label_name

    json_path = os.path.join(json_dir, json_file)
    f = open(json_path, "r")
    G = json.load(f)
    label2name = {}
    for product in G['products']:
        label2name[product['sku']] = product['name']

    return label2idx, idx2label, label2name

with open('C:\\Users\\weihan\\Courses\\COSEngProj\\tmp3\\test_results2.pkl', 'rb') as f:
    test_results = pickle.load(f)

with open('C:\\Users\\weihan\\Courses\\COSEngProj\\tmp3\\training_results.pkl', 'rb') as f:
    train_results = pickle.load(f)

label2idx, idx2label, label2name = create_label_lists(
      'C:\\Users\\weihan\\Courses\\COSEngProj\\tmp3','output_labels.txt',
      'D:\\PycharmProjects\\product-image-dataset-v0.1', 'products.json'
  )

num_correct = 0
num_incorrect = 0
num_viz = 4
plt.figure()

test_results = np.random.permutation(test_results)

for result in test_results:
    predicted = result['predicted_label']
    correct = result['correct_label']

    if result['prediction']:
        num_correct += 1
        if(num_correct > num_viz):
            continue
        #plt.subplot(2,num_viz,num_correct)
        plt.subplot(2, num_viz, num_correct)
        plt.imshow(result['image'])
        plt.title("\n".join(wrap('Pred: {0}'.format(label2name[predicted]),30)))

    if not result['prediction']:
        num_incorrect += 1
        if(num_incorrect > num_viz):
            continue
        #plt.subplot(2, num_viz, num_incorrect + num_viz)
        plt.subplot(2, num_viz, num_incorrect)
        plt.imshow(result['image'])
        plt.title("\n".join(wrap('Pred: {0}, \n Corr: {1}'.format(label2name[predicted], label2name[correct]),30)))

    test_results

features = np.array([result['features'] for result in test_results]
                    + [result['features'] for result in train_results])

print('Performing dimensionality reduction with tSNE...')

label2col = {}

for label in label2name.keys():
    label_id = int(label)
    label2col[label] = '#' + "{0:0{1}x}".format((label_id + np.random.randint(0, 0xFFFFFF)) % 0xFFFFFF, 6)
    print(label + ' color is : ' + label2col[label])


# dim reduction on the features!
tsne = TSNE(perplexity=30, n_components=2, init='pca', n_iter=5000, method='exact')
two_d_embeddings = tsne.fit_transform(features)

plt.figure()
for i, result in enumerate(test_results):
    x,y = two_d_embeddings[i,:]
    marker = 'o'
    if not result['prediction']:
        marker = 'x'
    plt.scatter(x,y,marker = marker,color=label2col[result['correct_label']], label=result['correct_label'])

for i, result in enumerate(train_results):
    x,y = two_d_embeddings[i+len(test_results),:]
    marker = '*'
    plt.scatter(x,y,marker = marker,color=label2col[result['correct_label']], label=result['correct_label'])

plt.title('2D visualization of features via TSNE reduction')

plt.show()
