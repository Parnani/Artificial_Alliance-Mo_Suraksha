# %%
# Imports
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn import svm
from sklearn.metrics import accuracy_score
import pickle

# %%
df_liver = pd.read_csv('datasets/liver.csv')
df_liver.head()

# %%
df_liver['Dataset'].value_counts()

# %%
gender = {'Male': 1,'Female': 0}
df_liver['Gender'] = [gender[item] for item in df_liver['Gender']]

# %%
df_liver.head()

# %%
df_liver['Albumin_and_Globulin_Ratio'].fillna(value=0, inplace=True)

# %%
df_liver['Dataset'] = df_liver['Dataset'].map({2:0,1:1})

# %%
df_liver['Dataset'].value_counts()

# %%
X = df_liver.drop(columns='Dataset', axis=1)
y = df_liver['Dataset']

# %%
X_train, X_test, y_train, y_test = train_test_split(X,y, test_size = 0.2, random_state=23)

# %%
classifier = LogisticRegression()

# %%
classifier.fit(X_train, y_train)

# %%
predictions = classifier.predict(X_test)
accuracy = accuracy_score(y_test,predictions)

# %%
print('Accuracy score : ', accuracy)

# %% [markdown]
# ### Saving the model

# %%
filename = 'saved-models/liver.sav'
pickle.dump(classifier, open(filename, 'wb'))

# %%
# loading the saved model
loaded_model = pickle.load(open('saved-models/liver.sav', 'rb'))

# %%
input_data = (65,0,0.7,0.1,187,16,18,6.8,3.3,0.90)

# change the input data to a numpy array
input_data_as_numpy_array= np.asarray(input_data)

# reshape the numpy array as we are predicting for only on instance
input_data_reshaped = input_data_as_numpy_array.reshape(1,-1)

prediction = classifier.predict(input_data_reshaped)
print(prediction)

if (prediction[0]== 0):
  print('The Person does not have a Liver Disease')
else:
  print('The Person has Liver Disease')

# %%
for column in X.columns:
  print(column)

# %%



