from tkinter import Canvas, StringVar
from customtkinter import CTkLabel, CTk
import pygame

from customtkinter import set_default_color_theme
from customtkinter import set_appearance_mode
set_default_color_theme("blue")
set_appearance_mode("dark")

from .rules import Game
from .const import Constants


class UI(Game):
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
        # self.root.geometry(f'{Constants.HEIGHT}x{Constants.WIDTH+Constants.EXTENDED_WIDTH}')
        self.root.title("Tetris")
        self.root.attributes('-alpha', 0.96)

        self.status_var = StringVar() 
        self.status_var.set("Level: 1, Score: 0")
        self.status = CTkLabel(self.root, textvariable=self.status_var, font=("Helvetica", 14, "bold"))
        self.status.pack()
        
        self.canvas = Canvas(self.root, width=Constants.WIDTH + Constants.EXTENDED_WIDTH, height=Constants.HEIGHT)
        self.canvas.configure(bg='black')
        self.v_line = self.canvas.create_line(Constants.WIDTH + 1, 0, Constants.WIDTH + 1, Constants.HEIGHT, fill='white', width=2)
        self.h_line = self.canvas.create_line(0, 1, Constants.WIDTH + Constants.EXTENDED_WIDTH, 1, fill='white')
        # self.b_line = self.canvas.create_line(0, Constants.HEIGHT, Constants.WIDTH + 200, Constants.HEIGHT, fill='white')
        self.canvas.pack()

        pygame.mixer.init()

        self.root.bind("<Key>", self.handle_events)
        self.timer()
        self.root.mainloop()