###
''' REQUIREMENTS: 1. pip install pygame, 2. pip install customtkinter 3. (iff at linux: sudo apt install python3-tk) '''
###


from tkinter import Canvas, StringVar, messagebox
from customtkinter import CTkLabel, CTk
import tkinter
import pygame
# from playsound import playsound
# import time

from customtkinter import set_appearance_mode
from customtkinter import set_default_color_theme
set_appearance_mode("dark")
set_default_color_theme("blue")

from random import choice, randint
from collections import Counter


class Game():
    WIDTH = 420
    HEIGHT = 720
    EXTENDED_WIDTH = 200

    def start(self):
        self.level = 1
        self.score = 0
        self.speed = 500
        self.counter = 0
        self.create_new_game = True

        self.root = CTk()
        self.root.geometry('520x620')
        self.root.minsize(520, 620)
        self.root.maxsize(520, 620)
        # self.root.geometry(f'{Game.HEIGHT}x{Game.WIDTH+Game.EXTENDED_WIDTH}')
        self.root.title("Tetris")
        self.root.attributes('-alpha', 0.96)

        self.status_var = StringVar() 
        self.status_var.set("Level: 1, Score: 0")
        self.status = CTkLabel(self.root, textvariable=self.status_var, font=("Helvetica", 14, "bold"))
        self.status.pack()
        
        self.canvas = Canvas(self.root, width=Game.WIDTH + Game.EXTENDED_WIDTH, height=Game.HEIGHT)
        self.canvas.configure(bg='black')
        self.v_line = self.canvas.create_line(Game.WIDTH + 1, 0, Game.WIDTH + 1, Game.HEIGHT, fill='white', width=2)
        self.h_line = self.canvas.create_line(0, 1, Game.WIDTH + Game.EXTENDED_WIDTH, 1, fill='white')
        # self.b_line = self.canvas.create_line(0, Game.HEIGHT, Game.WIDTH + 200, Game.HEIGHT, fill='white')
        self.canvas.pack()

        pygame.mixer.init()

        self.root.bind("<Key>", self.handle_events)
        self.timer()
        self.root.mainloop()
    
    def timer(self):
        if self.create_new_game == True:
            self.current_shape = Shape(self.canvas)
            self.create_new_game = False

        if not self.current_shape.fall():
            lines = self.remove_complete_lines()
            if lines:
                self.score += 10 * self.level**2 * lines**2
                self.status_var.set("Level: %d, Score: %d" % (self.level, self.score))

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
            pygame.mixer.music.load("nor.mp3")
            pygame.mixer.music.play()
        if event.keysym == "Right": 
            self.current_shape.move(1, 0)
            pygame.mixer.music.load("nor.mp3")
            pygame.mixer.music.play()
        if event.keysym == "Down": 
            self.current_shape.move(0, 1)
            pygame.mixer.music.load("nor.mp3")
            pygame.mixer.music.play()
        if event.keysym == "Up": 
            self.current_shape.rotate()
            pygame.mixer.music.load("nor.mp3")
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
            if self.canvas.coords(b)[2] <= Game.WIDTH:
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
        
        complete_lines = [k for k, v in counter.items() if v == (Game.WIDTH/Shape.BOX_SIZE)]
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
        
        pygame.mixer.music.load("succ.mp3")
        pygame.mixer.music.play()

        self.canvas.delete(self.h_line)
        # self.canvas.delete(self.b_line)
        # self.b_line = self.canvas.create_line(0, Game.HEIGHT, Game.WIDTH + 200, Game.HEIGHT, fill='white')
        self.v_line = self.canvas.create_line(Game.WIDTH + 1, 0, Game.WIDTH + 1, Game.HEIGHT, fill='white', width=2)
        self.h_line = self.canvas.create_line(0, 1, Game.WIDTH + Game.EXTENDED_WIDTH, 1, fill='white')
        
        return len(complete_lines)


    def game_over(self):
        messagebox.showinfo("Game Over", "You scored %d points." % self.score)
        self.canvas.delete(tkinter.ALL)
        self.level = 1
        self.score = 0
        self.counter = 0
        self.speed = 500
        self.status_var.set("Level: %d, Score: %d" % (self.level, self.score))
        self.v_line = self.canvas.create_line(Game.WIDTH + 1, 0, Game.WIDTH + 1, Game.HEIGHT, fill='white', width=2)
        self.h_line = self.canvas.create_line(0, 1, Game.WIDTH + Game.EXTENDED_WIDTH, 1, fill='white')
        # self.b_line = self.canvas.create_line(0, Game.HEIGHT, Game.WIDTH + 200, Game.HEIGHT, fill='white')



