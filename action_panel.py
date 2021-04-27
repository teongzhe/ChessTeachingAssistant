import tkinter
from tkinter import filedialog
import copy

import settings
import chesspieces, chessboard

class ActionPanel:
	def __init__(self, frame, chesspieces, chessboard):
		self.frame = frame
		settings.state = settings.state
		self.chesspieces = chesspieces
		self.chessboard = chessboard

		self.chess_type_panel()
		self.chessboard_state_panel()

	def chess_type_panel(self):
		labelFrame = tkinter.Frame(self.frame)
		labelFrame.pack(side=tkinter.TOP)
		tkinter.Label(labelFrame, text="What would you like to play today?").pack(side=tkinter.TOP)

		# Callback function and variable
		self.chess_type_var = tkinter.StringVar(value="CHESS")
		def callback():
			if settings.state["chess_type"] != self.chess_type_var.get():
				self.change_chess_type(self.chess_type_var.get())
			
		tkinter.Radiobutton(self.frame, command=callback, variable=self.chess_type_var, value="CHESS", text="Chess").pack(anchor="w")
		tkinter.Radiobutton(self.frame, command=callback, variable=self.chess_type_var, value="XIANGQI", text="Xiang Qi").pack(anchor="w")
	
	def change_chess_type(self, target_type):
		settings.state["chess_type"] = target_type
		self.chessboard.clear_pieces_from_board()
		self.chessboard.initialize_chess_board()
		self.chesspieces.initialize_menu()

		settings.state["clear_move_list"]()

	def chessboard_state_panel(self):
		BUTTON_WIDTH = 20

		main_frame = tkinter.Frame(self.frame)
		main_frame.pack(side=tkinter.TOP)

		# Starting positions and clear board options
		tkinter.Button(main_frame, text="Starting positions", command=self.chessboard.starting_positions, width=BUTTON_WIDTH).pack(anchor="w")
		tkinter.Button(main_frame, text="Clear board", command=self.chessboard.clear_pieces_from_board, width=BUTTON_WIDTH).pack(anchor="w")

		# Take back and undo take back
		tkinter.Button(main_frame, text="Take back move", command=self.chessboard.take_back, width=BUTTON_WIDTH).pack(anchor="w")
		tkinter.Button(main_frame, text="Undo take back", command=self.chessboard.forward, width=BUTTON_WIDTH).pack(anchor="w")

		# Quick save and quick load
		def quicksave():
			settings.state["quick_save_position"] = copy.deepcopy(settings.state["position"])
		tkinter.Button(main_frame, text="Quick save", command=quicksave, width=BUTTON_WIDTH).pack(anchor="w")

		def quickload():
			self.chessboard.clear_pieces_from_board()
			for coordinate, piece in settings.state["quick_save_position"].items():
				self.chessboard.add_piece_to_board(coordinate, piece)
			settings.state["clear_move_list"]()
		tkinter.Button(main_frame, text="Quick load", command=quickload, width=BUTTON_WIDTH).pack(anchor="w")

		# Save to file
		def save_to_file():
			filename = filedialog.asksaveasfilename(initialdir=".", title = "Select a File", defaultextension = ".csv", filetypes = (("csv files","*.csv*"), ("all files", "*.*")))
			if filename != "":
				file = open(filename, "w")
				for key, value in settings.state["position"].items():
					file.write(str(key[0]) + "," + str(key[1]) + "," + str(value) + "\n")
				file.close()

		tkinter.Button(main_frame, text="Save to file", command=save_to_file, width=BUTTON_WIDTH).pack(anchor="w")

		# Load from file
		def load_from_file():
			filename = filedialog.askopenfilename(initialdir=".", filetypes = (("Comma Separated Values","*.csv*"),("all files", "*.*")))

			if filename != "":			
				data = dict()
				file = open(filename, "r")
				for line in file.read().split("\n"):
					if line:
						x, y, piece = line.split(",")
						data[(int(x),int(y))] = piece
				file.close()

				# Get types of chess pieces
				chess_piece_types = set()
				for chess_piece in data.values():
					chess_piece_types.add(chess_piece.split("_")[1])

				# Find out what type of chess it is
				chess_type = "CHESS"
				for piece in chess_piece_types:
					if piece not in settings.parameters["CHESS"]["TYPES_OF_CHESS_PIECES"]:
						chess_type = "XIANGQI"
				
				# Change chess type if neccessary
				if chess_type != settings.state["chess_type"]:
					self.chess_type_var.set(chess_type)
					self.change_chess_type(chess_type)
				
				# Update chess pieces
				self.chessboard.clear_pieces_from_board()
				for coordinate, piece in data.items():
					self.chessboard.add_piece_to_board(coordinate, piece)
				settings.state["clear_move_list"]()

		tkinter.Button(main_frame, text="Load from file", command=load_from_file, width=BUTTON_WIDTH).pack(anchor="w")
