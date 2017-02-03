
import random
import collections
import string
import re
import math
# random.seed(1337)

def tokenize(sentence):
    sentence = ' '.join(sentence)
    sentence = sentence.lower()

    sentence = sentence.split(' ')
    return_list = []

    for each_word in sentence:
        if each_word not in stop_words_dict:
            return_list.append(re.sub(r'[^\w\s]', '', each_word.strip('\n')))

    return return_list

stop_words_dict = {'during': 0, 'has': 0, "it's": 0, 'very': 0, 'itself': 0, "why's": 0, "we'll": 0, 'hers': 0,
                   "isn't": 0, 'off': 0, 'we': 0, 'it': 0, 'the': 0, 'doing': 0, 'over': 0, 'its': 0, 'with': 0,
                   'so': 0, 'but': 0, 'they': 0, 'am': 0, 'until': 0, 'because': 0, "shouldn't": 0, "you're": 0,
                   'is': 0, "they're": 0, "you'd": 0, "mustn't": 0, 'would': 0, 'while': 0, 'should': 0, 'as': 0,
                   "i'd": 0, "we've": 0, 'when': 0, "wouldn't": 0, 'why': 0, "i'll": 0, 'theirs': 0, "aren't": 0,
                   'our': 0, 'from': 0, "we'd": 0, 'each': 0, 'only': 0, 'yourself': 0, 'been': 0, 'again': 0, 'of': 0,
                   'whom': 0, 'themselves': 0, 'or': 0, 'that': 0, 'me': 0, "how's": 0, 'those': 0, 'having': 0,
                   'was': 0, 'and': 0, 'few': 0, 'no': 0, 'any': 0, 'being': 0, 'an': 0, "let's": 0, "they'd": 0,
                   'own': 0, 'his': 0, 'herself': 0, 'before': 0, 'did': 0, 'too': 0, 'here': 0, 'were': 0, "that's": 0,
                   "what's": 0, "she'll": 0, 'i': 0, 'all': 0, 'have': 0, "weren't": 0, "you've": 0, "i'm": 0,
                   "he'd": 0, 'some': 0, 'into': 0, 'down': 0, 'this': 0, "she'd": 0, "i've": 0, 'do': 0, "can't": 0,
                   'for': 0, 'below': 0, 'through': 0, "don't": 0, 'more': 0, 'once': 0, "didn't": 0, 'same': 0,
                   "she's": 0, "they've": 0, "he'll": 0, 'not': 0, 'had': 0, 'such': 0, 'cannot': 0, 'about': 0,
                   'myself': 0, 'if': 0, "won't": 0, 'a': 0, 'how': 0, 'she': 0, 'you': 0, "we're": 0, "there's": 0,
                   'be': 0, 'yours': 0, "here's": 0, 'above': 0, 'at': 0, 'out': 0, 'does': 0, 'my': 0, 'to': 0,
                   'ought': 0, "hadn't": 0, "doesn't": 0, "couldn't": 0, 'he': 0, 'your': 0, 'ours': 0, 'up': 0,
                   'after': 0, "where's": 0, 'could': 0, 'under': 0, 'nor': 0, 'against': 0, 'further': 0, "they'll": 0,
                   'what': 0, 'then': 0, "you'll": 0, 'ourselves': 0, 'which': 0, 'between': 0, "shan't": 0, 'these': 0,
                   'in': 0, 'their': 0, "who's": 0, "he's": 0, 'yourselves': 0, 'himself': 0, 'both': 0, "wasn't": 0,
                   'him': 0, 'on': 0, 'them': 0, "when's": 0, 'there': 0, 'where': 0, 'than': 0, 'are': 0, 'her': 0,
                   "hasn't": 0, 'by': 0, 'other': 0, 'who': 0, "haven't": 0, 'most': 0}



f = open('train-text.txt', 'r')
l = open('train-labels.txt', 'r')

index = 0
key_to_index = {}
documents_full = []

for each_line in f:
    temp = each_line.split(' ')
    #temp[0] is the key
    #temp[1:] is the document space separated
    key_to_index[temp[0]] = index
    index += 1
    documents_full.append(list(temp[1:]))

class_dt = [0] * len(documents_full)
class_pn = [0] * len(documents_full)

for each_line in l:
    temp = each_line.split(' ')
    #temp[0] is key
    #temp[1] is the class1
    #temp[2] is the class2
    class_dt[key_to_index[temp[0]]] = temp[1].strip('\n')
    class_pn[key_to_index[temp[0]]] = temp[2].strip('\n')


"""
SPLIT TOTAL DATA INTO TRAIN AND TEST
"""

total_indices = range(len(documents_full))
train_percentage = 0.8

documents_train = []
class_dt_train = []
class_pn_train = []

train_indices =  random.sample(total_indices,int(len(total_indices)*train_percentage))

test_indices = list(set(total_indices)-set(train_indices))


documents_test = []
class_dt_test = []
class_pn_test = []

print(len(train_indices),len(test_indices))


for i in train_indices:
    '''
    JUST TOKENIZE THE TRAINING DATASET FOR NOW
    '''
    documents_train.append(tokenize(documents_full[i]))
    class_dt_train.append(class_dt[i])
    class_pn_train.append(class_pn[i])

