import pickle
import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
import py_files.diabetes as diabetes
import py_files.heart as heart
import py_files.liver as liver

# loading the saved models
diabetes_model = pickle.load(open('saved-models/diabetes.sav', 'rb'))

heart_disease_model = pickle.load(open('saved-models/heart.sav','rb'))

liver_disease_model = pickle.load(open('saved-models/liver.sav', 'rb'))

# sidebar for navigation
with st.sidebar:
    
    selected = option_menu('Mo Suraksha',

                          ['Diabetes Prediction',
                           'Heart Disease Prediction',
                           'Liver Disease Prediction'],
                          icons=['activity','heart','person'],
                          default_index=0,menu_icon='clipboard-data')

# Diabetes Prediction Page
if (selected == 'Diabetes Prediction'):
    
    # page title
    st.title('Diabetes Prediction')
    
    
    # getting the input data from the user
    col1, col2, col3 = st.columns(3)
    
    with col1:
        Pregnancies = st.slider('Number of Pregnancies',0,5,1)
        
    with col2:
        Glucose = st.slider('Glucose Level',20.0,200.0,100.0)
    
    with col3:
        BloodPressure = st.slider('Blood Pressure value',50.0,200.0,95.0)
    
    with col1:
        SkinThickness = st.slider('Skin Thickness value',1.00,20.00,10.00)
    
    with col2:
        Insulin = st.slider('Insulin Level',0.0,200.0,20.0)
    
    with col3:
        BMI = st.slider('BMI value',0.0,50.0,25.0)
    
    with col1:
        DiabetesPedigreeFunction = st.slider('Diabetes Pedigree Function value',0.0,10.0,1.2)
    
    with col2:
        Age = st.slider('Age of the Person',0,100,20)
    
    # code for Prediction
    diab_diagnosis = ''
    
    # creating a button for Prediction
    
    if st.button('Diabetes Test Result'):
        diab_prediction = diabetes_model.predict([[Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age]])
        
        if (diab_prediction[0] == 1):
          diab_diagnosis = 'The person is diabetic'
        else:
          diab_diagnosis = 'The person is not diabetic'
        
    st.success(diab_diagnosis)

    df_diabetes = pd.read_csv('datasets\diabetes.csv')
    st.subheader('Data Information: ')
    st.dataframe(df_diabetes)
    st.write(df_diabetes.describe())
    st.bar_chart(df_diabetes)
    st.write('### Model Accuracy - ',diabetes.accuracy)

# Heart Disease Prediction Page
if (selected == 'Heart Disease Prediction'):
    
    # page title
    st.title('Heart Disease Prediction')
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        age = st.slider('Age',10,100,40)
        
    with col2:
        sex = st.selectbox('Sex: 1-Male,0-Female',('1','0'))
        
    with col3:
        cp = st.slider('Chest Pain types',0.0,3.0,2.0)
        
    with col1:
        trestbps = st.slider('Resting Blood Pressure',90.0,200.0,110.0)
        
    with col2:
        chol = st.slider('Serum Cholestoral in mg/dl',150.0,350.0,170.0)
        
    with col3:
        fbs = st.selectbox('Fasting Blood Sugar: 1-Yes,0-No',('1','0'))
        
    with col1:
        restecg = st.selectbox('Resting Electrocardiographic results',('1','0'))
        
    with col2:
        thalach = st.slider('Maximum Heart Rate achieved',60.0,200.0,90.0)
        
    with col3:
        exang = st.selectbox('Exercise Induced Angina',('0','1'))
        
    with col1:
        oldpeak = st.slider('ST depression induced by exercise',0.0,4.0,1.1)
        
    with col2:
        slope = st.slider('Slope of the peak exercise ST segment',0,2,1)
        
    with col3:
        ca = st.slider('Major vessels colored by flourosopy',0,2,1)
        
    with col1:
        thal = st.selectbox('thal: 1 = normal; 2 = fixed defect; 3 = reversable defect',('1','2','3'))
        
    # code for Prediction
    heart_diagnosis = ''
    
    # creating a button for Prediction
    
    if st.button('Heart Disease Test Result'):
        heart_prediction = heart_disease_model.predict([[int(age), int(sex), int(cp), int(trestbps), int(chol), int(fbs), int(restecg),int(thalach),int(exang),int(oldpeak),int(slope),int(ca),int(thal)]])                          
        
        if (heart_prediction[0] == 1):
          heart_diagnosis = 'The person is having heart disease'
        else:
          heart_diagnosis = 'The person does not have any heart disease'
        
    st.success(heart_diagnosis)

    df_heart = pd.read_csv('datasets\heart.csv')
    st.subheader('Data Information: ')
    st.dataframe(df_heart,width=700)
    st.write(df_heart.describe())
    st.bar_chart(df_heart)
    st.write('### Model Accuracy - ',heart.accuracy)


# Liver Disease Prediction Page
if (selected == 'Liver Disease Prediction'):
    
    # page title
    st.title('Liver Disease Prediction')
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        Age = st.slider('Age',10,100,40)
        
    with col2:
        sex = st.selectbox('Gender',('Male','Female'))
        gender = {'Male': 1,'Female': 0}
        Gender = gender[sex]
        
    with col3:
        Total_Bilirubin = st.slider('Total Bilirubin',0.0,80.0,20.0)
        
    with col1:
        Direct_Bilirubin = st.slider('Direct Bilirubin',0.0,20.0,5.0)
        
    with col2:
        Alkaline_Phosphotase = st.slider('Alkaline Phosphotase',60,2200,290)
        
    with col3:
        Alamine_Aminotransferase = st.slider('Alamine Aminotransferase',10,2000,80)
        
    with col1:
        Aspartate_Aminotransferase = st.slider('Aspartate Aminotransferase',10,5000,110)
        
    with col2:
        Total_Protiens = st.slider('Total Protiens',0.0,10.0,6.5)
        
    with col3:
        Albumin = st.slider('Albumin',0.0,7.0,3.5)
        
    with col1:
        Albumin_and_Globulin_Ratio = st.slider('Albumin and Globulin_Ratio',0.0,3.0,1.0)
   
    # code for Prediction
    liver_diagnosis = ''
    
    # creating a button for Prediction
    
    if st.button('Liver Disease Test Result'):
        liver_prediction = liver_disease_model.predict([[Age,Gender,Total_Bilirubin,Direct_Bilirubin,Alkaline_Phosphotase,Alamine_Aminotransferase,Aspartate_Aminotransferase,Total_Protiens,Albumin,Albumin_and_Globulin_Ratio]])                          
        
        if (liver_prediction[0] == 1):
          liver_diagnosis = 'The person is having liver disease'
        else:
          liver_diagnosis = 'The person does not have any liver disease'
        
    st.success(liver_diagnosis)

    df_liver = pd.read_csv('datasets\liver.csv')
    gender = {'Male': 1,'Female': 0}
    df_liver['Gender'] = [gender[item] for item in df_liver['Gender']]
    st.subheader('Data Information: ')
    st.dataframe(df_liver,width=700)
    st.write(df_liver.describe())
    st.bar_chart(df_liver)
    st.write('### Model Accuracy - ',liver.accuracy)