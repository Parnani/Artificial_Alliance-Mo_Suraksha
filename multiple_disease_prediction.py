import pickle
import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
import py_files.diabetes as diabetes
import py_files.heart as heart
import py_files.liver as liver
import hashlib


# DB Management
import sqlite3
conn = sqlite3.connect('data.db')
c = conn.cursor()


def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()


def check_hashes(password, hashed_text):
    if make_hashes(password) == hashed_text:
        return hashed_text
    return False


def create_usertable():
    c.execute('CREATE TABLE IF NOT EXISTS users(username TEXT,password TEXT)')


def add_userdata(username, password):
    c.execute('INSERT INTO users(username,password) VALUES (?,?)',
              (username, password))
    conn.commit()


def login_user(username, password):
    c.execute('SELECT * FROM users WHERE username =? AND password = ?',
              (username, password))
    data = c.fetchall()
    return data


def view_all_users():
    c.execute('SELECT * FROM users')
    data = c.fetchall()
    return data


def liver_view(username):
    c.execute(f'SELECT * FROM liver WHERE username = "{username}"')
    data = c.fetchall()
    return data


def liver_ins(username, Age, Gender, Total_Bilirubin, Direct_Bilirubin, Alkaline_Phosphotase, Alamine_Aminotransferase, Aspartate_Aminotransferase, Total_Protiens, Albumin, Albumin_and_Globulin_Ratio, Dataset):
    sex = {'Male': 1, 'Female': 0}
    gender = sex[Gender]
    c.execute('INSERT INTO liver VALUES(?,?,?,?,?,?,?,?,?,?,?,?)', (username, Age, gender, Total_Bilirubin, Direct_Bilirubin,
              Alkaline_Phosphotase, Alamine_Aminotransferase, Aspartate_Aminotransferase, Total_Protiens, Albumin, Albumin_and_Globulin_Ratio, Dataset))
    conn.commit()


def heart_ins(username, age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal, target):
    c.execute('INSERT INTO heart VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', (username, age, sex,
              cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal, target))
    conn.commit()


def heart_view(username):
    c.execute(f'SELECT * FROM heart WHERE username = "{username}"')
    data = c.fetchall()
    return data


def diabetes_ins(username, Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age, Outcome):
    c.execute('INSERT INTO diabetes VALUES(?,?,?,?,?,?,?,?,?,?)', (username, Pregnancies, Glucose,
              BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age, Outcome))
    conn.commit()


def diabetes_view(username):
    c.execute(f'SELECT * FROM diabetes WHERE username = "{username}"')
    data = c.fetchall()
    return data


def liver_cleanup(data):
    sex = {1: 'Male', 0: 'Female'}
    data[2] = sex[data[2]]
    return data


def login_ui():
    st.title('View your stored data here')
    username = st.sidebar.text_input("User Name")
    password = st.sidebar.text_input("Password", type='password')
    if st.sidebar.checkbox("Login"):
        create_usertable()
        hashed_pswd = make_hashes(password)

        result = login_user(username, check_hashes(password, hashed_pswd))
        if result:
            check_hashes('password', hashed_pswd)
            st.success(f'Welcome back {username}')
            choice = st.radio("Select Dataset to Display",
                              ("Liver", "Heart", "Diabetes"))
            if choice == "Liver":
                raw = list(liver_view(username))
                data = pd.DataFrame(raw, columns=['Username', 'Age', 'Gender', 'Total Bilirubin', 'Direct Bilirubin', 'Alkaline Phosphotase',
                                    'Alamine Aminotransferase', 'Aspartate Aminotransferase', 'Total Protiens', 'Albumin', 'Albumin and Globulin Ratio', 'Prediction'])
                data.drop(columns=['Username'], inplace=True)

                gender = {1: 'Male', 0: 'Female'}
                data['Gender'] = [gender[item] for item in data['Gender']]
                predict = {0: 'No', 1: 'Yes'}
                data['Prediction'] = [predict[item]
                                      for item in data['Prediction']]
                st.write(data)

            if choice == "Heart":
                raw = heart_view(username)
                
                data = pd.DataFrame(raw, columns=['Username','Age','Sex','Chest Pain','BP','Cholestrol','Blood Sugar','ECG','Heart Rate','Angina','ST Depression','Slope of ST segment','Flourosopy','Haemoglobin','Prediction'])
                predict = {0: 'No', 1: 'Yes'}
                data.drop(columns=['Username'], inplace=True)
                
                data['Prediction'] = [predict[item]
                                      for item in data['Prediction']]
                gender = {1: 'Male', 0: 'Female'}
                data['Sex'] = [gender[item] for item in data['Sex']]
                st.write(data)
            if choice == "Diabetes":
                raw = diabetes_view(username)
                
                data = pd.DataFrame(raw,columns=['Username','Pregnancies','Glucose','Blood Pressure','Skin Thickness','Insulin','BMI','Diabetes Pedigree Function','Age','Prediction'])
                data.drop(columns=['Username'], inplace=True)
                predict = {0: 'No', 1: 'Yes'}
                data['Prediction'] = [predict[item]
                                      for item in data['Prediction']]
                st.write(data)
        else:
            st.warning('Incorrect Username/Password')
    else:
        st.subheader("New User?")
        if 'create' not in st.session_state:
            st.session_state.create = 0

        if st.session_state.create == 2:
            st.session_state.create = 0
            st.success('Account Created')
        if st.session_state.create == 3:
            st.session_state.create = 0
            st.warning('Username already exists')

        acc = st.button("Create Account", key='acc')
        if acc:
            st.session_state.create = 1
        if st.session_state.create == 1:
            with st.form("Create a new account"):
                new_username = st.text_input("User Name", key='username')
                new_password = st.text_input(
                    "Password", type='password', key='password')
                created = st.form_submit_button("Create Account")
                if (created):
                    c.execute(
                        f'SELECT * FROM users WHERE username = "{new_username}"')
                    data = c.fetchall()
                    if (len(data) == 0):
                        st.session_state.create = 2
                        add_userdata(new_username, make_hashes(new_password))
                        st.success('Account Created')
                    else:
                        st.session_state.create = 3
                        st.warning('Username already exists')


