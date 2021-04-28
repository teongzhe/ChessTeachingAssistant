import tkinter

import settings

class Moves:
	def __init__(self):
		self.player_color = ""

		self.start_piece = ""
		self.start_pos = 0

		self.end_piece = ""
		self.end_pos = 0

		self.piece_taken = ""
		self.piece_taken_pos = ""

		self.disabled_castling = list()


	def details(self):
		print(self.player_color, self.start_piece, "from", self.start_pos, "to", self.end_pos, "taking", self.piece_taken)


	def update(self, state, coordinate):
		selected_piece = ""
		player_color, piece = "", ""
		if coordinate in state["position"]:
			selected_piece = state["position"][coordinate]
			player_color, piece = selected_piece.split("_")
		
		if self.start_piece == "":
			# Select chess piece at specified coordinate
			if selected_piece != "":
				if player_color != state["previous_player"]:
					self.player_color = player_color
					self.start_piece = selected_piece
					self.start_pos = coordinate
					settings.state["highlight_active_square"](coordinate)
		else:
			# Change selection to new chess piece at specified coordinate
			if selected_piece != "" and player_color == self.player_color:
				self.start_piece = selected_piece
				self.start_pos = coordinate
				settings.state["highlight_active_square"](coordinate)
			else:
				if settings.state["chess_type"] == "CHESS":
					self.chess_move_checker(selected_piece, coordinate)
				elif settings.state["chess_type"] == "XIANGQI":
					self.xiangqi_move_checker(selected_piece, coordinate)
					
	def record_end_piece_and_pos(self, selected_piece, coordinate):
		self.end_piece = self.start_piece
		self.end_pos = coordinate
		self.piece_taken = selected_piece
		self.piece_taken_pos = coordinate
		
		settings.state["highlight_active_square"](coordinate)



	###########################################################
	###						Chess							###
	###########################################################
	def chess_move_checker(self, selected_piece, coordinate):
		# King
		if self.start_piece == "white_king":
			if settings.state["CHESS"]["CASTLE"]["white_short"] and coordinate == (6,7) and (5,7) not in settings.state["position"]:
				self.end_piece = self.start_piece
				self.end_pos = coordinate
			elif settings.state["CHESS"]["CASTLE"]["white_long"] and coordinate == (2,7) and (1,7) not in settings.state["position"] and (3,7) not in settings.state["position"]:
				self.end_piece = self.start_piece
				self.end_pos = coordinate
			elif abs(self.start_pos[0] - coordinate[0]) < 2 and abs(self.start_pos[1] - coordinate[1]) < 2:
				self.record_end_piece_and_pos(selected_piece, coordinate)
		elif self.start_piece == "black_king":
			if settings.state["CHESS"]["CASTLE"]["black_short"] and coordinate == (6,0) and (5,0) not in settings.state["position"]:
				self.end_piece = self.start_piece
				self.end_pos = coordinate
			elif settings.state["CHESS"]["CASTLE"]["black_long"] and coordinate == (2,0) and (1,0) not in settings.state["position"] and (3,0) not in settings.state["position"]:
				self.end_piece = self.start_piece
				self.end_pos = coordinate
			elif abs(self.start_pos[0] - coordinate[0]) < 2 and abs(self.start_pos[1] - coordinate[1]) < 2:
				self.record_end_piece_and_pos(selected_piece, coordinate)
		
		# Queen
		elif self.start_piece.split("_")[1] == "queen":
			invalid_move = False
			if self.start_pos[0] == coordinate[0] and self.start_pos[1] != coordinate[1]:
				for i in range(min(self.start_pos[1],coordinate[1])+1, max(self.start_pos[1],coordinate[1])):
					if (self.start_pos[0], i) in settings.state["position"]:
						invalid_move = True
			elif self.start_pos[1] == coordinate[1] and self.start_pos[0] != coordinate[0]:
				for i in range(min(self.start_pos[0],coordinate[0])+1, max(self.start_pos[0],coordinate[0])):
					if (i, self.start_pos[1]) in settings.state["position"]:
						invalid_move = True
			elif abs(self.start_pos[0]-coordinate[0]) == abs(self.start_pos[1]-coordinate[1]):
				x, y = self.start_pos
				x_dir = 1 if self.start_pos[0] < coordinate[0] else -1
				y_dir = 1 if self.start_pos[1] < coordinate[1] else -1
				for i in range(1, abs(self.start_pos[0]-coordinate[0])):
					if (x+i*x_dir, y+i*y_dir) in settings.state["position"]:
						invalid_move = True
			else:
				invalid_move = True
			if not invalid_move:
				self.record_end_piece_and_pos(selected_piece, coordinate)
		
		# Rook
		elif self.start_piece.split("_")[1] == "rook":
			invalid_move = False
			if self.start_pos[0] == coordinate[0]:
				for i in range(min(self.start_pos[1],coordinate[1])+1, max(self.start_pos[1],coordinate[1])):
					if (self.start_pos[0], i) in settings.state["position"]:
						invalid_move = True
			elif self.start_pos[1] == coordinate[1]:
				for i in range(min(self.start_pos[0],coordinate[0])+1, max(self.start_pos[0],coordinate[0])):
					if (i, self.start_pos[1]) in settings.state["position"]:
						invalid_move = True
			else:
				invalid_move = True
			if not invalid_move:
				self.record_end_piece_and_pos(selected_piece, coordinate)

		# Bishop
		elif self.start_piece.split("_")[1] == "bishop":
			invalid_move = False
			if abs(self.start_pos[0]-coordinate[0]) == abs(self.start_pos[1]-coordinate[1]):
				x, y = self.start_pos
				x_dir = 1 if self.start_pos[0] < coordinate[0] else -1
				y_dir = 1 if self.start_pos[1] < coordinate[1] else -1
				for i in range(1, abs(self.start_pos[0]-coordinate[0])):
					if (x+i*x_dir, y+i*y_dir) in settings.state["position"]:
						invalid_move = True
			else:
				invalid_move = True
			if not invalid_move:
				self.record_end_piece_and_pos(selected_piece, coordinate)
		
		# Knight
		elif self.start_piece.split("_")[1] == "knight":
			x_diff = abs(self.start_pos[0] - coordinate[0])
			y_diff = abs(self.start_pos[1] - coordinate[1])
			if (x_diff == 1 and y_diff == 2) or (x_diff == 2 and y_diff == 1):
				self.record_end_piece_and_pos(selected_piece, coordinate)

		# Pawn
		elif self.start_piece == "white_pawn":
			if self.start_pos[0] == coordinate[0] and coordinate not in settings.state["position"]:
				if self.start_pos[1] == 6 and coordinate[1] == 4:
					self.end_piece = self.start_piece
					self.end_pos = coordinate
				elif self.start_pos[1] == coordinate[1] + 1:
					self.end_piece = self.start_piece
					self.end_pos = coordinate
			elif abs(self.start_pos[0] - coordinate[0]) == 1 and self.start_pos[1] == coordinate[1] + 1:
				if coordinate in settings.state["position"] and settings.state["position"][coordinate].split("_")[0] == "black":
					self.record_end_piece_and_pos(selected_piece, coordinate)
				# En passant
				elif self.start_pos[1] == 3 and settings.state["move_list"][-1].start_piece == "black_pawn" and settings.state["move_list"][-1].end_pos[0] == coordinate[0] and settings.state["move_list"][-1].end_pos[1] == settings.state["move_list"][-1].start_pos[1] + 2:
					self.end_piece = self.start_piece
					self.end_pos = coordinate
					self.piece_taken = "black_pawn"
					self.piece_taken_pos = (coordinate[0], coordinate[1]+1)
			if self.end_pos != 0 and self.end_pos[1] == 0:
				self.end_piece = self.pawn_promotion("white")
		elif self.start_piece == "black_pawn":
			if self.start_pos[0] == coordinate[0] and coordinate not in settings.state["position"]:
				if self.start_pos[1] == 1 and coordinate[1] == 3:
					self.record_end_piece_and_pos(selected_piece, coordinate)
				elif self.start_pos[1] == coordinate[1] - 1:
					self.record_end_piece_and_pos(selected_piece, coordinate)
			elif abs(self.start_pos[0] - coordinate[0]) == 1 and self.start_pos[1] == coordinate[1] - 1:
				if coordinate in settings.state["position"] and settings.state["position"][coordinate].split("_")[0] == "white":
					self.record_end_piece_and_pos(selected_piece, coordinate)
				# En passant
				elif self.start_pos[1] == 4 and settings.state["move_list"][-1].start_piece == "white_pawn" and settings.state["move_list"][-1].end_pos[0] == coordinate[0] and settings.state["move_list"][-1].end_pos[1] == settings.state["move_list"][-1].start_pos[1] - 2:
					self.end_piece = self.start_piece
					self.end_pos = coordinate
					self.piece_taken = "black_pawn"
					self.piece_taken_pos = (coordinate[0], coordinate[1]-1)
			if self.end_pos != 0 and self.end_pos[1] == 7:
				self.end_piece = self.pawn_promotion("black")

	def pawn_promotion(self, color):
		class promotion_prompt:
			def __init__(self, master):
				self.piece_to_promote_to = ""

				# Create promotion window
				self.promotion_window = tkinter.Toplevel(master)
				self.promotion_window.title("Promotion")

				def callback(chosen_piece):
					self.piece_to_promote_to = chosen_piece
					self.promotion_window.destroy()

				for piece in settings.parameters["CHESS"]["TYPES_OF_CHESS_PIECES"]:
					if piece != "king" and piece != "pawn":
						chess_piece = color + "_" + piece
						img = settings.parameters["CHESS"]["IMG"][chess_piece]
						img_size = settings.parameters["CHESS"]["PIECE_SIZE"]
						tkinter.Button(self.promotion_window, image=img, command=lambda s=chess_piece:callback(s), width=img_size, height=img_size).pack(side=tkinter.LEFT)
				
				master.wait_window(self.promotion_window)

		promotion = promotion_prompt(settings.root)
		return promotion.piece_to_promote_to

	###########################################################
	###						Xiangqi							###
	###########################################################
	def xiangqi_move_checker(self, selected_piece, coordinate):
		# Shuai
		if self.start_piece == "red_shuai":
			if 3 <= coordinate[0] <= 5 and coordinate[1] > 6 and abs(self.start_pos[0] - coordinate[0]) + abs(self.start_pos[1] - coordinate[1]) == 1:
				self.record_end_piece_and_pos(selected_piece, coordinate)
		elif self.start_piece == "black_shuai":
			if 3 <= coordinate[0] <= 5 and coordinate[1] < 3 and abs(self.start_pos[0] - coordinate[0]) + abs(self.start_pos[1] - coordinate[1]) == 1:
				self.record_end_piece_and_pos(selected_piece, coordinate)

		# Shi
		elif self.start_piece == "red_shi":
			if 3 <= coordinate[0] <= 5 and coordinate[1] > 6 and abs(self.start_pos[0] - coordinate[0]) == abs(self.start_pos[1] - coordinate[1]) == 1:
				self.record_end_piece_and_pos(selected_piece, coordinate)
		elif self.start_piece == "black_shi":
			if coordinate[0] > 2 and coordinate[0] < 3 and coordinate[1] < 3 and abs(self.start_pos[0] - coordinate[0]) == abs(self.start_pos[1] - coordinate[1]) == 1:
				self.record_end_piece_and_pos(selected_piece, coordinate)
		
		# Xiang
		elif self.start_piece == "red_xiang":
			if coordinate[1] > 4 and abs(self.start_pos[0] - coordinate[0]) == abs(self.start_pos[1] - coordinate[1]) == 2 and ((self.start_pos[0]+coordinate[0])//2, (self.start_pos[1]+coordinate[1])//2) not in settings.state["position"]:
				self.record_end_piece_and_pos(selected_piece, coordinate)
		elif self.start_piece == "black_xiang":
			if coordinate[1] < 6 and abs(self.start_pos[0] - coordinate[0]) == abs(self.start_pos[1] - coordinate[1]) == 2 and ((self.start_pos[0]+coordinate[0])//2, (self.start_pos[1]+coordinate[1])//2) not in settings.state["position"]:
				self.record_end_piece_and_pos(selected_piece, coordinate)

		# Ju
		elif self.start_piece.split("_")[1] == "ju":
			invalid_move = False
			if self.start_pos[0] == coordinate[0]:
				for i in range(min(self.start_pos[1],coordinate[1])+1, max(self.start_pos[1],coordinate[1])):
					if (self.start_pos[0], i) in settings.state["position"]:
						invalid_move = True
			elif self.start_pos[1] == coordinate[1]:
				for i in range(min(self.start_pos[0],coordinate[0])+1, max(self.start_pos[0],coordinate[0])):
					if (i, self.start_pos[1]) in settings.state["position"]:
						invalid_move = True
			else:
				invalid_move = True
			if not invalid_move:
				self.record_end_piece_and_pos(selected_piece, coordinate)
		
		# Pao
		elif self.start_piece.split("_")[1] == "pao":
			if self.start_pos[0] == coordinate[0]:
				obstacles = 0
				for i in range(min(self.start_pos[1],coordinate[1])+1, max(self.start_pos[1],coordinate[1])):
					if (self.start_pos[0], i) in settings.state["position"]:
						obstacles += 1
				if selected_piece == '' and obstacles == 0 :
					self.record_end_piece_and_pos(selected_piece, coordinate)
				elif selected_piece != '' and obstacles == 1:
					self.record_end_piece_and_pos(selected_piece, coordinate)
			elif self.start_pos[1] == coordinate[1]:
				obstacles = 0
				for i in range(min(self.start_pos[0],coordinate[0])+1, max(self.start_pos[0],coordinate[0])):
					if (i, self.start_pos[1]) in settings.state["position"]:
						obstacles += 1
				if selected_piece == '' and obstacles == 0 :
					self.record_end_piece_and_pos(selected_piece, coordinate)
				elif selected_piece != '' and obstacles == 1:
					self.record_end_piece_and_pos(selected_piece, coordinate)

		# Ma
		elif self.start_piece.split("_")[1] == "ma":
			x_diff = abs(self.start_pos[0] - coordinate[0])
			y_diff = abs(self.start_pos[1] - coordinate[1])

			if x_diff == 1 and y_diff == 2 and (self.start_pos[0],(self.start_pos[1]+coordinate[1])//2) not in settings.state["position"]:
				self.record_end_piece_and_pos(selected_piece, coordinate)
			elif x_diff == 2 and y_diff == 1 and ((self.start_pos[0]+coordinate[0])//2,self.start_pos[1]) not in settings.state["position"]:
				self.record_end_piece_and_pos(selected_piece, coordinate)

		# Bing
		elif self.start_piece.split("_")[1] == "bing":
			if abs(self.start_pos[0] - coordinate[0]) + abs(self.start_pos[1] - coordinate[1]) == 1:
				if self.player_color == "red" and self.start_pos[1] >= coordinate[1]:
					if coordinate[1] < 5:
						self.record_end_piece_and_pos(selected_piece, coordinate)
					elif self.start_pos[0] == coordinate[0]:
						self.record_end_piece_and_pos(selected_piece, coordinate)
				elif self.player_color == "black" and self.start_pos[1] <= coordinate[1]:
					if coordinate[1] > 4:
						self.record_end_piece_and_pos(selected_piece, coordinate)
					elif self.start_pos[0] == coordinate[0]:
						self.record_end_piece_and_pos(selected_piece, coordinate)
