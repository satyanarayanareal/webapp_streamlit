import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns

# Set the page config
st.set_page_config(page_title='Data Visualizer', layout='centered', page_icon='📊')

# Title
st.title('📊 Elegant Data Visualizer')

# Getting the working directory of main.py
working_dir = os.path.dirname(os.path.abspath(__file__))

# Folder containing CSV files
folder_path = os.path.join(working_dir, "data")

# List all CSV files
files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

# File selection
selected_file = st.selectbox('📂 Select a CSV file to explore', files, index=None)

if selected_file:
    file_path = os.path.join(folder_path, selected_file)
    df = pd.read_csv(file_path)

    st.markdown("---")
    st.subheader('📋 Data Preview')
    st.dataframe(df.head(), use_container_width=True)

    st.markdown("---")
    st.subheader('🎯 Choose Plot Settings')

    col1, col2 = st.columns(2)

    columns = df.columns.tolist()

    with col1:
        x_axis = st.selectbox('🧭 Select X-axis', options=columns+["None"])
    with col2:
        y_axis = st.selectbox('🎯 Select Y-axis', options=columns+["None"])

    plot_list = ['Line Plot', 'Bar Chart', 'Scatter Plot', 'Distribution Plot', 'Count Plot']
    plot_type = st.selectbox('🛠️ Select Plot Type', options=plot_list)

    if st.button('🚀 Generate Plot'):
        if x_axis == "None" or (y_axis == "None" and plot_type not in ["Distribution Plot", "Count Plot"]):
            st.warning("⚠️ Please select valid X and Y axes.")
        else:
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.set_style("whitegrid")

            if plot_type == 'Line Plot':
                sns.lineplot(x=df[x_axis], y=df[y_axis], ax=ax)
            elif plot_type == 'Bar Chart':
                sns.barplot(x=df[x_axis], y=df[y_axis], ax=ax)
            elif plot_type == 'Scatter Plot':
                sns.scatterplot(x=df[x_axis], y=df[y_axis], ax=ax)
            elif plot_type == 'Distribution Plot':
                sns.histplot(df[x_axis], kde=True, color="skyblue", ax=ax)
                y_axis = 'Density'
            elif plot_type == 'Count Plot':
                sns.countplot(x=df[x_axis], palette="Set2", ax=ax)
                y_axis = 'Count'

            ax.set_xlabel(x_axis, fontsize=12)
            ax.set_ylabel(y_axis if y_axis else '', fontsize=12)
            plt.title(f'{plot_type}: {y_axis} vs {x_axis}', fontsize=16, color="#5DADE2")
            plt.xticks(rotation=45, ha='right', fontsize=10)
            plt.yticks(fontsize=10)

            st.pyplot(fig)

