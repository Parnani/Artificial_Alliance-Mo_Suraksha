
# Team - Artificial Alliance
# Mo Suraksha

## Minds that cure, hearts that care

Now you can predict the disease you are suffering from with just a few clicks.

We have three models to predict the disease you are suffering from.

You can choose the disease you want to predict from the sidebar.

## Setting up 

Make sure you have python installed in your machine. To clone the project, enter this command: 

```bash
pip install streamlit pickle pandas streamlit_option_menu hashlib sqlite3
```

Now clone this github repo by this command. Make sure you have git installed. 

```bash
cd <path-to-save-directory>
git clone https://github.com/Parnani/Artificial_Alliance-Mo_Suraksha.git
```

To run the web app locally in your machine, run this command

```bash
cd <path-to-folder>
streamlit run app.py
```

## Usage

- Navigate the app using sidebar between the menues. 
- Modify the sliders of the fields as per the test result data. 
- To save data, you will first need to sign up to the account. To create a new account: 
    - Navigate to 'View Stored Data'
    - You will be asked to sign up there. Make sure you remember/save password
    - Use same credentials to save all test data. 
- To view saved data, simply goto 'View Stored Data'. Then enter user details and check 'login' box. 

## Known issues 
- Implementation of signup/login button everywhere
- Slower initial load time (time will be consumed in training ML datas)
- Laggy graph
- Needed to press C and clear streamlit cache in case some weird bugs comes up

# Feel free to star this repo if you loved it
