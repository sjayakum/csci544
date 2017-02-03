
f = open('stop_words')

stop_words_dict = {}
for each_line in f:
    stop_words_dict[each_line.strip('\n')] = 0

print(stop_words_dict)