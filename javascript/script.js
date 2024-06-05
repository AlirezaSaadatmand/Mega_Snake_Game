const canvas = document.querySelector("canvas");
const ctx = canvas.getContext("2d");

const width = 1200;
const height = 600;

canvas.width = width;
canvas.height = height;

const UNIT = 15;

let snakeList = [];

let foodCount = 10;

let foodList = [];

class Snake {
    constructor(x, y, up, down, left, right, color) {

        this.parts = [
            { x: x + UNIT * 3, y: y },
            { x: x + UNIT * 2, y: y },
            { x: x + UNIT, y: y },
            { x: x, y: x }
        ];

        this.goingUp = false;
        this.goingDown = false;
        this.goingRight = true;
        this.goingLeft = false;

        this.move = {
            UP: up,
            DOWN: down,
            RIGHT: right,
            LEFT: left
        }

        this.color = color;
    }

    update(state) {
        let head = this.parts[0];
        if (!state) {
            this.parts.pop();
        }
        if (this.goingUp) {
            if (head.y - UNIT < 0) {
                this.parts.unshift({ x: head.x, y: height })
            } else {
                this.parts.unshift({ x: head.x, y: head.y - UNIT });
            }
        } else if (this.goingDown) {
            if (head.y + UNIT > height) {
                this.parts.unshift({ x: head.x, y: 0 });
            } else {
                this.parts.unshift({ x: head.x, y: head.y + UNIT });
            }
        } else if (this.goingRight) {
            if (head.x + UNIT > width) {
                this.parts.unshift({ x: 0, y: head.y });
            } else {
                this.parts.unshift({ x: head.x + UNIT, y: head.y });
            }
        } else if (this.goingLeft) {
            if (head.x - UNIT < 0) {
                this.parts.unshift({ x: width, y: head.y });

            } else {
                this.parts.unshift({ x: head.x - UNIT, y: head.y });
            }
        }
    }

    draw() {
        this.parts.forEach((part) => {
            if (part == this.parts[0]) {
                ctx.fillStyle = "black";
            } else {
                ctx.fillStyle = this.color;
            }
            ctx.fillRect(part.x, part.y, UNIT, UNIT);
            ctx.strokeRect(part.x, part.y, UNIT, UNIT);
        })
    }
}

snakeList.push(new Snake(150, 90, "ArrowUp", "ArrowDown", "ArrowLeft", "ArrowRight", "green"));
snakeList.push(new Snake(150, 180, "w", "s", "a", "d", "red"));
snakeList.push(new Snake(150, 360, "t", "g", "f", "h", "blue"));
snakeList.push(new Snake(150, 540, "o", "l", "k", ";", "yellow"));

class Food {
    constructor(x, y) {
        this.x = x;
        this.y = y;
    }

    draw() {
        ctx.fillStyle = "brown";
        ctx.fillRect(this.x, this.y, UNIT, UNIT);
        ctx.strokeRect(this.x, this.y, UNIT, UNIT);
    }
}

function random() {
    let xUnit = width / UNIT;
    let yUnit = height / UNIT;
    x = (Math.round(Math.random() * xUnit)) * UNIT;
    y = (Math.round(Math.random() * yUnit)) * UNIT;
    snakeList.forEach((snake) => {
        if (snake.parts[0].x == x && snake.parts[0].y == y) {
            random();
        }
    });
    return [x, y];
}

function check(snake) {
    let state = false;
    foodList.forEach((food) => {
        if (food.x == snake.parts[0].x && food.y == snake.parts[0].y) {
            foodList.splice(foodList.indexOf(food), 1);
            state = true;
        }
    });
    return state;
}

function draw() {
    ctx.fillStyle = "white";
    ctx.fillRect(0, 0, width, height);

    foodList.forEach((food) => {
        food.draw();
    });
    snakeList.forEach((snake) => {
        snake.update(check(snake));
        snake.draw();
    });
}

function main() {
    setInterval(() => {
        while (foodList.length <= foodCount) {
            foodList.push(new Food(...random()));
        }
        draw();
    }, 100);
}

main();

window.addEventListener("keydown", (event) => {
    snakeList.forEach((snake) => {
        if (Object.values(snake.move).includes(event.key)) {
            let index = Object.values(snake.move).indexOf(event.key)
            if (index == 0 && !snake.goingDown) {
                snake.goingRight = false;
                snake.goingLeft = false;
                snake.goingUp = true;
            } else if (index == 1 && !snake.goingUp) {
                snake.goingRight = false;
                snake.goingLeft = false;
                snake.goingDown = true;
            } else if (index == 2 && !snake.goingLeft) {
                snake.goingUp = false;
                snake.goingDown = false;
                snake.goingRight = true;
            } else if (index == 3 && !snake.goingRight) {
                snake.goingUp = false;
                snake.goingDown = false;
                snake.goingLeft = true;
            }
        }
    });
});