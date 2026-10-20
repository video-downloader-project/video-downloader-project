import os
import streamlit as st
import yt_dlp

# প্রফেশনাল পেজ সেটআপ
st.set_page_config(
    page_title="HQ Video Downloader - No Watermark",
    page_icon="📥",
    layout="centered"
)

# সিএসএস (CSS) দিয়ে ইন্টারফেস প্রফেশনাল ও কাস্টম বাটন ডিজাইন
st.markdown("""
    <style>
    .main { background-color: #0f111a; }
    h1 { color: #ff4b4b; text-align: center; font-family: 'Helvetica Neue', sans-serif; font-weight: bold; }
    .stButton>button { background-color: #ff4b4b; color: white; width: 100%; border-radius: 8px; font-weight: bold; height: 45px; }
    .stButton>button:hover { background-color: #ff3333; color: white; }
    /* রিসেট বাটনের কাস্টম কালার */
    div.stButton > button:first-child[aria-label="❌ লিঙ্ক ক্লিয়ার করুন"] {
        background-color: #333;
        color: #fff;
        height: 38px;
        margin-top: 5px;
    }
    div.stButton > button:first-child[aria-label="❌ লিঙ্ক ক্লিয়ার করুন"]:hover {
        background-color: #555;
    }
    </style>
""", unsafe_allow_html=True)

# ভিডিওর মেটাডেটা এবং উপলব্ধ কোয়ালিটি অপশন বের করার ফাংশন
def get_video_info(url):
    ydl_opts = {'quiet': True, 'no_warnings': True}
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            formats = info.get('formats', [])
            
            available_qualities = set()
            for f in formats:
                height = f.get('height')
                if height:
                    # ৪K ভিডিওর জন্য ২১৬০p বা তার বেশি উচ্চতা চেক করা
                    if height >= 2160:
                        available_qualities.add("2160p (4K Ultra HD)")
                    elif height >= 1440:
                        available_qualities.add("1440p (2K HD)")
                    elif height >= 1080:
                        available_qualities.add("1080p (Full HD)")
                    else:
                        available_qualities.add(f"{height}p")
            
            # কোয়ালিটি বড় থেকে ছোট ক্রমে সাজানো
            def sort_key(x):
                if "4K" in x: return 2160
                if "2K" in x: return 1440
                if "Full HD" in x: return 1080
                return int(x.replace('p', ''))

            quality_list = sorted(list(available_qualities), key=sort_key, reverse=True)
            if not quality_list:
                quality_list = ["Best Quality"]
                
            return info.get('title', 'Video'), quality_list
    except Exception as e:
        return None, [f"Error: {str(e)}"]

# ভিডিও ডাউনলোড করার ফিক্সড ফাংশন (H.264 mp4 নিশ্চিত করা)
def download_video(url, selected_quality, download_path="downloads"):
    if not os.path.exists(download_path):
        os.makedirs(download_path)
        
    if "Best Quality" in selected_quality or "4K" in selected_quality or "2K" in selected_quality:
        format_opt = 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best'
    else:
        q_num = selected_quality.split('p')[0]
        format_opt = f'bestvideo[height<={q_num}][ext=mp4]+bestaudio[ext=m4a]/best[height<={q_num}][ext=mp4]'
        
    ydl_opts = {
        'format': format_opt,
        'outtmpl': f'{download_path}/%(title)s.%(ext)s',
        'merge_output_format': 'mp4',
        'quiet': True,
        'no_warnings': True,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info_dict)
            base, _ = os.path.splitext(file_path)
            final_path = f"{base}.mp4"
            if os.path.exists(final_path):
                return final_path
            return file_path
    except Exception as e:
        return f"Error: {str(e)}"

# --- রিসেট লজিক সেকশন ---
if "input_url" not in st.session_state:
    st.session_state.input_url = ""

def clear_text():
    st.session_state.input_url = ""
    if 'last_url' in st.session_state: del st.session_state.last_url
    if 'video_title' in st.session_state: del st.session_state.video_title

# --- ওয়েবসাইটের মূল ইন্টারফেস ---
st.title("📥 ওয়াটারমার্ক-ফ্রি প্রফেশনাল ভিডিও ডাউনলোডার")
st.write("<p style='text-align: center; color: #aaa;'>যেকোনো প্ল্যাটফর্মের লিঙ্ক পেস্ট করে আপনার পছন্দের কোয়ালিটিতে ভিডিও ডাউনলোড করুন।</p>", unsafe_allow_html=True)

# বিজ্ঞাপনের স্লট
st.markdown("<div style='text-align:center; padding:15px; background:#1e2235; border-radius:8px; color:#999; border: 1px dashed #444; font-weight:bold;'>Top Advertisement Banner Slot</div>", unsafe_allow_html=True)
st.write("")

# লিঙ্ক ইনপুট বক্স (সেশন স্টেটের সাথে যুক্ত)
video_url = st.text_input("ভিডিওর লিঙ্কটি এখানে পেস্ট করুন:", value=st.session_state.input_url, key="url_box", placeholder="https://...")
st.session_state.input_url = video_url

# পরবর্তী লিঙ্কের জন্য ইনপুট বক্সটি এক ক্লিকে ক্লিয়ার করার বাটন
if video_url != "":
    st.button("❌ লিঙ্ক ক্লিয়ার করুন", on_click=clear_text)

if video_url:
    if 'last_url' not in st.session_state or st.session_state.last_url != video_url:
        with st.spinner("ভিডিওর কোয়ালিটি অপশনগুলো চেক করা হচ্ছে..."):
            title, qualities = get_video_info(video_url)
            st.session_state.video_title = title
            st.session_state.qualities = qualities
            st.session_state.last_url = video_url

    if st.session_state.video_title:
        st.info(f"🎬 **ভিডিও শিরোনাম:** {st.session_state.video_title}")
        chosen_q = st.selectbox("আপনার পছন্দের ভিডিও কোয়ালিটি সিলেক্ট করুন:", st.session_state.qualities)
        
        if st.button("ডাউনলোড ফাইল রেডি করুন"):
            with st.spinner("আপনার সিলেক্ট করা কোয়ালিটিতে ভিডিও প্রসেস হচ্ছে..."):
                result = download_video(video_url, chosen_q)
                if "Error" in result:
                    st.error("ডাউনলোড ব্যর্থ হয়েছে। লিঙ্কটি আবার চেক করুন।")
                else:
                    st.success("ফাইল সম্পূর্ণ রেডি!")
                    with open(result, "rb") as file:
                        st.download_button(
                            label="📥 ডিভাইসে সেভ করতে এখানে ক্লিক করুন",
                            data=file.read(),
                            file_name=os.path.basename(result),
                            mime="video/mp4"
                        )
    else:
        st.error("লিঙ্কটি থেকে কোনো ভিডিওর তথ্য পাওয়া যায়নি।")

st.write("")
st.markdown("<div style='text-align:center; padding:15px; background:#1e2235; border-radius:8px; color:#999; border: 1px dashed #444; font-weight:bold;'>Bottom Advertisement Banner Slot</div>", unsafe_allow_html=True)
