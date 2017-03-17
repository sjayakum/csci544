
# import sys
# file_name = sys.argv[1]

file_name = 'catalan_corpus_dev_tagged.txt'
with open(file_name,'r',encoding='utf-8') as file_pointer:
    actual = file_pointer.read()
    actual  = actual.split('\n')


with open('hmmoutput.txt','r',encoding='utf-8') as file_pointer:
    predicted = file_pointer.read()
    predicted  = predicted.split('\n')


actual_tags = []
for each_line in actual:
    set_of_words = each_line.split(' ')
    temp_list = []
    for each_word in set_of_words:

        try:
            word,tag = each_word.rsplit('/',1)
        except:
            print (each_word)
        temp_list.append(tag)
    actual_tags.append(temp_list)

predicted_tags = []
for each_line in predicted:
    set_of_words = each_line.split(' ')
    temp_list = []
    for each_word in set_of_words:
        try:
            word, tag = each_word.rsplit('/',1)
        except:
            print (each_word)
        temp_list.append(tag)
    predicted_tags.append(temp_list)

import collections
confusion_matrix = collections.defaultdict(dict)

total_count = 0
misclassified_count = 0
for i in range(len(actual_tags)):
    for j in range(len(actual_tags[i])):
        total_count +=1
        if actual_tags[i][j] != predicted_tags[i][j]:
            if actual_tags[i][j] in confusion_matrix:
                if predicted_tags[i][j] in confusion_matrix[actual_tags[i][j]]:
                    confusion_matrix[actual_tags[i][j]][predicted_tags[i][j]] +=1
                else:
                    confusion_matrix[actual_tags[i][j]][predicted_tags[i][j]] = 1
            else:
                confusion_matrix[actual_tags[i][j]][predicted_tags[i][j]] = 1
            misclassified_count +=1

print (misclassified_count,'misclassified')
print (total_count)
print (100*float(total_count - misclassified_count)/total_count ,'Accuracy')


final_answer = []
print ('Count, Correct, Wrong')
for each_main_tag in confusion_matrix:
    for each_sub_tag in confusion_matrix[each_main_tag]:
        if confusion_matrix[each_main_tag][each_sub_tag] >=100:
            final_answer.append([confusion_matrix[each_main_tag][each_sub_tag],each_main_tag,each_sub_tag])

for each_answer in final_answer:
    print (each_answer)