import streamlit as st
import pandas as pd
import requests
import base64
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# Access GitHub Token
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
if not GITHUB_TOKEN:
    st.error("GitHub Token not found. Please check your .env file.")
    st.stop()

REPO_NAME = "hireshnaik1989/fast-item-search-app"
BRANCH_NAME = "main"

# Load CSV data
@st.cache_data
def load_data():
    return pd.read_csv('data.csv')

df = load_data()

# Streamlit App
st.title('Fast Item Search App')
st.text('Search using Item Code, UPC ID, or Item Name')

# Search Input
query = st.text_input('Enter your search query:')

# Perform Search
if query:
    query = query.strip().lower()
    results = df[df.apply(lambda row: 
        query in str(row['Item Code']).lower() or 
        query in str(row['UPC ID']).lower() or 
        query in str(row['Item Name']).lower(), axis=1)]
    
    if not results.empty:
        st.write(f"Results Found: {len(results)}")
        st.dataframe(results)
    else:
        st.write('No results found.')

# File Upload to GitHub
st.subheader("Upload a CSV File to GitHub (Renamed as data.csv)")

uploaded_file = st.file_uploader("Choose a CSV file to upload", type=['csv'])
if uploaded_file is not None:
    file_content = uploaded_file.read()
    encoded_content = base64.b64encode(file_content).decode('utf-8')

    # Force the filename to be 'data.csv'
    file_name = "data.csv"
    github_url = f"https://api.github.com/repos/{REPO_NAME}/contents/{file_name}"

    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }

    # Prepare data for API request
    data = {
        "message": "Update data.csv with new upload",
        "content": encoded_content,
        "branch": BRANCH_NAME
    }

    # Check if the file exists using GET request
    check_response = requests.get(github_url, headers=headers)
    if check_response.status_code == 200:
        sha = check_response.json().get('sha')
        data["sha"] = sha

    # Upload or Update file using PUT request
    response = requests.put(github_url, json=data, headers=headers)

    if response.status_code in [200, 201]:
        st.success(f"File uploaded successfully: {response.json()['content']['html_url']}")
    else:
        st.error(f"Failed to upload file: {response.json()}")

# Confirm token loading
print("Token Loaded:", GITHUB_TOKEN)
