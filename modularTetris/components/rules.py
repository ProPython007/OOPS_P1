from collections import Counter
from tkinter import messagebox
import tkinter
import pygame

from .block import Shape
from .const import Constants


class Game():
    def timer(self):
        if self.create_new_game == True:
            self.current_shape = Shape(self.canvas)
            self.create_new_game = False
            pygame.mixer.music.load("8bit-music-for-game-68698.mp3")
            pygame.mixer.music.play(-1)

        if not self.current_shape.fall():
            lines = self.remove_complete_lines()
            if lines:
                self.score += 10 * self.level**2 * lines**2
                self.status_var.set("Level: %d, Score: %d" % (self.level, self.score))
                pygame.mixer.Channel(0).play(pygame.mixer.Sound('soundeffect.mp3'))
                pygame.mixer.Channel(1).play(pygame.mixer.Sound('8bit-music-for-game-68698.mp3'))
            self.current_shape = Shape(self.canvas) # rendering a new shape into the canvas

            if self.is_game_over(): 
                self.create_new_game = True
                self.game_over()

            self.counter += 1
            if self.counter == 5:
                self.level += 1
                self.speed -= 20
                self.counter = 0
                self.status_var.set("Level: %d, Score: %d" % (self.level, self.score))
        
        self.root.after(self.speed, self.timer)

    def handle_events(self, event):
        '''Handle all user events.'''
        if event.keysym == "Left": 
            self.current_shape.move(-1, 0)
            pygame.mixer.music.load("./assets/nor.mp3")
            pygame.mixer.music.play()
        if event.keysym == "Right": 
            self.current_shape.move(1, 0)
            pygame.mixer.music.load("./assets/nor.mp3")
            pygame.mixer.music.play()
        if event.keysym == "Down": 
            self.current_shape.move(0, 1)
            pygame.mixer.music.load("./assets/nor.mp3")
            pygame.mixer.music.play()
        if event.keysym == "Up": 
            self.current_shape.rotate()
            pygame.mixer.music.load("./assets/nor.mp3")
            pygame.mixer.music.play()
        # if event.keysym == "p": time.sleep(30)

    def is_game_over(self):
        for box in self.current_shape.boxes:
            if not self.current_shape.can_move_box(box, 0, 1):
                return True
        return False

    def remove_complete_lines(self):
        shape_boxes_coords = [self.canvas.coords(box)[3] for box in self.current_shape.boxes]
        # print(shape_boxes_coords)
        # for box in self.current_shape.boxes:
        #     print(self.canvas.coords(box))
        
        all_boxes = []
        all_boxes_raw = self.canvas.find_all()
        for b in all_boxes_raw:
            if self.canvas.coords(b)[2] <= Constants.WIDTH:
                all_boxes.append(b)
        all_boxes_coords = {k : v for k, v in zip(all_boxes, [self.canvas.coords(box)[3] for box in all_boxes])}
        # print(f'all box coords: {all_boxes_coords}')
        
        lines_to_check = set(shape_boxes_coords)
        # print(f'lines to check: {lines_to_check}')
        
        boxes_to_check = {k: v for k, v in all_boxes_coords.items() if v in [line for line in lines_to_check]}
        # print(f'boxes to check: {boxes_to_check}')
        
        counter = Counter()
        for box in boxes_to_check.values():
            counter[box] += 1

        # print([(k, v) for k, v in counter.items()])
        # print()
        
        complete_lines = [k for k, v in counter.items() if v == (Constants.WIDTH/Shape.BOX_SIZE)]
        # print('completed_lines:', complete_lines)
 
        if not complete_lines:
            return False

        for k, v in boxes_to_check.items():
            if v in complete_lines:
                self.canvas.delete(k)
                del all_boxes_coords[k]
        
        for (box, coords) in all_boxes_coords.items():
            for line in complete_lines:
                if coords < line:
                    self.canvas.move(box, 0, Shape.BOX_SIZE)
        
        pygame.mixer.music.load("./assets/succ.mp3")
        pygame.mixer.music.play()

        self.canvas.delete(self.h_line)
        # self.canvas.delete(self.b_line)
        # self.b_line = self.canvas.create_line(0, Constants.HEIGHT, Constants.WIDTH + 200, Constants.HEIGHT, fill='white')
        self.v_line = self.canvas.create_line(Constants.WIDTH + 1, 0, Constants.WIDTH + 1, Constants.HEIGHT, fill='white', width=2)
        self.h_line = self.canvas.create_line(0, 1, Constants.WIDTH + Constants.EXTENDED_WIDTH, 1, fill='white')
        
        return len(complete_lines)


    def game_over(self):
        messagebox.showinfo("Game Over", "You scored %d points." % self.score)
        self.canvas.delete(tkinter.ALL)
        self.level = 1
        self.score = 0
        self.counter = 0
        self.speed = 500
        self.status_var.set("Level: %d, Score: %d" % (self.level, self.score))
        self.v_line = self.canvas.create_line(Constants.WIDTH + 1, 0, Constants.WIDTH + 1, Constants.HEIGHT, fill='white', width=2)
        self.h_line = self.canvas.create_line(0, 1, Constants.WIDTH + Constants.EXTENDED_WIDTH, 1, fill='white')
        # self.b_line = self.canvas.create_line(0, Constants.HEIGHT, Constants.WIDTH + 200, Constants.HEIGHT, fill='white')
