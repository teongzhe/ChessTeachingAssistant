import tkinter
import tkinter.font

import settings
import action_panel, chessboard, chesspieces, moves

class MainWindow:
	def __init__(self):
		###########################################################
		###					Default settings					###
		###########################################################
		root = settings.root
		root.title("Chess Teaching Assistant")

		###########################################################
		###					Organize panels						###
		###########################################################
		# Chessboard
		self.chessboard = chessboard.ChessBoard(tkinter.Canvas(root, bg="white"))

		# Menu for Chess Pieces
		self.chesspiecesMenu = chesspieces.ChessPieces(tkinter.Frame(root, borderwidth=5), self.chessboard)

		# Action panel
		self.actionPanel = action_panel.ActionPanel(tkinter.Frame(root, borderwidth=5), self.chesspiecesMenu, self.chessboard)

		# Text panel
		self.textPanel = tkinter.Entry(root, width=20, font=(False,36), justify=tkinter.CENTER)
		settings.state["text_panel"] = self.textPanel

		def focus_root(event):
			root.focus_set()
		self.textPanel.bind("<Return>", focus_root)



		# Arrange everything
		self.textPanel.pack(side=tkinter.TOP)
		self.chesspiecesMenu.frame.pack(side=tkinter.LEFT)
		self.actionPanel.frame.pack(side=tkinter.RIGHT)
		self.chessboard.canvas.pack(side=tkinter.BOTTOM)



		# Resize chessboard to maximize screen usage
		root.update()
		maxPossibleWidth = root.winfo_width() - self.chesspiecesMenu.frame.winfo_width() - self.actionPanel.frame.winfo_width()
		maxPossibleHeight = root.winfo_height() - self.textPanel.winfo_height()
		self.chessboard.resize_canvas(min((maxPossibleWidth, maxPossibleHeight)))



if __name__ == "__main__":
	root = tkinter.Tk()
	root.state("zoomed")
	settings.init(root)
	MainWindow = MainWindow()
	settings.root.mainloop()
