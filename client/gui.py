
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<title>루미큐브</title>

<style>
body {
    margin: 0;
    background: #176B45;
    font-family: Arial, sans-serif;
    color: white;
}

.container {
    width: 95%;
    margin: 20px auto;
}

.game-room {
    background: #105235;
    height: 350px;
    border-radius: 15px;
    padding: 20px;
    position: relative;
    box-sizing: border-box;
}

h2 {
    text-align: center;
}

.my-tiles {
    background: #105235;
    min-height: 170px;
    border-radius: 15px;
    padding: 15px;
    margin-top: 20px;
}

.tile-list {
    display: flex;
    justify-content: center;
    flex-wrap: wrap;
    gap: 10px;
}

.tile {
    width: 55px;
    height: 75px;
    background: white;
    border-radius: 7px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 30px;
    font-weight: bold;
    box-shadow: 2px 3px 5px #083b27;
    cursor: grab;
    user-select: none;
    touch-action: none;
    position: relative;
}

.red { color: red; }
.blue { color: blue; }
.black { color: black; }
.orange { color: orange; }
.joker { color: purple; }

.tile.dragging {
    position: fixed;
    z-index: 1000;
    pointer-events: none;
}

.controls {
    text-align: center;
    margin-top: 15px;
}

button {
    padding: 12px 25px;
    background: #f5c542;
    border: none;
    border-radius: 8px;
    font-size: 16px;
    font-weight: bold;
    cursor: pointer;
}

button:hover {
    background: #ffe082;
}

#tileCount {
    text-align: center;
    margin-top: 10px;
}
</style>
</head>

<body>

<div class="container">

    <div class="game-room" id="gameRoom">
        <h2>게임방</h2>
    </div>

    <div class="my-tiles">
        <h2>내 타일</h2>

        <div class="tile-list" id="tileList"></div>

        <div class="controls">
            <button onclick="drawTile()">랜덤 타일 뽑기</button>
            <button onclick="startGame()">게임 시작 (14개)</button>
        </div>

        <p id="tileCount">남은 타일: 106개</p>
    </div>

</div>

<script>
const gameRoom = document.getElementById("gameRoom");
const tileList = document.getElementById("tileList");

let tiles = [];
let hand = [];

const colors = ["red", "blue", "black", "orange"];

// 타일 106개 생성
function createTiles() {
    tiles = [];

    colors.forEach(color => {
        for (let number = 1; number <= 13; number++) {
            tiles.push({color, number});
            tiles.push({color, number});
        }
    });

    tiles.push({color: "joker", number: 0});
    tiles.push({color: "joker", number: 0});

    // 랜덤 섞기
    for (let i = tiles.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [tiles[i], tiles[j]] = [tiles[j], tiles[i]];
    }

    updateCount();
}

// 타일 화면 만들기
function createTileElement(tile) {
    const div = document.createElement("div");

    div.className = "tile " + tile.color;
    div.innerText =
        tile.color === "joker" ? "★" : tile.number;

    div.addEventListener("pointerdown", e => {
        startDrag(e, div);
    });

    return div;
}

// 타일 뽑기
function drawTile() {
    if (tiles.length === 0) {
        alert("남은 타일이 없습니다!");
        return;
    }

    const tile = tiles.pop();

    hand.push(tile);

    tileList.appendChild(createTileElement(tile));

    updateCount();
}

// 게임 시작
function startGame() {
    if (hand.length > 0) {
        alert("이미 타일을 가지고 있습니다!");
        return;
    }

    for (let i = 0; i < 14; i++) {
        if (tiles.length === 0) break;

        const tile = tiles.pop();
        hand.push(tile);
        tileList.appendChild(createTileElement(tile));
    }

    updateCount();
}

// 남은 타일 표시
function updateCount() {
    document.getElementById("tileCount").innerText =
        "남은 타일: " + tiles.length + "개";
}

// 드래그 기능
let draggedTile = null;
let offsetX = 0;
let offsetY = 0;

function startDrag(e, tile) {
    draggedTile = tile;

    const rect = tile.getBoundingClientRect();

    offsetX = e.clientX - rect.left;
    offsetY = e.clientY - rect.top;

    tile.classList.add("dragging");
    document.body.appendChild(tile);

    moveTile(e);

    tile.setPointerCapture(e.pointerId);
}

document.addEventListener("pointermove", e => {
    if (!draggedTile) return;
    moveTile(e);
});

document.addEventListener("pointerup", e => {
    if (!draggedTile) return;

    const roomRect = gameRoom.getBoundingClientRect();

    const insideRoom =
        e.clientX >= roomRect.left &&
        e.clientX <= roomRect.right &&
        e.clientY >= roomRect.top &&
        e.clientY <= roomRect.bottom;

    draggedTile.classList.remove("dragging");

    if (insideRoom) {
        draggedTile.style.position = "absolute";
        draggedTile.style.left =
            (e.clientX - roomRect.left - offsetX) + "px";
        draggedTile.style.top =
            (e.clientY - roomRect.top - offsetY) + "px";

        gameRoom.appendChild(draggedTile);
    } else {
        draggedTile.style.position = "relative";
        draggedTile.style.left = "auto";
        draggedTile.style.top = "auto";

        tileList.appendChild(draggedTile);
    }

    draggedTile = null;
});

function moveTile(e) {
    draggedTile.style.left =
        (e.clientX - offsetX) + "px";

    draggedTile.style.top =
        (e.clientY - offsetY) + "px";
}

// 처음 실행
createTiles();

</script>

</body>
</html>
