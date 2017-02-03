training_percentage = 0.8
import random

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


def tokenize(sentence):
    sentence = ' '.join(sentence)
    sentence = sentence.lower()

    sentence = sentence.split(' ')
    return_list = []

    for each_word in sentence:
        if each_word not in stop_words_dict:
            return_list.append(each_word.strip('\n'))

    return return_list


f = open('train-text.txt', 'r')
l = open('train-labels.txt', 'r')

i = 0
keys = {}
words = []

for each_line in f:
    temp = each_line.split(' ')
    keys[temp[0]] = i
    i += 1
    words.append(tokenize(list(temp[1:])))

class1 = [0] * len(words)
class2 = [0] * len(words)

for each_line in l:
    temp = each_line.split(' ')
    class1[keys[temp[0]]] = temp[1].strip('\n')
    class2[keys[temp[0]]] = temp[2].strip('\n')

import collections

probs = collections.defaultdict(dict)

vocab = []

for each_sentence in words:
    for each_word in each_sentence:
        vocab.append(each_word)

vocab = set(vocab)

total_set = range(len(words))
training_set = random.sample(total_set,int(0.8*len(total_set)))
testing_set = list(set(total_set) - set(training_set))

print(training_set)
print(testing_set)


train_words  = 0
train_class1 = 0
train_class2 = 0

test_words = 0
test_class1 = 0
test_class2 = 0

