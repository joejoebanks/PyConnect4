from tkinter import *
from c4game import *

class GameScreen:
	def __init__(self,window,board,aiplayer):
		self.board = board
		self.aiplayer = aiplayer
		self.currentPlayer = 'x'
		self.isWinner = False

		self.window = window
		self.frame = Frame(window)
		self.frame.pack()
		self.winFrame = Frame(window)
		self.winFrame.pack()
		self.col = 7
		self.row = 6
		self.diameter = 700/board.height
		self.hoverCol = -1

		self.boardWidth = self.diameter*self.board.width+20
		self.boardHeight = self.diameter*self.board.height+20

		self.winText = Label(self.winFrame,text='',font=("Impact", 25))
		self.winText.pack(side=BOTTOM)

		self.bottomFrame = Frame(window).pack(side=BOTTOM)
		self.playerText = Label(self.bottomFrame, text='Click the column you would like to place the checker.',font=('Arial Black',20))
		self.playerText.pack(side=BOTTOM)

		self.var = DoubleVar()
		self.slider = Scale(self.frame,from_=1, to=10, orient=HORIZONTAL, command=self.setPly, variable=self.var,length=200,bd=0,font=('Impact',10))
		self.slider.pack(side=LEFT)
		self.slider.set(4)
		self.setPly(self.var)

		self.newGameButton = Button(self.frame, text='New Game', command=self.newGame,width=10, padx=20,font='Impact',bg='#05358a',fg='white',bd=0)
		self.newGameButton.pack(side=RIGHT)
		self.quitButton = Button(self.frame, text='Quit!', command=self.quitGame,width=3, padx=20,font='Impact',bg='#E74C3C',fg='white',bd=0)
		self.quitButton.pack(side=LEFT)

		self.draw = Canvas(window, height=self.boardHeight, width=self.boardWidth)
		self.draw.create_rectangle(0,0,self.boardWidth, self.boardHeight, fill='blue')
		self.draw.bind('<Button-1>', self.mouseInput)
		self.draw.pack()

		self.circles = []

		self.drawBoard()
		
	def newGame(self):
		self.playerText.config(text='Click the column you would like to place the checker.')
		self.isWinner = False
		self.winText.config(text='')
		self.board.clear()
		self.drawBoard()


	def setPly(self,var):
		self.aiplayer.ply = self.var.get()

	def displayWinner(self,winText):
		self.winText.config(text=winText)

	def displayPlayer(self,ox):
		if ox=='x':
			self.playerText.config(text=f'Red checker turn')
		else:
			self.playerText.config(text=f'Computers move')

	def displayMessage(self,message):
		self.playerText.config(text=message)

	def drawBoard(self):
		color = ''
		y = 0 
		for row in range(self.board.height):
			circleRow = []
			x = 0
			for col in range(self.board.width):
				if self.board.data[row][col] == ' ':
					color = 'white'
				elif self.board.data[row][col] == 'x':
					color = 'red'
				else:
					color = 'black'
				circleRow += [self.draw.create_oval(x+20,y+20, x+self.diameter, y+self.diameter, fill=color)]
				x += self.diameter
			y += self.diameter

	def quitGame(self):
		self.window.destroy()

	def displayTie(self):
		self.winText.config(text=f'Tie game!')

	def computerMove(self):
		aiMove = self.aiplayer.nextMove(self.board)
		self.displayMessage(f'Computer moved in column {aiMove+1}')
		self.board.addMove(aiMove, 'o')
		self.drawBoard()
		if self.board.winsFor('o'):
			self.isWinner = True
			self.displayWinner('The computer won!')
			return 'black'
		if self.board.isFull():
			self.displayTie()
			self.isWinner = True
			return 'tie'

	def mouseInput(self, event):
		col = int(event.x/self.diameter)
		row = int(event.y/self.diameter)
		if self.isWinner == False:
			if not self.board.addMove(col,self.currentPlayer):
				return False
			self.drawBoard()
			if self.board.winsFor('x'):
				self.displayWinner('You win!')
				self.isWinner = True
				return 'red'
			self.computerMove()

def main():
	board = Connect4(7,6)
	player = Player('o', 'Random', 4)

	root = Tk()
	root.title('Connect 4')
	gameScreen = GameScreen(root,board,player)
	root.mainloop()


if __name__ == '__main__':
	main()