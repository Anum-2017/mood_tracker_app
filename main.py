import streamlit as st
import pandas as pd
import csv
import datetime
import os
import plotly.express as px
import random

st.set_page_config(page_title="Mood Tracker", page_icon="🌈", layout="wide")

st.markdown("""
    <style>
        /* Styling for Mood Log Button */
        .stButton>button {
            background-color: #4CAF50; 
            color: white;
            border: none;
            border-radius: 12px;
            padding: 12px 30px;
            font-size: 18px;
            cursor: pointer;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            transition: background-color 0.3s ease;
            width: 100%;
        }

        .stButton>button:hover {
            background-color: #45a049;
            transform: scale(1.05); /* Hover scale effect */
        }

        /* Sidebar adjustments */
        .stSidebar .sidebar-content {
            padding: 20px;
            background-color: #f1f1f1;
        }

        /* Success message styling */
        .stSuccess>div {
            padding: 12px;
            background-color: #d4edda;
            color: #155724;
            border-radius: 8px;
            font-size: 16px;
            border: 1px solid #c3e6cb;
            margin-top: 20px;
        }

        /* Main page title */
        h1 {
            font-size: 40px;
            color: #4CAF50;
            text-align: center;
            margin-bottom: 20px;
        }

        /* Insights Section */
        .insight-header {
            font-size: 24px;
            font-weight: bold;
            color: #333;
            margin-top: 40px;
            text-align: center;
        }

        .stImage {
            margin-top: 20px;
            display: block;
            margin-left: auto;
            margin-right: auto;
        }

        .stWrite {
            font-size: 18px;
            color: #333;
            text-align: center;
            margin-bottom: 20px;
        }

        /* Custom Selectbox Styling */
        .stSelectbox select {
            font-size: 18px;   /* Same font size as button */
            padding: 12px 30px; /* Same padding as button */
            width: 50%;          /* Same width as button */
            border-radius: 12px; /* Same border radius as button */
            border: 2px solid #4CAF50; /* Same border color as button */
        }
        
    </style>
""", unsafe_allow_html=True)

# File to store mood data
MOOD_FILE = "mood_data.csv"
JOURNAL_FILE = "journal_entries.txt"

# Function to load mood data safely
def load_mood_data():
    if not os.path.exists(MOOD_FILE) or os.stat(MOOD_FILE).st_size == 0:
        return pd.DataFrame(columns=["Date", "Mood"])

    df = pd.read_csv(MOOD_FILE)
    df.columns = [col.strip() for col in df.columns]
    
    if "Date" not in df.columns or "Mood" not in df.columns:
        st.error("❌ CSV file format is incorrect! Deleting and recreating...")
        os.remove(MOOD_FILE)
        return pd.DataFrame(columns=["Date", "Mood"])
    
    return df

