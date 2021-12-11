import tkinter
from tkinter import filedialog, messagebox

from settings import Parameters, State

class ActionPanel:
	def __init__(self, frame, chesspieces, chessboard, CaptionPanel):
		self.frame = frame
		self.chesspieces = chesspieces
		self.ChessBoard = chessboard
		self.CaptionPanel = CaptionPanel

		self.chess_type_panel()
		self.ChessBoard_state_panel()

	def chess_type_panel(self):
		labelFrame = tkinter.Frame(self.frame)
		labelFrame.pack(side=tkinter.TOP)
		tkinter.Label(labelFrame, text="What would you like to play today?").pack(side=tkinter.TOP)

		# Callback function and variable
		self.chess_type_var = tkinter.StringVar(value="Chess")
		def callback():
			if State().GetChessType() != self.chess_type_var.get():
				self.change_chess_type(self.chess_type_var.get())
			
		tkinter.Radiobutton(self.frame, command=callback, variable=self.chess_type_var, value="Chess", text="Chess").pack(anchor="w")
		tkinter.Radiobutton(self.frame, command=callback, variable=self.chess_type_var, value="XiangQi", text="Xiang Qi").pack(anchor="w")

	
	def change_chess_type(self, target_type):
		State().SetChessType(target_type)
		self.ChessBoard.clear_pieces_from_board()
		self.ChessBoard.initialize_chess_board()
		self.chesspieces.initialize_menu()

		State().ClearMoveList()
		self.ChessBoard.remove_highlights()

	def ChessBoard_state_panel(self):
		BUTTON_WIDTH = 20

		main_frame = tkinter.Frame(self.frame)
		main_frame.pack(side=tkinter.TOP)

		# Starting positions and clear board options
		tkinter.Button(main_frame, text="Starting positions", command=self.ChessBoard.starting_positions, width=BUTTON_WIDTH).pack(anchor="w")
		tkinter.Button(main_frame, text="Clear board", command=self.ChessBoard.clear_pieces_from_board, width=BUTTON_WIDTH).pack(anchor="w")

		# Take back and undo take back
		tkinter.Button(main_frame, text="Take back move", command=self.ChessBoard.take_back, width=BUTTON_WIDTH).pack(anchor="w")
		tkinter.Button(main_frame, text="Undo take back", command=self.ChessBoard.forward, width=BUTTON_WIDTH).pack(anchor="w")

		# Quick save and quick load
		def quicksave():
			State().SetQuickSavePosition()
			State().SetSavedCaption(self.CaptionPanel.get())
		tkinter.Button(main_frame, text="Quick save", command=quicksave, width=BUTTON_WIDTH).pack(anchor="w")

		def quickload():
			self.ChessBoard.clear_pieces_from_board()
			for coordinate, piece in State().GetQuickSavePosition().items():
				self.ChessBoard.add_piece_to_board(coordinate, piece)
			State().ClearMoveList()
			self.ChessBoard.remove_highlights()

			self.CaptionPanel.delete(0, tkinter.END)
			self.CaptionPanel.insert(0, State().GetSavedCaption())
		tkinter.Button(main_frame, text="Quick load", command=quickload, width=BUTTON_WIDTH).pack(anchor="w")

		# Save to file
		def save_to_file():
			filename = filedialog.asksaveasfilename(initialdir=".", title = "Select a File", defaultextension = ".csv", filetypes = (("csv files","*.csv*"), ("all files", "*.*")))
			if filename != "":
				file = open(filename, "w")
				file.write(self.CaptionPanel.get() + "\n")
				for key, value in State().GetChessPiecePositions().items():
					file.write(str(key[0]) + "," + str(key[1]) + "," + str(value) + "\n")
				file.close()

		tkinter.Button(main_frame, text="Save to file", command=save_to_file, width=BUTTON_WIDTH).pack(anchor="w")

		# Load from file
		def load_from_file():
			filename = filedialog.askopenfilename(initialdir=".", filetypes = (("Comma Separated Values","*.csv*"),("all files", "*.*")))

			if filename != "":			
				data = dict()
				file = open(filename, "r")

				lines = file.read().split("\n")
				self.CaptionPanel.delete(0, tkinter.END)
				self.CaptionPanel.insert(0, lines[0])

				for line in lines[1:]:
					if line:
						x, y, piece = line.split(",")
						data[(int(x),int(y))] = piece
				file.close()

				# Get types of chess pieces
				chess_piece_types = set()
				for chess_piece in data.values():
					chess_piece_types.add(chess_piece.split("_")[1])

				# Find out what type of chess it is
				ChessType = "Chess"
				for piece in chess_piece_types:
					if ChessType == "Chess" and piece not in Parameters().GetTypesOfChessPieces("Chess"):
						ChessType = "XiangQi"
				
				# Change chess type if neccessary
				if ChessType != State().GetChessType():
					self.chess_type_var.set(ChessType)
					self.change_chess_type(ChessType)
				
				# Update chess pieces
				self.ChessBoard.clear_pieces_from_board()
				for coordinate, piece in data.items():
					if 0 <= coordinate[0] < Parameters().GetChessboardXArray(ChessType) and 0 <= coordinate[1] < Parameters().GetChessboardYArray(ChessType):
						self.ChessBoard.add_piece_to_board(coordinate, piece)
					else:
						msg = "Coordinate " + str(coordinate) + " is out of range!\nThe piece will be ignored."
						messagebox.showerror("Warning", msg)
				State().ClearMoveList()
				self.ChessBoard.remove_highlights()

		tkinter.Button(main_frame, text="Load from file", command=load_from_file, width=BUTTON_WIDTH).pack(anchor="w")
