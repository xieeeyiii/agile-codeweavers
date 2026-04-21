// 全局状态
let mazeData = null;
let inventoryCount = 0;

// DOM元素
const mazeContainer = document.getElementById("maze-container");
const newMazeBtn = document.getElementById("new-maze-btn");
const statusText = document.getElementById("status");
const inventoryText = document.getElementById("inventory");

// 初始化
newMazeBtn.addEventListener("click", generateNewMaze);
document.addEventListener("keydown", handleKeyPress);

/**
 * 生成新迷宫
 */
async function generateNewMaze() {
    try {
        statusText.textContent = "正在生成迷宫...";
        const response = await fetch("/api/generate-maze");
        mazeData = await response.json();
        
        // 重置状态
        inventoryCount = 0;
        inventoryText.textContent = inventoryCount;
        
        // 渲染迷宫
        renderMaze();
        statusText.textContent = "迷宫生成完成！按W/A/S/D移动，拾取钥匙到达终点～";
    } catch (error) {
        statusText.textContent = "生成迷宫失败：" + error.message;
        console.error(error);
    }
}

/**
 * 渲染迷宫到页面
 */
function renderMaze() {
    if (!mazeData) return;

    // 清空原有迷宫
    mazeContainer.innerHTML = "";

    // 遍历每一行
    mazeData.grid.forEach((row, y) => {
        const rowElement = document.createElement("div");
        rowElement.className = "maze-row";

        // 遍历每一列
        row.forEach((cell, x) => {
            const cellElement = document.createElement("div");
            cellElement.className = "maze-cell";

            // 设置单元格样式和内容
            if (x === mazeData.player_x && y === mazeData.player_y) {
                cellElement.classList.add("player");
                cellElement.textContent = "🐱";
            } else {
                switch (cell) {
                    case "#":
                        cellElement.classList.add("wall");
                        cellElement.textContent = "#";
                        break;
                    case ".":
                        cellElement.classList.add("floor");
                        cellElement.textContent = ".";
                        break;
                    case "🔑":
                        cellElement.classList.add("item");
                        cellElement.textContent = "🔑";
                        break;
                    case "🚩":
                        cellElement.classList.add("goal");
                        cellElement.textContent = "🚩";
                        break;
                }
            }

            rowElement.appendChild(cellElement);
        });

        mazeContainer.appendChild(rowElement);
    });
}

/**
 * 处理键盘按键
 */
async function handleKeyPress(e) {
    if (!mazeData) {
        statusText.textContent = "请先生成迷宫！";
        return;
    }

    // 只处理W/A/S/D键（忽略大小写）
    const key = e.key.toLowerCase();
    if (!["w", "a", "s", "d"].includes(key)) return;

    try {
        // 调用移动接口
       const response = await fetch(`/api/move-player/${key}`);
        const result = await response.json();

        if (result.success) {
            // 更新玩家位置
            mazeData.player_x = result.player_x;
            mazeData.player_y = result.player_y;

            // 处理拾取物品
            if (result.cell === "🔑") {
               mazeData.grid[result.player_y][result.player_x] = ".";
            inventoryCount++;
        inventoryText.textContent = inventoryCount;
        statusText.textContent = "✅ 拾取了钥匙！";
            }
            // 处理到达终点
            else if (result.cell === "🚩") {
                statusText.textContent = result.msg + " 点击「生成新迷宫」继续玩～";
                // 禁用移动（可选）
                // mazeData = null;
            }
            else {
                statusText.textContent = "移动成功！";
            }

            // 重新渲染迷宫
            renderMaze();
        } else {
            statusText.textContent = result.msg;
        }
    } catch (error) {
        statusText.textContent = "移动失败：" + error.message;
        console.error(error);
    }
}