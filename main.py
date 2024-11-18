import sys                              # Filehasznalathoz (texturak, zene, stb..)
import asyncio                          # Pybaghez      (hogy mehessen webre (webassemblywel))
import pygame                           # Mindenhez
from config import *                    # Ebbe szerveztem ki az alap beallitasokat (Pl.: palyameretet)
from minesweeper_components import *    # Ebbe meg szinte a teljes kodot, mert kulonben 300+ sor lenne a mainben a fo fuggvenyhivas elotti definiciokkal

pygame.mixer.init()
pygame.mixer.music.load("background_music.mp3")
pygame.mixer.music.play(-1)                     # Loopon fut, meg a fo jatek ujraindulasatol is fuggetlenul

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('MineSweeper')


async def main():           # A komponenseit a "minesweeper_components" reszletezgetem (vagy ott se)
    initialize_game()

    running = True
    while running:
        running = handle_events()

#       screen.fill(WHITE)          #mar nem is tudom, hogy miert raktam bele, de biztos jo volt valamire

        update_elapsed_time()
        draw_header()
        draw_field()

        pygame.display.flip()
        await asyncio.sleep(0)

    pygame.mixer.music.stop()       # Csak ha mar nem fut -az etikett megkoveteli-
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    asyncio.run(main())
