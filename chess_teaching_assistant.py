import tkinter
import tkinter.font
from moves import MoveHandler

from settings import Parameters, State
from ImgProcessor import *
import action_panel, chessboard, chesspieces

class MainWindow:
	###########################################################
	###					Default settings					###
	###########################################################
	def __init__(self, rootObj):
		root = rootObj
		root.title("Chess Teaching Assistant")

		self.InitCaptionPanel()
		self.InitChessBoard()
		self.InitChessPiecesMenu()
		MoveHandler(self.chessboard)
		self.InitActionPanel()
	
		self.CaptionPanel.pack(side=tkinter.TOP)
		self.chesspiecesMenu.frame.pack(side=tkinter.LEFT)
		self.actionPanel.frame.pack(side=tkinter.RIGHT)
		self.chessboard.canvas.pack(side=tkinter.BOTTOM)

		# Resize chessboard to maximize screen usage
		root.update()
		maxPossibleWidth = root.winfo_width() - self.chesspiecesMenu.frame.winfo_width() - self.actionPanel.frame.winfo_width()
		maxPossibleHeight = root.winfo_height() - self.CaptionPanel.winfo_height()
		self.chessboard.resize_canvas(min((maxPossibleWidth, maxPossibleHeight)))


	def InitCaptionPanel(self):
		self.CaptionPanel = tkinter.Entry(root, width=20, font=(False,36), justify=tkinter.CENTER)
		self.CaptionPanel.bind("<Return>", lambda e: root.focus_set())

	def InitChessBoard(self):
		self.chessboard = chessboard.ChessBoard(tkinter.Canvas(root, bg="white"))

	def InitChessPiecesMenu(self):
		self.chesspiecesMenu = chesspieces.ChessPieces(tkinter.Frame(root, borderwidth=5), self.chessboard, 0.1 * root.winfo_screenheight())

	def InitActionPanel(self):
		self.actionPanel = action_panel.ActionPanel(tkinter.Frame(root, borderwidth=5), self.chesspiecesMenu, self.chessboard, self.CaptionPanel)


if __name__ == "__main__":
	# Initialize Singletons
	Parameters()
	State()
	ImgProcessor()

	root = tkinter.Tk()
	root.state("zoomed")
	Parameters().SetRoot(root)

	MainWindow = MainWindow(root)
	root.mainloop()
