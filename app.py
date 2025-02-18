import validators
import streamlit as st
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain.chains.summarize import load_summarize_chain
from langchain_community.document_loaders import UnstructuredURLLoader
from langchain_community.document_loaders import YoutubeLoader
from langchain.schema import Document  # Import Document class
import yt_dlp  # Alternative for YouTube video extraction
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled  # Extract actual video transcript
import os
from dotenv import load_dotenv
## Langsmith Tracking
os.environ["LANGCHAIN_API_KEY"]=os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"]="true"
os.environ["LANGCHAIN_PROJECT"]=os.getenv("LANGCHAIN_PROJECT")

# Load environment variables from .env file
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")  # Fetch the Groq API Key from .env file

# Streamlit app configuration
st.set_page_config(page_title="LangChain: Summarize Text From YT or Website", page_icon="🦜")
st.title("🦜 LangChain: Summarize an Aritcle From YT or Website")
st.subheader("Summarize URL")

# Input for the URL (No need for API key input now, as it's set in the code)
generic_url = st.text_input("URL", label_visibility="collapsed")

# Extract video ID from YouTube URL
def extract_video_id(url):
    """Extracts the YouTube video ID from a given URL"""
    from urllib.parse import urlparse, parse_qs

    parsed_url = urlparse(url)
    if parsed_url.netloc in ["www.youtube.com", "youtube.com"]:
        return parse_qs(parsed_url.query).get("v", [None])[0]
    elif parsed_url.netloc in ["youtu.be"]:
        return parsed_url.path.lstrip("/")
    return None

# Ensure valid input before initializing LLM
if st.button("Summarize the Content from YT or Website"):
    if not api_key or not generic_url.strip():
        st.error("Please provide the required information to get started.")
    elif not validators.url(generic_url):
        st.error("Please enter a valid URL. It can be a YouTube video or a website URL.")
    else:
        try:
            with st.spinner("Waiting..."):
                docs = None

                # Load content from YouTube or website
                if "youtube.com" in generic_url or "youtu.be" in generic_url:
                    video_id = extract_video_id(generic_url)

                    try:
                        # ✅ First attempt: Use LangChain YoutubeLoader (pytube)
                        loader = YoutubeLoader.from_youtube_url(generic_url, add_video_info=True)
                        docs = loader.load()

                    except Exception as yt_error:
                        #st.warning("⚠️ Failed to load YouTube video using pytube. Switching to alternative method...")

                        try:
                            # ✅ Second attempt: Use youtube_transcript_api for actual transcript
                            transcript = YouTubeTranscriptApi.get_transcript(video_id)
                            transcript_text = " ".join([entry["text"] for entry in transcript])

                            docs = [Document(page_content=transcript_text)]

                        except TranscriptsDisabled:
                            st.warning("⚠️ No transcript available. Extracting description instead...")
                            
                            try:
                                # ✅ Third attempt: Use yt-dlp to extract video metadata
                                ydl_opts = {'quiet': True, 'noplaylist': True, 'skip_download': True}
                                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                                    info_dict = ydl.extract_info(generic_url, download=False)
                                    video_description = info_dict.get("description", "No description available.")
                                    
                                    docs = [Document(page_content=video_description)]

                            except Exception as ytdlp_error:
                                st.error(f"❌ Failed to extract video content using yt-dlp: {ytdlp_error}")
                                st.stop()
                else:
                    # If it's a website, use UnstructuredURLLoader
                    loader = UnstructuredURLLoader(
                        urls=[generic_url],
                        ssl_verify=True,
                        headers={
                            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
                        },
                    )
                    docs = loader.load()

                # Initialize LLM only if API key is valid
                llm = ChatGroq(model="llama3-70b-8192", groq_api_key=api_key)

                # Define summarization prompt
                prompt_template = """
                Provide a summary of the following content in 300 words
                Don't mention the no of words in your response
                Content: {text}
                """
                prompt = PromptTemplate(template=prompt_template, input_variables=["text"])

                # Chain for summarization
                chain = load_summarize_chain(llm, chain_type="stuff", prompt=prompt)
                output_summary = chain.run(docs)

                st.success(output_summary)
        except Exception as e:
            st.error(f"Exception: {e}")

# Custom footer styling
footer_html = """
    <style>
    body {
        margin: 0;
        padding: 0;
        min-height: 100%;
        display: flex;
        flex-direction: column;
    }

    .footer {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background: linear-gradient(135deg, #6a82fb, #fc5c7d);  /* Smooth purple-pink gradient */
        color: white;
        text-align: center;
        padding: 8px 16px;  /* Reduced padding to decrease height */
        font-size: 14px;  /* Reduced font size */
        font-family: 'Arial', sans-serif;
        border-top: 2px solid #ffffff33;
        box-shadow: 0 -2px 5px rgba(0, 0, 0, 0.3);
        animation: fadeIn 3s ease-out;
    }

    .footer b {
        color: #e0fffc;  /* Soft cyan color */
        font-size: 16px;  /* Reduced font size */
        transition: color 0.3s ease;
    }

    .footer b:hover {
        color: #ffdd00;  /* Bright yellow hover effect */
    }

    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    </style>

    <div class="footer">
        Developed by <b>Laavanjan</b> | © Faculty of IT B22
    </div>
"""

# Render the footer in the Streamlit app
st.markdown(footer_html, unsafe_allow_html=True)

