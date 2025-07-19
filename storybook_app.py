import streamlit as st
import openai
import os
from fpdf import FPDF

# Set OpenAI key securely
openai.api_key = st.secrets["OPENAI_API_KEY"]

st.set_page_config(page_title="AI Storybook", page_icon="📖")
st.title("📖 AI Storybook Generator")

st.write("Craft a personalized AI-generated story with narrator style, dedication, and PDF download!")

# 👫 Character count
character_count = st.radio("Number of main characters", [1, 2])

# 👤 Character names and ages
name1 = st.text_input("First character's name", "Alex")
age1 = st.slider("Age of first character", 3, 80, 10)

name2, age2 = "", None
if character_count == 2:
    name2 = st.text_input("Second character's name", "Jamie")
    age2 = st.slider("Age of second character", 3, 80, 10)

# 📚 Genre
genres = [
    "Adventure", "Fantasy", "Sci-Fi", "Mystery", "Thriller", "Romance", "Comedy",
    "Horror", "Superhero", "Coming of Age", "Historical Fiction", "Mythology",
    "Western", "Detective", "Time Travel", "Space Opera", "Fairy Tale", "Dystopian", "Cyberpunk"
]
genre = st.selectbox("Genre", genres)

# 🛑 Romance age gate
if genre == "Romance" and (age1 < 18 or (character_count == 2 and age2 < 18)):
    st.error("Romance stories require all characters to be 18 or older.")
    st.stop()

# 🎭 Theme
themes = {
    "Fantasy": ["Dragon Quest", "Magic School", "Elven Kingdom"],
    "Romance": ["Enemies to Lovers", "Lost Love", "Holiday Romance"],
    "Sci-Fi": ["Alien Encounter", "Time Loop", "AI Takeover"],
    "Mystery": ["Whodunnit", "Vanishing", "Heist"],
    "Horror": ["Haunted House", "Curse", "Urban Legend"]
}
theme = st.selectbox("Story theme (optional)", themes.get(genre, ["General"]))

# 🎁 Gift dedication
dedication = st.text_input("🎁 This story is for...", placeholder="My son Jack")

# 💬 Narrator style
narrator = st.selectbox("Narrator style", ["Neutral", "Poetic", "Sarcastic", "Noir Detective"])

# Story length
length = st.radio("Story length", ["Short (500 words)", "Medium (1000 words)"])

# Generate button
if st.button("Generate Story"):
    with st.spinner("Generating your personalized story..."):

        characters = f"{name1} (age {age1})" if character_count == 1 else f"{name1} (age {age1}) and {name2} (age {age2})"
        prompt = (
            f"Write a {length.lower()} {genre.lower()} story with the theme '{theme}'. "
            f"The story is for {dedication}. The main characters are {characters}. "
            f"Use a {narrator.lower()} narrator voice. Make it age-appropriate, imaginative, and engaging."
        )

        try:
            response = openai.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.8,
                max_tokens=1500
            )
            story = response.choices[0].message.content

            # 📝 Display the story
            st.subheader("📖 Your Story")
            st.write(story)

            # 📄 Create PDF
            pdf = FPDF()
            pdf.add_page()
            pdf.set_auto_page_break(auto=True, margin=15)
            pdf.set_font("Arial", size=12)
            for line in story.split('\n'):
                pdf.multi_cell(0, 10, line)
            pdf.output("/tmp/story.pdf")

            with open("/tmp/story.pdf", "rb") as f:
                st.download_button("📥 Download as PDF", f, file_name="storybook.pdf")

        except Exception as e:
            st.error(f"Something went wrong: {e}")
