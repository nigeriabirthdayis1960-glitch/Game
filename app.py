import streamlit as st
import random
import time

# Set up clean mobile viewport layout
st.set_page_config(page_title="Status", page_icon="📱", layout="centered")

# Custom CSS to mimic a premium social media app interface
st.markdown("""
<style>
    .stApp { background-color: #0f1419; color: #e7e9ea; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; }
    [data-testid="stSidebar"] { background-color: #15181c !important; }
    .header-container { display: flex; align-items: center; justify-content: space-between; border-bottom: 1px solid #2f3336; padding-bottom: 15px; margin-bottom: 20px; }
    .feed-card { background-color: #15181c; border: 1px solid #2f3336; border-radius: 16px; padding: 16px; margin-bottom: 16px; box-shadow: 0 4px 12px rgba(0,0,0,0.2); }
    .user-header { display: flex; align-items: center; gap: 10px; margin-bottom: 8px; }
    .avatar { width: 40px; height: 40px; border-radius: 50%; background: linear-gradient(45deg, #1d9bf0, #8ecdf8); display: flex; align-items: center; justify-content: center; font-weight: bold; color: white; }
    .npc-avatar { width: 32px; height: 32px; border-radius: 50%; background: #2f3336; display: flex; align-items: center; justify-content: center; font-size: 14px; }
    .username { font-weight: 700; color: #e7e9ea; }
    .handle { color: #71767b; font-size: 14px; }
    .post-text { font-size: 16px; line-height: 1.5; color: #e7e9ea; margin-bottom: 12px; }
    .stat-badge { background-color: rgba(29, 155, 240, 0.1); color: #1d9bf0; padding: 4px 10px; border-radius: 9999px; font-size: 12px; font-weight: bold; display: inline-block; }
    .stat-badge-down { background-color: rgba(244, 33, 46, 0.1); color: #f4212e; padding: 4px 10px; border-radius: 9999px; font-size: 12px; font-weight: bold; display: inline-block; }
    .comment-section { border-top: 1px solid #2f3336; margin-top: 12px; padding-top: 12px; display: flex; flex-direction: column; gap: 12px; }
    .comment-item { display: flex; gap: 10px; background: rgba(255,255,255,0.02); padding: 10px; border-radius: 8px; }
    textarea { background-color: #15181c !important; color: #e7e9ea !important; border: 1px solid #2f3336 !important; border-radius: 12px !important; }
    button { background-color: #1d9bf0 !important; color: white !important; border-radius: 9999px !important; border: none !important; font-weight: bold !important; width: 100% !important; }
</style>
""", unsafe_allow_html=True)

# Initialize game states
if "followers" not in st.session_state: st.session_state.followers = 1240
if "clout" not in st.session_state: st.session_state.clout = 50
if "history" not in st.session_state: st.session_state.history = []

# Sidebar Navigation Panel
with st.sidebar:
    st.markdown("### ⚙️ SIMULATOR SETTINGS")
    universe = st.selectbox("Feed Sector", ["Global Feed", "Hogwarts Network", "Anime Hub", "K-Pop Twitter"])
    st.divider()
    st.markdown("### 📊 LIFE STATS")
    st.metric("Followers 👥", f"{st.session_state.followers:,}")
    st.progress(st.session_state.clout / 100, text=f"Clout Level: {st.session_state.clout}%")
    
    if st.button("Clear Profile 🔄"):
        st.session_state.followers = 1240
        st.session_state.clout = 50
        st.session_state.history = []
        st.rerun()

# Header Dashboard
st.markdown(f"""
<div class="header-container">
    <div>
        <h2 style='margin:0;'>STATUS AI</h2>
        <span style='color:#71767b;'>Sector: {universe}</span>
    </div>
    <div class="avatar">ME</div>
</div>
""", unsafe_allow_html=True)

# Post Creator Input Box
user_post = st.text_area("", placeholder="What's your hot take today?...", max_chars=280, label_visibility="collapsed")

if st.button("✨ Publish Post"):
    if user_post.strip() != "":
        with st.spinner("Processing network metrics..."):
            time.sleep(0.6) # Short delay to give it an authentic application feel
            
            # Simulated context analyzer logic to pick clever algorithmic replies
            words = user_post.lower()
            if any(w in words for w in ["hate", "bad", "worst", "trash"]):
                sentiment = "drama"
            elif any(w in words for w in ["love", "amazing", "best", "hype"]):
                sentiment = "positive"
            else:
                sentiment = "neutral"

            # Point variations
            follower_change = random.randint(15, 250) if sentiment == "positive" else random.randint(-150, 400)
            st.session_state.followers = max(5, st.session_state.followers + follower_change)
            st.session_state.clout = min(100, max(0, st.session_state.clout + int(follower_change / 10)))

            # Brain template pool
            pool = {
                "Global Feed": {
                    "positive": [("@hype_beast", "🔥 Absolute massive win right here.", "💬"), ("@clout_chaser", "Agreed! Check your DM's let's link up.", "💎")],
                    "drama": [("@cancel_crew", "This is why nobody likes you. Cancelled.", "❌"), ("@ratio_king", "L take + ratio + touch grass.", "💀")],
                    "neutral": [("@lurker_john", "Hmm, interesting thought honestly.", "🤖"), ("@ad_bot", "Get cash fast! Link in bio!", "💸")]
                },
                "Hogwarts Network": {
                    "positive": [("@potter_j", "Brilliant! 20 points to Gryffindor!", "🦁"), ("@granger_h", "An incredibly accurate deduction.", "📚")],
                    "drama": [("@malfoy_d", "Wait until my father hears about this post.", "🐍"), ("@snape_p", "Insolent. Detention for this.", "🧪")],
                    "neutral": [("@weasley_r", "Bloody hell, that's wild.", "🧹"), ("@lovegood_l", "The Nargles influenced this post.", "✨")]
                }
            }
            
            universe_pool = pool.get(universe, pool["Global Feed"])
            comments = universe_pool.get(sentiment, universe_pool["neutral"])

            st.session_state.history.insert(0, {
                "text": user_post,
                "change": follower_change,
                "comments": comments,
                "timestamp": "Just now"
            })
            st.rerun()

# Main Interactive Feed Feed Timeline Display Loop
if not st.session_state.history:
    st.markdown("<div style='text-align:center; color:#71767b; padding:40px;'>Your profile feed is completely quiet. Drop your first post above!</div>", unsafe_allow_html=True)
else:
    for post in st.session_state.history:
        badge_html = f'<div class="stat-badge">📈 +{post["change"]} followers</div>' if post["change"] >= 0 else f'<div class="stat-badge-down">📉 {post["change"]} followers</div>'
        
        # Base structural layout wrapper
        st.markdown(f"""
        <div class="feed-card">
            <div class="user-header">
                <div class="avatar" style="background:#1d9bf0;">U</div>
                <div>
                    <span class="username">You</span> <span class="handle">@anonymous_user • {post['timestamp']}</span>
                </div>
            </div>
            <div class="post-text">{post['text']}</div>
            {badge_html}
            <div class="comment-section">
        """, unsafe_allow_html=True)
        
        # Secondary loop rendering responses seamlessly
        for handle, text, emo in post["comments"]:
            st.markdown(f"""
                <div class="comment-item">
                    <div class="npc-avatar">{emo}</div>
                    <div>
                        <span class="username" style="font-size:14px;">{handle}</span>
                        <div style="font-size:14px; color:#e7e9ea; margin-top:2px;">{text}</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
        st.markdown("</div></div>", unsafe_allow_html=True)
