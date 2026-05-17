// 全局状态
let mazeData = null;
let inventoryCount = 0;

// DOM元素
const mazeContainer = document.getElementById("maze-container");
const newMazeBtn = document.getElementById("new-maze-btn");
const resetBtn = document.getElementById("reset-btn");
const statusText = document.getElementById("status");
const inventoryText = document.getElementById("inventory");
const totalKeysText = document.getElementById("total-keys");
const progressFill = document.getElementById("progress-fill");

// 初始化事件监听
newMazeBtn.addEventListener("click", generateNewMaze);
resetBtn.addEventListener("click", resetGame);
document.addEventListener("keydown", handleKeyPress);

// 生成新迷宫
async function generateNewMaze() {
    try {
        statusText.textContent = "⏳ 正在生成神秘迷宫...";
        const response = await fetch("/api/generate-maze");
        mazeData = await response.json();
        
        inventoryCount = 0;
        inventoryText.textContent = inventoryCount;
        totalKeysText.textContent = mazeData.total_keys;
        updateProgress();
        
        renderMaze();
        statusText.textContent = "✨ 迷宫已生成！用 WASD 控制猫咪冒险 ✨";
    } catch (error) {
        statusText.textContent = "❌ 生成迷宫失败：" + error.message;
        console.error(error);
    }
}

// 重置游戏
async function resetGame() {
    if (!mazeData) {
        generateNewMaze();
        return;
    }
    
    try {
        const response = await fetch("/api/reset", {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' }
        });
        const result = await response.json();
        
        if (result.success) {
            inventoryCount = 0;
            inventoryText.textContent = inventoryCount;
            updateProgress();
            
            // 刷新迷宫数据
            const refreshResp = await fetch("/api/generate-maze");
            mazeData = await refreshResp.json();
            totalKeysText.textContent = mazeData.total_keys;
            renderMaze();
            statusText.textContent = "🔄 游戏已重置，重新开始冒险！";
        }
    } catch (error) {
        statusText.textContent = "重置失败：" + error.message;
    }
}

// 更新进度条
function updateProgress() {
    if (mazeData && mazeData.total_keys > 0) {
        const percent = (inventoryCount / mazeData.total_keys) * 100;
        progressFill.style.width = `${percent}%`;
    } else {
        progressFill.style.width = "0%";
    }
}

// 渲染迷宫
function renderMaze() {
    if (!mazeData) {
        mazeContainer.innerHTML = `
            <div class="placeholder">
                <span class="placeholder-icon">🗺️</span>
                <p>点击「生成新迷宫」开始游戏</p>
            </div>
        `;
        return;
    }

    mazeContainer.innerHTML = "";

    mazeData.grid.forEach((row, y) => {
        const rowElement = document.createElement("div");
        rowElement.className = "maze-row";

        row.forEach((cell, x) => {
            const cellElement = document.createElement("div");
            cellElement.className = "maze-cell";

            // 判断是否是玩家位置
            if (x === mazeData.player_x && y === mazeData.player_y) {
                cellElement.classList.add("player");
                cellElement.textContent = "🐱";
            } else {
                switch (cell) {
                    case "#":
                        cellElement.classList.add("wall");
                        cellElement.textContent = "█";
                        break;
                    case ".":
                        cellElement.classList.add("floor");
                        cellElement.textContent = "·";
                        break;
                    case "🔑":
                        cellElement.classList.add("item");
                        cellElement.textContent = "🔑";
                        break;
                    case "🚩":
                        cellElement.classList.add("goal");
                        cellElement.textContent = "🚩";
                        break;
                    default:
                        cellElement.textContent = "·";
                }
            }
            rowElement.appendChild(cellElement);
        });
        mazeContainer.appendChild(rowElement);
    });
}

// 处理键盘移动
async function handleKeyPress(e) {
    if (!mazeData) {
        statusText.textContent = "🔔 请先生成迷宫！点击「生成新迷宫」开始～";
        return;
    }

    const key = e.key.toLowerCase();
    if (!["w", "a", "s", "d"].includes(key)) return;
    
    e.preventDefault();

    try {
        const response = await fetch(`/api/move/${key}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' }
        });
        const result = await response.json();

        if (result.success) {
            // 更新玩家位置
            mazeData.player_x = result.player_x;
            mazeData.player_y = result.player_y;

            // 处理拾取钥匙
            if (result.cell === "🔑") {
                mazeData.grid[result.player_y][result.player_x] = ".";
                inventoryCount = result.keys_collected;
                inventoryText.textContent = inventoryCount;
                updateProgress();
                statusText.textContent = result.message || "🔑 拾取到一枚金钥匙！";
                
                // 播放拾取特效
                const statusDiv = document.querySelector(".status-message");
                statusDiv.style.animation = "none";
                setTimeout(() => statusDiv.style.animation = "", 10);
            }
            // 处理到达终点
            else if (result.cell === "🚩") {
                statusText.textContent = result.message;
                if (result.victory) {
                    statusText.innerHTML = "🎉🎉🎉 胜利！成功集齐钥匙并到达终点！🎉🎉🎉";
                    mazeContainer.classList.add("victory");
                    setTimeout(() => mazeContainer.classList.remove("victory"), 800);
                }
            }
            else {
                statusText.textContent = result.message || "🐱 移动成功";
            }
            
            renderMaze();
        } else {
            statusText.textContent = result.message || "🚫 无法移动！";
        }
    } catch (error) {
        statusText.textContent = "⚠️ 连接失败：" + error.message;
        console.error(error);
    }
}