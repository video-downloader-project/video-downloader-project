
import os
import streamlit as st
import yt_dlp

def download_video(url, download_path="downloads"):
    if not os.path.exists(download_path):
        os.makedirs(download_path)
        
    ydl_opts = {
        # 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4' নিশ্চিত করে এটি সাধারণ H.264 mp4 ফরম্যাটে ডাউনলোড হবে, যা সব প্লেয়ারে সাপোর্ট করে
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4',
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

# Streamlit UI
st.title("📥 ওয়াটারমার্ক-ফ্রি হাই-কোয়ালিটি ভিডিও ডাউনলোডার")
video_url = st.text_input("ভিডিওর লিঙ্কটি এখানে পেস্ট করুন:")

if st.button("ভিডিও প্রসেস করুন"):
    if video_url.strip() == "":
        st.warning("দয়া করে একটি লিঙ্ক দিন।")
    else:
        with st.spinner("প্রসেস হচ্ছে..."):
            result = download_video(video_url)
            if "Error" in result:
                st.error(result)
            else:
                st.success("সম্পন্ন হয়েছে!")
                with open(result, "rb") as file:
                    st.download_button(
                        label="🎬 ভিডিও ডাউনলোড করুন", 
                        data=file.read(), 
                        file_name=os.path.basename(result), 
                        mime="video/mp4"
                    )
