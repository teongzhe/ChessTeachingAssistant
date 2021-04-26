import tkinter

import settings
import action_panel, chessboard, chesspieces, moves

class MainWindow:
	def __init__(self):
		###########################################################
		###					Default settings					###
		###########################################################
		root = settings.root
		root.title('Chess Teaching Assistant')

		###########################################################
		###					Organize panels						###
		###########################################################
		self.center = chessboard.ChessBoard(tkinter.Canvas(root, bg='white', width=settings.parameters['CHESSBOARD_CANVAS_SIZE'], height=settings.parameters['CHESSBOARD_CANVAS_SIZE']))
		self.left_panel = chesspieces.ChessPieces(tkinter.Frame(root, borderwidth=5), self.center)
		self.right_panel = action_panel.ActionPanel(tkinter.Frame(root, borderwidth=5), self.left_panel, self.center)

		self.left_panel.frame.pack(side=tkinter.LEFT)
		self.center.canvas.pack(side=tkinter.LEFT)
		self.right_panel.frame.pack(side=tkinter.LEFT)



if __name__ == '__main__':
	root = tkinter.Tk()
	settings.init(root)
	MainWindow = MainWindow()
	settings.root.mainloop()
