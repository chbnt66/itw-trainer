# 🎙️ ITW Trainer

A Streamlit web app to help you prepare for job interviews in foreign languages.

![ITW Trainer Screenshot](logo/screenshot_itw.png)

---

## What it does

ITW Trainer guides you through a realistic interview preparation flow:

1. **Job Form**: Fill in your application details: company name, position, contract type, and job description.
2. **ITW**: Generate 1 to 10 interview questions tailored to your application. Choose your target language (English, French, or Spanish) and record an audio answer for each question.
3. **Report**: Generate a detailed feedback report in the selected language. Each answer is analyzed individually, and a global assessment is provided. The report can be downloaded as a **PDF**.

---

## Project structure

```
Itw_trainer_basic/
├── app.py            # Main Streamlit app entry point
├── utils/            # All helper functions (question generation, audio, report, etc.)
├── logo/             # App images and assets
└── requirements.txt
```

---

## Getting started

**1. Clone the repo and navigate to the project folder**
```bash
git clone https://github.com/your-username/itw-trainer.git
cd itw-trainer
```

**2. Create and activate a virtual environment**
```bash
python -m venv .venv
.\.venv\Scripts\activate   # Windows
source .venv/bin/activate  # macOS/Linux
```

**3. Install dependencies**
```bash
python -m pip install -r requirements.txt
```

**4. Run the app**
```bash
python -m streamlit run app.py
```

---

## Languages supported

- 🇬🇧 English
- 🇫🇷 French
- 🇪🇸 Spanish

---

## Roadmap

A second version of the app is currently in development with:

- 📧 User account creation and login via email
- 📄 Resume upload for personalized interview questions

---

## Tech stack

- [Streamlit](https://streamlit.io/)
- [OpenAI API](https://platform.openai.com/) — question generation and answer analysis
- PDF export
