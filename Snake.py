from sys import exit
import random
import pygame


class SnakeBlock():
    def __init__(self, x, y, gameWindow, mapSize, blockSize, id):
        self.id = id
        self.size = 0
        self.x = x
        self.y = y
        self.gameWindow = gameWindow
        self.mapSize = mapSize
        self.blockSize = blockSize

    def move(self, dirx, diry):
        pass

    def draw(self):
        pygame.draw.rect(self.gameWindow, (255, 255, 255),
                         (self.x, self.y, self.blockSize, self.blockSize), 0)


class Snake():
    def __init__(self, x, y, gameWindow, mapSize, blockSize):
        self.gameWindow = gameWindow
        self.mapSize = mapSize
        self.blockSize = blockSize
        self.headX = x
        self.headY = y
        self.tailX = x
        self.tailY = y
        self.body = [SnakeBlock(self.headX, self.headY,
                                self.gameWindow, self.mapSize, self.blockSize, 1)]
        self.turns = []
        self.size = 1

    def move(self, dir, foodX, foodY):
        eat = False
        if dir == "none":
            return
        if dir == "up":
            self.headY = self.headY - self.blockSize
        if dir == "down":
            self.headY = self.headY + self.blockSize
        if dir == "right":
            self.headX = self.headX + self.blockSize
        if dir == "left":
            self.headX = self.headX - self.blockSize
        if self.headX == foodX and self.headY == foodY:
            self.body.append(SnakeBlock(self.body[self.size-1].x, self.body[self.size-1].y,
                                        self.gameWindow, self.mapSize, self.blockSize, self.size+1))
            self.size += 1

            eat = True
        for i in reversed(range(self.size)):
            if i == 0:
                self.body[0].x = self.headX
                self.body[0].y = self.headY
            else:
                self.body[i].x = self.body[i-1].x
                self.body[i].y = self.body[i-1].y
        return eat

    def draw(self):
        for block in self.body:
            block.draw()

    def collide(self):
        collideFlag = False
        if self.headX < 0 or self.headX >= self.mapSize[0]*self.blockSize or \
                self.headY < 0 or self.headY >= self.mapSize[1]*self.blockSize:
            collideFlag = True

        for block1 in self.body:
            for block2 in self.body:
                if block1.id != block2.id:
                    if block1.x == block2.x and block1.y == block2.y:
                        collideFlag = True
        return collideFlag

    def getSnakePlaces(self):
        places = [[], []]
        for block in self.body:
            places[0].append(block.x)
            places[1].append(block.y)
        return places


class Food():
    def __init__(self, gameWindow, mapSize, blockSize):
        self.gameWindow = gameWindow
        self.mapSize = mapSize
        self.blockSize = blockSize
        self.x = 0
        self.y = 0

    def draw(self):
        pygame.draw.rect(self.gameWindow, (255, 0, 0),
                         (self.x, self.y, self.blockSize, self.blockSize), 0)

    def new(self, takenPlaces):
        self.x = random.randint(0, self.mapSize[0]-1)*self.blockSize
        self.y = random.randint(0, self.mapSize[1]-1)*self.blockSize
        while self.x in takenPlaces[0] and self.y in takenPlaces[1]:
            self.x = random.randint(0, self.mapSize[0]-1)*self.blockSize
            self.y = random.randint(0, self.mapSize[1]-1)*self.blockSize


class Map():
    def __init__(self, gameWindow, mapSize, blockSize):
        self.gameWindow = gameWindow
        self.mapSize = mapSize
        self.blockSize = blockSize
        self.food = Food(self.gameWindow, self.mapSize, self.blockSize)
        self.food.new([[], []])

    def draw(self):
        # draw grid
        self.gameWindow.fill((0, 0, 0))
        x = 0
        y = 0

        for i in range(self.mapSize[0]):
            x = x + self.blockSize
            pygame.draw.line(self.gameWindow, (255, 255, 255),
                             (x, 0), (x, self.blockSize*self.mapSize[1]))

        for i in range(self.mapSize[1]):
            y = y + self.blockSize
            pygame.draw.line(self.gameWindow, (255, 255, 255),
                             (0, y), (self.blockSize*self.mapSize[0], y))
        # draw food
        self.food.draw()

    def newFood(self, takenPlaces):
        self.food.new(takenPlaces)


def main():
    # parameters:
    blockSize = 30
    mapSize = (30, 30)
    foodEaten = False

    # game variables
    gameWindow = pygame.display.set_mode(
        (mapSize[0]*blockSize, mapSize[1]*blockSize))
    playFlag = True
    map = Map(gameWindow, mapSize, blockSize)
    snake = Snake((mapSize[0]/2)*blockSize, (mapSize[1]/2)
                  * blockSize, gameWindow, mapSize, blockSize)
    direction = "none"

    clock = pygame.time.Clock()
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
        clock.tick(10)
        foodEaten = snake.move(direction, map.food.x, map.food.y)
        if direction != "none" and foodEaten == False:
            if snake.collide() == True:
                playFlag = False
        if foodEaten:
            map.newFood(snake.getSnakePlaces())
            foodEaten = False
        map.draw()
        snake.draw()
        pygame.display.update()


if __name__ == "__main__":
    main()
