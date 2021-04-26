import tkinter
import copy

import settings
import chesspieces, chessboard

class ActionPanel:
	def __init__(self, frame, chesspieces, chessboard):
		self.frame = frame
		self.state = settings.state
		self.chesspieces = chesspieces
		self.chessboard = chessboard

		self.chess_type_panel()
		self.chessboard_state_panel()

	def chess_type_panel(self):
		labelFrame = tkinter.Frame(self.frame)
		labelFrame.pack(side=tkinter.TOP)
		tkinter.Label(labelFrame, text='What would you like to play today?').pack(side=tkinter.TOP)

		# Callback function and variable
		var = tkinter.StringVar(value='CHESS')
		def callback():
			if self.state['chess_type'] != var.get():
				self.state['chess_type'] = var.get()
				self.chessboard.clear_pieces_from_board()
				self.chessboard.initialize_chess_board()
				self.chesspieces.initialize_menu()

				self.state['clear_move_list']()
			
		tkinter.Radiobutton(self.frame, command=callback, variable=var, value='CHESS', text='Chess').pack(anchor='w')
		tkinter.Radiobutton(self.frame, command=callback, variable=var, value='XIANGQI', text='Xiang Qi').pack(anchor='w')

	def chessboard_state_panel(self):
		BUTTON_WIDTH = 20

		main_frame = tkinter.Frame(self.frame)
		main_frame.pack(side=tkinter.TOP)

		# Starting positions and clear board options
		tkinter.Button(main_frame, text='Starting positions', command=self.chessboard.starting_positions, width=BUTTON_WIDTH).pack(anchor='w')
		tkinter.Button(main_frame, text='Clear board', command=self.chessboard.clear_pieces_from_board, width=BUTTON_WIDTH).pack(anchor='w')

		# Take back and undo take back
		tkinter.Button(main_frame, text='Take back move', command=self.chessboard.take_back, width=BUTTON_WIDTH).pack(anchor='w')
		tkinter.Button(main_frame, text='Undo take back', command=self.chessboard.forward, width=BUTTON_WIDTH).pack(anchor='w')

		# Quick save and quick load
		def quicksave():
			self.state['quick_save_position'] = copy.deepcopy(self.state['position'])
		tkinter.Button(main_frame, text='Quick save', command=quicksave, width=BUTTON_WIDTH).pack(anchor='w')

		def quickload():
			self.chessboard.clear_pieces_from_board()
			for coordinate, piece in self.state['quick_save_position'].items():
				self.chessboard.add_piece_to_board(coordinate, piece)
			self.state['clear_move_list']()
		tkinter.Button(main_frame, text='Quick load', command=quickload, width=BUTTON_WIDTH).pack(anchor='w')
