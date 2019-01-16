from flappybird import FlappyBird
import random

game = FlappyBird()
counter = 0
while True:
    counter = counter + 1
    action = None
    if counter % 30 == 0:
        action = random.sample(['True', 'False'], k = 1)[0]
    game.run_frame(action=action)