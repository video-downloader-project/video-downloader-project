import os
import streamlit as st
import yt_dlp

# প্রফেশনাল পেজ সেটআপ
st.set_page_config(
    page_title="HQ Video Downloader - No Watermark",
    page_icon="📥",
    layout="centered"
)

# সিএসএস (CSS) দিয়ে ইন্টারফেস প্রফেশনাল ও আকর্ষণীয় করা
st.markdown("""
    <style>
    .main { background-color: #0f111a; }
    h1 { color: #ff4b4b; text-align: center; font-family: 'Helvetica Neue', sans-serif; font-weight: bold; }
    .stButton>button { background-color: #ff4b4b; color: white; width: 100%; border-radius: 8px; font-weight: bold; height: 45px; }
    .stButton>button:hover { background-color: #ff3333; color: white; }
    </style>
""", unsafe_allow_html=True)

# ভিডিওর মেটাডেটা এবং উপলব্ধ কোয়ালিটি অপশন বের করার ফাংশন
def get_video_info(url):
    ydl_opts = {'quiet': True, 'no_warnings': True}
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            formats = info.get('formats', [])
            
            # ডুপ্লিকেট ছাড়া সাধারণ কোয়ালিটি অপশন ফিল্টার করা
            available_qualities = set()
            for f in formats:
                height = f.get('height')
                if height:
                    available_qualities.add(f"{height}p")
            
            # কোয়ালিটি বড় থেকে ছোট ক্রমে সাজানো (যেমন: 1080p, 720p...)
            quality_list = sorted(list(available_qualities), key=lambda x: int(x.replace('p', '')), reverse=True)
            if not quality_list:
                quality_list = ["Best Quality"]
                
            return info.get('title', 'Video'), quality_list
    except Exception as e:
        return None, [f"Error: {str(e)}"]

# vidéo ডাউনলোড করার ফাংশন
def download_video(url, selected_quality, download_path="downloads"):
    if not os.path.exists(download_path):
        os.makedirs(download_path)
        
    # ব্যবহারকারীর সিলেক্ট করা কোয়ালিটি অনুযায়ী ফরম্যাট সেট করা
    if selected_quality == "Best Quality":
        format_opt = 'bestvideo+bestaudio/best'
    else:
        q_num = selected_quality.replace('p', '')
        format_opt = f'bestvideo[height<={q_num}][ext=mp4]+bestaudio[ext=m4a]/best[height<={q_num}]'
        
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

# --- ওয়েবসাইটের মূল ইন্টারফেস ---
st.title("📥 ওয়াটারমার্ক-ফ্রি প্রফেশনাল ভিডিও ডাউনলোডার")
st.write("<p style='text-align: center; color: #aaa;'>যেকোনো প্ল্যাটফর্মের লিঙ্ক পেস্ট করে আপনার পছন্দের কোয়ালিটিতে ভিডিও ডাউনলোড করুন।</p>", unsafe_allow_html=True)

# বিজ্ঞাপনের জন্য ওপরের ডেডিকেটেড স্পেস (Top Banner Ad)
st.markdown("<div style='text-align:center; padding:15px; background:#1e2235; border-radius:8px; color:#999; border: 1px dashed #444; font-weight:bold;'>Top Advertisement Banner Slot</div>", unsafe_allow_html=True)
st.write("")

# লিঙ্ক ইনপুট বক্স
video_url = st.text_input("ভিডিওর লিঙ্কটি এখানে পেস্ট করুন:", placeholder="https://...")

if video_url:
    # সেশন স্টেটে তথ্য সেভ রাখা যাতে বারবার লোড না হয়
    if 'last_url' not in st.session_state or st.session_state.last_url != video_url:
        with st.spinner("ভিডিওর কোয়ালিটি অপশনগুলো চেক করা হচ্ছে..."):
            title, qualities = get_video_info(video_url)
            st.session_state.video_title = title
            st.session_state.qualities = qualities
            st.session_state.last_url = video_url

    if st.session_state.video_title:
        st.info(f"🎬 **ভিডিও শিরোনাম:** {st.session_state.video_title}")
        
        # কোয়ালিটি কমানো/বাড়ানোর ড্রপডাউন বক্স (Quality Selector)
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

# বিজ্ঞাপনের জন্য নিচের ডেডিকেটেড স্পেস (Footer Ad)
st.write("")
st.markdown("<div style='text-align:center; padding:15px; background:#1e2235; border-radius:8px; color:#999; border: 1px dashed #444; font-weight:bold;'>Bottom Advertisement Banner Slot</div>", unsafe_allow_html=True)
