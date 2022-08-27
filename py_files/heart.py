# %%
#Imports
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import pickle

# %%
df_heart = pd.read_csv('datasets/heart.csv')
df_heart.head()

# %%
df_heart.shape

# %%
df_heart['target'].value_counts()

# %%
X = df_heart.drop(columns='target', axis=1)
y = df_heart['target']

# %%
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=30)

# %%
model = LogisticRegression()

# %%
model.fit(X_train,y_train)

# %%
predictions = model.predict(X_test)
accuracy = accuracy_score(y_test,predictions)

# %%
print('Accuracy score : ', accuracy)

# %% [markdown]
# ### Saving the model

# %%
filename = 'saved-models/heart.sav'
pickle.dump(model, open(filename, 'wb'))

# %%
# loading the saved model
loaded_model = pickle.load(open('saved-models/heart.sav', 'rb'))

# %%
input_data = (62,0,0,140,268,0,0,160,0,3.6,0,2,2)

# change the input data to a numpy array
input_data_as_numpy_array= np.asarray(input_data)

# reshape the numpy array as we are predicting for only on instance
input_data_reshaped = input_data_as_numpy_array.reshape(1,-1)

prediction = model.predict(input_data_reshaped)
print(prediction)

if (prediction[0]== 0):
  print('The Person does not have a Heart Disease')
else:
  print('The Person has Heart Disease')

# %%
for column in X.columns:
  print(column)

# %%