# loading the saved models
diabetes_model = pickle.load(open('./saved-models/diabetes.sav', 'rb'))

heart_disease_model = pickle.load(open('./saved-models/heart.sav','rb'))

liver_disease_model = pickle.load(open('./saved-models/liver.sav', 'rb'))

# sidebar for navigation
with st.sidebar:
    
    selected = option_menu('Mo Suraksha',

                          ['Home', 
                           'Diabetes Prediction',
                           'Heart Disease Prediction',
                           'Liver Disease Prediction',
                           'View Stored Data'],
                          icons=['house-door','activity','heart','person','cloud-arrow-down'],
                          default_index=0,menu_icon='clipboard-data')

if selected == 'View Stored Data':
    login_ui()
# Diabetes Prediction Page
if (selected == 'Diabetes Prediction'):
    
    # page title
    st.title('Diabetes Prediction')
    
    
    # getting the input data from the user
    col1, col2, col3 = st.columns(3)
    
    with col1:
        Pregnancies = st.slider('Number of Pregnancies',0,5,1)
        
    with col2:
        Glucose = st.slider('Glucose Level (mmol/L)',20.0,200.0,100.0)
    
    with col3:
        BloodPressure = st.slider('Blood Pressure value (mm Hg)',50.0,200.0,95.0)
    
    with col1:
        SkinThickness = st.slider('Skin Thickness value (mm)',1.00,20.00,10.00)
    
    with col2:
        Insulin = st.slider('Insulin Level (mmol/L)',0.0,200.0,20.0)
    
    with col3:
        BMI = st.slider('BMI value (weight in kg/(height in m)^2)',0.0,50.0,25.0)
    
    with col1:
        DiabetesPedigreeFunction = st.slider('Diabetes Pedigree Function value (weight in kg/(height in m)^2)',0.0,10.0,1.2)
    
    with col2:
        Age = st.slider('Age of the Person (years)',0,100,20)
    
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

    df_diabetes = pd.read_csv('./datasets/diabetes.csv')
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
        trestbps = st.slider('Resting Blood Pressure (mm Hg)',90.0,200.0,110.0)
        
    with col2:
        chol = st.slider('Serum Cholestoral (mg/dl)',150.0,350.0,170.0)
        
    with col3:
        fbs = st.selectbox('Fasting Blood Sugar: 1-Yes,0-No',('1','0'))
        
    with col1:
        restecg = st.selectbox('Resting Electrocardiographic results',('1','0'))
        
    with col2:
        thalach = st.slider('Maximum Heart Rate achieved (bpm)',60.0,200.0,90.0)
        
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

    df_heart = pd.read_csv('./datasets/heart.csv')
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
        Age = st.slider('Age (years)',10,100,40)
        
    with col2:
        sex = st.selectbox('Gender',('Male','Female'))
        gender = {'Male': 1,'Female': 0}
        Gender = gender[sex]
        
    with col3:
        Total_Bilirubin = st.slider('Total Bilirubin (mg/dl)',0.0,80.0,20.0)
        
    with col1:
        Direct_Bilirubin = st.slider('Direct Bilirubin (mg/dl)',0.0,20.0,5.0)
        
    with col2:
        Alkaline_Phosphotase = st.slider('Alkaline Phosphotase (μKat/L)',60,2200,290)
        
    with col3:
        Alamine_Aminotransferase = st.slider('Alamine Aminotransferase (μKat/L)',10,2000,80)
        
    with col1:
        Aspartate_Aminotransferase = st.slider('Aspartate Aminotransferase (μKat/L)',10,5000,110)
        
    with col2:
        Total_Protiens = st.slider('Total Protiens (g/dl)',0.0,10.0,6.5)
        
    with col3:
        Albumin = st.slider('Albumin (g/dl)',0.0,7.0,3.5)
        
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

    df_liver = pd.read_csv('./datasets/liver.csv')
    gender = {'Male': 1,'Female': 0}
    df_liver['Gender'] = [gender[item] for item in df_liver['Gender']]
    st.subheader('Data Information: ')
    st.dataframe(df_liver,width=700)
    st.write(df_liver.describe())
    st.bar_chart(df_liver)
    st.write('### Model Accuracy - ',liver.accuracy)