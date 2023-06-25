import nltk
import random
import string

nltk.warnings.filterwarnings('ignore')
f = open('chatbot.txt', 'r', errors='ignore')
raw = f.read()
raw = raw.lower()  # converts to lowercase
nltk.download('punkt')  # sentence tokenizer funtions
nltk.download('wordnet')  #
sent_tokens = nltk.sent_tokenize(raw)  # converts to list of sentences
word_tokens = nltk.word_tokenize(raw)  # converts to list of words
lemmer = nltk.stem.WordNetLemmatizer() #to find the meanings of words, synonyms, antonyms

#WordNet is an ordered dictionary of English included in NLTK.

#it removes punctuations  in a given text/corpus
def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]
remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)
def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))


GREETING_INPUTS = ("hello", "hi", "greetings", "namastey", "whats up", "hey",)
GREETING_RESPONSES = ["hi", "hey", "hi there", "hello", "I am glad! You are talking to me"]


def greeting(sentence):
    for word in sentence.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES)
from sklearn.feature_extraction.text import TfidfVectorizer #frequency
from sklearn.metrics.pairwise import cosine_similarity

def response(user_response):
    robo_response=''
    TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')# transform sentences into arrays of numbers
    tfidf = TfidfVec.fit_transform(sent_tokens)
    vals = cosine_similarity(tfidf[-1], tfidf)#to measure the text-similarity between two documents #vals=numpy array
    idx=vals.argsort()[0][-2]
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]
    if(req_tfidf==0):
        robo_response=robo_response+"I am sorry! I don't understand you"
        return robo_response
    else:
        robo_response = robo_response+sent_tokens[idx]
        return robo_response
def finalbot(user_response):


   # print("ROBO: My name is Robo. I will answer your queries about Chatbots. If you want to exit, type Bye!")

    word_tokens = nltk.word_tokenize(raw)
    user_response=user_response.lower()
    if(user_response!='bye'):
                if(user_response=='thanks' or user_response=='thank you' ):

                    return "You are welcome.."
                else:
                    if(greeting(user_response)!=None):
                        return greeting(user_response)
                    else:
                        sent_tokens.append(user_response)
                        word_tokens=word_tokens+nltk.word_tokenize(user_response)
                        final_words=list(set(word_tokens))
                      #  print("ROBO: ",end="")

                        return response(user_response)



    else:

            return "Bye!take care"
print(finalbot("bye"))