import random


UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

numRows = 9
numCols = 5

ghostRow = 3
probTopAndBotSingleCellJoin = 1

def makeCell(x, y ):
  return Cell(x, y)


def setGhostHomeCells(table):
    c = table[ghostRow][0]
    c.filled = True
    c.connect[LEFT] = c.connect[RIGHT] = c.connect[DOWN] = True

    c = table[ghostRow][1]
    c.filled = True
    c.connect[LEFT] = c.connect[DOWN] = True

    c = table[ghostRow + 1][0]
    c.filled = True
    c.connect[LEFT] = c.connect[UP] = c.connect[RIGHT] = True

    c = table[ghostRow + 1][1]
    c.filled = True
    c.connect[UP] = c.connect[LEFT] = True


def makeTable() :
    table = []
    cells = []
    for y in range(numRows):
        row = []
        for x in range(numCols):
          cell = makeCell(x, y)
          cells.append(cell)
          row.append(cell)

        table.append(row)

    for cell in cells:
        x = cell.x
        y = cell.y
        if x > 0:
            cell.next[LEFT] = table[y][x - 1]

        if x < numCols - 1:
            cell.next[RIGHT] = table[y][x + 1]

        if y > 0:
            cell.next[UP] = table[y - 1][x]

        if y < numRows - 1:
            cell.next[DOWN] = table[y + 1][x]

    setGhostHomeCells(table)

    return table


def getLeftMostEmptyCells(table):
    leftCells = []
    for x in range(numCols):
        for y in range(numRows):
            c = table[y][x]
            if not c:
              leftCells.append(c)

        if len(leftCells) > 0:
            break

    return leftCells


def makeState():
    return State()


def fillCell(state, cell):
    cell.filled = True
    state.numFilled += 1
    cell.no = state.numFilled
    cell.group = state.numGroups


def trySingleCellGroup(state):
    cell, singleCount = state
    if (cell.x < numCols - 1 and cell.y in singleCount
          and random.randint(100) / 100 <= probTopAndBotSingleCellJoin and singleCount[cell.y] == 0):
        dir = UP if cell.y == 0 else DOWN
        cell.connect[dir] = True
        singleCount[cell.y] += 1
        return True


def startNewGroup(state):
    table = state
    openCells = getLeftMostEmptyCells(table)
    cell = random.choice(openCells)
    if cell:
        fillCell(state, cell)
        state.firstCell = state.cell = cell

    return cell


def genRandomCells():
    state = makeState()
    while True:
        cell = startNewGroup(state)
        if not cell:
            break

        if trySingleCellGroup(state):
            continue

        state.size = 1

        if cell.x == numCols - 1:
          cell.connect[RIGHT] = True
          cell.isRaiseHeightCandidate = True
          continue


        print(state)
        break

    state.numGroups += 1


class State(object):
    def __init__(self):
        self.table = makeTable(),
        self.cell = None
        self.firstCell = None
        self.numFilled = 0
        self.numGroups = 0
        self.size = 0
        self.singleCount = {
            0: 0,
            numRows - 1: 0
        }


class Cell(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.filled = False
        self.connect = [False, False, False, False]
        self.next = {}
        self.no = None
        self.group = None


genRandomCells()