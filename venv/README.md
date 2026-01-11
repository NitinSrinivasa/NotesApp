NotesApp 📝

FastAPI + MySQL + OpenAI (GPT-4o) Notes Backend

NotesApp is a backend API built with FastAPI and SQLAlchemy that allows users to create and manage personal notes.
It also supports AI-generated notes and summaries using OpenAI’s GPT-4o model.

This project is designed as a backend service and includes client scripts for interacting with the API.

🚀 Features

User creation with unique username validation

Create, read, update, and delete notes

Fetch notes by user

Lookup users by username

AI-generated notes using OpenAI (GPT-4o)

API key–protected endpoints

MySQL database

CORS enabled for frontend integration

Command-line client scripts

📁 Project Structure

NotesApp/
├── notes-frontend/ (Frontend – not covered here)
├── client.py (Simple API client)
├── fetch_notes.py (Fetch notes + GPT-4o summary)
├── crud.py (Database operations)
├── database.py (Database connection)
├── init_db.py (Create database tables)
├── main.py (FastAPI application)
├── models.py (SQLAlchemy models)
├── schemas.py (Pydantic schemas)
├── README.md
├── venv/ (Virtual environment – ignored)

🔐 API Authentication

All endpoints require an API key sent as a request header:

X-API-Key: supersecretkey123

This key is hardcoded for development.
In production, move it to environment variables.

🗄 Database Configuration

The backend uses MySQL with the following connection string:

mysql+mysqlconnector://root:secretpassword@localhost:3307/notesapp

Create the database in MySQL:

CREATE DATABASE notesapp;

Make sure MySQL is running on port 3307.

🛠 Setup Instructions

Create and activate a virtual environment

python -m venv venv
source venv/bin/activate (macOS / Linux)
venv\Scripts\activate (Windows)

Install dependencies

pip install fastapi uvicorn sqlalchemy mysql-connector-python pydantic requests openai python-dotenv

Set OpenAI API key

export OPENAI_API_KEY="your_openai_api_key"

Create database tables

python init_db.py

Run the FastAPI server

uvicorn main:app --reload

API will be available at:
http://127.0.0.1:8000

Swagger docs:
http://127.0.0.1:8000/docs

📌 API Usage Examples

Create User (POST /users/)

username: nitin
email: nitin@example.com

Create Note (POST /users/{user_id}/notes/)

title: My Note
content: This is a test note

Update Note (PUT /users/{user_id}/notes/{note_id})

title: Updated Title
content: Updated content

Create AI Summary Note (POST /users/{user_id}/notes/ai-summary)

query: Explain FastAPI and its use cases

🧪 Client Scripts

Fetch notes for a user:

python client.py

Fetch notes and summarize with GPT-4o:

python fetch_notes.py