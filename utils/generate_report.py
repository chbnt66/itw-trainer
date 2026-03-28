import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os 
import json

load_dotenv()

class GenerateReport : 

    def __init__(self, answers, nb_questions,  selected_language_report, job_data) :

        OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        client = OpenAI(api_key= OPENAI_API_KEY) 

        self.answers = answers
        self.nb_questions = nb_questions
        self.selected_language_report = selected_language_report
        self.job_data = job_data
        self.client = client

    def convert_audio(self) : 

        # convert audio 
        # return a text_dictionary
        dict_audio_to_text = {}
        for question_i in self.answers.keys() : 
            transcription = self.client.audio.transcriptions.create(model= "gpt-4o-mini-transcribe", file = self.answers[question_i])
            dict_audio_to_text[question_i] = transcription.text

        return(dict_audio_to_text)

        
    def generate_report(self) : # Do i had a section if i have the resume to give even more context ? 

        # 1. Convert audio to text

        dict_audio_to_text = self.convert_audio()

        # 2. Generate report

        report = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
            {
            "role": "system",
            "content": "You are a demanding interview coach. Your goal is improvement, not comfort."
        },
        {
            "role": "user",
            "content": f"""
A candidate answered {self.nb_questions} interview questions orally.

Language of the report: {self.selected_language_report}

You will receive:
- Questions
- Candidate answers (transcribed from audio)
- Job description

For EACH question:
• Include the original question
• Include the candidate answer
• Provide demanding, constructive feedback
• Focus on clarity, structure, impact, and relevance
• Remember answers are oral (1–2 minutes)

At the end provide a global evaluation and concrete improvement plan.

Candidate answers:
{dict_audio_to_text}

Job description:
{self.job_data}
"""
        }
    ],
    response_format={
        "type": "json_schema",
        "json_schema": {
            "name": "interview_report",
            "schema": {
                "type": "object",
                "properties": {
                    "report_title": {"type": "string"},
                    "date": {"type": "string"},
                    "language": {"type": "string"},
                    "questions": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "question": {"type": "string"},
                                "candidate_answer": {"type": "string"},
                                "feedback": {"type": "string"}
                            },
                            "required": ["question", "candidate_answer", "feedback"]
                        }
                    },
                    "global_feedback": {"type": "string"}
                },
                "required": ["report_title", "questions", "global_feedback"]
            }
        }
    },
    temperature=0.2
)

        return report.choices[0].message.content