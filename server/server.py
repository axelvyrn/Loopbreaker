# server/server.py

import asyncio
import websockets
import json
from server.game_sessions import GameSessions

PORT = 6789
sessions = GameSessions()


async def handler(websocket, path):
    try:
        async for message in websocket:
            data = json.loads(message)

            action = data.get("action")
            username = data.get("username")

            if action == "create_game":
                room_code = sessions.create_game(username, websocket)
                await websocket.send(json.dumps({
                    "type": "game_created",
                    "room_code": room_code
                }))

            elif action == "join_game":
                room_code = data.get("room_code")
                success = sessions.join_game(room_code, username, websocket)
                await websocket.send(json.dumps({
                    "type": "join_status",
                    "success": success
                }))

            elif action == "submit_answer":
                room_code = data.get("room_code")
                answer = data.get("answer")
                await sessions.broadcast(room_code, {
                    "type": "answer",
                    "username": username,
                    "answer": answer
                })

            elif action == "start_game":
                room_code = data.get("room_code")
                await sessions.start_game(room_code)

    except websockets.exceptions.ConnectionClosed:
        sessions.remove_connection(websocket)


if __name__ == "__main__":
    print(f"🔌 Starting WebSocket server on port {PORT}...")
    start_server = websockets.serve(handler, "localhost", PORT)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
