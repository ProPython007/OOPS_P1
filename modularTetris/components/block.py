from random import choice, randint
from .const import Constants


class Shape:
    '''Defines a tetris shape.'''
    BOX_SIZE = 30
    START_POINT = Constants.WIDTH / 2 / BOX_SIZE * BOX_SIZE - BOX_SIZE
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
                    point[0] * Shape.BOX_SIZE + Constants.WIDTH + 70,
                    point[1] * Shape.BOX_SIZE + Constants.HEIGHT//2 - 30,
                    point[0] * Shape.BOX_SIZE + Shape.BOX_SIZE + Constants.WIDTH + 70,
                    point[1] * Shape.BOX_SIZE + Shape.BOX_SIZE + Constants.HEIGHT//2 - 30,
                    fill=shape[0])
            elif shape[1] == 4:
                nbox = canvas.create_rectangle(
                    point[0] * Shape.BOX_SIZE + Constants.WIDTH + 40,
                    point[1] * Shape.BOX_SIZE + Constants.HEIGHT//2 - 30,
                    point[0] * Shape.BOX_SIZE + Shape.BOX_SIZE + Constants.WIDTH + 40,
                    point[1] * Shape.BOX_SIZE + Shape.BOX_SIZE + Constants.HEIGHT//2 - 30,
                    fill=shape[0])
            else:
                nbox = canvas.create_rectangle(
                    point[0] * Shape.BOX_SIZE + Constants.WIDTH + 55,
                    point[1] * Shape.BOX_SIZE + Constants.HEIGHT//2 - 30,
                    point[0] * Shape.BOX_SIZE + Shape.BOX_SIZE + Constants.WIDTH + 55,
                    point[1] * Shape.BOX_SIZE + Shape.BOX_SIZE + Constants.HEIGHT//2 - 30,
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
        if coords[3] + y > Constants.HEIGHT: return False
        if coords[0] + x < 0: return False
        if coords[2] + x > Constants.WIDTH: return False

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