import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os 
import json

load_dotenv()

class GenerateQuestions : 
    def __init__(self, job_data,nb_questions , language_selected) : 

        OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        client = OpenAI(api_key= OPENAI_API_KEY)

        self.job_data = job_data
        self.nb_questions = nb_questions
        self.language_selected = language_selected
        self.client = client
    
    def generate_questions(self, is_resume=False):

        if not is_resume:

            response = self.client.chat.completions.create(
                model="gpt-4o-mini", 
                        messages=[
            {
                "role": "system",
                "content": "You are a specialist in job interviews."
            },
            {
                "role": "user",
                "content": f"""
                    Generate {self.nb_questions} interview questions in {self.language_selected} that could be asked by a recruiter and answered orally.

                    Rules:
                        - Must be answerable verbally (no coding tasks)
                        - Can be personal, philosophical, or technical
                        - Order from easiest to hardest
                        - Each takes 1–2 minutes to answer

                    Job Description:
                    {self.job_data}
                    """
            }
            ],
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": "interview_questions",
                    "schema": {
                        "type": "object",
                        "properties": {
                            "questions": {
                            "type": "array",
                            "items": {"type": "string"},
                            "minItems": self.nb_questions,
                            "maxItems": self.nb_questions
                        }
                    },
                    "required": ["questions"],
                    "additionalProperties": False
                }
            }
        },
        temperature=0.5,
        )
    
        if is_resume : # When I will update Resume Upload, this will influence the questions. 
            return(None)

    # JSON already guaranteed, just parse
        return json.loads(response.choices[0].message.content)

        
