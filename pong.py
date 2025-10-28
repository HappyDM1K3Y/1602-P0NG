import time
import threading
from OmegaExpansion import oledExp
from onionGpio import GPIO

# GPIO pin setup
PLAYER1_BTN = 0  # Replace with actual GPIO pin
PLAYER2_BTN = 1  # Replace with actual GPIO pin

# LCD setup
oledExp.driverInit()
oledExp.clear()

# Game state
paddle_pos = [0, 0]  # Top line, bottom line
ball_pos = 0
ball_dir = 1  # 1 = down, -1 = up
score = [0, 0]
running = True

# Button setup
btn1 = GPIO(PLAYER1_BTN)
btn2 = GPIO(PLAYER2_BTN)
btn1.setInputDirection()
btn2.setInputDirection()

def draw_screen():
    oledExp.clear()
    # Draw paddles
    line1 = [' '] * 16
    line2 = [' '] * 16
    line1[paddle_pos[0]] = '|'
    line2[paddle_pos[1]] = '|'
    # Draw ball
    if ball_pos == 0:
        line1[8] = '.'
    else:
        line2[8] = '.'
    import os
os.system("oled-exp -s 'Team 1 {}' -l 0".format(score[0]))
os.system("oled-exp -s 'Team 2 {}' -l 1".format(score[1]))

def check_collision():
    if ball_pos == 0 and paddle_pos[0] == 8:
        return True
    if ball_pos == 1 and paddle_pos[1] == 8:
        return True
    return False

def show_score():
    oledExp.clear()
    oledExp.setText('Team 1 {}'.format(score[0]), 0)
    oledExp.setText('Team 2 {}'.format(score[1]), 1)
    time.sleep(2)

def game_loop():
    global ball_pos, ball_dir, running
    while running:
        draw_screen()
        time.sleep(0.5)
        ball_pos += ball_dir
        if ball_pos > 1:
            ball_pos = 1
            ball_dir = -1
        elif ball_pos < 0:
            ball_pos = 0
            ball_dir = 1
        if not check_collision():
            if ball_pos == 0:
                score[1] += 1
            else:
                score[0] += 1
            show_score()
            paddle_pos[0] = 0
            paddle_pos[1] = 0
            ball_pos = 0
            ball_dir = 1

def input_loop():
    global paddle_pos
    while running:
        if btn1.getValue() == 0:
            paddle_pos[0] = (paddle_pos[0] + 1) % 16
        if btn2.getValue() == 0:
            paddle_pos[1] = (paddle_pos[1] + 1) % 16
        time.sleep(0.1)

# Start threads
threading.Thread(target=game_loop).start()
threading.Thread(target=input_loop).start()
