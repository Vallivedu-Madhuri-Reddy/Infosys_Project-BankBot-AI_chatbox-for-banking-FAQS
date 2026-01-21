# BankBot AI – Intelligent Banking FAQ Chatbot

![Python](https://img.shields.io/badge/Python-3.x-blue)
![AI/NLP](https://img.shields.io/badge/AI-NLP-orange)
![LLM](https://img.shields.io/badge/LLM-Transformer--based-green)
![Status](https://img.shields.io/badge/Status-Completed-success)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

---

## Project Description

**BankBot AI** is an intelligent AI-powered chatbot designed to handle **banking-related Frequently Asked Questions (FAQs)** using modern **Natural Language Processing (NLP)** and **Large Language Models (LLMs)**.
The chatbot understands user queries in natural language and provides accurate, context-aware responses related to banking services such as balance inquiries, card details, loans, transfers, and general banking information.

This project is developed as part of the **Infosys Springboard Internship / Certification program**, showcasing real-world application of AI, NLP, and LLM technologies in the banking domain.

---

## Features

* Conversational AI chatbot for banking FAQs
* Natural language query understanding
* Intelligent intent identification
* Context-aware response generation
* Transformer-based LLM integration
* Configurable LLM backend
* Modular and scalable architecture
* Easy local setup and execution
* Certification and academic ready project

---

## Techniques Used

### Natural Language Processing (NLP)

* Text preprocessing and normalization
* Tokenization and semantic understanding
* Intent recognition from user queries

### Prompt Engineering

* Domain-specific prompt design
* Structured prompts for accurate banking responses
* Improved response clarity and consistency

### LLM-based Text Generation

* Dynamic response generation using LLMs
* Contextual and human-like answers
* Easily extendable for advanced conversational flows

---

## Tech Stack

### Programming Language

* **Python**

### Libraries / Frameworks

* Streamlit – user interface
* LangChain – LLM orchestration and prompt management
* Transformers – model integration
* spaCy / NLTK – NLP processing

### AI / ML Technologies

* Natural Language Processing (NLP)
* Large Language Models (LLMs)
* Transformer architectures

---

## LLM Details

* Uses **transformer-based Large Language Models**
* Designed to be **LLM-agnostic and configurable**
* Supports integration with:

  * OpenAI models
  * Hugging Face transformer models
  * Other compatible LLM providers

The LLM can be changed or upgraded without modifying the core chatbot logic, making the system flexible and future-proof.

---

## Project Structure

```
BankBot_AI/
│
├── app.py                     # Main Streamlit application
├── backend/
│   ├── llm_handler.py         # LLM configuration and calls
│   ├── intent_classifier.py  # Intent recognition logic
│   └── response_engine.py    # Response generation
├── data/
│   └── faq_data.json          # Banking FAQs and knowledge base
├── ui/
│   └── chatbot_ui.py          # Chat interface components
├── requirements.txt           # Python dependencies
├── README.md                  # Project documentation
└── .env.example               # Environment variables template
```

---

## Installation Steps

1. **Clone the repository**

   ```
   git clone https://github.com/Vallivedu-Madhuri-Reddy/Infosys_Project-BankBot-AI_chatbox-for-banking-FAQS.git
   ```

2. **Navigate to the project directory**

   ```
   cd Infosys_Project-BankBot-AI_chatbox-for-banking-FAQS
   ```

3. **Create a virtual environment (recommended)**

   ```
   python -m venv venv
   ```

4. **Activate the virtual environment**

   * Windows:

     ```
     venv\Scripts\activate
     ```
   * macOS/Linux:

     ```
     source venv/bin/activate
     ```

5. **Install required dependencies**

   ```
   pip install -r requirements.txt
   ```

6. **Configure environment variables**

   * Copy `.env.example` to `.env`
   * Add LLM API keys if required

---

## How to Run the Project Locally

1. Ensure the virtual environment is activated
2. Run the Streamlit application:

   ```
   streamlit run app.py
   ```
3. Open the local URL shown in the terminal
4. Start chatting with **BankBot AI**

---

## Certification Use Case

This project is suitable for:

* **Infosys Springboard Internship Certification**
* Academic mini and major projects
* AI / NLP portfolio projects
* GitHub and resume showcase

It demonstrates:

* End-to-end AI chatbot development
* Practical use of NLP and LLMs
* Industry-relevant problem-solving skills

---

## License

This project is licensed under the **MIT License**.
You are free to use, modify, and distribute this project for educational and professional purposes.

---

**Developed by:** Vallivedu Madhuri Reddy
**Domain:**Python| Artificial Intelligence | NLP | Large Language Models
**Purpose:** Educational, Internship, and Certification Use
