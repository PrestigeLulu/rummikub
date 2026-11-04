"""
참고사항
tile = ["yellow", 3]
tiles = [
  ["yellow", 3],
  ["yellow", 4],
  ["joker", 0]
]
board = [
  tiles,
  tiles,
  tiles
]
"""

# 같은 숫자, 서로 다른 색상의 조합 검사
def is_valid_group(tiles):
    pass

# 같은 색상, 연속된 숫자의 조합 검사
def is_valid_run(tiles):
    pass

# 그룹 또는 연속 조합인지 검사
def is_valid_set(tiles):
    return is_valid_group(tiles) and is_valid_run(tiles)

# 보드의 모든 조합이 유효한지 검사
def validate_board(board):
    pass

# 최초 등록 30점 이상인지 검사
# sets = tiles
def validate_initial_meld(sets):
    pass

# 전체 패 제출의 유효성 검사
def validate_move(old_board, new_board, hand, initial_meld):
    pass