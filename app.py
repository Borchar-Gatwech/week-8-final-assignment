# app.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

st.title("CORD-19 Data Explorer")
st.write("Explore COVID-19 research papers from the CORD-19 dataset")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("data/metadata.csv")
    df = df[['title', 'abstract', 'publish_time', 'journal', 'source_x']].copy()
    df.dropna(subset=['title', 'publish_time'], inplace=True)
    df['publish_time'] = pd.to_datetime(df['publish_time'], errors='coerce')
    df.dropna(subset=['publish_time'], inplace=True)
    df['year'] = df['publish_time'].dt.year
    return df

df = load_data()

# Sidebar filters
year_range = st.slider("Select Year Range", int(df['year'].min()), int(df['year'].max()), (2020, 2021))
filtered = df[(df['year'] >= year_range[0]) & (df['year'] <= year_range[1])]

st.write(f"### Showing {len(filtered)} papers from {year_range[0]}–{year_range[1]}")

# Publications per year
st.subheader("Publications by Year")
year_counts = filtered['year'].value_counts().sort_index()
fig, ax = plt.subplots()
sns.barplot(x=year_counts.index, y=year_counts.values, ax=ax, palette="Blues_d")
st.pyplot(fig)

# Top journals
st.subheader("Top Journals")
top_journals = filtered['journal'].value_counts().head(10)
fig, ax = plt.subplots()
sns.barplot(y=top_journals.index, x=top_journals.values, ax=ax, palette="viridis")
st.pyplot(fig)

# Word Cloud
st.subheader("Word Cloud of Titles")
text = " ".join(filtered['title'].dropna().tolist())
wordcloud = WordCloud(width=800, height=400, background_color="white").generate(text)
fig, ax = plt.subplots(figsize=(10,5))
ax.imshow(wordcloud, interpolation="bilinear")
ax.axis("off")
st.pyplot(fig)

# Data preview
st.subheader("Sample Data")
st.write(filtered.sample(5))
