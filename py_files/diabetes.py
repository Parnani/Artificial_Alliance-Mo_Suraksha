# %%
# Imports
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn import svm
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import pickle

# %%
df_diabetes = pd.read_csv('datasets/diabetes.csv')
df_diabetes.head()

# %%
df_diabetes.shape

# %%
df_diabetes['Outcome'].value_counts()

# %%
X = df_diabetes.drop(columns = 'Outcome', axis=1)
y = df_diabetes['Outcome']

# %%
X_train, X_test, y_train, y_test = train_test_split(X,y, test_size = 0.2, random_state=20)

# %%
classifier = svm.SVC(kernel='linear',C=10,gamma=0.01)

# %%
classifier.fit(X_train,y_train)

# %%
predictions = classifier.predict(X_test)
accuracy = accuracy_score(y_test,predictions)

# %%
print('Accuracy score : ', accuracy)

# %% [markdown]
# ### Saving the model

# %%
filename = 'saved-models/diabetes.sav'
pickle.dump(classifier, open(filename, 'wb'))

# %%
# loading the saved model
loaded_model = pickle.load(open('saved-models/diabetes.sav', 'rb'))

# %%
input_data = (5,166,72,19,175,25.8,0.587,51)

# changing the input_data to numpy array
input_data_as_numpy_array = np.asarray(input_data)

# reshape the array as we are predicting for one instance
input_data_reshaped = input_data_as_numpy_array.reshape(1,-1)

prediction = loaded_model.predict(input_data_reshaped)
print(prediction)

if (prediction[0] == 0):
  print('The person is not diabetic')
else:
  print('The person is diabetic')

# %%
for column in X.columns:
  print(column)

# %%



