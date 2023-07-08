import numpy as np
import pygame as pg
import sys
import math

row_count = 6
col_count = 7

RED = (255,0,0)
YELLOW = (255,255,0)
BLACK = (0,0,0)
BLUE = (0,0,255)

def boards():
    board = np.zeros((row_count,col_count))
    return board

def drop_pieces(board,row,col,piece):
    board[row][col] = piece

def is_valid_location(board,col):
    return board[row_count-1][col] == 0

def get_next_row_open(board,col):
    for r in range(row_count):
        if board[r][col] == 0:
            return r

# def print_board(board):
#     print(np.flip(board,0))

def winning_board(board,piece):
    for c in range(col_count-3):
        for r in range(row_count):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True
    
    for c in range(col_count):
        for r in range(row_count-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True
            
    for c in range(col_count-3):
        for r in range(row_count-3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True
            
    for c in range(col_count-3):
        for r in range(3,row_count):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True

def draw_board(board):
    for c in range(col_count):
        for r in range(row_count):
            pg.draw.rect(screen, BLUE,(int(c*squaresize),int(r*squaresize+squaresize),int(squaresize),int(squaresize)))
            pg.draw.circle(screen, BLACK,(int(c*squaresize+squaresize/2),int(r*squaresize+squaresize+squaresize/2)),int(squaresize/2-5))
            
    for c in range(col_count):
        for r in range(row_count):
            if board[r][c] == 1:
                pg.draw.circle(screen, RED,(int(c*squaresize+squaresize/2),height-int(r*squaresize+squaresize/2)),int(squaresize/2-5))
            elif board[r][c] == 2:
                pg.draw.circle(screen, YELLOW,(int(c*squaresize+squaresize/2),height-int(r*squaresize+squaresize/2)),int(squaresize/2-5))

    pg.display.update()

board = boards()
# print_board(board)
game_over = False
turn = 0

pg.init()

squaresize = 100

width = col_count * squaresize
height = (row_count+1) * squaresize

size = (width, height)

screen = pg.display.set_mode(size)
draw_board(board)
myfont = pg.font.SysFont('monospace',75)
pg.display.update()

while not game_over:

    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()

        if event.type == pg.MOUSEMOTION:
            posx = event.pos[0]
            pg.draw.rect(screen, BLACK, (0,0,width,squaresize))
            if turn == 0:
                pg.draw.circle(screen, RED, (posx,squaresize/2),squaresize/2-5)
            elif turn == 1:
                pg.draw.circle(screen, YELLOW, (posx,squaresize/2),squaresize/2-5)
        pg.display.update()

        if event.type == pg.MOUSEBUTTONDOWN:
            pg.draw.rect(screen, BLACK, (0,0,width,squaresize))
            if turn == 0:
                posx = event.pos[0]
                col = math.floor(posx/squaresize)

                if is_valid_location(board, col):
                    row = get_next_row_open(board, col)
                    drop_pieces(board,row,col,1)

                    if winning_board(board, 1):
                        label = myfont.render("Player 1 Wins!",1,RED)
                        screen.blit(label, (40,10))
                        game_over = True

            else:
                posx = event.pos[0]
                col = math.floor(posx/squaresize)

                if is_valid_location(board, col):
                    row = get_next_row_open(board, col)
                    drop_pieces(board,row,col,2)

                    if winning_board(board, 2):
                        label = myfont.render("Player 2 Wins!",1,YELLOW)
                        screen.blit(label, (40,10))
                        game_over = True

            turn += 1
            turn = turn%2
            draw_board(board)
            if game_over:
                pg.time.wait(3000)
