
import random

f = open('full-text.txt', 'r')
l = open('full-labels.txt', 'r')


index = 0
key_to_index = {}
index_to_key = {}
documents_full = []

for each_line in f:
    temp = each_line.split(' ')
    key_to_index[temp[0]] = index
    index_to_key[index] = temp[0]
    index += 1
    documents_full.append(' '.join(temp[1:]))

labels_full = [0]*len(documents_full)
for each_line in l:
    temp = each_line.split(' ')
    key = temp[0]
    labels_full[key_to_index[key]] = ' '.join(temp[1:])

total_indices = range(len(documents_full))
train_percentage = 0.8
train_indices =  random.sample(total_indices,int(len(total_indices)*train_percentage))
test_indices = list(set(total_indices)-set(train_indices))

f.close()
l.close()



f = open('train-text.txt','w')
l = open('train-labels.txt','w')

for each_index in train_indices:
    f.write(index_to_key[each_index]+' '+documents_full[each_index])

for each_index in train_indices:
    l.write(index_to_key[each_index] + ' ' + labels_full[each_index])

f.close()
l.close()

f = open('test-text.txt','w')
l = open('test-labels.txt','w')

for each_index in test_indices:
    f.write(index_to_key[each_index]+' '+documents_full[each_index])

for each_index in test_indices:
    l.write(index_to_key[each_index] + ' ' + labels_full[each_index])

f.close()
l.close()

