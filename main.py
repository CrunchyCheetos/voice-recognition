# main.py       #
# Joseph Patton #

from components import get_data
from components import normalize_data
from rbf import train_rbf
from rbf import evaluate_point
import numpy as np


###################################################################
#
# Open audio file and extract training data from file
#
###################################################################

wav_file = './audio_files/obama_ns.wav'
isthisobama = 1  # this audio is obama
training_data = get_data(wav_file,isthisobama)

wav_file = './audio_files/obama2_ns.wav'
isthisobama = 1  # this audio is obama
training_data = np.vstack((training_data,get_data(wav_file,isthisobama)))

wav_file = './audio_files/romney_ns.wav'
isthisobama = 0  # this audio is not obama
training_data = np.vstack((training_data,get_data(wav_file,isthisobama)))

wav_file = './audio_files/sanders_ns.wav'
isthisobama = 0  # this audio is not obama
training_data = np.vstack((training_data,get_data(wav_file,isthisobama)))

# normalize data to [0,1] and shuffle it #
training_data = normalize_data(training_data)
np.random.shuffle(training_data)


###################################################################
#
# Train RBF with training data
#
###################################################################

learning_rate   = 0.00001
data_dimensions = 17
cluster_num     = data_dimensions
weights,afa = train_rbf(learning_rate,training_data[0:1200],data_dimensions,cluster_num)


###################################################################
#
# Test RBF with found weights and activation function parameters
#
###################################################################

true_pos = 0
true_neg = 0
false_pos = 0
false_neg = 0
for data in training_data[1200::]:
    val = evaluate_point(afa,weights,data[0:data_dimensions])
    # if data point is obama #
    if data[-1] == 1:
        if val >= 0.5:
            true_pos += 1
        else:
            false_neg += 1
    # if data point is not obama #
    else:
        if val < 0.5:
            true_neg += 1
        else:
            false_pos += 1
print(f'Pos ID Success: {100*true_pos/(true_pos+false_pos)}%')
print(f'Neg ID Success: {100*true_neg/(true_neg+false_neg)}%')
print(f'Overall Success: {100*(true_pos+true_neg)/(false_pos+false_neg+true_pos+true_neg)}%')
