import pygame._view
import pygame
import pgzrun
import sys
import warnings
import gameinput
import gamemaps
from pygame.locals import *
from random import randint
from datetime import datetime
pygame.init()


WIDTH = 600
HEIGHT = 660


player = Actor('pacman_o') 
SPEED = 3
player.score = 0


#центрирование окна
if not sys.warnoptions:
    warnings.simplefilter('ignore')
pygame.display.toggle_fullscreen()


def draw():
    '''
    draw()
    отрисовка графических элементов игры
    '''
    global pacDots, player
    screen.blit('header3', (70, 0))
    screen.blit('photo3', (0, 80))
    pacDotsLeft = 0
    for a in range(len(pacDots)):
        if pacDots[a].status == 0:
            pacDots[a].draw()
            pacDotsLeft += 1
        if pacDots[a].collidepoint((player.x, player.y)):
            if pacDots[a].status == 0:
                    player.score += 10
            pacDots[a].status = 1
    if pacDotsLeft == 0: player.status = 2
    drawGhosts()
    getPlayerImage()
    player.draw()
    gameinput.checkInputEsc()
    screen.draw.text(str(player.score) , topright=(590, 20), owidth=0.5, ocolor=(0,255,255), color=(0,0,255) , fontsize=60)
    if player.status == 1:
        screen.blit('window1', (100, 380))
        screen.draw.text('GAME OVER\nPress ESC to close' , center=(300, 440), owidth=0.5, ocolor=(153, 204, 255), color=(64,64,51) , fontsize=40)
    if player.status == 2:
        screen.blit('window1', (100, 380))
        screen.draw.text('YOU WIN!\nPress ESC to close' , center=(300, 440), owidth=0.5, ocolor=(176,14,84), color=(247,255,119) , fontsize=40)


def update():
    '''
    update()
    обновление и считывание карты, положения и движения призраков и игрока
    '''
    global player, moveGhostsFlag, ghosts#  global , которое позволяет изменять изнутри функции значение глобальной переменной
    if player.status == 0:
        if moveGhostsFlag == 4: moveGhosts()
        for g in range(len(ghosts)):
            if ghosts[g].collidepoint((player.x, player.y)):
                player.status = 1
                pass
        if player.inputActive:
            gameinput.checkInput(player)
            gamemaps.checkMovePoint(player)
            if player.movex or player.movey:
                inputLock()
                animate(player, pos=(player.x + player.movex, player.y + player.movey), duration=1/SPEED, tween='linear', on_finished=inputUnLock)


def init():
    '''
    init()
    определение стартового положения игрока;
    инициализация переменных;
    подключение музыкального сопровождения
    '''
    global player
    initDots()
    initGhosts()
    player.x = 290
    player.y = 570
    player.status = 0
    inputUnLock()
    music.play('pm12')
    music.set_volume(0.1)


def getPlayerImage():
    '''
    getPlayerImage()
    имитация движения игрока
    (смена изображений)
    '''
    global player
    dt = datetime.now()
    a = player.angle
    tc = dt.microsecond%(500000/SPEED)/(100000/SPEED)
    if tc > 2.5 and (player.movex != 0 or player.movey !=0):
        if a != 180:
            player.image = 'pacman_c'
        else:
            player.image = 'pacman_cr'
    else:
        if a != 180:
            player.image = 'pacman_o'
        else:
            player.image = 'pacman_or'
    player.angle = a


def drawGhosts():
    '''
    drawGhosts()
    отрисовка призрака
    '''
    for g in range(len(ghosts)):
        ghosts[g].image = 'ghost'+str(g+1)
        ghosts[g].draw()


