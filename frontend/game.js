// 游戏状态
let mazeData = null;
let inventoryCount = 0;
let cellSize = 32; // 动态计算的单元格大小

// DOM 元素
const canvas = document.getElementById('maze-canvas');
const ctx = canvas.getContext('2d');
const inventoryText = document.getElementById('inventory');
const totalKeysText = document.getElementById('total-keys');
const progressFill = document.getElementById('progress-fill');
const progressText = document.getElementById('progress-text');
const statusText = document.getElementById('status');

// 按钮
const newGameBtn = document.getElementById('new-game-btn');
const resetGameBtn = document.getElementById('reset-game-btn');
const backBtn = document.getElementById('back-btn');

// 初始化
newGameBtn.addEventListener('click', generateNewMaze);
resetGameBtn.addEventListener('click', resetGame);
backBtn.addEventListener('click', () => {
    window.location.href = 'index.html';
});
document.addEventListener('keydown', handleKeyPress);

// 生成新迷宫
async function generateNewMaze() {
    try {
        statusText.textContent = "⏳ 生成迷宫中...";
        const response = await fetch("/api/generate-maze");
        mazeData = await response.json();
        
        inventoryCount = 0;
        inventoryText.textContent = inventoryCount;
        totalKeysText.textContent = mazeData.total_keys;
        updateProgress();
        
        calculateCellSize();
        drawMaze();
        statusText.textContent = "✨ 游戏开始！使用 WASD 移动 ✨";
    } catch (error) {
        statusText.textContent = "❌ 生成失败：" + error.message;
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
            const refreshResp = await fetch("/api/generate-maze");
            mazeData = await refreshResp.json();
            inventoryCount = 0;
            inventoryText.textContent = inventoryCount;
            totalKeysText.textContent = mazeData.total_keys;
            updateProgress();
            calculateCellSize();
            drawMaze();
            statusText.textContent = "🔄 游戏已重置！";
        }
    } catch (error) {
        statusText.textContent = "重置失败：" + error.message;
    }
}

// 更新进度条
function updateProgress() {
    if (mazeData && mazeData.total_keys > 0) {
        const percent = Math.round((inventoryCount / mazeData.total_keys) * 100);
        progressFill.style.width = `${percent}%`;
        progressText.textContent = `${percent}%`;
    } else {
        progressFill.style.width = "0%";
        progressText.textContent = "0%";
    }
}

// 计算单元格大小（自适应屏幕）
function calculateCellSize() {
    if (!mazeData) return;
    
    const container = document.getElementById('maze-wrapper');
    const containerWidth = container.clientWidth - 20;  // 留边距
    const containerHeight = container.clientHeight - 20;
    
    const mazeWidth = mazeData.width;
    const mazeHeight = mazeData.height;
    
    // 计算最佳单元格大小
    const sizeByWidth = Math.floor(containerWidth / mazeWidth);
    const sizeByHeight = Math.floor(containerHeight / mazeHeight);
    
    cellSize = Math.min(sizeByWidth, sizeByHeight, 45); // 最大45px，最小20px
    cellSize = Math.max(cellSize, 20);
    
    // 设置canvas大小
    canvas.width = mazeWidth * cellSize;
    canvas.height = mazeHeight * cellSize;
    
    // 设置canvas样式
    canvas.style.width = `${canvas.width}px`;
    canvas.style.height = `${canvas.height}px`;
}

// 绘制迷宫（Canvas渲染）
function drawMaze() {
    if (!mazeData || !ctx) return;
    
    const grid = mazeData.grid;
    const playerX = mazeData.player_x;
    const playerY = mazeData.player_y;
    
    for (let y = 0; y < grid.length; y++) {
        for (let x = 0; x < grid[0].length; x++) {
            const cellX = x * cellSize;
            const cellY = y * cellSize;
            const cell = grid[y][x];
            
            // 绘制背景
            if (cell === '#') {
                ctx.fillStyle = '#2c3e50';
                ctx.fillRect(cellX, cellY, cellSize - 1, cellSize - 1);
                ctx.fillStyle = '#1a1a2e';
                ctx.fillRect(cellX + 2, cellY + 2, cellSize - 5, cellSize - 5);
            } else if (cell === '.') {
                ctx.fillStyle = '#2d4a6e';
                ctx.fillRect(cellX, cellY, cellSize - 1, cellSize - 1);
                ctx.fillStyle = '#3d5a7e';
                ctx.fillRect(cellX + 1, cellY + 1, cellSize - 3, cellSize - 3);
            } else {
                ctx.fillStyle = '#2d4a6e';
                ctx.fillRect(cellX, cellY, cellSize - 1, cellSize - 1);
            }
            
            // 绘制边框
            ctx.strokeStyle = 'rgba(0,0,0,0.2)';
            ctx.strokeRect(cellX, cellY, cellSize, cellSize);
            
            // 绘制物品
            if (x === playerX && y === playerY) {
                // 绘制玩家
                ctx.font = `${Math.floor(cellSize * 0.6)}px "Segoe UI Emoji"`;
                ctx.fillStyle = 'white';
                ctx.shadowBlur = 5;
                ctx.shadowColor = '#e74c3c';
                ctx.fillText("🐱", cellX + cellSize * 0.25, cellY + cellSize * 0.75);
                ctx.shadowBlur = 0;
            } else if (cell === '🔑') {
                ctx.font = `${Math.floor(cellSize * 0.55)}px "Segoe UI Emoji"`;
                ctx.fillStyle = '#f1c40f';
                ctx.fillText("🔑", cellX + cellSize * 0.25, cellY + cellSize * 0.75);
            } else if (cell === '🚩') {
                ctx.font = `${Math.floor(cellSize * 0.55)}px "Segoe UI Emoji"`;
                ctx.fillStyle = '#27ae60';
                ctx.fillText("🚩", cellX + cellSize * 0.25, cellY + cellSize * 0.75);
            } else if (cell === '#') {
                ctx.font = `${Math.floor(cellSize * 0.5)}px "Segoe UI"`;
                ctx.fillStyle = '#34495e';
                ctx.fillText("█", cellX + cellSize * 0.25, cellY + cellSize * 0.75);
            }
        }
    }
}

// 处理移动
async function handleKeyPress(e) {
    if (!mazeData) {
        statusText.textContent = "🔔 请先点击「新游戏」！";
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
            mazeData.player_x = result.player_x;
            mazeData.player_y = result.player_y;

            if (result.cell === "🔑") {
                mazeData.grid[result.player_y][result.player_x] = ".";
                inventoryCount = result.keys_collected;
                inventoryText.textContent = inventoryCount;
                updateProgress();
                statusText.textContent = result.message || "🔑 拾取到钥匙！";
            } else if (result.cell === "🚩") {
                statusText.textContent = result.message;
                if (result.victory) {
                    statusText.innerHTML = "🎉🎉🎉 胜利！通关成功！ 🎉🎉🎉";
                }
            } else {
                statusText.textContent = result.message || "🐱 移动成功";
            }
            
            drawMaze();
        } else {
            statusText.textContent = result.message || "🚫 无法移动！";
        }
    } catch (error) {
        statusText.textContent = "⚠️ 连接失败：" + error.message;
    }
}

// 窗口大小改变时重新计算
window.addEventListener('resize', () => {
    if (mazeData) {
        calculateCellSize();
        drawMaze();
    }
});

// 页面加载时自动生成迷宫
generateNewMaze();