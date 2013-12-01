__author__ = 'jheaton'

import os
import sys
import numpy as np

# Find the AIFH core files
aifh_dir = os.path.dirname(os.path.abspath(__file__))
aifh_dir = os.path.abspath(aifh_dir + os.sep + ".." + os.sep + "lib" + os.sep + "aifh")
sys.path.append(aifh_dir)

from normalize import Normalize


def multi_linear_regression(x,y):
    x_matrix = np.ones((len(x),len(x[0])+1),dtype=float)
    x_matrix[:,1:] = x
    print(y)
    return np.linalg.lstsq(x_matrix,y)[0]

def calc_linear_regression(coeff,x):
    result = 0
    for i in xrange(1,len(coeff)) :
        result += x[i - 1] * coeff[i]

    result += coeff[0]
    return result


# find the Iris data set
abaloneFile = os.path.dirname(os.path.realpath(__file__))
abaloneFile = os.path.abspath(abaloneFile + "../../datasets/abalone.csv")

# Normalize abalone file.

norm = Normalize()
abalone_work = norm.load_csv(abaloneFile)

# Make all columns beyond col #1 numeric.
for i in range(1, 9):
    norm.make_col_numeric(abalone_work, i)

# Discover all of the classes for column #1, the gender.
classes = norm.build_class_map(abalone_work, 0)

# Normalize gender one-of-n encoding.
norm.norm_col_one_of_n(abalone_work, 0, classes, 0, 1)

# Separate into input and ideal.

training = np.array(abalone_work)
training_input = training[:, 0:10]
training_ideal = training[:, 10:11]

coeff = multi_linear_regression(training_input,training_ideal)

print("Solution coefficients: " + coeff)

for i in range(0,len(training_input)) :
    row = training_input[i]
    y = calc_linear_regression(coeff,row)
    print( " -> Actual: " + str(y) + ", Ideal:" + str(training_ideal[i][0]))