# importing all the Required Libraries.
######################################
import random
import json
import pickle

import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer

from keras.models import Sequential
from keras.layers import Dense , Activation , Dropout
from keras.optimizers import SGD
#####################################

# Instantiating the object for lemmatization.
lemmatizer = WordNetLemmatizer()

# Loading the json file.
intents = json.load(open('C:/Users/saich/OneDrive/Desktop/chat app - Backup/intents.json',encoding="utf-8"))
print(intents)

# Creating the empty list for storing each words in the intent file.
words = []
classes = []
documents = []
ignore_letters = ['?' , '!' , '.' , ',']


# Looping through all 'intents.json' file tokenizing them and storing each of them in a list.
for intents in intents['intents']:
    for pattern in intents['patterns']:
        word_list = nltk.word_tokenize(pattern)
        words.extend(word_list)
        documents.append((word_list,intents['tag']))
        if intents['tag'] not in classes:
            classes.append(intents['tag'])

# Lemmatizing each word in the 'words' List.
words = [lemmatizer.lemmatize(word) for word in words if word not in ignore_letters ]

# Removing and Sorting the duplicates from the 'words' list.
words = sorted(set(words))

# Removing and Sorting the duplicates from the 'classes' list.
classes = sorted(set(classes))

# Saving the files (words & classes) using the pickle library.
pickle.dump(words,open('words.pkl','wb')) 
pickle.dump(classes,open('classes.pkl','wb'))

# Converting the text corpus to a binary format using bag of words.
training = []
output_empty = [0] * len(classes)

for document in documents:
    bag = []
    word_patterns = document[0]
    word_patterns = [lemmatizer.lemmatize(word.lower()) for word in word_patterns]
    for word in words:
        bag.append(1) if word in word_patterns else bag.append(0)

    output_row = list(output_empty)
    output_row[classes.index(document[1])] = 1
    training.append([bag,output_row])


random.shuffle(training)
training = np.array(training)


# Storing them in train_x and train_y.
train_x = list(training[:,0])
train_y = list(training[:,1])


# Building the neural network.
model = Sequential()
model.add(Dense(128,input_shape = (len(train_x[0]),),activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(64,activation='relu'))
model.add(Dense(len(train_y[0]),activation='softmax'))

sgd = SGD(learning_rate=0.01,momentum=0.9,nesterov=True)
model.compile(loss='categorical_crossentropy',optimizer=sgd,metrics=['accuracy'])

# Passing the training data (train_x and train_y) to the model. 
hist = model.fit(np.array(train_x),np.array(train_y),epochs=500,batch_size=5,verbose=1)
model.save('chatbot_model.h5',hist)
print('Done..')
