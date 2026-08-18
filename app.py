import streamlit as st
import random

st.set_page_config(page_title="Status Simulator", page_icon="📱", layout="centered")

# Custom CSS to make it look clean on mobile
st.markdown("""
<style>
    .stApp { max-width: 600px; margin: 0 auto; }
    .feed-box { border: 1px solid #e1e8ed; border-radius: 12px; padding: 15px; margin-bottom: 15px; background-color: #ffffff; }
    .comment-box { margin-left: 20px; border-left: 3px solid #1da1f2; padding-left: 10px; margin-top: 10px; }
</style>
""", unsafe_allow_html=True)

# Initialize Session State variables
if "followers" not in st.session_state:
    st.session_state.followers = 100
if "reputation" not in st.session_state:
    st.session_state.reputation = "Neutral 😄"
if "history" not in st.session_state:
    st.session_state.history = []

# Sidebar for Mobile Controls
with st.sidebar:
    st.title("👤 Your Dashboard")
    st.metric(label="Followers", value=f"{st.session_state.followers:,}")
    st.subheader(f"Status: {st.session_state.reputation}")
    
    universe = st.selectbox(
        "Choose Fandom / Universe",
        ["Standard Internet", "Hogwarts Social", "Anime World", "K-Pop Stan Twitter"]
    )
    
    st.divider()
    if st.button("Reset Game 🔄"):
        st.session_state.followers = 100
        st.session_state.reputation = "Neutral 😄"
        st.session_state.history = []
        st.rerun()

# Main Application Feed
st.title("📱 Status Simulator")
st.caption(f"Currently broadcasting to the **{universe}** universe.")

user_post = st.text_area("What are you thinking?", placeholder="Type your post here...", max_chars=280)

if st.button("🚀 Post to Feed"):
    if user_post.strip() == "":
        st.error("You can't post an empty thoughts draft!")
    else:
        change = random.randint(-40, 120)
        st.session_state.followers = max(0, st.session_state.followers + change)
        
        if st.session_state.followers > 500:
            st.session_state.reputation = "Influencer 🌟"
        elif st.session_state.followers < 20:
            st.session_state.reputation = "Cancelled ❌"
        else:
            st.session_state.reputation = "Neutral 😄"
            
        mock_comments = {
            "Standard Internet": [("@troll_master", "Lmao delete this immediately."), ("@bestie_99", "Preach! Louder for the people in the back! 🙌"), ("@brand_bot", "Check your DMs for a collab deal!")],
            "Hogwarts Social": [("@draco_m", "My father will hear about this awful post."), ("@hermione_g", "Honestly, did you even read Hogwarts: A History?"), ("@potter_j", "Brilliant post mate, Gryffindor wins 10 points.")],
            "Anime World": [("@sub_over_dub", "This post is filler arc material."), ("@hokage_hopeful", "Believe it! This is a top-tier take."), ("@senpai_noticed", "Nani? What does this even mean??")],
            "K-Pop Stan Twitter": [("@orbit_universe", "Clear the searches and stream the new music video instead."), ("@bias_stan", "Omo! This is literal perfection."), ("@anti_patrol", "Delete this before the fandom reporting accounts see it.")]
        }
        
        current_comments = mock_comments.get(universe, mock_comments["Standard Internet"])
        
        st.session_state.history.insert(0, {
            "post": user_post,
            "change": change,
            "comments": current_comments
        })
        st.rerun()

# Display Timeline
st.divider()
if not st.session_state.history:
    st.info("Your feed is empty. Write your very first post above!")
else:
    for idx, item in enumerate(st.session_state.history):
        st.markdown(f"""
        <div class="feed-box">
            <strong>You Posted:</strong><br>
            {item['post']}<br>
            <small style="color: {'green' if item['change'] >= 0 else 'red'};">
                {'📈 +' if item['change'] >= 0 else '📉 '}{item['change']} followers
            </small>
        </div>
        """, unsafe_allow_html=True)
        
        for user, comment in item["comments"]:
            st.markdown(f"""
            <div class="comment-box">
                <strong>{user}</strong>: {comment}
            </div>
            """, unsafe_allow_html=True)
