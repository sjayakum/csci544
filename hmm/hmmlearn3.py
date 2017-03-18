f = 0
vocab = []
data_set_tags = []
data_set_words_split = []
distinct_tags = []

from io import open


def load_data(file_name):
    global f, vocab,data_set_tags,data_set_words_split,distinct_tags


    with open(file_name, 'r',encoding='utf-8') as file_pointer:
        f = file_pointer.read()
        lines = f.split('\n')
        lines.remove('')
        list_of_all_tags = ['Q0']
        for each_line in lines:
            list_of_words = each_line.split(' ')
            temp_list_tags = ['Q0']
            temp_list_words = ['']
            for each_word in list_of_words:
                word, tag = each_word.rsplit('/', 1)

                temp_list_tags.append(tag)
                temp_list_words.append(word)

                list_of_all_tags.append(tag)
                vocab.append(word)

            data_set_tags.append(temp_list_tags)
            data_set_words_split.append(temp_list_words)

        vocab = set(vocab)
        distinct_tags = set(list_of_all_tags)






from collections import defaultdict
import copy
import math

transition_matrix = defaultdict(dict)
emission_matrix = defaultdict(dict)

def build_transition():
    global transition_matrix
    temp_dict = {}
    for each_tag in distinct_tags:
        temp_dict[each_tag] = 0

    for each_tag in distinct_tags:
        transition_matrix[each_tag] = copy.deepcopy(temp_dict)

    for k in range(len(data_set_tags)):
        for j in range(1,len(data_set_tags[k])):
            transition_matrix[data_set_tags[k][j-1]][data_set_tags[k][j]] +=1


    for each_main_key in transition_matrix:
        for each_sub_key in transition_matrix[each_main_key]:
            transition_matrix[each_main_key][each_sub_key] +=1

    for each_main_key in transition_matrix:
        norm_value = 0
        for each_sub_key in transition_matrix[each_main_key]:
            norm_value += transition_matrix[each_main_key][each_sub_key]

        for each_sub_key in transition_matrix[each_main_key]:
            transition_matrix[each_main_key][each_sub_key] /= float(norm_value)




def build_emission():
    global emission_matrix

    # for each_tag in distinct_tags:
    #     if each_tag == 'Q0':
    #         continue
    #     for each_word in vocab:
    #         emission_matrix[each_tag][each_word] = 0

    for each_tag in distinct_tags:
        if each_tag == 'Q0':
            continue
        emission_matrix[each_tag] = {}


    for i in range(len(data_set_tags)):
        set_tags = data_set_tags[i]
        set_sentence_split = data_set_words_split[i]

        for j in range(1, len(set_tags)):
            current_tag = set_tags[j]
            current_word  = set_sentence_split[j]

            if current_word in emission_matrix[current_tag]:
                emission_matrix[current_tag][current_word] +=1
            else:
                emission_matrix[current_tag][current_word] = 1


    # for i in range(len(data_set_tags)):
    #     set_tags = data_set_tags[i]
    #     set_sentence_split = data_set_words_split[i]
    #     for j in range(1, len(set_tags)):
    #         current_word = set_sentence_split[j]
    #         current_tag = set_tags[j]
    #         emission_matrix[current_tag][current_word] += 1


    for each_main_key in emission_matrix.keys():
        if each_main_key =='Q0':
            continue
        norm_constant = 0

        for each_sub_key in emission_matrix[each_main_key]:
            norm_constant += emission_matrix[each_main_key][each_sub_key]



        for each_sub_key in emission_matrix[each_main_key].keys():
            emission_matrix[each_main_key][each_sub_key] /= float(norm_constant)



def write_model():

    f_new = open('hmmmodel.txt','w',encoding='utf-8')
    hmmmodel = {}
    hmmmodel['transition'] = transition_matrix
    hmmmodel['emission'] = emission_matrix




    import json

    json.dump(hmmmodel,f_new)

    #
    # json_obj = json.dumps(hmmmodel)
    #
    # f_new.write(json_obj)

    f_new.close()


if __name__ == '__main__':
    import sys
    file_name = sys.argv[1]
    # file_name = 'catalan_corpus_train_tagged.txt'
    load_data(file_name)

    build_transition()
    build_emission()

    write_model()