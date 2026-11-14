COLORS = ["red", "blue", "yellow", "black"]


def _is_joker(tile):
    return tile[0] == "joker"


# 조커타일 일반 타일 구분
def _split(tiles):
    jokers = []
    normals = []
    for t in tiles:
        if _is_joker(t):
            jokers.append(t)
        else:
            normals.append(t)
    return jokers, normals

# 첫번째 조건 같은숫자이면서 다른 색상인지 검사
def is_valid_group(tiles):
    # 같은 색상이라면 패가 무조건 3개 아니면 4
    if len(tiles) not in (3, 4):
        return False
    _, normals = _split(tiles)
    # 일반 타일이 1개 이상 필수
    if not normals: # 빈 배열은 Fasle 가 된다
        return False
    # 행렬 변환으로 색과 숫자 분리
    colors, numbers = zip(*normals)
    # 조건검증
    return (
        # 숫자의 집합이 같은 숫자들
        len(set(numbers)) == 1
        # 색상의 집합이 패의 갯수와 같다면 전부 다른 색
        and len(set(colors)) == len(normals)
    )


# 2번째 같은 색상이면서 연속된 숫자인지 검사
def is_valid_run(tiles):
    n = len(tiles)
    if n < 3 or n > 13:
        return False

    jokers, normals = _split(tiles)
    if len(normals) == 0:
        return False

    color = normals[0][0]
    if color not in COLORS:
        return False

    numbers = []
    for t in normals:
        if t[0] != color:                 
            return False
        if t[1] < 1 or t[1] > 13:         
            return False
        if t[1] in numbers:               
            return False
        numbers.append(t[1])

    numbers.sort()
    smallest = numbers[0]
    biggest = numbers[-1]

    # 숫자 사이 빈칸 수 <= 조커 수 여야 함
    gaps = (biggest - smallest + 1) - len(numbers)
    if gaps > len(jokers):
        return False

    # 길이 n짜리 연속 구간이 1~13 안에 들어갈 수 있는지
    lo = max(1, biggest - n + 1)
    hi = min(smallest, 14 - n)
    return lo <= hi


def is_valid_set(tiles):
    return is_valid_group(tiles) or is_valid_run(tiles)   # and가 아니라 or


def validate_board(board):
    for s in board:
        if not is_valid_set(s):
            return False
    return True


# 조합 점수 (조커는 대체한 숫자로 계산)
def _set_score(tiles):
    jokers, normals = _split(tiles)
    n = len(tiles)

    if is_valid_group(tiles):
        return normals[0][1] * n

    # 런: 가장 작은 숫자를 찾고, 조커가 끝에 붙으면 점수가 큰 쪽으로 계산
    smallest = normals[0][1]
    for t in normals:
        if t[1] < smallest:
            smallest = t[1]
    start = min(smallest, 14 - n)

    total = 0
    for num in range(start, start + n):
        total += num
    return total


# sets = 조합들의 리스트
def validate_initial_meld(sets):
    total = 0
    for s in sets:
        if not is_valid_set(s):
            return False
        total += _set_score(s)
    return total >= 30


# 타일 목록을 {("yellow", 3): 2, ...} 형태의 딕셔너리로 셈
def _count(tiles):
    result = {}
    for t in tiles:
        key = tuple(t)              
        if key in result:
            result[key] += 1
        else:
            result[key] = 1
    return result


# 보드의 모든 타일을 한 줄 리스트로 펼침
def _flatten(board):
    result = []
    for s in board:
        for t in s:
            result.append(t)
    return result


# 전체 패 제출의 유효성 검사 (initial_meld: 이미 최초 등록했으면 True)
def validate_move(old_board, new_board, hand, initial_meld):
    old_count = _count(_flatten(old_board))
    new_count = _count(_flatten(new_board))
    hand_count = _count(hand)

    # 1) 기존 보드의 타일이 줄어들면 안 됨
    for key in old_count:
        if new_count.get(key, 0) < old_count[key]:
            return False

    # 2) 손패에서 낸 타일 확인 (최소 1장, 손패에 실제로 있어야 함)
    used_total = 0
    for key in new_count:
        used = new_count[key] - old_count.get(key, 0)
        if used > 0:
            used_total += used
            if hand_count.get(key, 0) < used:
                return False
    if used_total == 0:
        return False

    # 3) 새 보드가 모두 유효해야 함
    if not validate_board(new_board):
        return False

    # 4) 최초 등록 전이면: 기존 조합은 그대로, 새 조합만 30점 이상
    if not initial_meld:
        new_sets = list(new_board)   # 복사본
        for old_set in old_board:
            found = False
            for i in range(len(new_sets)):
                if _count(old_set) == _count(new_sets[i]):   # 같은 조합인지
                    new_sets.pop(i)
                    found = True
                    break
            if not found:            # 기존 조합이 바뀌었음
                return False
        return validate_initial_meld(new_sets)   # 남은 건 새로 만든 조합

    return True
