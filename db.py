import hashlib
import streamlit as st
import pandas as pd
from datetime import datetime

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


if __name__ == '__main__':
    login_ui()
