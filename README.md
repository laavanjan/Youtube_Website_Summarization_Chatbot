
# Youtube_Website_Summarization_Chatbot 🤖

This Streamlit application leverages the power of LangChain and llama3-70b-8192 LLMs to provide concise summaries of content from both YouTube videos and website URLs.  It offers a user-friendly interface for quickly grasping the key information from articles or video transcripts, saving you valuable time.

## Table of Contents

- [Features](#features)
- [Usage](#usage)
- [Screenshots](#screenshots)
- [Environment Variables](#environment-variables)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Features ✨

- **Summarization:** Condenses lengthy YouTube videos and website articles into easily digestible summaries.
- **Multiple YouTube Content Handling:**  Gracefully handles cases where transcripts are unavailable by extracting video descriptions as a fallback.  Uses `pytube`, `youtube_transcript_api`, and `yt-dlp` to maximize content retrieval.
- **User-Friendly Interface:** Built with Streamlit for a simple and intuitive user experience.
- **Powered by LangChain and Groq:** Utilizes LangChain for chain management and Groq's LLMs for high-quality summarization.
- **LangSmith Integration:**  Includes LangSmith tracing for debugging and monitoring.
- **Clear Error Handling:** Provides informative error messages to guide users.
- **Stylish Footer:**  Includes a custom footer with gradient and animation.


## Usage 🚀

1.  **Set up environment variables:** Create a `.env` file in the project directory and add  your API key and LangSmith details (see [Environment Variables](#environment-variables) section below).

2.  **Run the Streamlit app:**

    ```bash
    streamlit run app.py
    ```

3.  **Open the app in your browser:** Streamlit will provide a URL (usually `http://localhost:8501`).

4.  **Enter a YouTube video URL or a website URL in the input field.**

5.  **Click the "Summarize the Content from YT or Website" button.**

6.  **The summarized content will be displayed below.**

## Screenshots 📸

*(Include screenshots here demonstrating the app's interface and functionality.  Examples:)*

*Screenshot 1: Main interface with URL input.*
![Screenshot 1](about:sanitized)  *(Replace with actual screenshot)*

*Screenshot 2: Example YouTube video summarization.*
![Screenshot 2](about:sanitized)  *(Replace with actual screenshot)*

*Screenshot 3: Example website summarization.*
![Screenshot 3](about:sanitized)  *(Replace with actual screenshot)*

## Environment Variables 🔑

Create a `.env` file in the project directory and add the following environment variables:

```
API_KEY="YOUR_API_KEY"
LANGCHAIN_API_KEY="YOUR_LANGCHAIN_API_KEY"  # For LangSmith tracing
LANGCHAIN_TRACING_V2="true" # For LangSmith tracing
LANGCHAIN_PROJECT="YOUR_LANGCHAIN_PROJECT" # For LangSmith tracing
```

Replace `"YOUR_GROQ_API_KEY"`, `"YOUR_LANGCHAIN_API_KEY"`, and `"YOUR_LANGCHAIN_PROJECT"` with your actual API keys and project name.  **Do not commit this file to your repository.**

## Troubleshooting 🐛

  - **API Key Issues:** Ensure your  API key is correctly set in the `.env` file.
  - **YouTube Loading Errors:** The app attempts multiple methods for YouTube content. If one fails, it tries others.  Check the error messages for details.
  - **Dependency Issues:** Double-check that all required packages are installed using `pip install -r requirements.txt`.
  - **Streamlit Issues:** Refer to the Streamlit documentation for troubleshooting Streamlit-specific problems.

## Contributing 🤝

Contributions are welcome\! Feel free to submit pull requests or open issues.

## License 📄

This project is licensed under the GPL-3.0 License - see the [LICENSE](LICENSE) file for details.

## Contact 📧

Laavanjan - [Your Email Address]

-----

If you found this project helpful, please consider leaving a like\! 👍


