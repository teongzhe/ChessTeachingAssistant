import tkinter
import action_panel, chessboard, chesspieces

class MainWindow:
	def __init__(self, root):
		###########################################################
		###					Default settings					###
		###########################################################
		self.root = root
		root.title("Chess Teaching Assistant")

		self.parameters = dict()
		self.parameters['CHESSBOARD_CANVAS_SIZE'] = 700

		self.state = dict()
		self.state["chess_type"] = "CHESS"
		self.state['chess_piece_size'] = 100

		###########################################################
		###					Organize panels						###
		###########################################################
		self.center = chessboard.ChessBoard(tkinter.Canvas(root, bg="white", width=self.parameters['CHESSBOARD_CANVAS_SIZE'], height=self.parameters['CHESSBOARD_CANVAS_SIZE']), self.parameters, self.state)
		self.left_panel = chesspieces.ChessPieces(tkinter.Frame(root, borderwidth=5), self.parameters, self.state, self.center)
		self.right_panel = action_panel.ActionPanel(tkinter.Frame(root, borderwidth=5), self.state, self.left_panel, self.center)

		self.left_panel.frame.pack(side=tkinter.LEFT)
		self.center.canvas.pack(side=tkinter.LEFT)
		self.right_panel.frame.pack(side=tkinter.LEFT)


if __name__ == "__main__":
	root = tkinter.Tk()
	MainWindow = MainWindow(root)
	root.mainloop()
