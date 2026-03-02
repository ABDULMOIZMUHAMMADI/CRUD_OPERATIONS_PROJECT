import streamlit as st
import requests

BASE_URL = "http://127.0.0.1:8000"  

st.set_page_config(page_title="User Management & Text Analysis", layout="wide")

st.title("🧑 User Management & Text Analysis")
st.markdown("**Modern, minimal interface to manage users and analyze text.**")

st.sidebar.title("Menu")
option = st.sidebar.radio("Select Action", ["Add User", "View All Users", "View Single User", 
                                             "Update User", "Delete User", "Analyze Text"])


if option == "Add User":
    st.subheader("➕ Add User")
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=1, max_value=150)
    text = st.text_area("Text (max 200 chars)", max_chars=200)

    if st.button("Add User"):
        if name and text:
            data = {"name": name, "age": int(age), "text": text}
            response = requests.post(f"{BASE_URL}/user", params=data)
            if response.status_code == 200:
                st.success("User added successfully!")
                st.json(response.json())
            else:
                st.error(response.json())
        else:
            st.warning("Name and Text cannot be empty!")

elif option == "View All Users":
    st.subheader("👥 All Users")
    response = requests.get(f"{BASE_URL}/users")
    if response.status_code == 200:
        users = response.json()
        st.write(f"Total Users: {len(users)}")
        st.dataframe(users)
    else:
        st.error("Error fetching users")

elif option == "View Single User":
    st.subheader("🔍 View Single User")
    user_id = st.number_input("Enter User ID", min_value=1)
    if st.button("Get User"):
        response = requests.get(f"{BASE_URL}/user/{user_id}")
        if response.status_code == 200:
            st.json(response.json())
        else:
            st.error(response.json()["detail"])

elif option == "Update User":
    st.subheader("✏️ Update User")
    user_id = st.number_input("User ID", min_value=1)
    name = st.text_input("New Name (leave blank if not changing)")
    age = st.number_input("New Age (leave blank if not changing)", min_value=0, max_value=150, value=0)
    text = st.text_area("New Text (leave blank if not changing)", max_chars=200)

    if st.button("Update User"):
        data = {}
        if name.strip() != "":
            data["name"] = name
        if age != 0:
            data["age"] = int(age)
        if text.strip() != "":
            data["text"] = text
        if data:
            response = requests.put(f"{BASE_URL}/user/{user_id}", params=data)
            if response.status_code == 200:
                st.success(f"User {user_id} updated!")
                st.json(response.json())
            else:
                st.error(response.json()["detail"])
        else:
            st.warning("Provide at least one field to update!")

elif option == "Delete User":
    st.subheader("🗑 Delete User")
    user_id = st.number_input("User ID", min_value=1)
    if st.button("Delete User"):
        response = requests.delete(f"{BASE_URL}/user/{user_id}")
        if response.status_code == 200:
            st.success(f"User {user_id} deleted successfully!")
        else:
            st.error(response.json()["detail"])

elif option == "Analyze Text":
    st.subheader("📊 Text Analysis")
    user_id = st.number_input("User ID", min_value=1)
    if st.button("Analyze"):
        response = requests.post(f"{BASE_URL}/user/{user_id}/analyze")
        if response.status_code == 200:
            st.success(f"Text analysis for User {user_id}:")
            st.json(response.json())
        else:
            st.error(response.json()["detail"])