import streamlit as st
from utils.generate_questions import GenerateQuestions
from utils.generate_report import GenerateReport
from utils.markdown_to_pdf import MarkdownPDF
import json
import time

tab1, tab2, tab3,  tab4= st.tabs(["Job Form", "ITW", "Report","Feedback"])

# Logo
sidebar_logo = "logo/logo_text_v2_no_background.png"   # big version
icon_logo = "logo/logo_no_background.png"                  # small square icon

st.logo(
    sidebar_logo,
    icon_image=icon_logo, 
    size = "large",
)


st.markdown("""
<style>
[data-testid="stSidebar"] img {
    width: 110% !important;
    height: auto !important;
    margin-bottom: 10px;
}
[data-testid="stSidebar"] {
    padding-top: 50px;
}
</style>
""", unsafe_allow_html=True)
        



#### 1 : information form ####

if "job_data" not in st.session_state:
        st.session_state.job_data = {}

with tab1 :
    
    st.title("Job Information Form 📝")
    with st.form("job_form"):

        # Small input boxes
        company = st.text_input("🏢 Company Name")
        role = st.text_input("💼 Role / Position")

        contract_type = st.selectbox(
            "📄 Type of Contract",
            ["Permanent", "Fixed-term", "Internship", "Freelance", "Other"]
        )

        # Large text area
        job_description = st.text_area(
            "📝 Job Description",
            height=200,  
            placeholder="Paste or write the job description here..."
        )

        # Submit button INSIDE the form
        submitted = st.form_submit_button("Submit")

    # What happens after submission
    if submitted:
        st.success("Form submitted successfully!", icon="✅")
        st.session_state.job_data = {
            "company": company,
            "role": role,
            "contract_type": contract_type,
            "job_description": job_description,
        }
        

#### 2 : Generate Interview ####

with tab2 :

    st.title("Generate Interview 🎙️")

    if "answers" not in st.session_state:
        st.session_state.answers = {}

    if "json_questions" not in st.session_state:
        st.session_state.questions = {}

    if "questions_generated" not in st.session_state:
        st.session_state.questions_generated = False
    
    if "language selected" not in st.session_state:
        st.session_state.language_selected = False

    if "nb_questions" not in st.session_state:
        st.session_state.nb_questions = 0
    
    nb_questions = st.select_slider( "How many questions would you like to train on?", options=[str(i) for i in range(1, 11)], )

    left, middle, right = st.columns(3)
    
    st.session_state.language_selected = middle.selectbox(
        "Language Selection.",
        ["English", "French", "Spanish"],
        key="selection_language_itw",
    )

    left.write("")
    left.write("")

    if left.button("Generate questions") and st.session_state.language_selected :
        st.session_state.nb_questions = int(nb_questions)
        st.session_state.answers = {}  # reset old answers

        GenQues = GenerateQuestions(st.session_state.job_data, st.session_state.nb_questions, st.session_state.language_selected)
        st.session_state.json_questions = GenQues.generate_questions()
        st.session_state.questions_generated = True
    
    else : 
        st.warning("Choose a language first.")

    if st.session_state.questions_generated and st.session_state.language_selected :

        st.success(f"{st.session_state.nb_questions} questions generated!")

        for i in range(st.session_state.nb_questions):
            container = st.container(border=True)

            with container:
                left_question, middle_question, right_question = st.columns(3)

                left_question.write(f"**Q{i+1}: {st.session_state.json_questions['questions'][i]}**")

                audio = middle_question.audio_input("Your Answer:", key=f"audio_{i}")

                right_question.write("")
                right_question.write("")

                if right_question.button("Save your audio ✅", key=f"save_{i}"):

                    if audio is not None:
                        st.session_state.answers[f"**Q{i+1}: {st.session_state.json_questions['questions'][i]}**"] = audio
                        st.success(f"Answer for Question {i+1} saved!")
                    else:
                        st.warning("Please record audio first.")
                right.write("")
    

#### 3 : Report ####

with tab3 : 

    if "report" not in st.session_state:
        st.session_state.report = {}

    st.title("Report 🧗‍♂️")

    if  st.session_state.answers == {} : 
        st.warning("Go to the ITW section first and record your answers! 🎙️")
    else : 

        left, middle, right = st.columns(3)
        st.session_state.language_selected_report = middle.selectbox(
        "Language Selection.",
        ["English", "French", "Spanish"],
        key="selection_language_report",
    )

        left.write("")
        left.write("")
        if left.button("Generate Report.") and st.session_state.language_selected_report :
            GenReport = GenerateReport(st.session_state.answers, st.session_state.nb_questions, st.session_state.language_selected_report, st.session_state.job_data)
            st.session_state.report = json.loads(GenReport.generate_report())

        else : 
            st.warning("Choose a language first.")

        if st.session_state.report  != {} : 
            container = st.container(border=True)
            with container : 
                st.title(st.session_state.report["report_title"])
                st_mkdn = """" """
                for nb, q in enumerate(st.session_state.report["questions"]):
                    st.markdown(f"#### Q{nb+1}: *{q['question']}*")                 
                    st.markdown(f"**Candidate answer:** :orange[{q['candidate_answer']}]")
                    st.markdown(f"*Coach feedback:* {q['feedback']}")   # italic
                    
                st.markdown("---")
                st.subheader("Global Feedback")
                st.write(f"{st.session_state.report['global_feedback']}")
                
            MkdnPDF = MarkdownPDF(st.session_state.report)
            pdf_buffer = MkdnPDF.build_pdf()
            # 📄 Download button
            st.download_button(
                label="Download Report as PDF",
                data=pdf_buffer,
                file_name="interview_report.pdf",
                mime="application/pdf",
                icon=":material/download:",
                )
            if st.download_button : 
                st.success("Report downloaded!", icon="🎉")
        
        
                    

#### 4 : Feedback ####

with tab4 : 
    st.title("Feedback 👍👎")

    with st.form("feedback_form"):

        # Feedback choice
        sentiment_selection = st.feedback(options = "stars", width = "stretch")
        sentiment_mapping = ["one", "two", "three", "four", "five"]

        if sentiment_selection is not None:
            st.markdown(f"You selected {sentiment_mapping[sentiment_selection]} star(s).")

        # Reason box
        reason = st.text_area(
            "Could you tell us briefly why? ☺️",
            height=120,
            placeholder="Your feedback helps us improve..."
        )

        # Submit button
        submitted = st.form_submit_button("Submit")

    # After form submission
    if submitted:
        feedback = {
            "sentiment": sentiment_selection,
            "reason": reason
        }
        st.session_state.feedback = feedback
        st.success("Thank you very much for your feedback! 💛")

        

#### 4 : Login + Resume upload ####

with st.sidebar:
    uploaded_file = st.file_uploader('Upload your resume in .pdf', type="pdf", label_visibility="hidden")
    if uploaded_file is not None:
        st.success('Resume uploaded successfully!', icon="✅")

