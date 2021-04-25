import tkinter
import action_panel, chessboard, chesspieces, moves

class MainWindow:
	def __init__(self, root):
		###########################################################
		###					Default settings					###
		###########################################################
		self.root = root
		root.title("Chess Teaching Assistant")

		self.parameters = dict()
		self.initialize_parameters()

		self.state = dict()
		self.initialize_state()
		
		###########################################################
		###					Organize panels						###
		###########################################################
		self.center = chessboard.ChessBoard(tkinter.Canvas(root, bg="white", width=self.parameters['CHESSBOARD_CANVAS_SIZE'], height=self.parameters['CHESSBOARD_CANVAS_SIZE']), self.parameters, self.state)
		self.left_panel = chesspieces.ChessPieces(tkinter.Frame(root, borderwidth=5), self.parameters, self.state, self.center)
		self.right_panel = action_panel.ActionPanel(tkinter.Frame(root, borderwidth=5), self.state, self.left_panel, self.center)

		self.left_panel.frame.pack(side=tkinter.LEFT)
		self.center.canvas.pack(side=tkinter.LEFT)
		self.right_panel.frame.pack(side=tkinter.LEFT)

	def initialize_parameters(self):
		self.parameters['CHESSBOARD_CANVAS_SIZE'] = 700

		# Chess
		self.parameters['CHESS'] = dict()
		self.parameters['CHESS']['IMG'] = dict()
		self.parameters['CHESS']['PLAYER_COLORS'] = ('white','black')
		self.parameters['CHESS']['TYPES_OF_CHESS_PIECES'] = ('king','queen','rook','knight','bishop','pawn')

		# Xiangqi
		self.parameters['XIANGQI'] = dict()
		self.parameters['XIANGQI']['IMG'] = dict()
		self.parameters['XIANGQI']['PLAYER_COLORS'] = ('red','black')
		self.parameters['XIANGQI']['TYPES_OF_CHESS_PIECES'] = ('shuai', 'shi', 'xiang', 'ju', 'ma', 'pao', 'bing')
	
	def initialize_state(self):
		self.state['chess_type'] = 'CHESS'
		self.state['move_list'] = list()
		self.state['previous_player'] = ''
		self.state['current_move'] = moves.Moves()
		self.state['current_move_index'] = -1




if __name__ == "__main__":
	root = tkinter.Tk()
	MainWindow = MainWindow(root)
	root.mainloop()
