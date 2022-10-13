import random

class Connect4(object):
    
    def __init__(self, width, height, window=None):
        self.width = width
        self.height = height
        self.data = []
        
        self.makeBoard()

    def __repr__(self):
        s = ''
        for i in range(0,self.height):
            s += '|'
            for j in range(self.width):
                s+=(self.data[i][j] + "|")
            s+= '\n'
        s += '--'*self.width + '-\n'
        for i in range(self.width):
            s += f' {i}'
        return s

    def hostGame(self):
        currentPlayer = 'O'
        playerMoved = False
        while True:
            print(self)
            if playerMoved == True:
                if currentPlayer == 'X':
                    currentPlayer = 'O'
                    playerMoved = False
                else:
                    currentPlayer = 'X'
                    playerMoved = False
            while playerMoved != True:
                playerMove = input(f'Player {currentPlayer}, please enter the index you want to drop: ')
                if playerMove.isnumeric():
                    playerMove = int(playerMove)
                    move_allowed = self.addMove(playerMove, currentPlayer)
                    if move_allowed == True:
                        playerMoved = True
                        if self.winsFor(currentPlayer.lower()):
                            print(self)
                            print(f'CONGRATS PLAYER {currentPlayer}, YOU WON!!!!!!')
                            return 'win'
                        break
                    if self.isFull():
                        print('FULL BOARD! TIE GAME')
                        return 'tie'
                    else:
                        print('ILLEGAL MOVE! TRY AGAIN')
                else:
                    print('PLEASE ENTER AN INTEGER')

    def clear(self):
        self.data = []
        self.makeBoard()

    def makeBoard(self):
        for row in range(self.height):
            boardRow = []
            for col in range(self.width):
                boardRow += [' ']
            self.data += [boardRow]

    def addMove(self, col, ox):
        if self.allowsMove(col):
            for row in range( self.height ):
                if self.data[row][col] != ' ':
                    self.data[row-1][col] = ox
                    return True
            self.data[self.height-1][col] = ox
            return True
        else:
            return False

    def findRow(self,col):
        if self.allowsMove(col):
            for row in range( self.height ):
                if self.data[row][col] != ' ':
                    return row-1
            return self.height-1
        else:
            return False

    def delMove(self,col):
        for i in range(self.height):
             if self.data[i][col] != ' ':
                self.data[i][col] = ' '
                break

    def allowsMove(self, col):
        if (0 <=  col < self.width) and (' ' in [self.data[i][col] for i in range(self.height)]):
            return True
        else:
            return False

    def isFull(self):
        for i in range(self.height):
            if ' ' in self.data[i]:
                return False
        return True

    def cross_diagonal1(self,row, col,ox):
        bottom_left = ''
        top_right = ''
        if (len(self.data[row:-1])> 0):
            for i in range(1,4):
                if (0 <= col-i < self.width) and (0 <= row+i < self.height):
                    bottom_left = str(self.data[row+i][col-i]) + bottom_left
                else:
                    break
        if (len(self.data[row][col:-1]) > 0):
            for i in range(1,4):
                if (0 <= col+i < self.width) and (0 <= row-i < self.height):
                    top_right += str(self.data[row-i][col+i])
                else:
                    break
        diagonal = bottom_left+ox+top_right
        return diagonal
    
    def cross_diagonal2(self, row,col,ox):
        bottom_right = ''
        top_left = ''
        if (len(self.data[row:-1])> 0):
            for i in range(1,4):
                if (0 <= col+i < self.width) and (0 <= row+i < self.height):
                    bottom_right = bottom_right + str(self.data[row+i][col+i])
                else:
                    break
        if (len(self.data[row][0:col])> 0):
            for i in range(1,4):
                if (0 <= col-i < self.width) and (0 <= row-i < self.height):
                    top_left = str(self.data[row-i][col-i]) + top_left
                else:
                    break
        diagonal = top_left+ox+bottom_right
        return diagonal

    def winsFor(self, ox):
        for row in range(self.height):
            for col in range(self.width):
                if self.data[row][col] == ox:
                    horizontal = ''.join(self.data[row])
                    if f'{ox}'*4 in horizontal:
                        return True
                    vertical = ''.join([self.data[i][col] for i in range(self.height)])
                    if f'{ox}'*4 in vertical:
                        return True
                    if f'{ox}'*4 in self.cross_diagonal1(row,col,ox):
                        return True
                    if f'{ox}'*4 in self.cross_diagonal2(row,col,ox):
                        return True
        return False

    def playGameWith(self, aiPlayer):
        if aiPlayer.ox == 'X':
            realPlayer = 'O'
        else:
            realPlayer = 'X'
        playerMoved = False
        currentPlayer = 'X'
        while True:
            print(self)
            if playerMoved == True:
                if currentPlayer == 'X':
                    currentPlayer = 'O'
                    playerMoved = False
                else:
                    currentPlayer = 'X'
                    playerMoved = False
            while playerMoved != True:
                if currentPlayer == realPlayer:
                    playerMove = input(f'Player {realPlayer}, please enter the index you want to drop: ')
                    if playerMove.isnumeric():
                        playerMove = int(playerMove)
                        move_allowed = self.addMove(playerMove, currentPlayer)
                        if move_allowed == True:
                            playerMoved = True
                            break
                        else:
                            print('ILLEGAL MOVE! TRY AGAIN')
                    else:
                        print('PLEASE ENTER AN INTEGER')
                else:
                    self.addMove(aiPlayer.nextMove(self),aiPlayer.ox)
                    playerMoved = True
            if self.winsFor(currentPlayer.lower()):
                print(self)
                print(f'CONGRATS PLAYER {currentPlayer}, YOU WON!!!!!!')
                return 'win'
            if self.isFull():
                print('FULL BOARD! TIE GAME')
                return 'tie'

