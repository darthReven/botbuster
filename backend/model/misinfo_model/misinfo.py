# install the modules with 
# pip install scikit-learn

# Import Libraries
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
# from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
# from sklearn import metrics
import pandas as pd
# import numpy as np
# from tqdm import tqdm

# from google.colab import drive
# drive.mount('/content/drive')
# %cd /content/drive/MyDrive/hackathon/

# Read data, remove cv columns and fill NA with ''
data = pd.read_csv("./train.csv")
data = data[data.columns[:-2]]
data = data.fillna('')

# One-hot encode Target column (real=0, fake=1)
data['label'] = pd.get_dummies(data.nlp_class)['fake']

# Join title, text and comments together
data['combined'] = data['nlp_title'] + data['nlp_text'] + data['nlp_comments']

data.head()

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(data['combined'], data.label, test_size=0.20, random_state=3101)

# print(X_test)
# Count Vectorizer
count_vectorizer = CountVectorizer(ngram_range=(1, 2), stop_words='english')
# Fit and transform the training data
count_train = count_vectorizer.fit_transform(X_train)
# Transform the test set
count_test = count_vectorizer.transform(X_test)

# Ensemble with Hyperparam Tuning
model = LogisticRegression(random_state=3101,solver='liblinear')
model.fit(count_train, y_train)

# calculating accuracy of model
# real
text="yamashimaxgriot, the lead developer of skyrim together (and previously skyrim online), the same person who said they don't owe the community anything, has a long and shady history within the community. he got busted for making an eso emulator when it was still in beta. he also created emulators for other mmos (tor, gw2, etc.). bethesda shut him down faster than you can say 'dragonborn', and skyrim online was scrapped immediately afterward. there was hearsay that he might have been banned from ever modifying another bethesda product, hence why he changed his handle from yamashi to maxgriot. after he was caught maliciously stealing code from the skyrim script extender (skse) team people asked him why he didn't even credit them. his response? he didn't have time to credit them. and, 'well since you offer your time and skills to design a proper credit page, i am eager to see it.' of course, the story then was that there was almost nothing left of skse in their code, and that they could remove it easily and replace it. but now that it's been a few months, people are starting to believe that the project is far more dependent on skse than they let on, thus why the project seems to be frozen. they are effectively taking $18,000 a month from the community and delivering nothing. and it was north of $24,000 a month or two back! listen, multiplayer skyrim is the dream. i would love to play it someday! but if there's one thing you should take away from this post, it's that you absolutely should not trust the skyrim together team with any of your personal information. and given that you must make an account and play through their dedicated servers... if you ever decide to give it a go, please just be smart and use a burner email and password. these people cannot be trusted, and so you should not give them any information that could be valuable to them, or harmful to you. if you want to support a truly community-driven multiplayer elder scrolls eerience, i urge you to check out openmw and its accompanying add-on, tes3mp. here's a link to a good thread on  talking about it, and it also has links to patreon pages if you want to support people who aren't running off with $18,000 a month:  it works, and it's wonderful. morrowind is already fully playable in co-op. but interestingly, they are building towards a future where other bethesda games (oblivion, skyrim, but also the fallout games) are supported. if that happens, you'll be able to enjoy elder scrolls and fallout in multiplayer, built at the engine level. no need to connect to servers or create accounts, host them yourself! thanks for taking the time to read. i've been a long-time follower of this project, and maybe one of the few people left in the community who followed yamashi during the skyrim online days. it is absolutely heartbreaking to see how everything has turned out with skyrim together."
# fake
text="as a turk, i don't think this map is accurate. over %20 would just flee the country, no way %73 would fight for turkey. and the context is missing. i mean, what kind of war? i would never fight an islamist war; though i would fight to preserve my national identity and secular republic. same goes for others... some people would not fight for a 'secular' turkey but an islamist one. the map just makes no sense as it is."
# real
# text='theres already too many kids in the***system!!! removing potential adoptive parents just ensures more kids will grow up in this broken ***ty system.'
text=count_vectorizer.transform([text])
# predictions = model.predict(text)
probabilities = model.predict_proba(text)
prediction = probabilities[0][1]
print(prediction)
# predictions = model.predict(count_test)
# from sklearn.metrics import accuracy_score
# # Calculate accuracy
# accuracy = accuracy_score(y_test, predictions)
# print("Accuracy:", accuracy)