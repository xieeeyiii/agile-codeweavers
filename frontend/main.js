// 主界面逻辑
document.addEventListener('DOMContentLoaded', () => {
    // 开始游戏按钮
    const startBtn = document.getElementById('start-game-btn');
    if (startBtn) {
        startBtn.addEventListener('click', () => {
            window.location.href = 'game.html';
        });
    }

    // 游戏说明弹窗
    const howtoBtn = document.getElementById('how-to-play-btn');
    const howtoModal = document.getElementById('howto-modal');
    const aboutBtn = document.getElementById('about-btn');
    const aboutModal = document.getElementById('about-modal');
    const closeBtns = document.querySelectorAll('.modal-close');

    if (howtoBtn) {
        howtoBtn.addEventListener('click', () => {
            howtoModal.classList.add('show');
        });
    }

    if (aboutBtn) {
        aboutBtn.addEventListener('click', () => {
            aboutModal.classList.add('show');
        });
    }

    // 关闭弹窗
    closeBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            howtoModal.classList.remove('show');
            aboutModal.classList.remove('show');
        });
    });

    // 点击弹窗背景关闭
    window.addEventListener('click', (e) => {
        if (e.target.classList.contains('modal')) {
            e.target.classList.remove('show');
        }
    });
});