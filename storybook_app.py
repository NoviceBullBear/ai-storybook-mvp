import streamlit as st
import os
import openai

# Set OpenAI key securely
openai.api_key = st.secrets["OPENAI_API_KEY"]

st.set_page_config(page_title="AI Storybook", page_icon="📖")
st.title("📖 AI Storybook Generator")

st.write("Craft a personalized story by choosing characters, genre, and theme!")

# 👫 Number of characters
character_count = st.radio("Number of main characters", [1, 2])

# 📚 Genre selector with more options
genre_options = [
    "Adventure", "Fantasy", "Sci-Fi", "Mystery", "Thriller", "Romance", "Comedy",
    "Horror", "Superhero", "Coming of Age", "Historical Fiction", "Mythology", "Western",
    "Detective", "Time Travel", "Space Opera", "Fairy Tale", "Dystopian", "Cyberpunk"
]
genre = st.selectbox("Choose a genre", genre_options)

# 🎭 Sub-theme selector
theme_options = {
    "Adventure": ["Treasure Hunt", "Jungle Escape", "Pirate Voyage"],
    "Fantasy": ["Magic School", "Dragon Quest", "Elven Kingdom"],
    "Romance": ["Enemies to Lovers", "Lost Love", "Holiday Romance"],
    "Sci-Fi": ["Alien Encounter", "Robot Rebellion", "Futuristic City"],
    "Mystery": ["Whodunnit", "Locked Room", "Missing Artifact"],
    "Horror": ["Haunted House", "Cursed Object", "Urban Legend"]
}
theme = st.selectbox("Select a theme (if applicable)", theme_options.get(genre, ["General"]))

# 🎂 Age and validation
age = st.slider("Character's Age", min_value=3, max_value=80, value=10)

# 🔐 Romance restriction
if genre == "Romance" and age < 18:
    st.error("Romance stories are only available for characters aged 18 or over.")
    st.stop()

# 👤 Names
name1 = st.text_input("Main character's name", "Alex")
name2 = ""
if character_count == 2:
    name2 = st.text_input("Second character's name", "Jamie")

# 📝 Story length
length = st.radio("Story length", ["Short (500 words)", "Medium (1000 words)"])

# Generate story
if st.button("Generate Story"):
    with st.spinner("Spinning the tale..."):

        # Construct base prompt
        characters = f"{name1}" if character_count == 1 else f"{name1} and {name2}"
        prompt = (
            f"Write a {length.lower()} {genre.lower()} story with the theme '{theme}'. "
            f"The main character(s) are {characters}, age {age}. "
            f"The story should be age-appropriate, engaging, and imaginative."
        )

        try:
            response = openai.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.8,
                max_tokens=1500
            )
            story = response.choices[0].message.content
            st.subheader("📝 Your Story:")
            st.write(story)
            st.download_button("📥 Download Story", story, file_name=f"{name1}_story.txt")

        except Exception as e:
            st.error(f"Something went wrong: {e}")