def moveGhosts():
    '''
    moveGhosts()
    программирование движения призраков
    '''
    global moveGhostsFlag
    dmoves = [(1,0),(0,1),(-1,0),(0,-1)]
    moveGhostsFlag = 0
    for g in range(len(ghosts)):
        dirs = gamemaps.getPossibleDirection(ghosts[g])
        if ghostCollided(ghosts[g],g) and randint(0,3) == 0: ghosts[g].dir = 3
        if dirs[ghosts[g].dir] == 0 or randint(0,50) == 0:
            d = -1
            while d == -1:
                rd = randint(0,3)
                if dirs[rd] == 1:
                    d = rd
            ghosts[g].dir = d
        animate(ghosts[g], pos=(ghosts[g].x + dmoves[ghosts[g].dir][0]*20, ghosts[g].y + dmoves[ghosts[g].dir][1]*20), duration=1/SPEED, tween='linear', on_finished=flagMoveGhosts)


def flagMoveGhosts():
    '''
    flagMoveGhosts()
    счётчик для запуска движения призраков
    '''
    global moveGhostsFlag
    moveGhostsFlag += 1


def ghostCollided(ga,gn):
    '''
    ghostCollided(ga,gn)
    возвращает TRUE, если два объекта пересекаются
    '''
    for g in range(len(ghosts)):
        if ghosts[g].colliderect(ga) and g != gn:
            return True
    return False

    
def initDots():
    '''
    initDots()
    заполнение лабиринта точками;
    инициализация точек
    '''
    global pacDots
    pacDots = []
    a = x = 0
    while x < 30:
        y = 0
        while y < 29:
            if gamemaps.checkDotPoint(10+x*20, 10+y*20):
                pacDots.append(Actor('dot2',(10+x*20, 90+y*20)))
                pacDots[a].status = 0
                a += 1
            y += 1
        x += 1


def initGhosts():
    '''
    initGhosts()
    инициализация привидений
    '''
    global ghosts, moveGhostsFlag
    moveGhostsFlag = 4
    ghosts = []
    g = 0
    while g < 4:
        ghosts.append(Actor('ghost'+str(g+1),(270+(g*20), 370)))
        ghosts[g].dir = randint(0, 3)
        g += 1


def inputLock():
    '''
    inputLock()
    управление движением(остановка)
    '''
    global player
    player.inputActive = False


def inputUnLock():
    '''
    inputUnLock()
    управление движением(продолжение движения)
    '''
    global player
    player.movex = player.movey = 0
    player.inputActive = True


def crist_exit():
    '''
    crist_exit()
    выход из программы при нажатии кнопки, закрывающей окно
    '''
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()


init()
pgzrun.go()
'''
from cx_Freeze import Executable, setup

# Список всех файлов и папок вашего проекта, за исключением исполняемого, 
# находящихся в корневой папке
include_files = ['pacmandotmap.png', 'pacmanmovemap.png', 'gameinput.py', 'gamemaps.py', 'C:\\Users\\dns\\Desktop\\Проект\\pacman истинный\\images', 'C:\\Users\\dns\\Desktop\\Проект\\pacman истинный\\music']  # file or directory

options = {
'build_exe': {
    'include_msvcr': True,
    'build_exe': 'name_exe',
    'include_files': include_files,
    }
}

# Задаем исполняемый файл и свою иконку.
executables = [
    Executable("pacman1.py", icon='game.ico'),
]

setup(
    name="game",
    version="1.0",
    description="Game",
    executables=executables,
    options=options,
)




import cx_Freeze
import os
os.environ['TCL_LIBRARY'] = "C:\\Users\\dns\\AppData\\Local\\Programs\\Python\\Python38\\tcltcl8.6"
os.environ['TK_LIBRARY'] = "C:\\Users\\dns\\AppData\\Local\\Programs\\Python\\Python38\\tcltk8.6"
executables = [cx_Freeze.Executable("pacman1.py")]

cx_Freeze.setup(
    name="Pac-man",
    options={"build_exe":{"packages":["pygame"], "include_files":['pacmandotmap.png', 'pacmanmovemap.png','dot2.jpg', 'ghost1.png', 'ghost2.png', 'ghost3.png', 'ghost4.png', 'header3.jpg', 'pacman_c.png', 'pacman_cr.png', 'pacman_o.png', 'pacman_or.png', 'photo3.jpg', 'pm12.mp3', 'window1.jpg',  'gameinput.py', 'gamemaps.py']}},

    description = "Pacman Game made in python with pygame.",
    executables = executables
    )
'''
input()

