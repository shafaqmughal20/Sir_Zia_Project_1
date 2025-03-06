
import streamlit as st
import pandas as pd
import os
from io import BytesIO

st.set_page_config(page_title="Data Sweppar", layout="wide")

# Custom Styling
st.markdown(
    """
    <style>
    .stApp {
        background-color: #121212;
        color: white;
        font-size: 18px;
        font-family: 'Arial', sans-serif;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True
)

# Title and Description
st.title("📊 Data Sweppar - Streamlined Data Processing By Saad Qureshi")
st.write("Effortlessly clean, transform, and visualize your data.")

# Upload Files
uploaded_files = st.file_uploader("📂 Upload your CSV or Excel files:", type=["csv", "xlsx"], accept_multiple_files=True)

dataframes = {}
if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()
        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"Invalid file type: {file_ext}")
            continue
        dataframes[file.name] = df

# Display Data Preview
if dataframes:
    st.subheader("📄 Data Preview")
    selected_file = st.selectbox("Choose a file to preview:", list(dataframes.keys()))
    st.dataframe(dataframes[selected_file].head())

    # Data Cleaning Options
    st.subheader("🛠 Data Cleaning")
    df = dataframes[selected_file]
    
    if st.button("Remove Duplicates"):
        df.drop_duplicates(inplace=True)
        st.success("✅ Duplicates removed!")

    if st.button("Fill Missing Values"):
        numeric_cols = df.select_dtypes(include=['number']).columns
        df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
        st.success("✅ Missing values filled!")
    
    # Column Selection
    st.subheader("📌 Select Columns to Visualize")
    selected_columns = st.multiselect("Choose columns:", df.columns, default=df.columns)
    df = df[selected_columns]

    # Data Visualization
    st.subheader("📈 Data Visualization")
    if st.checkbox("Show Bar Chart"):
        st.bar_chart(df.select_dtypes(include=['number']))

    # File Conversion
    st.subheader("🔄 Convert & Download Data")
    conversion_type = st.radio("Convert file to:", ["CSV", "Excel"], key=selected_file)
    if st.button("Download File"):
        buffer = BytesIO()
        if conversion_type == "CSV":
            df.to_csv(buffer, index=False)
            file_name = selected_file.replace(file_ext, ".csv")
            mime_type = "text/csv"
        elif conversion_type == "Excel":
            df.to_excel(buffer, index=False)
            file_name = selected_file.replace(file_ext, ".xlsx")
            mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        buffer.seek(0)
        st.download_button(
            label=f"Download {conversion_type}",
            data=buffer,
            file_name=file_name,
            mime=mime_type
        )
        st.success("All files downloaded successfully")