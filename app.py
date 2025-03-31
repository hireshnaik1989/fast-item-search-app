import streamlit as st
import pandas as pd

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
