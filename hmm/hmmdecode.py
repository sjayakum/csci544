f = 0

data_set_words_split = []

solution_tags = []


from collections import defaultdict
import copy
import math

transition_matrix = defaultdict(dict)
emission_matrix = defaultdict(dict)


def load_data(file_name):
    global f, data_set_words_split
    with open(file_name, 'r') as file_pointer:
        f = file_pointer.read()
        lines = f.split('\n')
        for each_line in lines:
            list_of_words = each_line.split(' ')
            temp_list_words = ['']
            for each_word in list_of_words:
                temp_list_words.append(str(each_word))
            data_set_words_split.append(temp_list_words)



def read_model():
    import json
    global transition_matrix
    global emission_matrix
    with open('hmmmodel.txt', 'r') as file_pointer:
        f_new = file_pointer.read()


        hmmmodel = json.loads(f_new)

        transition_matrix = hmmmodel['transition']
        emission_matrix = hmmmodel['emission']


def viterbi_algorithm(sentence):


    start_state = 'Q0'
    T = len(sentence)
    set_of_states = transition_matrix.keys()

    probability = {}
    back_pointer = {}

    given_sentence = sentence

    for each_state in set_of_states:

        probability[(1,each_state)] = transition_matrix[start_state][each_state]*emission_matrix[each_state][given_sentence[1]] if given_sentence[1] in emission_matrix[each_state] else transition_matrix[start_state][each_state]
        if len(given_sentence[1]) == 1 and each_state == 'FF' and not given_sentence[1].isalnum():
            probability[(1,each_state)] = 1

        # if len(given_sentence[1]) == 1 and each_state == 'SP' and  given_sentence[1].isalnum():
        #         probability[(1, each_state)] = 1

        back_pointer[(1,each_state)] = start_state

    for i in range(2,T):
        for state in set_of_states:

            probability[(i,state)] = float('-inf')
            if len(given_sentence[i]) == 1 and state == 'FF' and not given_sentence[1].isalnum():
                probability[(i, state)] = 1

            # if len(given_sentence[i]) == 1 and state == 'SP' and  given_sentence[1].isalnum():
            #     probability[(i, state)] = 1

            back_pointer[(i,state)] = 0
            temp = float('-inf')
            for q_dash in set_of_states:

                probability[(i,state)] = max(probability[(i,state)],    probability[(i-1,q_dash)]*transition_matrix[q_dash][state]*emission_matrix[state][given_sentence[i]] if given_sentence[i] in emission_matrix[state] else probability[(i-1,q_dash)]*transition_matrix[q_dash][state])

                val = probability[(i-1, q_dash)]*transition_matrix[q_dash][state]
                if val > temp:
                    temp = val
                    back_pointer[(i, state)] = q_dash

    # print probability
    # print back_pointer
    final_state = 0
    max_value = float('-inf')

    final_answer = []

    for each_key in probability.keys():
        if each_key[0] == T-1:
            if probability[each_key] > max_value:
                max_value = probability[each_key]
                final_state = each_key[1]

    # print final_state

    previous_state = final_state
    for i in reversed(range(1, T)):
        new_state = back_pointer[(i, previous_state)]
        final_answer.append((i, previous_state))
        previous_state = new_state

    final_answer.append((i - 1, previous_state))

    final_answer.reverse()
    return final_answer



def test_model():
    global solution_tags
    for each_sentence in data_set_words_split:
        return_answer = viterbi_algorithm(each_sentence)
        return_answer = map(lambda x:x[1],return_answer)
        solution_tags.append(return_answer)



    pass
def write_answer_to_file():

    #hmmoutput.txt
    f = open('hmmoutput.txt','w')

    for i in range(len(data_set_words_split)):
        big_string = """"""
        for j in range(1,len(data_set_words_split[i])):
            big_string = big_string +  str(data_set_words_split[i][j])+'/' + str(solution_tags[i][j]) + ' '
        f.write(big_string.rstrip(' ')+'\n')


    f.close()
if __name__ == '__main__':
    import sys
    file_name = sys.argv[1]
    load_data(file_name)
    read_model()
    test_model()
    write_answer_to_file()



