import pygame as pg
import random,math
import tkinter as tk
from tkinter import simpledialog



colors = {
    "on": (243,231,211),
    "off": (0,0,0),
    "background": (92, 64, 51)
    }



class Cell:
    def __init__(self,x,y):
        self.x,self.y = x,y
        self.enabled = False
        self.rect = pg.Rect(0.1*tilesize+self.x*tilesize*1.1,0.1*tilesize+self.y*tilesize*1.1,tilesize,tilesize)

 
    def switch(self):
        self.enabled = not self.enabled


    def toggle(self,board):
        self.switch()
        if self.y != 0:
            board.cells[self.y-1][self.x].switch()
        if self.y != board.h-1:
            board.cells[self.y+1][self.x].switch()
        if self.x != 0:        
            board.cells[self.y][self.x-1].switch()
        if self.x != board.w-1:
            board.cells[self.y][self.x+1].switch()
        

    def draw_self(self,display):
        if self.enabled:
            clr = colors["on"]
        else:
            clr = colors["off"]
            
        pg.draw.rect(display,clr,self.rect)




class Board:
    def __init__(self,w,h):
        self.w,self.h = w,h
        self.cells = [[Cell(x,y) for x in range(w)] for y in range(h)]



    def randomize(self,iterations):
        out = []
        for row in self.cells:
            for cell in row:
                cell.switch()
        for i in range(iterations):
            x,y = random.randint(0,self.w-1),random.randint(0,self.h-1)
            self.cells[y][x].toggle(self)
            out.append((x,y))
        return out



    def draw_self(self,display):
        display.fill(colors["background"])
        for row in self.cells:
            for cell in row:
                cell.draw_self(display)


    def detect_click(self,mousepos):
        global moves
        for row in self.cells:
            for cell in row:
                if cell.rect.collidepoint(mousepos):
                    cell.toggle(self)
                    moves.append((cell.x,cell.y))

    def detect_win(self):
        for row in self.cells:
            for cell in row:
                if not cell.enabled:
                    return False
        return True
                    



def main(w,h,itrs):
    pg.init()
    global tilesize,moves
    tilesize = (pg.display.Info().current_h/h)*0.8
    board = Board(w,h)
    moves = board.randomize(itrs)
    displaysize = (0.1*tilesize+w*(tilesize*1.1),0.1*tilesize+h*(tilesize*1.1))
    display = pg.display.set_mode(displaysize)
    won = False
    autoplay = False
    dead = False
    while not dead:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                dead = True
                continue
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_q:
                    dead = True
                    continue
                if event.key == pg.K_g:
                    autoplay = not autoplay

                if event.key == pg.K_ESCAPE:
                    dead = True
                    won = "GET ME OUT GET ME OUT GET ME OUT GET ME OUT GET ME OUT GET ME OUT GET ME OUT GET ME OUT "
                    continue

            elif event.type == pg.MOUSEBUTTONDOWN:
                if pg.mouse.get_pressed(3)[0] and not autoplay:
                    mousepos = pg.mouse.get_pos()
                    board.detect_click(mousepos)
                    won = board.detect_win()
                    break
                
                elif autoplay:
                    x,y = moves.pop()
                    board.cells[y][x].toggle(board)
                    won = board.detect_win()
                    break


                    



        board.draw_self(display)       
        pg.display.flip()


        if won:
            dead = True
            break
    pg.quit()
    return won


def startup(): # chad chattus gippitus
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    # Ask for board width
    board_width = simpledialog.askinteger("Input", "Enter board width:", minvalue=1)

    # Ask for board height
    board_height = simpledialog.askinteger("Input", "Enter board height:", minvalue=1)

    # Ask for iteration count
    iteration_count = simpledialog.askinteger("Input", "Enter iteration count:", minvalue=1)

    # Ask for number of games
    num_games = simpledialog.askinteger("Input", "Enter the number of games:", minvalue=1)

    root.destroy()  # Close the Tkinter window

    return board_width, board_height, iteration_count, num_games




def run_games():
    board_width, board_height, iteration_count, num_games = startup()

    for _ in range(num_games):
        won = main(board_width, board_height, iteration_count)
        if won:
            if type(won) != bool:
                break
            else:
                print("Congratulations, you win!")
        else:
            print("Sorry, you didn't win this time.")



run_games()




























