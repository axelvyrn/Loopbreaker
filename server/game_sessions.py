import uuid
from collections import defaultdict

class GameSession:
    def __init__(self, host_ws):
        self.room_code = self.generate_room_code()
        self.players = [host_ws]  # list of WebSocket connections
        self.host = host_ws
        self.game_state = {
            "started": False,
            "sequence": [],
            "current_turn": 0,
        }

    @staticmethod
    def generate_room_code():
        return str(uuid.uuid4())[:6]  # 6-character room code

    def add_player(self, player_ws):
        if player_ws not in self.players:
            self.players.append(player_ws)

    def broadcast(self, message):
        for player in self.players:
            try:
                player.send_json(message)
            except Exception as e:
                print(f"[Broadcast Error]: {e}")

    def remove_player(self, ws):
        if ws in self.players:
            self.players.remove(ws)
            if ws == self.host:
                self.host = self.players[0] if self.players else None

    def start_game(self):
        self.game_state["started"] = True

    def update_sequence(self, new_sequence):
        self.game_state["sequence"] = new_sequence

    def next_turn(self):
        self.game_state["current_turn"] += 1


# Global dictionary to manage sessions
sessions = defaultdict(lambda: None)

def create_session(host_ws):
    session = GameSession(host_ws)
    sessions[session.room_code] = session
    return session

def get_session(room_code):
    return sessions.get(room_code, None)

def remove_session(room_code):
    if room_code in sessions:
        del sessions[room_code]
