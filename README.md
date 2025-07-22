# 📄 Real-Time Collaborative Document Editor

A powerful, real-time collaborative document editing platform built using **Django**, **Django Channels**, and **WebSockets**. It enables multiple users to collaborate simultaneously on documents, with grammar checking (LanguageTool) and AI writing assistance (OpenAI GPT).

---

## 🚀 Features

- ✍️ Live document editing via WebSocket
- 📜 Auto-saving and persistent changes
- 🧠 Grammar suggestions with LanguageTool
- 🤖 AI-powered writing improvements using OpenAI
- 🧾 Upload DOCX & PDF documents
- 📈 View & restore document version history
- 🔐 User authentication and document sharing

---

## 🛠 Tech Stack

| Category      | Technologies                          |
|---------------|----------------------------------------|
| Backend       | Django, Django REST Framework          |
| Realtime      | Django Channels, Daphne, Redis         |
| Frontend      | HTML, CSS, JS, Quill.js                |
| AI Integration| OpenAI GPT, LanguageTool API           |
| Auth System   | Custom Django User Model               |
| Static Files  | WhiteNoise (for ASGI static serving)   |
| DB            | SQLite (for dev), PostgreSQL (prod)    |

---

## 📁 Project Structure

collab_editor/
├── editor/ # Main app logic
│ ├── views.py # Editor views
│ ├── consumers.py # WebSocket consumers
│ ├── ai.py # OpenAI & Grammar logic
├── users/ # Custom User model
├── static/ # JS, CSS, Quill, etc.
├── templates/ # HTML templates
├── collab_editor/ # Project settings
├── manage.py
├── requirements.txt
├── README.md
└── .env (not tracked)


**Steps For Run :**

**Setup Virtual Environment**
    python -m venv env
    env\Scripts\activate       # For Windows

    source env/bin/activate    # For Mac/Linux

**Install Dependencies**
     pip install -r requirements.txt
     
**Configure .env**
    SECRET_KEY=your-django-secret-key
    DEBUG=True
    OPENAI_API_KEY=your-openai-api-key

**Database Migration & Superuser**
    python manage.py makemigrations
    python manage.py migrate
    python manage.py createsuperuser

**Running the Server**
    **Standard Django (No WebSocket)**
        python manage.py runserver
        
**With WebSocket Support (Recommended)**
    uvicorn collab_editor.asgi:application --host 127.0.0.1 --port 8000 --reload

🌐 **Key Routes**
      Feature	Path
      Admin Panel	/admin/
      Document Dashboard	/editor/
      Create Document	/editor/create/
      Edit Document	/editor/<doc_id>/
      Upload File	/editor/upload/
      Version History	/editor/<doc_id>/versions/
      Share Document	/editor/<doc_id>/share/


🙏 **Acknowledgements**
      Django
      Channels
      Quill.js
      OpenAI API
      LanguageTool


📞 **Contact**
      Author: Jayesh Savant
      Email: jayeshsavant754@gmail.com
      GitHub: @Savantjayesh
