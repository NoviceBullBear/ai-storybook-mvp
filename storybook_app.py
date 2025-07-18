import streamlit as st
import os
import openai

# Load OpenAI API key from environment
openai.api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="AI Storybook", page_icon="📖")
st.title("📖 AI Storybook Generator")

st.write("Create a personalized short story based on your name, genre, and age!")

# User Inputs
name = st.text_input("Enter a name for the main character", "Alex")
age = st.slider("Select their age", 3, 80, 10)
genre = st.selectbox("Choose a genre", ["Adventure", "Fantasy", "Thriller", "Romance", "Sci-Fi"])
length = st.radio("Choose story length", ["Short (500 words)", "Medium (1000 words)"])

if st.button("Generate Story"):
    with st.spinner("Crafting your tale..."):

        prompt = (
            f"Write a {length.lower()} {genre.lower()} story featuring a main character named {name}, "
            f"who is {age} years old. The story should be engaging, appropriate for their age, and imaginative."
        )

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.8,
                max_tokens=1500
            )
            story = response['choices'][0]['message']['content']

            st.subheader("📝 Your Story:")
            st.write(story)

            st.download_button("📥 Download Story", story, file_name=f"{name}_story.txt")

        except Exception as e:
            st.error(f"Something went wrong: {e}")


