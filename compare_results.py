import sys
import collections

def compare(actual_file_path,predicted_file_path):
    correct_answer = 0
    wrong_answer = 0

    confusion_matrix = [[0, 0],
                        [0, 0]]

    confusion_matrix2 = [[0, 0],
                        [0, 0]]

    actual_data = collections.defaultdict(list)

    actual_file = open(actual_file_path,'r')
    predicted_file = open(predicted_file_path,'r')

    for each_line in actual_file:
        temp = each_line.strip('\n').split(' ')
        actual_data[temp[0]] =list([temp[1],temp[2]])

    for each_line in predicted_file:
        temp = each_line.strip('\n').split(' ')
        actual_answer = actual_data[temp[0]]
        predicted_answer = [temp[1],temp[2]]


        if actual_answer[0] == 'truthful':
            if predicted_answer[0] == 'truthful':
                confusion_matrix[0][0] += 1
            if predicted_answer[0] == 'deceptive':
                confusion_matrix[0][1] += 1
        if actual_answer[0] == 'deceptive':
            if predicted_answer[0] == 'truthful':
                confusion_matrix[1][0] += 1
            if predicted_answer[0] == 'deceptive':
                confusion_matrix[1][1] += 1

        if actual_answer[1] == 'positive':
            if predicted_answer[1] == 'positive':
                confusion_matrix2[0][0] += 1
            if predicted_answer[1] == 'negative':
                confusion_matrix2[0][1] += 1

        if actual_answer[1] == 'negative':
            if predicted_answer[1] == 'positive':
                confusion_matrix2[1][0] += 1
            if predicted_answer[1] == 'negative':
                confusion_matrix2[1][1] += 1


    precision_truthful = confusion_matrix[0][0] / (confusion_matrix[0][0] + confusion_matrix[0][1])
    recall_truthful = confusion_matrix[0][0] / (confusion_matrix[0][0] + confusion_matrix[1][0])

    f1_truthful = 2 * precision_truthful * recall_truthful / (recall_truthful + precision_truthful)

    precision_deceptive = confusion_matrix[1][1] / (confusion_matrix[1][1] + confusion_matrix[0][1])
    recall_deceptive = confusion_matrix[1][1] / (confusion_matrix[1][1] + confusion_matrix[1][0])

    f1_deceptive = 2 * recall_deceptive * precision_deceptive / (recall_deceptive + precision_deceptive)

    precision_positive = confusion_matrix2[0][0] / (confusion_matrix2[0][0] + confusion_matrix2[0][1])
    recall_positive = confusion_matrix2[0][0] / (confusion_matrix2[0][0] + confusion_matrix2[1][0])

    f1_positive = 2 * precision_positive * recall_positive / (recall_positive + precision_positive)

    precision_negative = confusion_matrix2[1][1] / (confusion_matrix2[1][1] + confusion_matrix2[0][1])
    recall_negative = confusion_matrix2[1][1] / (confusion_matrix2[1][1] + confusion_matrix2[1][0])

    f1_negative = 2 * recall_negative * precision_negative / (recall_negative + precision_negative)

    accuracy = ( f1_negative + f1_positive + f1_deceptive + f1_truthful)/4

    print('Weighted Average F1- ',accuracy)
    print('Precision,Recall,F1  [N P D T]')
    print(precision_negative,recall_negative,f1_negative)
    print(precision_positive,recall_positive,f1_positive)
    print(precision_deceptive,recall_deceptive,f1_deceptive)
    print(precision_truthful,recall_truthful,f1_truthful)

if __name__ == '__main__':
    args_list = sys.argv
    actual_file = args_list[1]
    predicted_file = args_list[2]
    compare(actual_file,predicted_file)
