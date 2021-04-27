import tkinter
from PIL import Image, ImageTk

import moves

def init(master):
	global root
	root = master

	###########################################################
	###					Default parameters					###
	###########################################################
	global parameters
	parameters = dict()

	# Commonly used measurements
	parameters["CHESSBOARD_CANVAS_SIZE"] = 700
	parameters["BOARD_MARGIN"] = int(0.1 * parameters["CHESSBOARD_CANVAS_SIZE"])
	parameters["BOARD_SIZE"] = int(0.8 * parameters["CHESSBOARD_CANVAS_SIZE"])
	parameters["HIGHLIGHT_LINEWIDTH"] = 7
	parameters["HIGHLIGHT_COLOR"] = "blue"

	# Chess
	parameters["CHESS"] = dict()
	parameters["CHESS"]["IMG"] = dict()
	parameters["CHESS"]["PLAYER_COLORS"] = ("white","black")
	parameters["CHESS"]["TYPES_OF_CHESS_PIECES"] = ("king","queen","rook","knight","bishop","pawn")

	parameters["CHESS"]["CHESSBOARD_X_ARRAY"] = 8
	parameters["CHESS"]["CHESSBOARD_Y_ARRAY"] = 8
	parameters["CHESS"]["CELL_SIZE"] = int(parameters["BOARD_SIZE"] / 8)
	parameters["CHESS"]["TEXT_MARGIN"] = 10
	parameters["CHESS"]["PIECE_SIZE"] = int(0.8 * parameters["CHESS"]["CELL_SIZE"])

	parameters["CHESS"]["BOARD_X_START"] = parameters["BOARD_MARGIN"]
	parameters["CHESS"]["BOARD_X_END"] = parameters["BOARD_MARGIN"] + parameters["BOARD_SIZE"]
	parameters["CHESS"]["BOARD_Y_START"] = parameters["BOARD_MARGIN"]
	parameters["CHESS"]["BOARD_Y_END"] = parameters["BOARD_MARGIN"] + parameters["BOARD_SIZE"]

	parameters["CHESS"]["CENTER"] = dict()
	for i in range(parameters["CHESS"]["CHESSBOARD_X_ARRAY"]):
		for j in range(parameters["CHESS"]["CHESSBOARD_Y_ARRAY"]):
			parameters["CHESS"]["CENTER"][(i,j)] = (int((i+0.5)*parameters["CHESS"]["CELL_SIZE"] + parameters["BOARD_MARGIN"]), int((j+0.5)*parameters["CHESS"]["CELL_SIZE"] + parameters["BOARD_MARGIN"]))

	# Xiangqi
	parameters["XIANGQI"] = dict()
	parameters["XIANGQI"]["IMG"] = dict()
	parameters["XIANGQI"]["PLAYER_COLORS"] = ("red","black")
	parameters["XIANGQI"]["TYPES_OF_CHESS_PIECES"] = ("shuai", "shi", "xiang", "ju", "ma", "pao", "bing")

	parameters["XIANGQI"]["CHESSBOARD_X_ARRAY"] = 9
	parameters["XIANGQI"]["CHESSBOARD_Y_ARRAY"] = 10
	parameters["XIANGQI"]["CELL_SIZE"] = int(parameters["BOARD_SIZE"] / 10)
	parameters["XIANGQI"]["TEXT_MARGIN"] = 15
	parameters["XIANGQI"]["PIECE_SIZE"] = int(parameters["XIANGQI"]["CELL_SIZE"])

	parameters["XIANGQI"]["BOARD_X_START"] = parameters["BOARD_MARGIN"] + parameters["XIANGQI"]["CELL_SIZE"] - 0.5*parameters["XIANGQI"]["PIECE_SIZE"]
	parameters["XIANGQI"]["BOARD_X_END"] = parameters["BOARD_MARGIN"] + parameters["BOARD_SIZE"] - parameters["XIANGQI"]["CELL_SIZE"] + 0.5*parameters["XIANGQI"]["PIECE_SIZE"]
	parameters["XIANGQI"]["BOARD_Y_START"] = parameters["BOARD_MARGIN"] + 0.5*parameters["XIANGQI"]["CELL_SIZE"] - 0.5*parameters["XIANGQI"]["PIECE_SIZE"]
	parameters["XIANGQI"]["BOARD_Y_END"] = parameters["BOARD_MARGIN"] + parameters["BOARD_SIZE"] - 0.5*parameters["XIANGQI"]["CELL_SIZE"] + 0.5*parameters["XIANGQI"]["PIECE_SIZE"]

	parameters["XIANGQI"]["CENTER"] = dict()
	for i in range(parameters["XIANGQI"]["CHESSBOARD_X_ARRAY"]):
		for j in range(parameters["XIANGQI"]["CHESSBOARD_Y_ARRAY"]):
			parameters["XIANGQI"]["CENTER"][(i,j)] = (int((i+1)*parameters["XIANGQI"]["CELL_SIZE"] + parameters["BOARD_MARGIN"]), int((j+0.5)*parameters["XIANGQI"]["CELL_SIZE"] + parameters["BOARD_MARGIN"]))



	###########################################################
	###					Default state						###
	###########################################################
	global state
	state = dict()

	state["chess_type"] = "CHESS"
	state["position"] = dict()

	state["CHESS"] = dict()

	# Set initial state for move_list etc
	def function_to_clear_move_list():
		state["active_square"] = 0
		state["move_list"] = list()
		state["previous_player"] = ""
		state["current_move"] = moves.Moves()
		state["current_move_index"] = -1

		if state["chess_type"] == "CHESS":
			state["CHESS"]["CASTLE"] = {"white_short":False, "white_long":False, "black_short":False, "black_long":False}
			castle = state["CHESS"]["CASTLE"]
			
			if (4,7) in state["position"] and state["position"][(4,7)] == "white_king":
				if (7,7) in state["position"] and state["position"][(7,7)] == "white_rook":
					castle["white_short"] = True
				if (0,7) in state["position"] and state["position"][(0,7)] == "white_rook":
					castle["white_long"] = True
			if (4,0) in state["position"] and state["position"][(4,0)] == "black_king":
				if (7,0) in state["position"] and state["position"][(7,0)] == "black_rook":
					castle["black_short"] = True
				if (0,0) in state["position"] and state["position"][(0,0)] == "black_rook":
					castle["black_long"] = True

	state["clear_move_list"] = function_to_clear_move_list

	###########################################################
	###			Read images for chess pieces				###
	###########################################################
	def process_png(chess_piece, img_size):
		img = Image.open("img/" + chess_piece + ".png")

		# Scale image
		longer_side = img.size[0] if img.size[0] > img.size[1] else img.size[1]
		scaling_factor = img_size / longer_side
		scaled_size = (int(scaling_factor*img.size[0]), int(scaling_factor*img.size[1]))
		img = img.resize(scaled_size)

		return ImageTk.PhotoImage(img)

	for chess_type in ("CHESS", "XIANGQI"):
		for color in parameters[chess_type]["PLAYER_COLORS"]:
			for piece in parameters[chess_type]["TYPES_OF_CHESS_PIECES"]:
				chess_piece = color + "_" + piece
				parameters[chess_type]["IMG"][chess_piece] = process_png(chess_piece, parameters[chess_type]["PIECE_SIZE"])
