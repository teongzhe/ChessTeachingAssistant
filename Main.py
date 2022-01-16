import tkinter
import logging, os
from datetime import date

from moves import MoveHandler
from settings import Parameters, State
from ImgProcessor import *
import ActionPanel, chessboard, chesspieces


class MainWindow:
	###########################################################
	###					Default settings					###
	###########################################################
	def __init__(self, rootObj):
		self.root = rootObj
		self.root.title('Chess Teaching Assistant')

		self.InitCaptionPanel()
		self.InitChessBoard()
		self.InitChessPiecesMenu()
		self.InitActionPanel()
	
		self.CaptionPanel.pack(side=tkinter.TOP)
		self.chesspiecesMenu.frame.pack(side=tkinter.LEFT)
		self.actionPanel.frame.pack(side=tkinter.RIGHT)
		self.chessboard.canvas.pack(side=tkinter.BOTTOM)

		self.ResizeWindow()
		self.root.bind('<Configure>', lambda event: self.ResizeWindow())


	def InitCaptionPanel(self):
		self.CaptionPanel = tkinter.Entry(root, width=20, font=(False,36), justify=tkinter.CENTER)
		self.CaptionPanel.bind('<Return>', lambda event: self.root.focus_set())

	def InitChessBoard(self):
		self.chessboard = chessboard.ChessBoard(tkinter.Canvas(root, bg='white', highlightthickness=0))

	def InitChessPiecesMenu(self):
		self.chesspiecesMenu = chesspieces.ChessPieces(tkinter.Frame(root, borderwidth=5), self.chessboard, 0.1 * self.root.winfo_screenheight())

	def InitActionPanel(self):
		self.actionPanel = ActionPanel.ActionPanel(tkinter.Frame(root, borderwidth=5), self.chesspiecesMenu, self.chessboard, self.CaptionPanel)

	def ResizeWindow(self):
		self.root.update()
		maxPossibleWidth = self.root.winfo_width() - self.chesspiecesMenu.frame.winfo_width() - self.actionPanel.frame.winfo_width()
		maxPossibleHeight = self.root.winfo_height() - self.CaptionPanel.winfo_height()
		self.chessboard.ResizeCanvas(min((maxPossibleWidth, maxPossibleHeight)))


def SetupLogging():
	logDirName = 'log'
	if not os.path.exists(logDirName):
		os.makedirs(logDirName)
	logging.basicConfig(
		filename=logDirName + os.path.sep + date.today().strftime('%Y%m%d') + '.log',
		encoding='utf-8',
		format='%(asctime)s %(levelname)-8s %(module)-30s: %(message)s',
		level = logging.INFO,
		datefmt='%Y-%m-%d %H:%M:%S',
	)


if __name__ == '__main__':
	SetupLogging()
	logging.info('Program has started')

	Parameters()
	State()
	ImgProcessor()

	root = tkinter.Tk()
	root.state('zoomed')
	Parameters().SetRoot(root)

	MainWindow = MainWindow(root)
	root.mainloop()
