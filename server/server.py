"""
server.py
---------
Python WebSocket server :
  1. Chat UI (frontend) 
  2. User message received to WebSocket 
  3. Message sent to Dialogflow ES  (REST API)
  4. Dialogflow reply return to client 
"""

import asyncio
import json
import os
import uuid
import websockets
from dotenv import load_dotenv
from google.cloud import dialogflow_v2 as dialogflow

# ── .env file load karo ──────────────────────────────────────────────────────
load_dotenv()

PROJECT_ID    = os.getenv("DIALOGFLOW_PROJECT_ID")
LANGUAGE_CODE = os.getenv("DIALOGFLOW_LANGUAGE_CODE", "en")
PORT          = int(os.getenv("PORT", 3000))

# Startup pe check karo ke PROJECT_ID hai ya nahi
if not PROJECT_ID:
    raise EnvironmentError("  DIALOGFLOW_PROJECT_ID missing hai .env mein!")


# ── Dialogflow Function ──────────────────────────────────────────────────────
def send_to_dialogflow(message: str, session_id: str) -> str:
   

    # Dialogflow Sessions 
    session_client = dialogflow.SessionsClient()

    # Session path:  projects->PROJECT_ID
    session_path = session_client.session_path(PROJECT_ID, session_id)

    # Request object 
    text_input    = dialogflow.TextInput(text=message, language_code=LANGUAGE_CODE)
    query_input   = dialogflow.QueryInput(text=text_input)

    # Dialogflow request
    response      = session_client.detect_intent(
        request={"session": session_path, "query_input": query_input}
    )

    result        = response.query_result

    print(f"  ↳ Intent detect hua : {result.intent.display_name}")
    print(f"  ↳ Bot ka reply      : {result.fulfillment_text}")

    return result.fulfillment_text or "Mujhe samajh nahi aaya, dobara try karo."


# ── WebSocket Handler ────────────────────────────────────────────────────────
async def handle_client(websocket):
    """
    Har nayi WebSocket connection ke liye yeh function chalta hai.
    Ek unique session ID assign hoti hai — taake Dialogflow context yaad rakhe.
    """

    session_id = str(uuid.uuid4())
    print(f"\n[+] Client connect hua  (session: {session_id})")

    try:
        # Client messages 
        async for raw_message in websocket:

            # JSON 
            try:
                data         = json.loads(raw_message)
                user_message = data.get("message", "").strip()

                if not user_message:
                    raise ValueError("Message empty hai")

            except (json.JSONDecodeError, ValueError) as e:
                print(f"  Parse error: {e}")
                await websocket.send(json.dumps({"error": "Invalid message format"}))
                continue

            print(f"\n[→] User    : \"{user_message}\"")

            # ──  Send t Dialogflow  ──
            try:
                # Dialogflow blocking call 
                
                loop      = asyncio.get_event_loop()
                bot_reply = await loop.run_in_executor(
                    None, send_to_dialogflow, user_message, session_id
                )

                print(f"[←] Bot     : \"{bot_reply}\"")

                # ── Reply client ──
                await websocket.send(json.dumps({"text": bot_reply}))

            except Exception as df_error:
                print(f"  Dialogflow error: {df_error}")
                await websocket.send(json.dumps({
                    "text": "Sorry, something went wrong."
                }))

    except websockets.exceptions.ConnectionClosedOK:
        print(f"[-] Client disconnect hua (session: {session_id})")

    except websockets.exceptions.ConnectionClosedError as e:
        print(f"  Connection error (session: {session_id}): {e}")


# ── Server Start ─────────────────────────────────────────────────────────────
async def main():
    print(f"\n  WebSocket server   ws://localhost:{PORT}")
    print(f"  Dialogflow Project ID : {PROJECT_ID}")
    print(f"  Language              : {LANGUAGE_CODE}\n")

    # WebSocket server start 
    async with websockets.serve(handle_client, "localhost", PORT):
        await asyncio.Future()  # Server ko hamesha chalta rakho


if __name__ == "__main__":
    asyncio.run(main())
