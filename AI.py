import numpy as np
import snake
import random
import pygame


def main():
    pygame.init()
    clock = pygame.time.Clock()
    white = (255, 255, 255)

    block_size = 40
    map_size = (8, 8)
    # [blocked_left, blocked_up, blocked_right, blocked_down, food_left, food_up, food_right, food_down]
    states = 2**4
    actions = 4
    Q = np.zeros((states, actions))
    lr = 0.4
    gamma = 0.4
    epsilon = 0.8
    epochs = 50000
    Qs = np.zeros((epochs, states, actions))
    play_flag = True

    for epoch in range(epochs):
        if epoch % 100 == 0:
            print(epoch)
            if epsilon > 0.05:
                epsilon = epsilon - 0.01

        game = snake.SnakeGame(map_size, block_size)
        state = game.get_state()

        state_num = get_state_num(state)
        while play_flag:
            if random.uniform(0, 1) < epsilon:
                action = random.randint(0, actions - 1)
            else:
                p = Q[state_num, :]
                action = np.argmax(p)

            end_game, reward = game.move(action_to_dir(action))
            new_state = game.get_state()
            new_state_num = get_state_num(new_state)
            # Q[state_num, action] = Q[state_num, action] + lr * \
            #     (reward + gamma *
            #      np.max(Q[new_state_num, np.argmax(Q[new_state_num, :])]) - Q[state_num, np.argmax(Q[state_num, :])])

            Q[state_num, action] = reward + \
                gamma * \
                np.max(Q[new_state_num, np.argmax(Q[new_state_num, :])])
            state = new_state
            state_num = new_state_num
            if epoch % 1000 == 0:

                print(state)
                game.show_text(
                    str(epoch), (10, 10))
                clock.tick(0.5)
                game.draw()
            if end_game:
                play_flag = False
        play_flag = True
        Qs[epoch, :, :] = np.copy(Q)
    pass


def action_to_dir(action):
    if action == 0:
        return "left"
    if action == 1:
        return "up"
    if action == 2:
        return "right"
    if action == 3:
        return "down"


def bin_to_dec(state):
    dec = 0
    for i, bit in enumerate(state):
        dec += 2**i * bit
    return dec


def get_state_num(state):
    state_num = bin_to_dec(state[8:12])
    state_num = state_num * np.where(state[0:8] == 1)[0][0]
    return state_num


if __name__ == "__main__":
    main()