class Shape:
    '''Defines a tetris shape.'''
    BOX_SIZE = 30
    START_POINT = Game.WIDTH / 2 / BOX_SIZE * BOX_SIZE - BOX_SIZE
    SHAPES = (
            ("yellow", 2, (0, 0), (1, 0), (0, 1), (1, 1)),     # square
            ("lightblue", 4, (0, 0), (1, 0), (2, 0), (3, 0)),  # line
            ("orange", 3, (2, 0), (0, 1), (1, 1), (2, 1)),     # right el
            ("blue", 3, (0, 0), (0, 1), (1, 1), (2, 1)),       # left el
            ("green", 3, (0, 1), (1, 1), (1, 0), (2, 0)),      # right wedge
            ("red", 3, (0, 0), (1, 0), (1, 1), (2, 1)),        # left wedge
            ("purple", 3, (1, 0), (0, 1), (1, 1), (2, 1)),     # symmetrical wedge
            )
    
    next_ch = None
    nextstruct = []

    def __init__(self, canvas):
        self.boxes = [] # the squares drawn by canvas.create_rectangle()
        
        if Shape.next_ch is None:
            self.shape = choice(Shape.SHAPES) # a random shape
            Shape.next_ch = randint(0, len(Shape.SHAPES) - 1)
        else:
            self.shape = Shape.SHAPES[Shape.next_ch]
            Shape.next_ch = randint(0, len(Shape.SHAPES) - 1)

        # print(f'cur shape: {self.shape}, next shape: {Shape.SHAPES[Shape.next_ch]}')
        self.draw_next(canvas, Shape.SHAPES[Shape.next_ch])

        # self.shape = choice(Shape.SHAPES) # a random shape
        self.color = self.shape[0]
        self.canvas = canvas

        for point in self.shape[2:]:
            box = canvas.create_rectangle(
                point[0] * Shape.BOX_SIZE + Shape.START_POINT,
                point[1] * Shape.BOX_SIZE,
                point[0] * Shape.BOX_SIZE + Shape.BOX_SIZE + Shape.START_POINT,
                point[1] * Shape.BOX_SIZE + Shape.BOX_SIZE,
                fill=self.color, outline='black')
            self.boxes.append(box)

    
    def draw_next(self, canvas, shape):
        if Shape.nextstruct:
            for item in Shape.nextstruct:
                canvas.delete(item)
            Shape.nextstruct = []

        for point in shape[2:]:
            if shape[1] == 2:
                nbox = canvas.create_rectangle(
                    point[0] * Shape.BOX_SIZE + Game.WIDTH + 70,
                    point[1] * Shape.BOX_SIZE + Game.HEIGHT//2 - 30,
                    point[0] * Shape.BOX_SIZE + Shape.BOX_SIZE + Game.WIDTH + 70,
                    point[1] * Shape.BOX_SIZE + Shape.BOX_SIZE + Game.HEIGHT//2 - 30,
                    fill=shape[0])
            elif shape[1] == 4:
                nbox = canvas.create_rectangle(
                    point[0] * Shape.BOX_SIZE + Game.WIDTH + 40,
                    point[1] * Shape.BOX_SIZE + Game.HEIGHT//2 - 30,
                    point[0] * Shape.BOX_SIZE + Shape.BOX_SIZE + Game.WIDTH + 40,
                    point[1] * Shape.BOX_SIZE + Shape.BOX_SIZE + Game.HEIGHT//2 - 30,
                    fill=shape[0])
            else:
                nbox = canvas.create_rectangle(
                    point[0] * Shape.BOX_SIZE + Game.WIDTH + 55,
                    point[1] * Shape.BOX_SIZE + Game.HEIGHT//2 - 30,
                    point[0] * Shape.BOX_SIZE + Shape.BOX_SIZE + Game.WIDTH + 55,
                    point[1] * Shape.BOX_SIZE + Shape.BOX_SIZE + Game.HEIGHT//2 - 30,
                    fill=shape[0])
                
            Shape.nextstruct.append(nbox)


    def move(self, x, y):
        '''Moves this shape (x, y) boxes.'''
        if not self.can_move_shape(x, y):          
            return False         
        else:
            for box in self.boxes: 
                self.canvas.move(box, x * Shape.BOX_SIZE, y * Shape.BOX_SIZE)
            return True

    def fall(self):
        '''Moves this shape one box-length down.'''
        if not self.can_move_shape(0, 1):
            return False
        else:
            for box in self.boxes:
                self.canvas.move(box, 0 * Shape.BOX_SIZE, 1 * Shape.BOX_SIZE)
            return True

    def rotate(self):
        '''Rotates the shape clockwise.'''
        boxes = self.boxes[:]
        pivot = boxes.pop(2)

        def get_move_coords(box):
            '''Return (x, y) boxes needed to rotate a box around the pivot.'''
            box_coords = self.canvas.coords(box)
            pivot_coords = self.canvas.coords(pivot)
            x_diff = box_coords[0] - pivot_coords[0]
            y_diff = box_coords[1] - pivot_coords[1]
            x_move = (- x_diff - y_diff) / self.BOX_SIZE
            y_move = (x_diff - y_diff) / self.BOX_SIZE
            return x_move, y_move

        # Check if shape can legally move
        for box in boxes:
            x_move, y_move = get_move_coords(box)
            if not self.can_move_box(box, x_move, y_move): 
                return False
            
        # Move shape
        for box in boxes:
            x_move, y_move = get_move_coords(box)
            self.canvas.move(box, x_move * self.BOX_SIZE, y_move * self.BOX_SIZE)

        return True

    def can_move_box(self, box, x, y):
        '''Check if box can move (x, y) boxes.'''
        x = x * Shape.BOX_SIZE
        y = y * Shape.BOX_SIZE
        coords = self.canvas.coords(box)
        
        # Returns False if moving the box would overrun the screen
        if coords[3] + y > Game.HEIGHT: return False
        if coords[0] + x < 0: return False
        if coords[2] + x > Game.WIDTH: return False

        # Returns False if moving box (x, y) would overlap another box
        overlap = set(self.canvas.find_overlapping(
                (coords[0] + coords[2]) / 2 + x, 
                (coords[1] + coords[3]) / 2 + y, 
                (coords[0] + coords[2]) / 2 + x,
                (coords[1] + coords[3]) / 2 + y
                ))
        other_items = set(self.canvas.find_all()) - set(self.boxes)
        if overlap & other_items: return False

        return True


    def can_move_shape(self, x, y):
        '''Check if the shape can move (x, y) boxes.'''
        for box in self.boxes:
            if not self.can_move_box(box, x, y): 
                return False
        return True

if __name__ == "__main__":
    game = Game()
    game.start()
