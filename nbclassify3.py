import sys
import re
import math

deceptive_prior = 0
truthful_prior = 0
positive_prior = 0
negative_prior = 0
probs = {}

stop_words_dict = {'during': 0, 'has': 0, "it's": 0, 'very': 0, 'itself': 0, "why's": 0, "we'll": 0, 'hers': 0,
                       "isn't": 0, 'off': 0, 'we': 0, 'it': 0, 'the': 0, 'doing': 0, 'over': 0, 'its': 0, 'with': 0,
                       'so': 0, 'but': 0, 'they': 0, 'am': 0, 'until': 0, 'because': 0, "shouldn't": 0, "you're": 0,
                       'is': 0, "they're": 0, "you'd": 0, "mustn't": 0, 'would': 0, 'while': 0, 'should': 0, 'as': 0,
                       "i'd": 0, "we've": 0, 'when': 0, "wouldn't": 0, 'why': 0, "i'll": 0, 'theirs': 0, "aren't": 0,
                       'our': 0, 'from': 0, "we'd": 0, 'each': 0, 'only': 0, 'yourself': 0, 'been': 0, 'again': 0,
                       'of': 0,
                       'whom': 0, 'themselves': 0, 'or': 0, 'that': 0, 'me': 0, "how's": 0, 'those': 0, 'having': 0,
                       'was': 0, 'and': 0, 'few': 0,  'any': 0, 'being': 0, 'an': 0, "let's": 0, "they'd": 0,
                       'own': 0, 'his': 0, 'herself': 0, 'before': 0, 'did': 0, 'too': 0, 'here': 0, 'were': 0,
                       "that's": 0,
                       "what's": 0, "she'll": 0, 'i': 0, 'all': 0, 'have': 0, "weren't": 0, "you've": 0, "i'm": 0,
                       "he'd": 0, 'some': 0, 'into': 0, 'down': 0, 'this': 0, "she'd": 0, "i've": 0, 'do': 0,
                       "can't": 0,
                       'for': 0, 'below': 0, 'through': 0, "don't": 0, 'more': 0, 'once': 0, "didn't": 0, 'same': 0,
                       "she's": 0, "they've": 0, "he'll": 0,  'had': 0, 'such': 0, 'cannot': 0, 'about': 0,
                       'myself': 0, 'if': 0, "won't": 0, 'a': 0, 'how': 0, 'she': 0, 'you': 0, "we're": 0, "there's": 0,
                       'be': 0, 'yours': 0, "here's": 0, 'above': 0, 'at': 0, 'out': 0, 'does': 0, 'my': 0, 'to': 0,
                       'ought': 0, "hadn't": 0, "doesn't": 0, "couldn't": 0, 'he': 0, 'your': 0, 'ours': 0, 'up': 0,
                       'after': 0, "where's": 0, 'could': 0, 'under': 0, 'nor': 0, 'against': 0, 'further': 0,
                       "they'll": 0,
                       'what': 0, 'then': 0, "you'll": 0, 'ourselves': 0, 'which': 0, 'between': 0, "shan't": 0,
                       'these': 0,
                       'in': 0, 'their': 0, "who's": 0, "he's": 0, 'yourselves': 0, 'himself': 0, 'both': 0,
                       "wasn't": 0,
                       'him': 0, 'on': 0, 'them': 0, "when's": 0, 'there': 0, 'where': 0, 'than': 0, 'are': 0, 'her': 0,
                       "hasn't": 0, 'by': 0, 'other': 0, 'who': 0, "haven't": 0, 'most': 0}

"""

def tokenize(sentence):
    sentence = ' '.join(sentence)
    sentence = sentence.lower()

    sentence = sentence.split(' ')
    return_list = []

    for each_word in sentence:
        if each_word not in stop_words_dict:
            temp = re.sub(r'[^\w\s]', '', each_word.strip('\n'))
            import string
            for c in string.punctuation:
                temp = temp.replace(c, "")
            return_list.append(temp)

    return return_list

"""

def tokenize(sentence):
    sentence = ' '.join(sentence)
    sentence = sentence.lower().replace('.',' ').replace(',',' ').replace('&',' ').replace('/',' ').replace('-','')

    sentence = sentence.split(' ')
    return_list = []


    for each_word in sentence:
        if each_word not in stop_words_dict:
            temp = each_word.rstrip('\'\"-,.:;!?() ').lstrip('\'\"-,.:;!?()').strip('\n').strip('!')
            temp = re.sub(r'\d', '', temp)
            # temp = temp.rstrip('\'\"-,.:;!?()*<>+@ ').lstrip('\'\"-,.:;!?()*<>+@ ').strip('\n').strip('!')
            if len(temp)>1:
                return_list.append(temp)

    return return_list


def load_classifier(model_file_path):
    global deceptive_prior,truthful_prior,positive_prior,negative_prior,probs
    f = open(model_file_path,'r')


    temp = f.readline()
    deceptive_prior = float(temp.split(' ')[0])
    temp = f.readline()
    truthful_prior = float(temp.split(' ')[0])
    temp = f.readline()
    positive_prior = float(temp.split(' ')[0])
    temp = f.readline()
    negative_prior = float(temp.split(' ')[0])


    for each_line in f:
        temp_dict = {}
        values = each_line.split('|')
        temp_dict['deceptive'] = float(values[1])
        temp_dict['truthful'] = float(values[2])
        temp_dict['positive'] = float(values[3])
        temp_dict['negative'] = float(values[4])
        probs[values[0]] = temp_dict
    f.close()

def test_classifier(test_text):
    f = open(test_text,'r')


    output = open('nboutput.txt','w')
    for each_line in f:
        split_line = each_line.split(' ')
        test_key = split_line[0]
        test_data = split_line[1:]
        test_data = tokenize(test_data)

        # CLASS 1a
        positive_posterior = 0

        positive_final = 0

        # CLASS 1b
        negative_posterior = 0
        negative_final = 0

        # CLASS 2a
        deceptive_posterior = 0
        deceptive_final = 0
        # CLASS 2b
        truthful_posterior = 0
        truthful_final = 0

        for each_word in test_data:
            try:
                positive_posterior += math.log(probs[each_word]['positive'])
                negative_posterior += math.log(probs[each_word]['negative'])
                deceptive_posterior += math.log(probs[each_word]['deceptive'])
                truthful_posterior += math.log(probs[each_word]['truthful'])
            except:
                # print(each_word,' found in test but NOT in train.')
                pass


        negative_final = negative_posterior * negative_prior
        positive_final = positive_posterior * positive_prior

        deceptive_final = deceptive_posterior * deceptive_prior
        truthful_final = truthful_posterior * truthful_prior

        # print(negative_final,positive_final)

        if positive_final>negative_final:
            pred1 = 'positive'
        else:
            pred1 = 'negative'

        if deceptive_final>truthful_final:
            pred2 = 'deceptive'
        else:
            pred2 = 'truthful'
        output.write(str(test_key) + ' ' + str(pred2) + ' '+str(pred1)+'\n')

    output.close()


if __name__ == '__main__':
    args_list = sys.argv
    test_data_file = args_list[1]
    load_classifier('nbmodel.txt')
    test_classifier(test_data_file)
