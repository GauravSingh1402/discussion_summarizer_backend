
<h1 align="center" id="title">SummaSense-Multimedia Summarization using AI</h1>

<p align="center">
    <a href="https://summa-sense.vercel.app/">View Live Project</a>
  </p>

<p align="center"><img src="https://socialify.git.ci/GauravSingh1402/discussion_summarizer_backend/image?description=1&descriptionEditable=Advanced%20AI%20Summarization%20for%20Multilingual%20Text%2C%20Audio%2C%20and%20Video.&font=Raleway&language=1&logo=https%3A%2F%2Fraw.githubusercontent.com%2FGauravSingh1402%2Fdiscussion_summarizer%2Fmain%2Fpublic%2Fassets%2Flogo-black.svg&name=1&owner=1&pattern=Charlie%20Brown&theme=Light" width="640" height="320" alt="project-image"/></p>

<p id="description">
SummaSense is a multimedia summarization tool that leverages AI to generate English language summaries for various types of input content. It is built using Next.js and Tailwind CSS for the frontend and Flask for the backend. With support for text, audio, and video inputs, SummaSense provides flexibility and accuracy in summarization.</p>

> The frontend repository of the project is [here](https://github.com/GauravSingh1402/discussion_summarizer)

<h2>📃 Table of Contents</h2>

* [Features](#features)
* [Installation Steps](#installation-steps)
* [Built With](#built-with)
* [Usage](#usage)
* [Authors Contribution](#authors)
* [Ending-note](#ending-note)

<h2 id="features">💡 Features</h2>

Here're some of the project's best features:

-   Step-by-step Process:
    
    -   The homepage guides users through the summarization process, providing clear instructions and a "Generate Summary" button.
-   Input Types:
    
    -   Text: Users can input text directly in the textbox or upload a document, which is processed with Optical Character Recognition (OCR) to identify the input text.
    -   Audio: Users can record audio in real-time with transcription or upload an audio file for summarization.
    -   Video: Users can upload a video file, and SummaSense generates a summary based on its content.
-   Multilingual Support:
    
    -   SummaSense supports multilingual input and can process a variety of languages using the Google Translate API.
-   Content Editing:
    
    -   Users can edit the input content before proceeding with summarization, allowing them to refine and improve accuracy.
-   State-of-the-Art AI Models:
    
    -   SummaSense utilizes pretrained abstractive and extractive summarization models, such as Bart, LSA, and KL-Sum, to generate multiple summary options.
    -   Specialized model Conversation Bart is used to handle conversational input, detecting the type of input (descriptive or conversational) and selecting the appropriate model accordingly.
-   Succinct Title Generation:
    
    -   SummaSense generates a concise title for the content using the T5 model.
-   User Accounts and Profile:
    
    -   Users can create an account to save their summaries and titles in their profile for future use.


<h2 id="installation-steps">⚙️ Installation</h2>
To run SummaSense locally, follow these steps:

1.  Clone the backend repository:
```
git clone https://github.com/GauravSingh1402/discussion_summarizer_backend.git
```
2. For setting the frontend of the project, follow the instructions in the [discussion_summarizer](https://www.github.com/GauravSingh1402/discussion_summarizer) repository
3. Navigate to the project directory:
```
cd discussion_summarizer_backend
```
4. Set up a virtual environment (optional but recommended):
```
virtualenv venv
source venv/bin/activate
```
5. Install the dependencies:
```
pip install -r requirements.txt
```
6.Export Flask environment variables:

* For Linux/Mac:
    
```
export FLASK_APP=app.py
export FLASK_ENV=development
```
  
* For Windows:
    
```
set FLASK_APP=app.py
set FLASK_ENV=development
```
    
7. Start the backend server:
```
flask run
```

<h2 id="built-with">💻 Built With</h2>

-   Frontend: Next.js, Tailwind CSS
-   Backend: Flask
-   AI Models: Bart, LSA, KL-Sum, Conversation Bart, T5
-   OCR: Optical Character Recognition
-   API: Google Translate

<h2 id="usage">🖱️ Usage</h2>

1.  Visit the SummaSense homepage and follow the step-by-step instructions.
2.  Choose the desired input type: text, audio, or video.
3.  Enter or upload the content for summarization.
4.  Edit the input content, if needed, to enhance accuracy.
5.  Submit the summary request, and SummaSense processes the input on the backend using state-of-the-art AI models.
6.  Explore the generated summaries and select the most suitable option.
7.  Optionally, create an account to save and access summaries and titles in your profile.


<h2 id="authors">🧑‍💻Authors</h2>

This project was developed by [Gaurav Singh](https://github.com/GauravSingh1402), [Advait Nurani](https://github.com/ADIVADER19) and [Hridayesh Padalkar](https://github.com/Hridayesh12). 

Contributions:

- Gaurav Singh: Conducted UX research, designed the complete user interface in Figma, and developed the visually stunning frontend of the application with light and dark modes. Performed research on available models, trained, and compared abstractive summarization models.

- Advait Nurani: Performed training and comparison of initial extractive summarization models. Collaborated with Hridayesh in developing backend functions and setting up the API.

- Hridayesh Padalkar: Implemented backend setup, API configuration, and data transmission between the frontend and backend. Collaborated with Advait in developing backend functions.



<h2 id="ending-note">🔚 Ending Note</h2>

While the tool offers advanced summarization capabilities, it is necessary to acknowledge that the recent advancements in generative AI influences a further scope for improvement. The tool may require further enhancements and fine-tuning for specific use cases and improved performance.
