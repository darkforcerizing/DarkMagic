import pygame


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.left = 10
        self.top = 10
        self.cell_size = 30
        self.gameField = []
        self.initField()
        self.imageList = []
        self.size = []
        self.screen = 0

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        self.size = self.cell_size * self.width, self.cell_size * self.height
        self.screen = screen
        screen2 = pygame.Surface(self.size)
        bg_color = pygame.Color('black')
        cell_color = pygame.Color('white')
        screen2.fill(bg_color)
        for row in range(0, self.height):
            for col in range(0, self.width):
                rect = ((col * self.cell_size, row * self.cell_size), (self.cell_size, self.cell_size))
                if self.gameField[row][col] == -1:
                    screen2.fill((0, 0, 0), rect)
                else:
                    screen2.fill((105, 105, 105), rect)
                    if self.gameField[row][col] >= 0:
                        chip = self.imageList[self.gameField[row][col]]
                        screen2.blit(chip.getImage(), rect)

                pygame.draw.rect(screen2, (255, 255, 255), rect, 1)
        screen.blit(screen2, (self.left, self.top))

    def getCell(self, mouse_pos):
        x, y = mouse_pos
        x, y = x - self.left, y - self.top
        x, y = x + self.cell_size // 2, y + self.cell_size // 2
        if x <= 0 or y <= 0 or x >= (self.size[0]) or y >= (self.size[1]):
            print('out', x, y)
            return -1, -1
        col = x // self.cell_size
        row = y // self.cell_size
        #print('x: ', x, ', y: ', y, ', row: ', row, ', col: ', col)
        return row, col

    def onClick(self, cell_coords):
        row, col = cell_coords
        self.gameField[row][col] = 1 if self.board[row][col] == 0 else 0

    def initField(self):
        self.gameField = []
        for i in range(0, self.height):
            row = []
            for j in range(0, self.width):
                row.append(-1)
            self.gameField.append(row)

    def setCell(self, row, col, cursorIndex):
        self.gameField[row][col] = cursorIndex

    def setImageList(self, imageList):
        self.imageList = imageList

    def checkCell(self, row, col, cursorIndex):
        # проверка на занятость клетки
        if self.getCellValue(row, col) >= 0:
            return False

        # Алтарь?
        if cursorIndex != 0:
            # проверка на отсутствие соседeй
            if self.checkNoNeighbours(row, col) is True:
                return False
        else:
            return True

        if self.tolcoAltar(row, col) is True:
            return True

        neighbours = self.getNeighbours(row, col)
        if self.checkNeighbourMatches(cursorIndex, neighbours) is True:
            return True
        return False

    def getCellValue(self, row, col):
        return self.gameField[row][col]

    def checkNoNeighbours(self, row, col):
        # (0, 0)
        if row == 0 and col == 0:
            if self.getCellValue(row, col + 1) < 0 and self.getCellValue(row + 1, col) < 0:
                print(row, col, '0,0')
                return True
            else:
                return False

        # (width, 0)
        if row == 0 and col == self.width - 1:
            if self.getCellValue(row + 1, col) < 0 and \
                    self.getCellValue(row, col - 1) < 0:
                print(row, col, 'width,0')
                return True
            else:
                return False

        # (0, height)
        if row == self.height - 1 and col == 0:
            if self.getCellValue(row - 1, col) < 0 and \
                    self.getCellValue(row, col + 1) < 0:
                print(row, col, '0,height')
                return True
            else:
                return False

        # (width, height)
        if row == self.height - 1 and col == self.width - 1:
            if self.getCellValue(row - 1, col) < 0 and \
                    self.getCellValue(row, col - 1) < 0:
                print(row, col, 'width, height')
                return True
            else:
                return False

        # крайние левые
        if col == 0:
            if self.getCellValue(row - 1, col) < 0 and self.getCellValue(row + 1, col) < 0 and \
                   self.getCellValue(row, col + 1) < 0:
                print(row, col, 'крайние левые')
                return True

        # крайние правые
        if col == self.width - 1:
            if self.getCellValue(row - 1, col) < 0 and self.getCellValue(row + 1, col) < 0 and \
                    self.getCellValue(row, col - 1) < 0:
                print(row, col, 'крайние правые')
                return True
            else:
                return False

        # крайние нижние
        if row == self.height - 1:
            if self.getCellValue(row - 1, col) < 0 and self.getCellValue(row, col - 1) < 0 and \
                    self.getCellValue(row, col + 1) < 0:
                print(row, col, 'крайние нижние')
                return True
            else:
                return False

        # крайние верхние
        if row == 0:
            if self.getCellValue(row + 1, col) < 0 and self.getCellValue(row, col - 1) < 0 and \
                    self.getCellValue(row, col + 1) < 0:
                print(row, col, 'крайние верхние')
                return True
            else:
                return False

        #  остальные
        if self.getCellValue(row, col + 1) < 0 and self.getCellValue(row, col - 1) < 0 and \
                self.getCellValue(row + 1, col) < 0 and self.getCellValue(row - 1, col) < 0:
            return True
        else:
            return False

    # проверка рядом только алтарь
    def tolcoAltar(self, row, col):
        if row == 0 and col == 0:
            if self.getCellValue(row, col + 1) <= 0 and self.getCellValue(row + 1, col) <= 0:
                return True
            else:
                return False

        # (width, 0)
        if row == 0 and col == self.width - 1:
            if self.getCellValue(row + 1, col) <= 0 and \
                    self.getCellValue(row, col - 1) <= 0:
                return True
            else:
                return False

        # (0, height)
        if row == self.height - 1 and col == 0:
            if self.getCellValue(row - 1, col) <= 0 and \
                    self.getCellValue(row, col + 1) <= 0:
                print(row, col, '0,height')
                return True
            else:
                return False

        # (width, height)
        if row == self.height - 1 and col == self.width - 1:
            if self.getCellValue(row - 1, col) <= 0 and \
                    self.getCellValue(row, col - 1) <= 0:
                print(row, col, 'width, height')
                return True
            else:
                return False

        # крайние левые
        if col == 0:
            if self.getCellValue(row - 1, col) <= 0 and self.getCellValue(row + 1, col) <= 0 and \
                   self.getCellValue(row, col + 1) <= 0:
                print(row, col, 'крайние левые')
                return True

        # крайние правые
        if col == self.width - 1:
            if self.getCellValue(row - 1, col) <= 0 and self.getCellValue(row + 1, col) <= 0 and \
                    self.getCellValue(row, col - 1) <= 0:
                print(row, col, 'крайние правые')
                return True
            else:
                return False

        # крайние нижние
        # print('r', row, self.height, row == self.height - 1)
        if row == self.height - 1:
            if self.getCellValue(row - 1, col) <= 0 and self.getCellValue(row, col - 1) <= 0 and \
                    self.getCellValue(row, col + 1) <= 0:
                print(row, col, 'крайние нижние')
                return True
            else:
                return False

        # крайние верхние
        if row == 0:
            if self.getCellValue(row + 1, col) <= 0 and self.getCellValue(row, col - 1) <= 0 and \
                    self.getCellValue(row, col + 1) <= 0:
                print(row, col, 'крайние верхние')
                return True
            else:
                return False

        #  остальные
        if self.getCellValue(row, col + 1) <= 0 and self.getCellValue(row, col - 1) <= 0 and \
                self.getCellValue(row + 1, col) <= 0 and self.getCellValue(row - 1, col) <= 0:
            return True
        else:
            return False

    def getNeighbours(self, row, col):
        neighbours = []
        # (0, 0)
        if row == 0 and col == 0:
            if self.getCellValue(row, col + 1) > 0:
                neighbours.append(self.getCellValue(row, col + 1))
            if self.getCellValue(row + 1, col) > 0:
                neighbours.append(self.getCellValue(row + 1, col))
            return neighbours

        # (width, 0)
        if row == 0 and col == self.width - 1:
            if self.getCellValue(row + 1, col) > 0:
                neighbours.append(self.getCellValue(row + 1, col))
            if self.getCellValue(row, col - 1) > 0:
                neighbours.append(self.getCellValue(row, col - 1))

        # (0, height)
        if row == self.height - 1 and col == 0:
            if self.getCellValue(row - 1, col) > 0:
                neighbours.append(self.getCellValue(row - 1, col))
            if self.getCellValue(row, col + 1) > 0:
                neighbours.append(self.getCellValue(row, col + 1))
            return neighbours

        # (width, height)
        if row == self.height - 1 and col == self.width - 1:
            if self.getCellValue(row - 1, col) > 0:
                neighbours.append(self.getCellValue(row - 1, col))
            if self.getCellValue(row, col - 1) > 0:
                neighbours.append(self.getCellValue(row, col - 1))
            return neighbours

        # крайние левые
        if col == 0:
            if self.getCellValue(row - 1, col) > 0:
                neighbours.append(self.getCellValue(row - 1, col))
            if self.getCellValue(row + 1, col) > 0:
                neighbours.append(self.getCellValue(row + 1, col))
            if self.getCellValue(row, col + 1) > 0:
                neighbours.append(self.getCellValue(row, col + 1))
            return neighbours

        # крайние правые
        if col == self.width - 1:
            if self.getCellValue(row - 1, col) > 0:
                neighbours.append(self.getCellValue(row - 1, col))
            if self.getCellValue(row + 1, col) > 0:
                neighbours.append(self.getCellValue(row + 1, col))
            if self.getCellValue(row, col - 1) > 0:
                neighbours.append(self.getCellValue(row, col - 1))
            return neighbours

        # крайние нижние
        if row == self.height - 1:
            if self.getCellValue(row - 1, col) > 0:
                neighbours.append(self.getCellValue(row - 1, col))
            if self.getCellValue(row, col - 1) > 0:
                neighbours.append(self.getCellValue(row, col - 1))
            if self.getCellValue(row, col + 1) > 0:
                neighbours.append(self.getCellValue(row, col + 1))
            return neighbours

        # крайние верхние
        if row == 0:
            if self.getCellValue(row + 1, col) > 0:
                neighbours.append(self.getCellValue(row + 1, col))
            if self.getCellValue(row, col - 1) > 0:
                neighbours.append(self.getCellValue(row, col - 1))
            if self.getCellValue(row, col + 1) > 0:
                neighbours.append(self.getCellValue(row, col + 1))
            return neighbours
        #  остальные
        if self.getCellValue(row, col + 1) > 0:
            neighbours.append(self.getCellValue(row, col + 1))
        if self.getCellValue(row, col - 1) > 0:
            neighbours.append(self.getCellValue(row, col - 1))
        if self.getCellValue(row + 1, col) > 0:
            neighbours.append(self.getCellValue(row + 1, col))
        if self.getCellValue(row - 1, col) > 0:
            neighbours.append(self.getCellValue(row - 1, col))
        return neighbours

    def checkNeighbourMatches(self, cursorIndex, neighbours):
        matches = []
        chip = self.imageList[cursorIndex]
        for i in range(0, len(neighbours)):
            if chip.getType() == self.imageList[neighbours[i]].getType() or \
                    chip.getColor() == self.imageList[neighbours[i]].getColor():
                matches.insert(i, 1)
        if len(neighbours) != len(matches):
            return False
        else:
            return True

    def checkRowCol(self, row, col):
        countCol = 0
        for i in range(0, len(self.gameField)):
            if i == row:
                for j in range(0, len(self.gameField[i])):
                    if self.getCellValue(i, j) >= 0:
                        countCol += 1

        countRow = 0
        for i in range(0, len(self.gameField)):
            for j in range(0, len(self.gameField[i])):
                if j == col:
                    if self.getCellValue(i, j) >= 0:
                        countRow += 1

        return countCol == self.width, countRow == self.height

    def clearRow(self, row):
        for j in range(0, self.width):
            self.gameField[row][j] = -2

    def clearCol(self, col):
        for i in range(0, self.height):
            self.gameField[i][col] = -2

    def checkFilled(self):
        counter = 0
        for i in range(0, len(self.gameField)):
            for j in range(0, len(self.gameField[i])):
                if self.getCellValue(i, j) == -1:
                    counter += 1
        if counter == 0:
            return True
        else:
            return False
