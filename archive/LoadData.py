
stop_words_dict= {'': 0, 'all': 0, 'these': 0, 'are': 0, "weren't": 0, "they're": 0, 'those': 0, 'why': 0, 'under': 0, 'same': 0, "aren't": 0, 'his': 0, 'her': 0, 'had': 0, "she'd": 0, 'no': 0, 'your': 0, 'not': 0, 'because': 0, 'they': 0, 'which': 0, 'further': 0, "hadn't": 0, "he's": 0, 'while': 0, 'himself': 0, "here's": 0, "doesn't": 0, "you'll": 0, 'so': 0, "wasn't": 0, 'that': 0, "hasn't": 0, "we'll": 0, 'any': 0, "you'd": 0, "we'd": 0, "shouldn't": 0, 'nor': 0, 'their': 0, 'who': 0, 'into': 0, 'were': 0, 'some': 0, 'whom': 0, 'over': 0, "she's": 0, 'each': 0, "they'll": 0, 'until': 0, 'me': 0, "what's": 0, 'of': 0, 'themselves': 0, 'being': 0, 'against': 0, 'or': 0, "you're": 0, "where's": 0, "i'll": 0, 'from': 0, 'him': 0, 'is': 0, 'out': 0, 'on': 0, "i've": 0, 'theirs': 0, 'about': 0, 'few': 0, 'could': 0, "haven't": 0, "they've": 0, "don't": 0, 'been': 0, "couldn't": 0, "how's": 0, 'has': 0, 'only': 0, 'you': 0, 'yours': 0, 'most': 0, 'she': 0, "it's": 0, 'when': 0, 'ought': 0, 'did': 0, "can't": 0, "she'll": 0, 'down': 0, "why's": 0, "we've": 0, "let's": 0, "isn't": 0, 'here': 0, "mustn't": 0, 'where': 0, 'again': 0, "that's": 0, 'should': 0, 'hers': 0, 'an': 0, "who's": 0, 'do': 0, 'other': 0, 'be': 0, 'if': 0, "wouldn't": 0, 'then': 0, 'but': 0, 'between': 0, 'once': 0, 'at': 0, 'too': 0, 'both': 0, 'its': 0, "i'm": 0, 'and': 0, "didn't": 0, 'to': 0, 'through': 0, 'than': 0, 'our': 0, 'how': 0, 'in': 0, 'he': 0, 'herself': 0, "when's": 0, 'yourself': 0, 'cannot': 0, 'having': 0, 'was': 0, 'them': 0, 'itself': 0, "shan't": 0, "he'd": 0, 'there': 0, "he'll": 0, 'would': 0, "you've": 0, 'myself': 0, 'it': 0, 'i': 0, 'during': 0, 'am': 0, "i'd": 0, "there's": 0, 'off': 0, 'very': 0, 'below': 0, 'what': 0, 'a': 0, 'own': 0, 'up': 0, 'above': 0, 'my': 0, "they'd": 0, 'does': 0, "won't": 0, 'before': 0, 'by': 0, 'for': 0, 'such': 0, 'ours\tourselves': 0, 'yourselves': 0, 'more': 0, 'the': 0, 'this': 0, 'as': 0, 'we': 0, 'have': 0, "we're": 0, 'with': 0, 'doing': 0, 'after': 0}

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

keys = {}
words = []








i = 0

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

# print(words[:2])
# print(class1[:2])
# print(class2[:2])


import collections

probs  = collections.defaultdict(dict)

vocab = []

for each_sentence in words:
    for each_word in each_sentence:
        vocab.append(each_word)

vocab = set(vocab)

for each_vocab in vocab:
    temp_dict = {}
    temp_dict['positive']=0
    temp_dict['negative']=0
    temp_dict['deceptive']=0
    temp_dict['truthful']=0
    probs[each_vocab] = temp_dict


deceptive_prior = 0
truthful_prior = 0
positive_prior = 0
negative_prior = 0

for each_class in class1:
    if each_class == 'deceptive':
        deceptive_prior += 1
    if each_class == 'truthful':
        truthful_prior += 1

for each_class in class2:
    if each_class == 'positive':
        positive_prior += 1
    if each_class == 'negative':
        negative_prior += 1

deceptive_prior = (deceptive_prior / len(class1))
truthful_prior = (truthful_prior / len(class1))
positive_prior = (positive_prior / len(class1))
negative_prior = (negative_prior / len(class1))

positive_words_count = {}
negative_words_count = {}

for i in range(len(class1)):
    if class2[i] == 'positive':
        for each_word in words[i]:
            probs[each_word]['positive']+=1
            if each_word not in positive_words_count:
                positive_words_count[each_word] = 1
            else:
                positive_words_count[each_word] += 1

    if class2[i] == 'negative':
        probs[each_word]['negative'] += 1
        for each_word in words[i]:
            if each_word not in negative_words_count:
                negative_words_count[each_word] = 1
            else:
                negative_words_count[each_word] += 1

truthful_words_count = {}
deceptive_words_count = {}

for i in range(len(class1)):
    if class1[i] == 'deceptive':
        probs[each_word]['deceptive'] += 1
        for each_word in words[i]:
            if each_word not in deceptive_words_count:
                deceptive_words_count[each_word] = 1
            else:
                deceptive_words_count[each_word] += 1

    if class1[i] == 'truthful':
        probs[each_word]['truthful'] += 1
        for each_word in words[i]:
            if each_word not in truthful_words_count:
                truthful_words_count[each_word] = 1
            else:
                truthful_words_count[each_word] += 1

positive_words_count = {k: v / total for total in (sum(positive_words_count.values()),) for k, v in
                        positive_words_count.items()}
negative_words_count = {k: v / total for total in (sum(negative_words_count.values()),) for k, v in
                        negative_words_count.items()}

truthful_words_count = {k: v / total for total in (sum(truthful_words_count.values()),) for k, v in
                        truthful_words_count.items()}
deceptive_words_count = {k: v / total for total in (sum(deceptive_words_count.values()),) for k, v in
                         deceptive_words_count.items()}

# print(positive_words_count)


print(probs)

test_data_point_number = 1245


import math
test_data = tokenize(words[test_data_point_number])
print(' '.join(words[test_data_point_number]))

#CLASS1
positive_posterior = 0
positive_final = 0

for each_word in test_data:
    try:
        positive_posterior += math.log(positive_words_count[each_word])
    except:
        pass

positive_final = positive_posterior * positive_prior


#CLASS 2

negative_posterior = 0
negative_final = 0

for each_word in test_data:
    try:
        negative_posterior += math.log(negative_words_count[each_word])
    except:
        print(each_word,' not in source')
        pass

negative_final = negative_posterior * negative_prior

print(positive_final,negative_final)


if positive_final > negative_final:
    print('POSITIVE')
else:
    print('NEGATIVE')


print(class2[test_data_point_number])