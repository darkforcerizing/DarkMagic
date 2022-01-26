import pygame
import sys
import os
import random
import tkinter.messagebox
import sqlite3
from button import Button
from GameBoard import Board
from chip import Chip


class Game:
    def __init__(self):
        self.board = 0
        self.score = 0
        self.cauldron = 0
        self.state = ''
        self.level = 1

        self.QuitButton = 0
        self.PauseButton = 0

        self.scoreCoords = (250, 10)
        self.cauldronCoords = (10, 10)
        self.levelCoords = (10, 60)

        self.dbFile = 'db\\stats.db'
        self.dir = os.path.split(os.path.abspath(__file__))[0]

        pygame.init()
        self.screen = pygame.display.set_mode((600, 600))
        pygame.display.set_caption('Dark Magic')

        tkwindow = tkinter.Tk()
        tkwindow.withdraw()

        self.imageList = []
        self.chipNames = ('1.png', '2.png', '3.png', '4.png', '5.png', '6.png', '7.png', '8.png')
        self.chipColors = ((255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255),
                           (160, 192, 255), (255, 192, 160))
        self.loadImages()

        self.allsprites = ''

        self.soundFile = 'smb_pause.ogg'
        pygame.mixer.get_init()
        self.sound = self.loadSound(self.soundFile)

    def startScreen(self):
        intro_text = ["DARK MAGIC", "",
                      'Greetings from association of dark magicians',
                      'press any button to play']

        self.screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 30)
        text_coord = 50
        for line in intro_text:
            string_rendered = font.render(line, True, pygame.Color('red'))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 10
            text_coord += intro_rect.height
            self.screen.blit(string_rendered, intro_rect)
            pygame.display.flip()
        self.setState('start')
        while True:
            event = pygame.event.wait()
            if event.type == pygame.QUIT:
                self.terminate()
            if event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONUP:
                pygame.event.clear()
                self.setState('menu')
                return

    def drawMenuWindow(self):
        pygame.mouse.set_visible(True)
        self.screen.fill((0, 0, 0))
        screen2 = pygame.Surface(self.screen.get_size())
        screen2.fill((0, 0, 0))
        StartButton = Button((0, 255, 0), 150, 100, 250, 100, "Start")
        ScoreButton = Button((0, 0, 255), 150, 220, 250, 100, 'Score')
        QuitButton = Button((255, 0, 0), 150, 340, 250, 100, "Quit")
        StartButton.draw(screen2, (0, 0, 0))
        ScoreButton.draw(screen2, (0, 0, 0))
        QuitButton.draw(screen2, (0, 0, 0))

        clock = pygame.time.Clock()
        delta = 600
        delay = 60 * 600
        side = random.randint(0, 1)
        while True:
            clock.tick(delay)
            delta -= 1
            if delta < 0:
                break
            if side == 0:
                mov_x = 0
                mov_y = delta
            else:
                mov_x = delta
                mov_y = 0
            self.screen.blit(screen2, (mov_x, mov_y))
            pygame.display.update()

        self.setState("menu")
        while True:
            event = pygame.event.wait()
            pos = pygame.mouse.get_pos()
            # print(event.type, pygame.MOUSEBUTTONDOWN)
            if event.type == pygame.QUIT:
                if self.confirmQuit():
                    self.terminate()
                else:
                    self.screen.blit(screen2, (mov_x, mov_y))
                    pygame.display.update()
                    pygame.display.flip()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.terminate()

            if event.type == pygame.MOUSEBUTTONDOWN:
                print(event.type, pos)
                if StartButton.isOver(pos):
                    print("statr")
                    self.setState('game')
                    self.sound.play()
                    return

                if QuitButton.isOver(pos):
                    self.sound.play()
                    if self.confirmQuit():
                        self.terminate()

                if ScoreButton.isOver(pos):
                    print('score')
                    self.setState('score')
                    self.sound.play()
                    return

    def getState(self):
        return self.state

    def setState(self, state):
        self.state = state

    def run(self):
        clock = pygame.time.Clock()
        pygame.mouse.set_visible(False)
        cursorIndex = self.setChipCursor(0)
        self.board = Board(8, 8)
        self.board.set_view(175, 150, 50)
        self.board.setImageList(self.imageList)
        self.setCauldron(5)
        isShift = False
        isCtrl = False

        while True:
            clock.tick(60)

            self.redrawGameScreen()

            event = pygame.event.wait()
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                if self.confirmQuit():
                    self.terminate()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_LSHIFT:
                isShift = True
            if event.type == pygame.KEYUP and event.key == pygame.K_LSHIFT:
                isShift = False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_LCTRL:
                isCtrl = True
            if event.type == pygame.KEYUP and event.key == pygame.K_LCTRL:
                isCtrl = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.QuitButton.isOver(pos):
                    if self.confirmQuit():
                        self.terminate()
                if event.button == 3:
                    cursorIndex = self.setRandomCursor()
                    if isShift is False:
                        if self.lowCauldron() <= 0:
                            self.gameOver()
                            return
                    continue
                row, col = self.board.getCell(pos)
                # print('mouse', pos)
                # print(row, col)
                if row >= 0:
                    if self.board.checkCell(row, col, cursorIndex) or isCtrl is True:
                        self.board.setCell(row, col, cursorIndex)
                        self.addScore(15)
                        if self.board.checkFilled() is True:
                            self.levelUp()
                            cursorIndex = self.setChipCursor(0)
                            continue
                        self.highCauldron()
                        isRow, isCol = self.checkRowCol(row, col)
                        if isRow is True:
                            self.board.clearRow(row)
                            self.addScore(120)
                        if isCol is True:
                            self.board.clearCol(col)
                            self.addScore(120)

                        cursorIndex = self.setRandomCursor()

    def terminate(self):
        pygame.quit()
        sys.exit()

    def score(self):
        pass

    def redrawGameScreen(self):
        self.screen.fill((0, 0, 0))
        self.QuitButton = Button((255, 0, 0), 25, 500, 125, 50, "Quit", 20)
        self.QuitButton.draw(self.screen, (0, 0, 0))
        # self.PauseButton = Button((255, 0, 0), 25, 425, 125, 50, "Pause", 20)
        # self.PauseButton.draw(self.screen, (0, 0, 0))
        self.board.render(self.screen)
        self.allsprites.update()
        self.allsprites.draw(self.screen)
        self.drawCauldron()
        self.drawScore()
        self.drawLevel()
        pygame.display.update()

    def confirmQuit(self):
        return tkinter.messagebox.askokcancel('Dark Magic', "Want to quit?")

    def loadImages(self):
        self.loadAltar()
        for i in range(0, len(self.chipNames)):
            image = pygame.image.load(os.path.join(self.dir, 'images\\', self.chipNames[i]))
            for j in range(0, len(self.chipColors)):
                chip = Chip(i, j)
                chip.setImage(self.changeColor(image, self.chipColors[j]))
                self.imageList.append(chip)

    def changeColor(self, image, color):
        colouredImage = pygame.Surface(image.get_size())
        colouredImage.fill(color)

        finalImage = image.copy()
        finalImage.blit(colouredImage, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        return finalImage

    def setChipCursor(self, cursorIndex):
        chip = self.imageList[cursorIndex]
        self.allsprites = pygame.sprite.RenderPlain(chip)
        return cursorIndex

    def loadAltar(self):
        image = pygame.image.load(os.path.join(self.dir, 'images\\0.png'))
        chip = Chip(0, 0)
        chip.setImage(image)
        self.imageList.append(chip)

    def setRandomCursor(self):
        cursorIndex = random.randint(0, len(self.imageList) - 1)
        return self.setChipCursor(cursorIndex)

    def checkRowCol(self, row, col):
        return self.board.checkRowCol(row, col)

    def setCauldron(self, value):
        self.cauldron = value

    def lowCauldron(self):
        self.cauldron -= 1
        return self.cauldron

    def highCauldron(self):
        if self.cauldron == 5:
            return
        else:
            self.cauldron += 1

    def getCauldron(self):
        return self.cauldron

    def drawCauldron(self):
        font = pygame.font.Font(None, 50)
        image = font.render('tries:  ' + str(self.getCauldron()), True, pygame.Color('blue'))
        self.screen.blit(image, self.cauldronCoords)

    def getScore(self):
        return self.score

    def setScore(self, value):
        self.score = value

    def drawScore(self):
        font = pygame.font.Font(None, 50)
        image = font.render('score:  ' + str(self.getScore()), True, pygame.Color('blue'))
        self.screen.blit(image, self.scoreCoords)

    def addScore(self, value):
        self.setScore(self.getScore() + value)

    def drawLevel(self):
        font = pygame.font.Font(None, 50)
        image = font.render('level:  ' + str(self.getLevel()), True, pygame.Color('blue'))
        self.screen.blit(image, self.levelCoords)

    def getLevel(self):
        return self.level

    def setLevel(self, value):
        self.level = value

    def highLevel(self):
        self.setLevel(self.getLevel() + 1)

    def levelUp(self):
        print('level up')
        self.addScore(500)
        self.board.initField()
        self.highLevel()

    def gameOver(self):
        if self.getScore() == 0:
            text = "You are such an idiot that you couldn't get 15 points!"
        else:
            errorsList = self.saveStats()
            if len(errorsList) > 0:
                print(errorsList)
                text = 'При сохранении результатов возникли ошибки.'
            else:
                text = 'You lost!'
        window = tkinter.Tk()
        window.wm_withdraw()
        tkinter.messagebox.showinfo('Game over', text)
        self.setState('menu')

    def saveStats(self):
        # Добавление в базу данных
        errors_lst = []
        try:
            con = sqlite3.connect(os.path.join(self.dir, self.dbFile))
        except sqlite3.DatabaseError:
            errors_lst.append('Не удалось подключиться к базе данных')
            return errors_lst

        try:
            cur = con.cursor()
            sql = """\
CREATE TABLE IF NOT EXISTS stats (
    id         INTEGER  PRIMARY KEY AUTOINCREMENT NOT NULL,
    score      INT  NOT NULL,
    level      INT  NOT NULL,
    name       VARCHAR  NOT NULL,
    extra      VARCHAR      NOT NULL,
    date_added DATETIME DEFAULT (CURRENT_TIMESTAMP) NOT NULL
);
"""
            cur.executescript(sql)
        except sqlite3.DatabaseError:
            errors_lst.append('Ошибка создания таблицы.')
            return errors_lst

        values = (self.getScore(), self.getLevel(), '', '')
        req = "INSERT INTO stats (score, level, name, extra) VALUES (?, ?, ?, ?)"
        try:
            cur.execute(req, values)
        except sqlite3.DatabaseError:
            errors_lst.append('Не удалось добавить запись в базу данных.')
            print(sys.exc_info())
        else:
            con.commit()

        cur.close()
        con.close()
        return errors_lst

    def scoreScreen(self):
        req = 'SELECT * FROM stats ORDER BY score DESC LIMIT 5'
        errorsList = []
        try:
            con = sqlite3.connect(self.dbFile)
        except sqlite3.DatabaseError:
            errorsList.append('Не удалось подключиться к базе данных')
            return errorsList
        cur = con.cursor()
        try:
            cur.execute(req)
        except sqlite3.DatabaseError:
            # print(sys.exc_info())
            errorsList.append('Не удалось прочитать из базы.')
            return errorsList
        else:
            dbScores = cur.fetchall()

        self.screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 50)
        text_coord = 250

        for i in range(0, len(dbScores)):
            score = dbScores[i][1]
            level = dbScores[i][2]
            line = "{0:d} score:{1:d}   level:{2:d}".format(i + 1, score, level)
            string_rendered = font.render(line, True, pygame.Color('red'))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 10
            text_coord += intro_rect.height
            self.screen.blit(string_rendered, intro_rect)
            pygame.display.flip()

        while True:
            event = pygame.event.wait()
            if event.type == pygame.QUIT:
                self.terminate()
            if event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                pygame.event.clear()
                self.setState('menu')
                return

    def loadSound(self, name):
        return pygame.mixer.Sound(os.path.join(self.dir, 'sounds\\', name))

