import streamlit as st
from pdfextractor import text_extractor
from langchain_google_genai import ChatGoogleGenerativeAI
import os

# First lets configure the model
gemini_api_key = os.getenv('GOOGLE_API_KEY1')
model = ChatGoogleGenerativeAI(
    model='gemini-2.5-flash-lite',
    api_key = gemini_api_key,
    temperature = 0.9
)

# Lets create the side bar to upload the resume
st.sidebar.title(':red[UPLOAD YOUR RESUME (Only PDF)]')
file=st.sidebar.file_uploader('Resume',type=['pdf'])
if file:
    file_text = text_extractor(file)
    st.sidebar.success('File Uploaded Successfully')


# Create the main page of the application
st.title(':orange[SKILLMATCH:-] :blue[AI Assisted Skill Matching Tool]',width='content')
st.markdown('#### :green[This application will match and analyze your resume and the job description provided]',width='content')
tips = '''
Follow these steps:-
1. Upload your resume (PDF Only) in side bar. 
2. Copy and paste the job Description below.
3. Click on submit the run the application'''
st.write(tips)

job_desc = st.text_area(':red[Copy and paste your job description over here.]',max_chars=50000)

if st.button('SUBMIT'):
    prompt = f'''
    <Role> You are an expert in analyzing resume and matching it with job description.
    <Goal> Match the resume and the job description provided by the applicant and create a report.
    <Context> The following content has been provided by the applicant:
    * Resume : {file_text}
    * Job Description: {job_desc}
    <Format> The report should follow these steps:
    * Give a breif description of the applicant in 3 to 5 lines.
    * Describe in percentage what are the chances of this resume of getting selecetd.
    * Need not be the exact percentage, you can give interval of percentage.
    * Give the expected ATS score along with matching and non matching keywords.
    * Perform SWAT analysis and expalain each paramter ie strength, Weakness, Opportunity and Threat.
    * Give what all sections in the current resume that are required to be changed in order to imropve the ATS score and selection percentage.
    * Show both current version and improved version of the section in resume.
    * Create two sample resume which can maximize the ATS score and selection percentage.

    <Instruction>
    * Use bullet points for explanation where ver possible.
    * Create tables for description where ever required.
    * Strictly do not add any new skill in sample resume.
    * Avoid displaying any HTML anchors and characters.
    * The format of sample resumes should be in such a way that they can be copied and pasted directly in word.'''

    response = model.invoke(prompt)
    st.write(response.content)