class Player:
    def __init__(self,ox,tbt,ply):
        self.ox = ox
        self.tieBreakType = tbt
        self.ply = ply

    def nextMove(self, board):
        scorer = [{'wins':0, 'loss':0, 'illegalIndex':-1} for i in range(board.width)]
        final_scores = self.scoresFor(board,self.ox,self.ply,scorer)
        colIndex = self.tieBreakMove(final_scores)
        return colIndex

    def scoresFor(self,board,ox,ply,scorer):
        if ox == 'x':
            nextPlayer = 'o'
        else:
            nextPlayer = 'x'
        if ply<=0:
            return 'done'
        elif ply<self.ply:
            for i in range(board.width):
                if board.addMove(i, ox):
                    if board.winsFor(ox):
                        if ox==self.ox:
                            scorer['wins']+=1
                            board.delMove(i)
                            return scorer
                        else:
                            scorer['loss']+=1
                    self.scoresFor(board,nextPlayer,ply-1,scorer)    
                    board.delMove(i)
        else:
            for i in range(board.width):
                if board.addMove(i, ox):
                    if board.winsFor(ox):
                        if ox==self.ox:
                            scorer[i]['wins']+=1
                        else:
                            scorer[i]['loss']+=1
                            board.delMove(i)
                            return scorer
                    self.scoresFor(board,nextPlayer,ply-1,scorer[i])
                    board.delMove(i)
                else:
                    scorer[i]['illegalIndex'] = i
            return scorer
            
    def tieBreakMove(self,scores):
    	max_indexes = self.maxIndexes(scores)
    	if self.tieBreakType == 'Left':
    		return max_indexes[0]
    	elif self.tieBreakType == 'Right':
    		return max_indexes[-1]
    	elif self.tieBreakType == 'Random':
    		return random.choice(max_indexes)

    def maxIndexes(self,scores):
        final_ratios = []
        final_indexes = []
        for i in range(len(scores)):
            if scores[i]['illegalIndex'] < 0:
                wins = scores[i]['wins']
                loss =scores[i]['loss']
                if loss == 0 and wins > 0:
                    loss-=wins
                final_ratios += [loss]
                final_indexes+=[i]
        return [final_indexes[i] for i,x in enumerate(final_ratios) if x==min(final_ratios)]
