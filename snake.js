const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

// Load images for snake and food (mouse)
const snakeImg = new Image();
snakeImg.src = 'snake_resized.gif';

const foodImg = new Image();
foodImg.src = 'mouse_resized.gif';

// Ensure images are loaded before starting the game loop
let imagesLoaded = 0;

snakeImg.onload = () => {
    imagesLoaded++;
    checkImagesLoaded();
};

foodImg.onload = () => {
    imagesLoaded++;
    checkImagesLoaded();
};

function checkImagesLoaded() {
    if (imagesLoaded === 2) {
        gameLoop(); // Start the game loop after images are loaded
    }
}

let snake = [{ x: 300, y: 300 }];
let food = randomFoodPosition();
let direction = { x: 0, y: 0 };
let score = 0;
const gridSize = 20;
let gameSpeed = 100;

// Control snake direction with arrow keys
document.addEventListener("keydown", (event) => {
    if (event.code === "ArrowUp" && direction.y === 0) {
        direction = { x: 0, y: -gridSize };
    } else if (event.code === "ArrowDown" && direction.y === 0) {
        direction = { x: 0, y: gridSize };
    } else if (event.code === "ArrowLeft" && direction.x === 0) {
        direction = { x: -gridSize, y: 0 };
    } else if (event.code === "ArrowRight" && direction.x === 0) {
        direction = { x: gridSize, y: 0 };
    }
});

// Random food position function aligned to grid
function randomFoodPosition() {
    return {
        x: Math.floor(Math.random() * (canvas.width / gridSize)) * gridSize,
        y: Math.floor(Math.random() * (canvas.height / gridSize)) * gridSize
    };
}

// Game loop function
function gameLoop() {
    const newHead = { x: snake[0].x + direction.x, y: snake[0].y + direction.y };

    // Check collision with walls or self
    if (newHead.x < 0 || newHead.y < 0 || newHead.x >= canvas.width || newHead.y >= canvas.height || snake.some(part => part.x === newHead.x && part.y === newHead.y)) {
        alert("Game Over! Your score: " + score);
        snake = [{ x: 300, y: 300 }];
        direction = { x: 0, y: 0 };
        score = 0;
        gameSpeed = 100;
        food = randomFoodPosition();
        return;
    }

    // Check collision with food
    if (newHead.x === food.x && newHead.y === food.y) {
        score += 10;
        gameSpeed = Math.max(50, gameSpeed - 5); // Increase speed with each food eaten
        food = randomFoodPosition();
    } else {
        snake.pop(); // Remove last segment if no food is eaten
    }

    snake.unshift(newHead); // Add the new head to the snake

    // Draw everything
    ctx.clearRect(0, 0, canvas.width, canvas.height); // Clear the canvas

    // Draw food
    ctx.drawImage(foodImg, food.x, food.y, gridSize, gridSize);

    // Draw snake
    snake.forEach(part => ctx.drawImage(snakeImg, part.x, part.y, gridSize, gridSize));

    setTimeout(gameLoop, gameSpeed); // Continue the game loop with updated speed
}