for i in test_indices:
    documents_test.append(documents_full[i])
    class_dt_test.append(class_dt[i])
    class_pn_test.append(class_pn[i])



assert len(class_dt_train)==len(class_pn_train)==len(documents_train)==len(train_indices) , "Error"


probs = collections.defaultdict(dict)

vocab_train = []

for each_sentence in documents_train:
    for each_word in each_sentence:
        vocab_train.append(each_word)

vocab_train = set(vocab_train)

print('Length of Train Vocabulary = ', len(vocab_train))
# print('Vocab = ',vocab_train)
vocab_train_len = len(vocab_train)

for each_vocab in vocab_train:
    temp_dict = {}
    temp_dict['positive'] = 0
    temp_dict['negative'] = 0
    temp_dict['deceptive'] = 0
    temp_dict['truthful'] = 0
    probs[each_vocab] = temp_dict


for i in range(len(train_indices)):
    if class_pn_train[i] == 'positive':
        for each_word in documents_train[i]:
            probs[each_word]['positive'] += 1
    if class_pn_train[i] == 'negative':
        for each_word in documents_train[i]:
            probs[each_word]['negative'] += 1

    if class_dt_train[i] == 'deceptive':
        for each_word in documents_train[i]:
            probs[each_word]['deceptive'] += 1

    if class_dt_train[i] == 'truthful':
        for each_word in documents_train[i]:
            probs[each_word]['truthful'] += 1



"""
ADD -1 SMOOTHING

And convert frequencies into probabilites by normalizing them
"""

for each_word in vocab_train:
    probs[each_word]['positive'] += 1
    probs[each_word]['negative'] += 1
    probs[each_word]['deceptive'] += 1
    probs[each_word]['truthful'] += 1

positive_normalize = 0
negative_normalize = 0
deceptive_normalize = 0
truthful_normalize = 0

for each_word in vocab_train:
    positive_normalize += probs[each_word]['positive']
    negative_normalize += probs[each_word]['negative']
    deceptive_normalize += probs[each_word]['deceptive']
    truthful_normalize += probs[each_word]['truthful']

for each_word in vocab_train:
    probs[each_word]['positive'] = probs[each_word]['positive'] / positive_normalize
    probs[each_word]['negative'] = probs[each_word]['negative'] / negative_normalize
    probs[each_word]['deceptive'] = probs[each_word]['deceptive'] / deceptive_normalize
    probs[each_word]['truthful'] = probs[each_word]['truthful'] / truthful_normalize


"""

PRIOR PROBABILITIES

"""

deceptive_prior = 0
truthful_prior = 0
positive_prior = 0
negative_prior = 0

for each_class in class_dt_train:
    if each_class == 'deceptive':
        deceptive_prior += 1
    if each_class == 'truthful':
        truthful_prior += 1

for each_class in class_pn_train:
    if each_class == 'positive':
        positive_prior += 1
    if each_class == 'negative':
        negative_prior += 1


"""

TEST DATASET

"""

correct_answer = 0
wrong_answer = 0

confusion_matrix = [ [0,0],
                     [0,0]]

for each_index in range(len(test_indices)):
    test_data = tokenize(documents_test[each_index])
    # CLASS1
    positive_posterior = 0
    positive_final = 0
    # CLASS 2
    negative_posterior = 0
    negative_final = 0

    for each_word in test_data:
        try:
            positive_posterior += math.log(probs[each_word]['positive'])
            negative_posterior += math.log(probs[each_word]['negative'])
        except:
            # print(each_word,' found in test but NOT in train.')
            pass

    negative_final = negative_posterior * negative_prior
    positive_final = positive_posterior * positive_prior

    if positive_final > negative_final:
        temp_pred = 'positive'
    else:
        temp_pred = 'negative'

    temp_actual = class_pn_test[each_index]

    if temp_pred == temp_actual:
        correct_answer += 1
    else:
        wrong_answer += 1

    if temp_actual == 'positive':
        if temp_pred == 'positive':
            confusion_matrix[0][0] +=1
        if temp_pred == 'negative':
            confusion_matrix[0][1] +=1
    if temp_actual == 'negative':
        if temp_pred == 'positive':
            confusion_matrix[1][0] +=1
        if temp_pred == 'negative':
            confusion_matrix[1][1] +=1


print(correct_answer)
print(wrong_answer)
print('Accuracy = ',(correct_answer)/(correct_answer+wrong_answer))

print(confusion_matrix[0])
print(confusion_matrix[1])

precision_positive = confusion_matrix[0][0]/ (confusion_matrix[0][0]+confusion_matrix[0][1])
recall_positive = confusion_matrix[0][0]/(confusion_matrix[0][0]+confusion_matrix[1][0])

f1_positive = 2*precision_positive*recall_positive/(recall_positive + precision_positive)

precision_negative = confusion_matrix[1][1]/(confusion_matrix[1][1]+confusion_matrix[0][1])
recall_negative = confusion_matrix[1][1]/(confusion_matrix[1][1] + confusion_matrix[1][0])

f1_negative = 2*recall_negative*precision_negative/(recall_negative+precision_negative)

print('F1-Score Positive:',f1_positive)
print('F1-Score Negative:',f1_negative)

print('F1-Score Average',(f1_negative+f1_positive)*50)