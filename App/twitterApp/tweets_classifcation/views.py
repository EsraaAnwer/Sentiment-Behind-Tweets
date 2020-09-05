from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth import logout
from tweets_classifcation.forms import SignUpForm
#import pymongo
import twitter 
# from .souq_configs import *
from .models import  Contact_us
from tweets_classifcation.ml_work.cleaning import *
from tweets_classifcation.ml_work.cleaning_arabic import *
import json
import sys
import os
import pickle
import io
import urllib, base64
from matplotlib import pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from sklearn.model_selection import train_test_split
from django.contrib.auth.models import User
# Features Extraction
from sklearn.feature_extraction.text import TfidfVectorizer

# Evaluation
from sklearn.metrics import confusion_matrix
from sklearn.metrics import f1_score

# models
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC

from decimal import Decimal


tfidf_vectorizer = pickle.load(open("tweets_classifcation/ml_work/tfidf_vectorizer.pickle", "rb"))
logistic_model = pickle.load(open("tweets_classifcation/ml_work/logistic_model.sav", 'rb'))

tfidf_vectorizer_arabic = pickle.load(open("tweets_classifcation/ml_work/tfidf_vectorizer_Arabic.pickle", "rb"))
logistic_model_arabic = pickle.load(open("tweets_classifcation/ml_work/logistic_model_liblinear_Arabic_60%_5991.pickle", 'rb'))

# Create your views here.



CONSUMER_KEY='cSkU3KpTxMwMC2qhIMeaA'
CONSUMER_SECRET='k9PPEgjfUQDmNiFd6LmdinDY5lyonSFjIAsTJ1Q9H6M'
ACCESS_TOKEN_KEY='1575234234-cEMHfmhoygyhlOwEtaRIwRCHYcvhuOU4n4zpbfg'
ACCESS_TOKEN_SECRET='LOslB0IiT6nCW9H3ik52EpAF4WNcBeQ8M16c43NbHS0lN'
#######################################################
def get_tweets(api=None, screen_name=None):
    # returned as list
    timeline = api.GetUserTimeline(screen_name=screen_name, count=200)
    earliest_tweet = min(timeline, key=lambda x: x.id).id
    while True:
        tweets = api.GetUserTimeline(
            screen_name=screen_name, max_id=earliest_tweet, count=200
        )
        new_earliest = min(tweets, key=lambda x: x.id).id

        if not tweets or new_earliest == earliest_tweet:
            break
        else:
            earliest_tweet = new_earliest
            # print("getting tweets before:", earliest_tweet)
            timeline += tweets
    timeline = timeline[:100]
    return timeline



def home_page(request):
	if request.method == "POST":
		
		try:
			data = json.loads(request.body) # get data hat user inout in text area
			clean_new_sentence = []
			clean_new_sentence.append(data['user_text'])

			if data['language_selected'] 	== 'English': 
				
				clean_new_sentence = english_pip_line(clean_new_sentence)
				transform_text     = tfidf_vectorizer.transform(clean_new_sentence)
				transform_text     = transform_text.toarray()
				predict            = logistic_model.predict(transform_text)
				if predict[0] == 0:
					data['Polarity'] = "Negative"
				elif predict[0] == 1:
					data['Polarity'] = "Neutral"
				else: data['Polarity'] = "Positive"

				return JsonResponse(data)
			elif data['language_selected'] 	== 'Arabic':
				clean_new_sentence.append(data['user_text'])
				clean_new_sentence = arabic_pip_line(clean_new_sentence)
				transform_text     = tfidf_vectorizer_arabic.transform(clean_new_sentence)
				transform_text     = transform_text.toarray()
				predict            = logistic_model_arabic.predict(transform_text)

				if predict[0] == 0:
					data['Polarity'] = "Negative"
				elif predict[0] == 1:
					data['Polarity'] = "Neutral"
				else: data['Polarity'] = "Positive"

				return JsonResponse(data)
		except:
			data = json.loads(request.body) # get data hat user inout in text area

			# clean_new_sentence = []
			screen_name = data['twitter_account']

			api = twitter.Api(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET)
			timeline = get_tweets(api=api, screen_name=screen_name)

			all_tweets = []
			for tweet in timeline:
			    all_tweets.append(tweet._json['text'])
			# print(screen_name, "-----------")
			predict = []
			if data['language_selected'] 	== 'English':
				tweet_text = all_tweets
				all_tweets 		   			= english_pip_line(all_tweets)
				transform_text     			= tfidf_vectorizer.transform(all_tweets)
				transform_text     			= transform_text.toarray()
				predict            			= logistic_model.predict(transform_text)
			elif data['language_selected'] 	== 'Arabic':
				tweet_text = all_tweets
				all_tweets 		   			= arabic_pip_line(all_tweets)
				transform_text     			= tfidf_vectorizer_arabic.transform(all_tweets)
				transform_text     			= transform_text.toarray()
				predict            			= logistic_model_arabic.predict(transform_text)

			classifed_tweets   			= {}
			Negative, Neutral, Positive = 0,0,0

			for i in range(len(predict)):
				tweet = {}
				if predict[i] == 0:
				    tweet = {
				    str(i+1): [tweet_text[i], "Negative"]
				    }
				    Negative +=1
				elif predict[i] == 1:
				    tweet = {
				    str(i+1): [tweet_text[i], "Neutral"]
				    }
				    Neutral +=1
				else:
				    tweet = {
				    str(i+1): [tweet_text[i], "Positive"]
				    }
				    Positive +=1
				classifed_tweets["tweet " + str(i+1)] = tweet

			labels = ['Negative', 'Neutral', 'Positive']
			sizes = [Negative, Neutral, Positive]
			explode = (0, 0.1, .2)
			fig = plt.figure(figsize=(5,5))
			plt.pie(sizes, explode=explode, labels=labels, 
			autopct='%1.1f%%', shadow=True, startangle=140)

			# print("#"*50)
			plt.savefig('tweets_classifcation/static/images/charts/' + data['twitter_account'] + ".png")

			# pri/nt(x)
			# print("*"*50)
			data['tweets'] = classifed_tweets
			# data['img'] = "pie.png"
			return JsonResponse(data)

	return render(request, 'tweets_classifcation/home_page.html')
	



################################## Forms


def signup_form(request):
    if request.method == 'POST':
        data = json.loads(request.body) # get data hat user inout in text area
        form = SignUpForm(data)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data.get('username')
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            # data['success'] = True
            return JsonResponse(data)
        else:
            form = SignUpForm(request.POST)
            return JsonResponse({'errors': form.errors})
    else:
        form = SignUpForm()
    return render(request, 'tweets_classifcation/signup.html', {'form': form})



def login_form(request):


    if request.method == 'POST':
        data = json.loads(request.body) # get data hat user inout in text area
        username = data['username']
        password = data['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return JsonResponse(data)
        else: 
            return render(request, 'tweets_classifcation/login.html')


    return render(request, 'tweets_classifcation/login.html')



def logout_form(request):
    logout(request)
    return redirect('home_page')


def contact_form(request):
    if request.method == "POST":
        data = json.loads(request.body)
        if request.user.is_authenticated:
            data['mail'] = request.user.username
            data['first_name'] = request.user.first_name
        Contact_us.objects.create(
            mail=data['mail'],
            first_name=data['first_name'],
            phonenumber=data['phonenumber'],
            message=data['message']
        )
        return JsonResponse(data)
    else:
        return render(request, 'tweets_classifcation/contact_us.html')