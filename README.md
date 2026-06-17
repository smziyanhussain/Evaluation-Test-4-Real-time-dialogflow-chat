# 🤖 Real-time Chat Application
### Dialogflow ES + Python WebSocket + HTML Frontend

> Evaluation Test 4 — Real-time Chat Application using Google Dialogflow ES  
> with Fulfillment Webhook and WebSocket

---

## 🏗️ Architecture

```
┌──────────────────┐        WebSocket         ┌──────────────────────┐        HTTPS        ┌───────────────┐
│   Chat UI        │ ◄──────────────────────► │   Python WS Server   │ ◄─────────────────► │ Dialogflow ES │
│  (index.html)    │                           │     (server.py)      │                     │               │
└──────────────────┘                           └──────────────────────┘                     └───────────────┘
     Browser                                        Terminal                                   Google Cloud
```

**Flow:**
1. User types a message in the Chat UI
2. Frontend sends the message to the server via WebSocket
3. Server makes a REST API call to Dialogflow ES
4. Dialogflow matches the intent and returns a reply
5. Server sends the reply back to the frontend via WebSocket
6. Frontend displays the reply in the chat

---

## 📁 Project Structure

```
dialogflow-chat/
├── frontend/
│   └── index.html              # Chat UI (HTML + CSS + JavaScript)
├── server/
│   ├── server.py               # Python WebSocket Server
│   ├── requirements.txt        # Python dependencies
│   ├── .env.example            # Environment variables template
│   └── .gitignore              # Git ignore rules
└── README.md
```

---

## ⚙️ Prerequisites

| Tool | Version |
|------|---------|
| Python | 3.8+ |
| pip | latest |
| Google Cloud Account | — |
| Dialogflow ES Agent | Created & Trained |

---


---

### Step 2 — Create a Dialogflow ES Agent
1. Go to [dialogflow.cloud.google.com](https://dialogflow.cloud.google.com)


---

### Step 3 — Create a Google Cloud Service Account Key
1. Go to [console.cloud.google.com](https://console.cloud.google.com)



---

### Step 4 — Configure Environment Variables
cd server


---

### Step 5 — Install Dependencies
```bash
cd server
pip install -r requirements.txt
```

---

### Step 6 — Start the Server
```bash
python server.py
```

If everything is set up correctly, you will see:
```
🚀  WebSocket server running on ws://localhost:3000
📡  Dialogflow Project ID : your-project-id
🌐  Language              : en
```

---

### Step 7 — Open the Frontend
Open `frontend/index.html` in your browser by **double-clicking** the file.

You will see **🟢 Connected** — you can now start chatting!

---

## 🔧 Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| `websockets` | 12.0 | WebSocket server |
| `google-cloud-dialogflow` | 2.29.0 | Dialogflow ES API client |
| `python-dotenv` | 1.0.1 | Loads environment variables from .env |

---

## ❗ Common Errors & Fixes

| Error | Reason | Fix |
|-------|--------|-----|
| `DIALOGFLOW_PROJECT_ID missing` | `.env` file not created | Copy `.env.example` and rename it to `.env` |
| `403 SERVICE_DISABLED` | Dialogflow API is disabled | Enable the API in Google Cloud Console |
| `403 IAM permission denied` | Service account missing role | Assign `Dialogflow API Client` role in IAM |
| `ModuleNotFoundError` | Dependencies not installed | Run `pip install -r requirements.txt` |
| `🔴 Disconnected` in frontend | Server is not running | Run `python server.py` in the terminal |

---

## 📝 Notes

- The server and frontend must **both be running** at the same time
- Always **start the server first**, then open the frontend
- Each browser tab gets its own **Dialogflow session** — conversation context is preserved per tab

