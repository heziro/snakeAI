from sys import exit
import random
import pygame
import numpy as np


class SnakeBlock():
    def __init__(self, x, y, game_window, map_size, block_size, id):
        self.id = id
        self.size = 0
        self.x = x
        self.y = y
        self.game_window = game_window
        self.map_size = map_size
        self.block_size = block_size

    def draw(self):
        pygame.draw.rect(self.game_window, (255, 255, 255),
                         (self.x, self.y, self.block_size, self.block_size), 0)


class Snake():
    def __init__(self, game_window, x, y, map_size, block_size):
        self.game_window = game_window
        self.map_size = map_size
        self.block_size = block_size
        self.headX = x
        self.headY = y
        self.tailX = x
        self.tailY = y
        self.body = [SnakeBlock(self.headX, self.headY,
                                self.game_window, self.map_size, self.block_size, 1)]
        self.turns = []
        self.size = 1
        self.steps_between_foods = 0

    def move(self, dir, foodX, foodY):
        def food_dir(dir, foodX, foodY):
            if dir == 'up' and self.headY > foodY:
                return True
            if dir == 'down' and self.headY < foodY:
                return True
            if dir == 'left' and self.headX > foodX:
                return True
            if dir == 'right' and self.headX < foodX:
                return True
            return False
        self.steps_between_foods = self.steps_between_foods + 1
        eat = False
        snake_collide = False
        reward = 0
        if dir == "none":
            return (snake_collide, eat, reward)
        if dir == "up":
            self.headY = self.headY - self.block_size
        if dir == "down":
            self.headY = self.headY + self.block_size
        if dir == "right":
            self.headX = self.headX + self.block_size
        if dir == "left":
            self.headX = self.headX - self.block_size

        if self.headX == foodX and self.headY == foodY:
            self.body.append(SnakeBlock(self.body[self.size - 1].x, self.body[self.size - 1].y,
                                        self.game_window, self.map_size, self.block_size, self.size + 1))
            self.size += 1
            reward = 0.5
            eat = True
            self.steps_between_foods = 0
        else:
            if self.collide():
                snake_collide = True
                reward = -0.5
            else:
                if food_dir(dir, foodX, foodY):
                    reward = 0.1
                else:
                    pass
                    reward = -0.1

        for i in reversed(range(self.size)):
            if i == 0:
                self.body[0].x = self.headX
                self.body[0].y = self.headY
            else:
                self.body[i].x = self.body[i - 1].x
                self.body[i].y = self.body[i - 1].y
        return (snake_collide, eat, reward)

    def collide(self):
        collideFlag = False
        if self.headX < 0 or self.headX >= self.map_size[0] * self.block_size or \
                self.headY < 0 or self.headY >= self.map_size[1] * self.block_size:
            collideFlag = True

        for block1 in self.body:
            for block2 in self.body:
                if block1.id != block2.id:
                    if block1.x == block2.x and block1.y == block2.y:
                        collideFlag = True
        return collideFlag

    def draw(self):
        for block in self.body:
            block.draw()

    def getSnakePlaces(self):
        places = [[], []]
        for block in self.body:
            places[0].append(block.x)
            places[1].append(block.y)
        return places


class Food():
    def __init__(self, game_window, map_size, block_size):
        self.game_window = game_window
        self.map_size = map_size
        self.block_size = block_size
        self.x = 0
        self.y = 0

    def draw(self):
        pygame.draw.rect(self.game_window, (255, 0, 0),
                         (self.x, self.y, self.block_size, self.block_size), 0)

    def new(self, takenPlaces):
        self.x = random.randint(0, self.map_size[0] - 1) * self.block_size
        self.y = random.randint(0, self.map_size[1] - 1) * self.block_size
        while self.x in takenPlaces[0] and self.y in takenPlaces[1]:
            self.x = random.randint(0, self.map_size[0] - 1) * self.block_size
            self.y = random.randint(0, self.map_size[1] - 1) * self.block_size


class Map():
    def __init__(self, game_window, map_size, block_size):
        self.game_window = game_window
        self.map_size = map_size
        self.block_size = block_size
        self.food = Food(self.game_window, self.map_size, self.block_size)
        self.food.new([[], []])

    def draw(self):
        # draw grid

        x = 0
        y = 0

        for i in range(self.map_size[0]):
            x = x + self.block_size
            pygame.draw.line(self.game_window, (255, 255, 255),
                             (x, 0), (x, self.block_size * self.map_size[1]))

        for i in range(self.map_size[1]):
            y = y + self.block_size
            pygame.draw.line(self.game_window, (255, 255, 255),
                             (0, y), (self.block_size * self.map_size[0], y))
        # draw food
        self.food.draw()

    def newFood(self, takenPlaces):
        self.food.new(takenPlaces)