# Function to save mood data safely
def save_mood_data(date, mood):
    file_exists = os.path.exists(MOOD_FILE)
    with open(MOOD_FILE, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        if not file_exists or os.stat(MOOD_FILE).st_size == 0:
            writer.writerow(["Date", "Mood"])
        writer.writerow([date, mood])

# Function to calculate mood insights
def get_mood_insights(data):
    mood_counts = data["Mood"].value_counts()
    most_frequent_mood = mood_counts.idxmax()
    most_frequent_count = mood_counts.max()
    total_entries = len(data)
    return most_frequent_mood, most_frequent_count, total_entries

# Function to get a random motivational quote or joke
def get_fun_insight(mood):
    quotes = {
    "😊 Happy": [
        "You are a Super Star today! Keep smiling and spread positivity! 😄", 
        "The best way to predict the future is to create it! 💪"
    ],
    "😢 Sad": [
        "It's okay to feel low sometimes. Take a deep breath, you got this! 💖", 
        "Remember, every storm passes, and there's always a rainbow after it! 🌈"
    ],
    "😡 Angry": [
        "Anger is temporary. Calm down and remember peace starts from within! 🧘", 
        "Take a moment to breathe, you'll feel much better! 💭"
    ],
    "😰 Stressed": [
        "Take a break, do some deep breathing. You deserve peace of mind! 🧘", 
        "Stress is like a rocking chair: it gives you something to do but gets you nowhere! 😌"
    ],
    "😟 Anxious": [
        "It's normal to feel anxious. Try some relaxation techniques to calm down. 🧘", 
        "Breathe in, breathe out. You got this! 💪"
    ],
    "😐 Neutral": [
        "Sometimes neutrality is the best approach! Keep the balance and move forward! ⚖️"
    ],
    "😆 Excited": [
        "The world is yours to conquer! Seize the day and let your excitement fuel you! 🌟", 
        "Good things are coming your way. Stay excited and keep going! 🚀"
    ],
    "😲 Surprised": [
        "Wow! What a pleasant surprise! Enjoy the unexpected moments! 🎉", 
        "Embrace the surprises that life throws at you—they often lead to great adventures! ✨"
    ],
    "🤔 Confused": [
        "It's okay to feel confused. Take a moment, gather your thoughts, and clarity will follow. 🧠", 
        "Confusion is the first step towards discovery. Keep going! 🔍"
    ],
    "😴 Bored": [
        "Sometimes boredom leads to creativity. Use this time to explore something new! 🎨", 
        "Boredom is just a temporary feeling. Find a new hobby or interest to dive into! 📚"
    ],
    "😍 Love": [
        "Love is a powerful force. Let it guide you to amazing places today! 💖", 
        "Spread love wherever you go. It makes the world a better place! 🌍"
    ],
    "😩 Tired": [
        "Rest is just as important as work. Take a moment to recharge, you'll feel better! 😴", 
        "Tired? Take a break and come back stronger. You got this! 💪"
    ],
    "😬 Nervous": [
        "Nerves are just excitement in disguise. You've got everything under control! 🌟", 
        "It's okay to feel nervous. Take a deep breath, and trust in yourself! 💖"
    ],
    "😳 Shy": [
        "Shyness is just a small step towards growth. Believe in yourself and take that step forward! 🌱", 
        "Everyone feels shy at times. Embrace it, and let your confidence shine through! ✨"
    ],
    "🙏 Grateful": [
        "Gratitude is the key to happiness. Appreciate every little moment today! 🙏", 
        "Being grateful brings peace and joy. Take a moment to reflect on your blessings. 🌸"
    ],
    "😳 Embarrassed": [
        "It's okay to feel embarrassed. Just remember, everyone has those moments! 🌻", 
        "Laugh it off and move forward—embarrassment is temporary! 😊"
    ],
    "🤞 Hopeful": [
        "Hope is the light that guides you through challenges. Keep believing! 🌟", 
        "Your hope is powerful. Keep dreaming, the future is bright! ✨"
    ],
    "😞 Lonely": [
        "You're never truly alone. Reach out, there are people who care about you! 💖", 
        "Loneliness is just a moment. Things will get better soon, hang in there! 🤗"
    ],
    "🧐 Curious": [
        "Curiosity leads to great discoveries. Keep asking questions and seeking answers! 🔍", 
        "The world is full of wonders. Keep exploring, there's always something new to learn! 🌍"
    ],
    "😌 Relaxed": [
        "Relaxation is the key to a peaceful mind. Take a moment to breathe and enjoy the calm. 🌿", 
        "Sometimes the best thing to do is nothing at all. Enjoy this moment of peace. 😌"
    ],
    "😎 Proud": [
        "You’ve come so far! Be proud of your achievements and keep pushing forward. 🌟", 
        "Pride in yourself is the first step to greatness. Keep going! 💪"
    ],
    "💪 Determined": [
        "Your determination is your superpower. Keep going, nothing can stop you! 💥", 
        "Stay focused, stay determined. Success is right around the corner! 🚀"
    ],
    "🤪 Playful": [
        "Life is too short to be serious all the time! Let your playful side shine through! 😜", 
        "Playfulness is the key to a happy heart. Embrace the fun! 🎉"
    ],
    "😎 Confident": [
        "Confidence is magnetic. Let your self-assurance lead the way today! ✨", 
        "You've got the power to conquer anything. Trust in your abilities! 💪"
    ],
    "🤪 Silly": [
        "Let your inner silly out and have some fun today! Life is better with laughter. 😜", 
        "Don't take things too seriously. Embrace the silliness and enjoy the ride! 🤪"
    ],
    "🕊️ Peaceful": [
        "Peace comes from within. Embrace the calm and let your soul rest. 🌿", 
        "Find peace in the present moment. Breathe and let go of any stress. 🧘"
    ],
    "😣 Frustrated": [
        "Frustration is a sign that you're pushing yourself. Take a deep breath and keep going! 💪", 
        "Sometimes the hardest paths lead to the most rewarding destinations. Keep moving forward! 🚶"
    ],
    "😌 Relieved": [
        "Ahh, the feeling of relief! Take a moment to appreciate how far you’ve come. 🌟", 
        "Relief is like a deep breath after a long day. You deserve it! 💖"
    ],
    "🎉 Lively": [
        "Stay lively and spread your energy wherever you go today! 🎉", 
        "Your lively spirit brings joy to everyone around you. Keep shining! ✨"
    ],
    "❤️ Affectionate": [
        "Show affection to those around you, love is the greatest gift you can give! 💖", 
        "Affection creates bonds that last a lifetime. Spread love today! 🥰"
    ],
    "🧠 Reflective": [
        "Take some time to reflect on your journey. Growth happens when you look back. 🌱", 
        "Reflection helps us move forward. Use it as a tool for personal growth. 💭"
    ],
    "🎯 Focused": [
        "Focus is the key to success. Stay on track and keep pushing towards your goal! 🎯", 
        "When you focus, you can achieve anything. Stay sharp and keep moving forward! 💥"
    ],
    "😌 Mellow": [
        "Take it easy today and enjoy the calm. Sometimes less is more! 🌿", 
        "Mellow out and enjoy the quiet moments. Peace is within reach. 🌸"
    ],
    "🤩 Joyful": [
        "Let your joy light up the world! Your happiness is contagious! 😄", 
        "Joy is a choice. Choose to embrace it today and every day! 🎉"
    ],
    "🧘‍♀️ Calm": [
        "Find peace within yourself. Take a deep breath and enjoy the stillness. 🌊", 
        "Calmness is the foundation for a peaceful day. Take it slow and steady. 🌸"
    ],
    "💭 Thoughtful": [
        "A thoughtful mind creates a thoughtful world. Keep reflecting and growing. 💭", 
        "Being thoughtful brings meaning to your actions. Keep making the world a better place! 🌍"
    ],
    "🐾 Playful": [
        "Let the fun begin! Be playful and enjoy every moment! 🐾", 
        "Playfulness keeps the spirit young. Have fun and enjoy the little things! 🎉"
    ]
}
    
    return random.choice(quotes.get(mood, ["Stay strong! 💪"]))

# App Title
st.title("🌈 Mood Tracker - Capture Your Emotional Moments")

# Get Today's Date
today = datetime.datetime.today().strftime("%Y-%m-%d")

# Sidebar for Mood Selection
st.sidebar.markdown("<h2 style='text-align: center; font-weight: bold;'>📅 Log Your Mood</h2>", unsafe_allow_html=True)
mood = st.sidebar.selectbox("**How are you feeling today?**", [
    "😊 Happy", "😢 Sad", "😡 Angry", "😰 Stressed", "😟 Anxious", "😐 Neutral", 
    "😆 Excited", "😲 Surprised", "🤔 Confused", "😴 Bored", "😍 Love", "😩 Tired",
    "😬 Nervous", "😳 Shy", "🙏 Grateful", "😳 Embarrassed", "🤞 Hopeful", 
    "😞 Lonely", "🧐 Curious", "😌 Relaxed", "😎 Proud", "💪 Determined", 
    "🤪 Playful", "😎 Confident", "🤪 Silly", "🕊️ Peaceful", "😣 Frustrated", 
    "😌 Relieved", "🎉 Lively", "❤️ Affectionate", "🧠 Reflective", "🎯 Focused",
    "😌 Mellow", "🤩 Joyful", "🧘‍♀️ Calm", "💭 Thoughtful", "🐾 Playful"
])


# Log Mood Button
if st.sidebar.button("Log Your Mood"):
    save_mood_data(today, mood)
    st.sidebar.success("✅ Mood Logged Successfully! 🎉")

# Load mood data
data = load_mood_data()

# Ensure DataFrame is not empty
if not data.empty:
    # Get mood insights
    most_frequent_mood, most_frequent_count, total_entries = get_mood_insights(data)
    
    # Display insights
    st.subheader("🌟 Mood Insights")
    # st.write(f"**Your most frequent mood is:** **{most_frequent_mood}** with **{most_frequent_count}** occurrences. 🌟")
    st.write(f"**Your most frequent mood is:** <span style='color:blue;'>**{most_frequent_mood}**</span> with <span style='color:red;'>**{most_frequent_count}**</span> occurrences. 🌟", unsafe_allow_html=True)
    # st.write(f"You've logged a total of **{total_entries}** mood entries so far. 📊")
    # Using HTML to change color
    st.write(f"You've logged a total of <span style='color:green;'>**{total_entries}**</span> mood entries so far. 📊", unsafe_allow_html=True)

    # Visualization for mood trends
    st.subheader("📊 Mood Frequency")
    mood_counts = data["Mood"].value_counts()
    fig = px.bar(mood_counts, x=mood_counts.index, y=mood_counts.values, 
                 labels={'x':'Mood', 'y':'Count'}, 
                 color=mood_counts.index, color_discrete_sequence=px.colors.qualitative.Pastel)
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("💬 Fun Insight: ")
    st.markdown(
    f"<div style='font-size: 18px; font-weight: bold; color: #FF6F61; padding: 10px; background-color: #F7F7F7; border-radius: 10px;'>"
    f"{get_fun_insight(mood)}"
    f"</div>",
    unsafe_allow_html=True
)
    
else:
    st.markdown("<p style='text-align: center;'>No mood data available yet. Please log your first mood entry. 📝</p>", unsafe_allow_html=True)