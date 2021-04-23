import tkinter

import action_panel, chessboard, chesspieces

class MainWindow:
	def __init__(self, root):
		###########################################################
		###					Default settings					###
		###########################################################
		self.root = root
		root.title("Chess Teaching Assistant")

		self.state = dict()
		self.state["chess_type"] = "CHESS"
		self.state["canvas_size"] = 700

		###########################################################
		###					Organize panels						###
		###########################################################
		self.left_panel = chesspieces.ChessPieces(tkinter.Frame(root, borderwidth=5), self.state)
		self.left_panel.frame.pack(side=tkinter.LEFT)

		self.center = chessboard.ChessBoard(tkinter.Canvas(root, bg="white", width=self.state["canvas_size"], height=self.state["canvas_size"]), self.state)
		self.center.canvas.pack(side=tkinter.LEFT)

		self.right_panel = action_panel.ActionPanel(tkinter.Frame(root, borderwidth=5), self.state, self.center)
		self.right_panel.frame.pack(side=tkinter.RIGHT)



if __name__ == "__main__":
	root = tkinter.Tk()
	MainWindow = MainWindow(root)
	root.mainloop()
