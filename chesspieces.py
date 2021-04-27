import tkinter

import settings

class ChessPieces:
	def __init__(self, frame, chessboard):
		self.frame = frame
		self.initialize_menu()

	def initialize_menu(self):
		for widget in self.frame.winfo_children():
			widget.destroy()

		self.add_menu()


	def add_menu(self):
		colors = settings.parameters[settings.state["chess_type"]]["PLAYER_COLORS"]
		pieces = settings.parameters[settings.state["chess_type"]]["TYPES_OF_CHESS_PIECES"]
		
		settings.state["game_is_ongoing"] = True
		settings.state["selected_piece_to_add_to_board"] = "deselect"
		var = tkinter.StringVar(value="deselect")
		def callback():
			if settings.state["selected_piece_to_add_to_board"] != var.get():
				if var.get() != "deselect":
					settings.state["clear_move_list"]()

				settings.state["selected_piece_to_add_to_board"] = var.get()
				settings.state["game_is_ongoing"] = True if var.get() == "deselect" else False
		
		for piece in pieces:
			temp_frame = tkinter.Frame(self.frame)
			temp_frame.pack(anchor="w")
			for color in colors:
				temp_str = color + "_" + piece
				img = settings.parameters[settings.state["chess_type"]]["IMG"][temp_str]
				radiobtn_size = settings.parameters[settings.state["chess_type"]]["PIECE_SIZE"]

				radiobtn = tkinter.Radiobutton(temp_frame, command=callback, variable=var, value=temp_str, image=img, indicatoron=0, width=radiobtn_size, height=radiobtn_size)
				radiobtn.image = img
				radiobtn.pack(side=tkinter.LEFT)

		tkinter.Radiobutton(self.frame, command=callback, variable=var, value="remove", text="Remove").pack(anchor="w")
		tkinter.Radiobutton(self.frame, command=callback, variable=var, value="deselect", text="Deselect").pack(anchor="w")
