import socketio

sio = socketio.Client()

### 서버에 보내는 함수 ###

# 서버 주소로 연결 시도
def connect_to_server():
    pass

def join(name):
    pass

# 보드 검증, 및 제출
def play(board, hand_count):
    pass

def draw():
    pass

### 서버에서 받는 함수 ###
@sio.event
def connect():
    pass

# 손패 14장 저장, 최초 등록 False로 초기화, 게임 시작 상태 값 True로 할당
@sio.on("initial_hand")
def on_initial_hand(data):
    pass

# 받은 패를 손패에 추가
@sio.on("draw_result")
def on_draw_result(data):
    pass

# 보드 상태값 갱신, 현재 턴 갱신, 플레이어별 손패 개수 갱신
@sio.on("state_update")
def on_state_update(data):
    pass

# 승자 결과 표시
@sio.on("game_over")
def on_game_over(data):
    pass