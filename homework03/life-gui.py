import argparse
import pygame
from pygame.locals import *

import life
from life import GameOfLife
from ui import UI


class GUI(UI):
    def __init__(self, life: GameOfLife, cell_size: int = 10, speed: int = 10) -> None:
        super().__init__(life)
        self.cell_size = cell_size
        self.speed = speed
        self.screen_size = self.life.cols * self.cell_size, self.life.rows * self.cell_size

        self.screen = pygame.display.set_mode(self.screen_size)

    def change_state(self, cell: life.Cell) -> None:
        cell_a = cell[0] // self.cell_size
        cell_b = cell[1] // self.cell_size
        if self.life.curr_generation[cell_a][cell_b]:
            self.life.curr_generation[cell_a][cell_b] = 0
        else:
            self.life.curr_generation[cell_a][cell_b] = 1

    def draw_lines(self) -> None:
        # Copy from previous assignment
        for x in range(0, self.screen_size[0], self.cell_size):
            pygame.draw.line(
                self.screen, pygame.Color("black"), (x, 0), (x, self.screen_size[1])
            )
        for y in range(0, self.screen_size[1], self.cell_size):
            pygame.draw.line(
                self.screen, pygame.Color("black"), (0, y), (self.screen_size[0], y)
            )

    def draw_grid(self) -> None:
        # Copy from previous assignment
        for l in range(self.life.rows):
            for k in range(self.life.cols):
                if self.life.curr_generation[l][k]:
                    pygame.draw.rect(
                        self.screen,
                        pygame.Color("green"),
                        (
                            k * self.cell_size,
                            l * self.cell_size,
                            self.cell_size,
                            self.cell_size,
                        ),
                    )
                else:
                    pygame.draw.rect(
                        self.screen,
                        pygame.Color("white"),
                        pygame.Rect(
                            k * self.cell_size,
                            l * self.cell_size,
                            self.cell_size,
                            self.cell_size,
                        ),
                    )

    def run(self) -> None:
        # Copy from previous assignment
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))
        running = True
        pause = False
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    (cell_y, cell_x) = pygame.mouse.get_pos()
                    self.change_state((cell_x, cell_y))
                    self.draw_grid()
                    self.draw_lines()
                    pygame.display.flip()
                    clock.tick(self.speed)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        pause = not pause
            if not pause:
                self.life.step()

            self.draw_grid()
            self.draw_lines()

            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()


def main():
    game = GameOfLife(size=(48, 64))
    app = GUI(game)
    app.run()


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Let's play the Game of Life", prog="gof-gui.py")
    parser.add_argument('--width', type=int, default=640, help='Enter width of window with game')
    parser.add_argument('--height', type=int, default=480, help='Enter height of window with game')
    parser.add_argument('--cell_size', type=int, default=20, help='Enter cell size')
    args = parser.parse_args()
    w = args.width > 0
    h = args.height > 0
    c = args.cell_size > 0

    if w and h and c and args.width // args.cell_size > 0 and args.height // args.cell_size > 0:
        gui = GUI(GameOfLife((args.width // args.cell_size, args.height // args.cell_size)), cell_size=args.cell_size)
        gui.run()
    else:
        print('The input received incorrect values. Tre again please')
        if not w:
            print ('Incorrect value of width')
        if not h:
            print ('Incorrect value of height')
        if not c:
            print ('Incorrect value of cell_size')
