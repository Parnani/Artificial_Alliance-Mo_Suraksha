import hashlib
import streamlit as st
import pandas as pd

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
    sex = {'Male': 1,'Female': 0}
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
            st.success('Login Successful')
            choice = st.radio("Select Dataset to Display", ("Liver", "Heart", "Diabetes"))
            if choice == "Liver":
                data = liver_view(username)
                st.write(data)
            if choice == "Heart":
                data = heart_view(username)
                st.write(data)
            if choice == "Diabetes":
                data = diabetes_view(username)
                st.write(data)
        else:
            st.warning('Incorrect Username/Password')
            


if __name__ == '__main__':
    login_ui()
