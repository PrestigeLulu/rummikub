
import tkinter as tk
from tkinter import messagebox
import random

# -------------------------
# 기본 설정
# -------------------------

root = tk.Tk()
root.title("루미큐브")
root.geometry("1000x750")
root.configure(bg="#176B45")
root.resizable(False, False)

# 색상
colors = {
    "red": "#e53935",
    "blue": "#1565c0",
    "black": "#222222",
    "orange": "#ef8c00",
    "joker": "purple"
}

# 타일 데이터
tiles = []
hand = []
room_tiles = []

dragging = None
drag_start = None

# -------------------------
# 타일 106개 생성
# -------------------------

def create_tiles():
    global tiles

    tiles = []

    for color in ["red", "blue", "black", "orange"]:
        for number in range(1, 14):
            tiles.append({
                "color": color,
                "number": number
            })
            tiles.append({
                "color": color,
                "number": number
            })

    # 조커 2개
    tiles.append({
        "color": "joker",
        "number": 0
    })

    tiles.append({
        "color": "joker",
        "number": 0
    })

    random.shuffle(tiles)
    update_count()


# -------------------------
# 화면 구성
# -------------------------

canvas = tk.Canvas(
    root,
    width=960,
    height=700,
    bg="#176B45",
    highlightthickness=0
)

canvas.pack(padx=20, pady=20)

# 게임방
canvas.create_rectangle(
    10, 10, 950, 370,
    fill="#105235",
    outline="#105235"
)

canvas.create_text(
    480, 35,
    text="게임방",
    fill="white",
    font=("Arial", 22, "bold")
)

# 내 타일 영역
canvas.create_rectangle(
    10, 390, 950, 680,
    fill="#105235",
    outline="#105235"
)

canvas.create_text(
    480, 415,
    text="내 타일",
    fill="white",
    font=("Arial", 22, "bold")
)

# -------------------------
# 타일 그리기
# -------------------------

def draw_tile(tile, x, y, zone):

    tag = f"tile_{id(tile)}"

    color = colors[tile["color"]]

    if tile["color"] == "joker":
        number = "★"
    else:
        number = str(tile["number"])

    canvas.create_rectangle(
        x, y, x + 50, y + 65,
        fill="white",
        outline="#dddddd",
        width=2,
        tags=(tag, "tile")
    )

    canvas.create_text(
        x + 25, y + 32,
        text=number,
        fill=color,
        font=("Arial", 25, "bold"),
        tags=(tag, "tile")
    )

    canvas.addtag_withtag(zone, tag)


# -------------------------
# 내 타일 정렬
# -------------------------

def arrange_hand():

    canvas.delete("hand")

    for i, tile in enumerate(hand):

        x = 25 + (i % 16) * 57
        y = 440 + (i // 16) * 75

        draw_tile(tile, x, y, "hand")


# -------------------------
# 게임방 타일 그리기
# -------------------------

def arrange_room():

    canvas.delete("room")

    for tile in room_tiles:

        draw_tile(
            tile,
            tile["x"],
            tile["y"],
            "room"
        )


# -------------------------
# 랜덤 타일 뽑기
# -------------------------

def draw_random_tile():

    if not tiles:
        messagebox.showinfo(
            "알림",
            "남은 타일이 없습니다!"
        )
        return

    tile = tiles.pop()

    hand.append(tile)

    arrange_hand()
    update_count()


# -------------------------
# 게임 시작
# -------------------------

def start_game():

    if hand:
        messagebox.showinfo(
            "알림",
            "이미 타일을 가지고 있습니다!"
        )
        return

    for i in range(14):

        if not tiles:
            break

        hand.append(tiles.pop())

    arrange_hand()
    update_count()


# -------------------------
# 타일 개수 표시
# -------------------------

def update_count():

    canvas.delete("count")

    canvas.create_text(
        480, 655,
        text=f"남은 타일: {len(tiles)}개",
        fill="white",
        font=("Arial", 14, "bold"),
        tags="count"
    )


# -------------------------
# 드래그 시작
# -------------------------

def mouse_down(event):

    global dragging, drag_start

    items = canvas.find_overlapping(
        event.x, event.y,
        event.x, event.y
    )

    for item in reversed(items):

        tags = canvas.gettags(item)

        for tag in tags:

            if tag.startswith("tile_"):

                dragging = tag

                drag_start = (
                    event.x,
                    event.y
                )

                return


# -------------------------
# 타일 이동
# -------------------------

def mouse_move(event):

    global dragging

    if dragging is None:
        return

    canvas.move(
        dragging,
        event.x - drag_start[0],
        event.y - drag_start[1]
    )

    drag_start = (event.x, event.y)


# -------------------------
# 드래그 종료
# -------------------------

def mouse_up(event):

    global dragging

    if dragging is None:
        return

    coords = canvas.coords(dragging)

    if not coords:
        dragging = None
        return

    x = coords[0]
    y = coords[1]

    tile = None

    for t in hand + room_tiles:

        if f"tile_{id(t)}" == dragging:
            tile = t
            break

    if tile is None:
        dragging = None
        return

    # 게임방 안에 놓았을 때
    if 10 <= x <= 900 and 10 <= y <= 300:

        if tile in hand:
            hand.remove(tile)
            room_tiles.append(tile)

        tile["x"] = x
        tile["y"] = y

    else:

        # 내 타일 영역으로 이동
        if tile in room_tiles:
            room_tiles.remove(tile)
            hand.append(tile)

    dragging = None

    arrange_hand()
    arrange_room()
    update_count()


# -------------------------
# 버튼
# -------------------------

draw_button = tk.Button(
    root,
    text="랜덤 타일 뽑기",
    font=("Arial", 13, "bold"),
    bg="#f5c542",
    command=draw_random_tile
)

start_button = tk.Button(
    root,
    text="게임 시작 (14개)",
    font=("Arial", 13, "bold"),
    bg="#f5c542",
    command=start_game
)

draw_button.place(x=330, y=725)
start_button.place(x=510, y=725)

# -------------------------
# 마우스 이벤트
# -------------------------

canvas.bind("<Button-1>", mouse_down)
canvas.bind("<B1-Motion>", mouse_move)
canvas.bind("<ButtonRelease-1>", mouse_up)

# -------------------------
# 처음 실행
# -------------------------

create_tiles()

root.mainloop()
