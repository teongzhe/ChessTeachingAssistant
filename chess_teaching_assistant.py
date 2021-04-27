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
		self.chessboard = chessboard.ChessBoard(tkinter.Canvas(root, bg="white", width=settings.parameters["CHESSBOARD_CANVAS_SIZE"], height=settings.parameters["CHESSBOARD_CANVAS_SIZE"]))

		# Menu for Chess Pieces
		self.chess_pieces_menu = chesspieces.ChessPieces(tkinter.Frame(root, borderwidth=5), self.chessboard)

		# Action panel
		self.action_panel = action_panel.ActionPanel(tkinter.Frame(root, borderwidth=5), self.chess_pieces_menu, self.chessboard)

		# Text panel
		self.text_panel = tkinter.Entry(root, width=15, font=(False,48), justify=tkinter.CENTER)

		def focus_root(event):
			root.focus_set()
		self.text_panel.bind("<Return>", focus_root)


		# Arrange everything
		self.text_panel.pack(side=tkinter.TOP)
		self.chess_pieces_menu.frame.pack(side=tkinter.LEFT)
		self.chessboard.canvas.pack(side=tkinter.LEFT)
		self.action_panel.frame.pack(side=tkinter.LEFT)



if __name__ == "__main__":
	root = tkinter.Tk()
	settings.init(root)
	MainWindow = MainWindow()
	settings.root.mainloop()
