# csci544

Naive Bayes classifier to identify hotel reviews as either truthful or deceptive, and either positive or negative. 


## Procedure

1. Split the given data into training and test set using random sampling.

2. Further, keep a part of training data as development set.

3. Create a Naive-Bayes Classifier using the training data and store the model parameters into a file `nbmodel.txt`

4. Use the development data to further generate the ouput label for each datapoint.

5. Compare the actual and predicted labels and calulate the Precision, Recall and F-1 score

Run the shell script that automates this pipeline completely.

`sh main.sh`

## Naive-Bayes Model Features and Parameters

Used unigram bag-of-words model as features.

Applied Laplace (Add-1) smoothing to overcome zero probabilities.

Further, Ignored tokens that are not part of intitial training vocabulary.


