import streamlit as st
import requests

if "session" not in st.session_state:
    st.session_state.session = requests.Session()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "registered" not in st.session_state:
    st.session_state.registered = True

if not st.session_state.registered:
    st.title("Register to skillshare")
    email = st.text_input("Enter your email: ")
    password = st.text_input("Your password ")
    if email and password and st.button("Register"):
        res_re = st.session_state.session.post(
            "https://skillshare-backend-apha.onrender.com/create_account",
            json = {"email":email, "hashed_password":password}
        )
        st.session_state.registered = True
        st.write(res_re.json())
        st.button("login")

elif not st.session_state.logged_in:

    st.title("Login to SkillShare")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        response = st.session_state.session.post(
            "https://skillshare-backend-apha.onrender.com/login",
            json={"email": email, "hashed_password": password}
        )
        if response.status_code == 200:
            st.session_state.logged_in = True
            st.success("Login successful!")
            st.button("Explore")
        else:
            st.error(f"Login failed: {response.json()['detail']}")
            st.session_state.registered = False
            st.button("Register")



else:
    st.title("Welcome! What do you want to do?")
    st.session_state.session.post(f"https://skillshare-backend-apha.onrender.com/refresh")
    # Initialize the flags if they don't exist
    if "search_clicked" not in st.session_state:
        st.session_state.search_clicked = False
    if "post_clicked" not in st.session_state:
        st.session_state.post_clicked = False
    if "skill_clicked" not in st.session_state:
        st.session_state.skill_clicked = False

    if "logout_clicked" not in st.session_state:
        st.session_state.logout_clicked = False
    # Buttons and mutual exclusivity
    if st.button("Search user"):
        st.session_state.search_clicked = True
        # st.session_state.post_clicked = False

    if st.button("Post an update"):
        st.session_state.post_clicked = True
        # st.session_state.search_clicked = False
    
    if st.button("Post a skill"):
        st.session_state.skill_clicked = True
        # st.session_state.search_clicked = False
    if st.button("Logout"):
        st.session_state.logout_clicked = True
        st.session_state.logged_in = False
    # Display Search UI
    if st.session_state.search_clicked:
        query = st.text_input("Enter username to search")
        if st.button("Search"):
            response = st.session_state.session.get(f"https://skillshare-backend-apha.onrender.com/search?username={query}")
            if response.status_code == 200:
                st.write(response.json())
                st.session_state.search_clicked = False
            else:
                st.error("User doesnt exist.")
                st.session_state.search_clicked = False

    # Display Post UI
    if st.session_state.post_clicked:
        update_text = st.text_area("Write your update here")
        if st.button("Post"):
            response = st.session_state.session.post(
                "https://skillshare-backend-apha.onrender.com/post",
                json={"post": update_text}
            )
            if response.status_code == 200:
                st.success("Post created!")
                st.session_state.post_clicked = False
            else:
                st.error("Post could not be created.")
                st.session_state.post_clicked = False
    
    if st.session_state.skill_clicked:
        new_skill = st.text_area("New skill")
        l = [new_skill]
        if st.button("Post"):
            response = st.session_state.session.post(f"https://skillshare-backend-apha.onrender.com/post-skill", json = {"skills":l})
            st.success("Posted skill")
            st.session_state.skill_clicked = False
