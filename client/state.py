# 내 클라이언트 아이디
player_id = None

# 현재 턴인 플레이어 아이디
current_turn = None

# 게임 시작 상태 
game_started = False

# 최초 등록 여부
initial_meld = False

# 내 손패
hand = []

# 확정된 보드
board = []

# 수정 중인 손패
editing_hand = []

# 수정 중인 보드
editing_board = []

# 플레이어별 핸드 갯수 { 아이디: 갯수 ,,,}
hand_counts = {}