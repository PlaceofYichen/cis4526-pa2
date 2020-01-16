'''
In PA 2, you might finish the assignment with only built-in types of Python 3.
However, one may choose to use higher level libraries such as numpy and scipy.
Add your code below the TO-DO statement and include necessary import statements.
'''

import sys
import csv
from sklearn import tree


def main():
    
    '''
    Get the first command line argument of the program.
    For example, sys.argv[1] could be a string such as 'breast_cancer.csv' or 'titanic_train.csv'
    '''
    #szDatasetPath = sys.argv[1]
	# Comment out the following line and uncomment the above line in your final submission
    szDatasetPath = 'breast_cancer.csv'
    #szDatasetPath = 'titanic_train.csv'

    '''
    Read the data from the csv file
    listColNames[j] stores the jth column name
    listData[i][:-1] are the features of the ith example
    listData[i][-1] is the target value of the ith example
    '''
    listColNames = [] # The list of column names
    listData = [] # The list of feature vectors of all the examples
    nRow = 0
    with open(szDatasetPath) as csvFile:
        csvReader = csv.reader(csvFile, delimiter=',')
        for row in csvReader:
            if 0 == nRow:
                listColNames = row
            else:
                listData.append(row)
            nRow += 1

    '''
    Scan the data and store the unique values of each column.
    listColUniqueVals[j] stores a list of unique values of the jth column
    '''
    listColUniqueVals = [[] for i in range(len(listColNames))]
    for example in listData:
        for i in range(len(example)):
            if example[i] not in listColUniqueVals[i]:
                listColUniqueVals[i].append(example[i])

    # For each feature, compute the training error of a one-level decision tree
    # TO-DO: add your code here
    
    numerical_cols_unique_vals = []
    for i, col in enumerate(listColUniqueVals):
        numerical_cols_unique_vals.append({})
        for k, v in enumerate(col):
            numerical_cols_unique_vals[i][v] = k
    
    
    
    X = []
    y = []
    for i, e in enumerate(listData):
        X.append([])
     
        for k, v in enumerate(e[:-1]):
            X[i].append(numerical_cols_unique_vals[k][v])
        y.append(numerical_cols_unique_vals[-1][e[-1]])
    
    num_steps = 10
    max_col = [max(col) for col in zip(*X)]
    min_col = [min(col) for col in zip(*X)]
    
    X_T = [list(col) for col in zip(*X)]

    for i in range(len(X[0])):  # For each of the features
        min_val, max_val = min_col[i], max_col[i]
        step_size = (max_val - min_val) / num_steps
        error_rates = []
        for j in range(0, int(num_steps) + 1):
            for inequal in ['lt', 'gt']:
                thresh = min_val + j * step_size
                pred_y = []
                if inequal == 'lt':
                    for v in X_T[i]:
                        if v <= thresh:
                            pred_y.append(0)
                        else:
                            pred_y.append(1.0)
                elif inequal == 'gt':
                    for v in X_T[i]:
                        if v > thresh:
                            pred_y.append(0)
                        else:
                            pred_y.append(1.0)
                
                error_num = 0
                for ii in range(len(y)):
                    if y[ii] != pred_y[ii]:
                        error_num += 1
                error_rates.append((error_num*1.0/len(y), inequal, thresh, min_val, max_val))
                
        res = min(error_rates)
        print("for feature {:12s}, min error rate is {:.4f} when value {} {}".format(listColNames[i], res[0], "<=" if res[1] == "lt" else ">", res[2]))
        
    
    

    # Construct a full decision tree on the dataset and compute the training error
    # TO-DO: add your code here
    
    print("*"*30, " full tree ", "*"*30)
    
    clf = tree.DecisionTreeClassifier()
    clf.fit(X, y)
    pred_y = clf.predict(X)
    
    error_num = 0
    for i in range(len(y)):
        if y[i] != pred_y[i]:
            error_num += 1
    
    print("for full decision tree, train error rate is {:.4f}".format(error_num*1.0/len(y)))

    return None

if __name__ == '__main__':

    main()
