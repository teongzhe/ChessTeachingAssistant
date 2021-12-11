import tkinter
import tkinter.font

from settings import *
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
		self.InitActionPanel()
	
		# Arrange everything
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
		# Text panel
		self.CaptionPanel = tkinter.Entry(root, width=20, font=(False,36), justify=tkinter.CENTER)

		def focus_root(event):
			root.focus_set()
		self.CaptionPanel.bind("<Return>", focus_root)

	def InitChessBoard(self):
		# Chessboard
		self.chessboard = chessboard.ChessBoard(tkinter.Canvas(root, bg="white"))

	def InitChessPiecesMenu(self):
		# Menu for Chess Pieces
		self.chesspiecesMenu = chesspieces.ChessPieces(tkinter.Frame(root, borderwidth=5), self.chessboard, 0.1 * root.winfo_screenheight())

	def InitActionPanel(self):
		# Action panel
		self.actionPanel = action_panel.ActionPanel(tkinter.Frame(root, borderwidth=5), self.chesspiecesMenu, self.chessboard, self.CaptionPanel)


if __name__ == "__main__":
	root = tkinter.Tk()
	root.state("zoomed")

	# Initialize
	init()
	Parameters()
	ImgProcessor()

	MainWindow = MainWindow(root)
	root.mainloop()
