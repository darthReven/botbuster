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

# Count Vectorizer
count_vectorizer = CountVectorizer(ngram_range=(1, 2), stop_words='english')
# Fit and transform the training data
count_train = count_vectorizer.fit_transform(X_train)
# Transform the test set
count_test = count_vectorizer.transform(X_test)

# Ensemble with Hyperparam Tuning
clf1 = LogisticRegression(random_state=3101)
clf1.fit(count_train, y_train)

# calculating accuracy of model
predictions = clf1.predict(count_test)
from sklearn.metrics import accuracy_score
# Calculate accuracy
accuracy = accuracy_score(y_test, predictions)
print("Accuracy:", accuracy)