class SnakeGame():
    def __init__(self, map_size, block_size):
        self.block_size = block_size
        self.map_size = map_size
        self.width = map_size[0] * block_size
        self.height = map_size[0] * block_size
        self.score = 0
        self.state = np.zeros(12, dtype=int)

        pygame.init()
        self.game_window = pygame.display.set_mode(
            (self.width, self.height))

        self.board = Map(self.game_window, self.map_size, self.block_size)
        self.snake = Snake(self.game_window, self.width // 2,
                           self.height // 2, self.map_size, self.block_size)
        self.board.newFood(self.snake.getSnakePlaces())

        playFlag = True
        direction = "none"

    def move(self, dir):
        snake_collide, food_eaten, reward = self.snake.move(
            dir, self.board.food.x, self.board.food.y)

        if food_eaten:
            self.board.newFood(self.snake.getSnakePlaces())
            foodEaten = False
            self.score = self.score + 1

        # if collide
        if self.snake.steps_between_foods > 500:
            return (True, reward)
        return (snake_collide, reward)

    def draw_stats(self):
        x = self.width + 50
        y = (self.height // 4) * 3

        for i in range(3):
            x = x + self.block_size
            pygame.draw.line(self.game_window, (255, 255, 255),
                             (x, y), (x, y+self.block_size * 3))

        for i in range(4):
            y = y + self.block_size
            pygame.draw.line(self.game_window, (255, 255, 255),
                             (x - 4*self.block_size, y), (x, y))

    def draw(self):
        self.game_window.fill((0, 0, 0))
        # self.draw_stats()
        self.board.draw()
        self.snake.draw()
        pygame.display.update()
        pass

    def show_text(self, text, pos=(200, 200)):
        font = pygame.font.SysFont("comicsansms", 30)
        render = font.render("generation: " + text, True, (255, 255, 255))
        self.game_window.blit(render, pos)
        pygame.display.flip()

    def update_state(self):
        def blocked(pos):
            if pos[0] < 0 or pos[0] >= self.map_size[0] * self.block_size or \
                    pos[1] < 0 or pos[1] >= self.map_size[1] * self.block_size:
                return True
            for block in self.snake.body:
                if (block.x, block.y) == pos:
                    return True
            return False

        def head_new_pos(head_pos, dir):
            if dir == "up":
                return (head_pos[0], head_pos[1] - self.snake.block_size)
            if dir == "down":
                return (head_pos[0], head_pos[1] + self.snake.block_size)
            if dir == "right":
                return (head_pos[0] + self.snake.block_size, head_pos[1])
            if dir == "left":
                return (head_pos[0] - self.snake.block_size, head_pos[1])

        def get_food_state():
            food_state = np.zeros(4, dtype=int)

            if self.snake.headX > self.board.food.x:
                food_state[0] = 1
            if self.snake.headY > self.board.food.y:
                food_state[1] = 1
            if self.snake.headX < self.board.food.x:
                food_state[2] = 1
            if self.snake.headY < self.board.food.y:
                food_state[3] = 1

            # if self.snake.headX < self.board.food.x and self.snake.headY > self.board.food.y:
            #     food_state[0] = 1
            # if self.snake.headX == self.board.food.x and self.snake.headY > self.board.food.y:
            #     food_state[1] = 1
            # if self.snake.headX > self.board.food.x and self.snake.headY > self.board.food.y:
            #     food_state[2] = 1
            # if self.snake.headX < self.board.food.x and self.snake.headY == self.board.food.y:
            #     food_state[3] = 1
            # if self.snake.headX > self.board.food.x and self.snake.headY == self.board.food.y:
            #     food_state[4] = 1
            # if self.snake.headX < self.board.food.x and self.snake.headY < self.board.food.y:
            #     food_state[5] = 1
            # if self.snake.headX == self.board.food.x and self.snake.headY < self.board.food.y:
            #     food_state[6] = 1
            # if self.snake.headX > self.board.food.x and self.snake.headY < self.board.food.y:
            #     food_state[7] = 1
            return food_state

        def get_blocked_state():
            head_pos = (self.snake.headX, self.snake.headY)
            blocked_state = np.zeros(4, dtype=int)
            if blocked(head_new_pos(head_pos, "left")):
                blocked_state[0] = 1
            if blocked(head_new_pos(head_pos, "up")):
                blocked_state[1] = 1
            if blocked(head_new_pos(head_pos, "right")):
                blocked_state[2] = 1
            if blocked(head_new_pos(head_pos, "down")):
                blocked_state[3] = 1
            return blocked_state

        # food_pos = (self.board.food.x, self.board.food.y)
        # head_pos = (self.snake.headX, self.snake.headY)
        # neck_pos = (self.snake.body[-1].x, self.snake.body[-1].y)

        self.state = np.zeros(8, dtype=int)

        self.state[:4] = get_food_state()
        self.state[4:8] = get_blocked_state()

    def get_state(self):
        self.update_state()
        return self.state


def main():
    pygame.init()
    # parameters:
    block_size = 40
    map_size = (16, 16)
    playFlag = True
    direction = "none"
    clock = pygame.time.Clock()

    game = SnakeGame(map_size, block_size)

    while playFlag:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)
            keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            direction = "up"
        if keys[pygame.K_DOWN]:
            direction = "down"
        if keys[pygame.K_RIGHT]:
            direction = "right"
        if keys[pygame.K_LEFT]:
            direction = "left"
        snake_collide, reward = game.move(direction)
        if snake_collide:
            playFlag = False
        print(reward)
        game.draw()
        clock.tick(8)


if __name__ == "__main__":
    main()
