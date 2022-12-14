# Team - Artificial Alliance
# Mo Suraksha

- added 3 .ipynb files for diabetes, heart disease and liver disease.
    - diabetes.ipynb -
        - imported all the required libraries.
        - created a pandas dataframe with diabetes.csv file.
        - performed a train_test_split() on the data.
        - implemented Support Vector Machine algorithm with kernel as linear and fitted the training data in it.
        - made the predictions and generated the accuracy score of the model.
        - saved the model using pickle library of python which converts the model into binary stream.
        - implemented the prediction on a random data and checked if he/she is diabetic.
    - heart.ipynb -
        - created a pandas dataframe with heart.csv file.
        - implemented LogisticRegression() algorithm.
    - liver.ipynb -
        - created a pandas dataframe with liver.csv file.
        - mapped the string value of gender to (0,1) for ('Female','Male') respectively.
        - replaced the NaN values in df_liver['Albumin_and_Globulin_Ratio'] column with 0.
        - implemented LogisticRegression() algorithm.

- exported the .ipynb files into .py files.

- multiple_disease_prediction.py -
    - loaded the saved models using pickle.
    - implemented user database
        - created a table for user details and entries for individual data and stored them to data.db
        - implemented login system to website
        - added an option to print the table
        - added session-based sign up system
        - upon login, users can now view all stored datas 
        - implemented database save system 
    - implemented database access page
    - implemented sidebar containg Home, Diabetes Prediction, Heart Disease Prediction, Liver Disease Prediction, View Stored Data.
    - implemented sliders for each of the features in all 3 diseases.
    - added diseases' dataframes, description of the dataframe and a bar-chart visualization of the data.
