# websocket server for dialogflow chatbot
# connects the chat frontend to dialogflow ES

import asyncio
import json
import os
import uuid
import websockets
from dotenv import load_dotenv
from google.cloud import dialogflow_v2 as dialogflow

load_dotenv()

PROJECT_ID = os.getenv("DIALOGFLOW_PROJECT_ID")
LANGUAGE_CODE = os.getenv("DIALOGFLOW_LANGUAGE_CODE", "en")
PORT = int(os.getenv("PORT", 3000))

if not PROJECT_ID:
    raise EnvironmentError("DIALOGFLOW_PROJECT_ID is missing in .env file")


def send_to_dialogflow(message, session_id):
    # create a session and send user message to dialogflow
    session_client = dialogflow.SessionsClient()
    session_path = session_client.session_path(PROJECT_ID, session_id)

    text_input = dialogflow.TextInput(text=message, language_code=LANGUAGE_CODE)
    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={"session": session_path, "query_input": query_input}
    )

    result = response.query_result
    print(f"Intent: {result.intent.display_name}")
    print(f"Reply: {result.fulfillment_text}")

    return result.fulfillment_text or "Sorry, I did not understand that."


async def handle_client(websocket):
    # each client gets a unique session so dialogflow remembers context
    session_id = str(uuid.uuid4())
    print(f"Client connected - session: {session_id}")

    try:
        async for raw_message in websocket:
            try:
                data = json.loads(raw_message)
                user_message = data.get("message", "").strip()

                if not user_message:
                    raise ValueError("empty message")

            except (json.JSONDecodeError, ValueError) as e:
                print(f"Parse error: {e}")
                await websocket.send(json.dumps({"error": "invalid message"}))
                continue

            print(f"User: {user_message}")

            try:
                # run dialogflow call in thread so async loop doesnt block
                loop = asyncio.get_event_loop()
                bot_reply = await loop.run_in_executor(
                    None, send_to_dialogflow, user_message, session_id
                )

                print(f"Bot: {bot_reply}")
                await websocket.send(json.dumps({"text": bot_reply}))

            except Exception as e:
                print(f"Dialogflow error: {e}")
                await websocket.send(json.dumps({"text": "Something went wrong, please try again."}))

    except websockets.exceptions.ConnectionClosedOK:
        print(f"Client disconnected - session: {session_id}")

    except websockets.exceptions.ConnectionClosedError as e:
        print(f"Connection error: {e}")


async def main():
    print(f"Server running on ws://localhost:{PORT}")
    print(f"Project: {PROJECT_ID}")

    async with websockets.serve(handle_client, "localhost", PORT):
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
