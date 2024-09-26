# AI Chatbot

This project is a Retrieval-Augmented Generation (RAG)-based chatbot designed to answer questions from PDF documents. By integrating semantic search with an open-source large language model (LLM), the chatbot can provide accurate, context-aware responses to user queries.

---

## Table of Contents

1. [Features](#features)
2. [Prerequisites](#prerequisites)
3. [Installation](#installation)
4. [Running the Application](#running-the-application)
5. [API Documentation](#api-documentation)

---

## Features

- 📄 Simple Interface: Upload PDF documents and submit queries through an easy-to-use interface.
- 🧠 Semantic Search: Retrieves relevant information from the uploaded documents using vector-based search techniques.
- 🖥️ LLM-Powered Answers: Uses an open-source LLM to generate responses based on the retrieved document content.
  Prerequisites

---

## Prerequisites

The following tools and technologies are required to run the application:

- Python 3.8.2+
- [FastAPI](https://fastapi.tiangolo.com/) (for creating the API)
- [Uvicorn](https://www.uvicorn.org/) (ASGI server to run FastAPI)
- [Pipenv](https://pipenv.pypa.io/en/latest/) or [virtualenv](https://virtualenv.pypa.io/en/latest/) (for environment management)

---

## Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/your-repo-name.git
cd your-repo-name
```

### Step 2: Create a Virtual Environment

You can create a virtual environment using the virtualenv package:

```bash
pip install virtualenv
python3 -m venv your_env_name
source env/bin/activate  # On macOS/Linux
env\Scripts\activate  # On Windows
```

### Step 3: Install Dependencies

Once the virtual environment is activated, install the required Python packages::

```bash
pip install -r requirements.txt
```

### Step 4 : Create Hugging Face Token

Create a Hugging Face token from the Hugging Face website and assign it the necessary permissions. Then, add the token to the .env file

```
HF_TOKEN = "Your Hugging Face Token"
```

## Running the Application

### Step 1: Start the Uvicorn Server

```bash
 python3 -m uvicorn app:app --reload
```

### Step 2: Access the App

Once the server is running, visit http://127.0.0.1:8000 in your browser.

### Step 3: Explore API Docs

FastAPI automatically generates interactive API documentation:

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

#
