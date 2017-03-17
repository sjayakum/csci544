f = 0

data_set_words_split = []

solution_tags = []

from io import open
from collections import defaultdict
import copy
import math

transition_matrix = defaultdict(dict)
emission_matrix = defaultdict(dict)


def load_data(file_name):
    global f, data_set_words_split
    with open(file_name, 'r', encoding='utf-8') as file_pointer:
        f = file_pointer.read()
        lines = f.split('\n')
        for each_line in lines:
            list_of_words = each_line.split(' ')
            temp_list_words = ['']
            for each_word in list_of_words:
                temp_list_words.append(each_word)
            data_set_words_split.append(temp_list_words)


def read_model():
    import json
    global transition_matrix
    global emission_matrix
    with open('hmmmodel.txt', 'r', encoding='utf-8') as file_pointer:
        f_new = file_pointer

        hmmmodel = json.load(f_new)

        transition_matrix = hmmmodel['transition']
        emission_matrix = hmmmodel['emission']


def viterbi_algorithm(sentence):
    def my_function(word):
        import re
        temp1 =  bool(re.search(r'\d', word))
        temp2 =  bool(re.search('_',word))
        return temp1 and (not temp2)
        pass
    start_state = 'Q0'
    T = len(sentence)
    set_of_states = transition_matrix.keys()
    set_of_states = list(set_of_states)
    set_of_states.remove('Q0')

    probability = {}
    back_pointer = {}

    given_sentence = sentence

    for each_state in set_of_states:

        if given_sentence[1] in emission_matrix[each_state]:
            probability[(1, each_state)] = transition_matrix[start_state][each_state] * emission_matrix[each_state][
                given_sentence[1]]
        else:
            probability[(1, each_state)] = transition_matrix[start_state][each_state]

        if my_function(given_sentence[1]):
            if each_state == 'ZZ':
                probability[(1, each_state)] = 1

        back_pointer[(1, each_state)] = start_state

    for i in range(2, T):
        for state in set_of_states:



            probability[(i, state)] = float('-inf')
            back_pointer[(i, state)] = None

            for q_dash in set_of_states:

                if given_sentence[i] in emission_matrix[state]:
                    val = probability[(i - 1, q_dash)] * transition_matrix[q_dash][state] * emission_matrix[state][
                        given_sentence[i]]
                else:
                    val = probability[(i - 1, q_dash)] * transition_matrix[q_dash][state]

                if my_function(given_sentence[i]):
                    if each_state == 'ZZ':
                        probability[(i, state)] = 1
                        back_pointer[(i,state)] = q_dash


                if val > probability[(i, state)]:
                    probability[(i, state)] = val
                    back_pointer[(i, state)] = q_dash

    # print probability
    # print back_pointer
    final_state = 0
    max_value = float('-inf')

    final_answer = []

    for each_key in probability.keys():
        if each_key[0] == T - 1:
            if probability[each_key] > max_value:
                max_value = probability[each_key]
                final_state = each_key[1]

    # print final_state

    previous_state = final_state
    for i in reversed(range(1, T)):
        final_answer.append((i, previous_state))
        new_state = back_pointer[(i, previous_state)]

        previous_state = new_state

    final_answer.append((i - 1, previous_state))

    final_answer.reverse()

    return final_answer


def test_model():
    global solution_tags
    # print data_set_words_split
    for each_sentence in data_set_words_split:
        return_answer = viterbi_algorithm(each_sentence)
        new_return_answer = []
        for each_answer in return_answer:
            new_return_answer.append(each_answer[1])
        return_answer = new_return_answer

        # return_answer = map(lambda x:x[1],return_answer)
        solution_tags.append(return_answer)

    pass


def write_answer_to_file():
    # hmmoutput.txt
    f = open('hmmoutput.txt', 'w', encoding='utf-8')

    # for i in range(len(data_set_words_split)):
    #     big_string = ""
    #
    #     for j in range(1, len(data_set_words_split[i])):
    #         print data_set_words_split[i][j]


    for i in range(len(data_set_words_split)):
        big_string = """"""
        for j in range(1, len(data_set_words_split[i])):
            big_string = big_string + str(data_set_words_split[i][j]) + '/' + str(solution_tags[i][j]) + ' '
        f.write(big_string.rstrip(' ') + '\n')

    f.close()


if __name__ == '__main__':
    import sys

    file_name = sys.argv[1]
    # file_name = 'catalan_corpus_dev_raw.txt'
    load_data(file_name)
    read_model()
    test_model()
    write_answer_to_file()
