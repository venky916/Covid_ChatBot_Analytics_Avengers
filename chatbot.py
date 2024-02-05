# Importing all the required libraries.
######################################
import random
import json 
import pickle
import numpy as np

import nltk
from nltk.stem import WordNetLemmatizer

from keras.models import load_model
######################################

# Instantiating the class for lemmatizer.
lemmatizer = WordNetLemmatizer()

# Opening the json file.
intents = json.load(open('C:/Users/saich/OneDrive/Desktop/chat app - Backup/intents.json',encoding="utf-8"))

# Storing the words and classes file that are stored using pickle.
words = pickle.load(open('words.pkl','rb'))
classes = pickle.load(open('classes.pkl','rb'))
print(words)
print(classes)

# Loading the model.
model = load_model('chatbot_model.h5')

# Cleaning the Sentence.
def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word) for word in sentence_words]
    return sentence_words

# Making Bag of words with the sentence.
def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for w in sentence_words:
        for i,word in enumerate(words):
            if word == w:
                bag[i] = 1
    return np.array(bag)

# Predicting the words by passing the array.
def predict_class(sentence):
    sentence = sentence.lower()
    bow = bag_of_words(sentence)
    res = model.predict(np.array([bow]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i,r] for i,r in enumerate(res) if r > ERROR_THRESHOLD]
    results.sort(key=lambda x : x[1],reverse=True)
    return_list = []
    for r in results:
        if 1 in bow:
            return_list.append({'intent' : classes[r[0]],'probability': str(r[1])})
        else:
            return_list.append({'intent' : 'random','probability': str("0.99")})
    return return_list

# Function for getting the response from the bot.
def get_response(intents_list,intents_json):
    tag = intents_list[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if i['tag'] == tag:
            result = random.choice(i['responses'])
            break
    return result

# Creating the starting Print statements.
# print('\n')
# print("Welcome to Makonis Software Solutions")
# print("_"*38,"\n")
# print("Ask any Queries regarding Makonis Software Solutions (quit or exit if u want to end the chat !)\n")
# options = ["services","contacts","about us","ai"]
# print("Select any option : \n")
# no = 1
# for i in options:
#     print(str(no)+")",i,"\n")
#     no+=1

# message = predict_class("oyugfsdauf")

# print(message)

# response = get_response(message,intents)


# Code for the input and output predictions
# while True:
    # message = input("User (Main) : ")
    # if message.lower() == "exit" or message.lower() == 'quit':
    #     break
    # elif message == ' ' or message == '':
    #     print("I could'nt get it can u write a proper text !") 
    # elif message == '1' or message == 'services':
    #     message = 'services'
    #     ints = predict_class(message)
    #     res = get_response(ints,intents)
    #     no = 1
    #     print("\nMakonis Provide these Services : \n")
    #     for i in res.split(","):
    #         print(str(no)+")",i,"\n")
    #         no+=1
    #     print("Want to know further details please select any option above : (Enter 'back' to the main page)\n")
    #     print("_"*20,"\n")
    #     print("Service page\n")
    #     while True :
    #         message = input("User (Service) : ")
    #         message = message.lower()
    #         if message == "1" or message == "Testing":
    #             print("\nThis is the testing box\n")
    #         elif message == "2" or message == "Analytics":
    #             print("\nThis is the analytics box\n")
    #         elif message == "3" or message == "web development":
    #             print("\nThis is the web development box\n")
    #         elif message == "4" or message == "Mobile Development":
    #             print("\nThis is the mobile development box\n")
    #         elif message == "5" or message == "Internet of things":
    #             print("\nThis is the IOT box\n")
    #         elif message == "6" or message == "Embedded systems":
    #             print("\nThis is the Embedded systems box\n")
    #         elif message == "7" or message == "E-Learning services":
    #             print("\nThis is the E-learning Service box\n")
    #         elif message.lower() == "back" or message.lower() == 'go back' or message.lower() == 'exit' or message.lower() == 'quit':
    #             break
    #         else:
    #             print("\nEnter the correct option...\n")
    # elif message == '2' or message == 'contacts':
    #     message = 'any contacts'
    #     ints = predict_class(message)
    #     res = get_response(ints,intents)
    #     print("Bot :",res)
    # elif message == '3' or message == 'about us' :
    #     message = "a brief intro of makonis"
    #     ints = predict_class(message)
    #     res = get_response(ints,intents)
    #     print("Bot :",res)
    # elif message == '4' or message == 'ai' :
    #     message = 'any ai'
    #     ints = predict_class(message)
    #     res = get_response(ints,intents)
    #     print("Bot :",res)
    # try : 
    #     print("\n")
    #     if int(message) > len(options):
    #         print("Please select the options that are available !!\n")
    # except:
    #     if type(message) == str or message == "back" or message == "exit" or message == "go back":
    #         if message in options:
    #             print("Enter a valid input\n")