import moves
import ImgProcessor


def InitializeDimensions():
	parameters["CanvasSize"] = 700
	parameters["BoardMargin"] = 0.05 * parameters["CanvasSize"]
	parameters["BoardSize"] = 0.9 * parameters["CanvasSize"]

	parameters["CellSize"] = dict()
	for ChessType in parameters["TypesOfChess"]:
		parameters["CellSize"][ChessType] = parameters["BoardSize"] / max(parameters[ChessType]["ChessboardXArray"], parameters[ChessType]["ChessboardYArray"])
	
	parameters["PieceSize"] = dict()
	parameters["PieceSize"]["Chess"] = 0.8 * parameters["CellSize"]["Chess"]
	parameters["PieceSize"]["XiangQi"] = 0.98 * parameters["CellSize"]["XiangQi"]


def init(master):
	global root
	root = master

	###########################################################
	###					Default parameters					###
	###########################################################
	global parameters
	parameters = dict()

	

	# types of chess available
	parameters["TypesOfChess"] = ("Chess", "XiangQi")
	for ChessType in parameters["TypesOfChess"]:
		parameters[ChessType] = dict()
	
	# Chess
	parameters["Chess"]["PlayerColors"] = ("white", "black")
	parameters["Chess"]["TypesOfChessPieces"] = ("king", "queen", "rook", "knight", "bishop", "pawn")
	parameters["Chess"]["ChessboardXArray"] = 8
	parameters["Chess"]["ChessboardYArray"] = 8

	# XiangQi
	parameters["XiangQi"]["PlayerColors"] = ("red", "black")
	parameters["XiangQi"]["TypesOfChessPieces"] = ("shuai", "shi", "xiang", "ju", "ma", "pao", "bing")
	parameters["XiangQi"]["ChessboardXArray"] = 9
	parameters["XiangQi"]["ChessboardYArray"] = 10

	InitializeDimensions()
	ImgProcessor.InitChessPieceImages()


	# Chess
	parameters["CHESS"] = dict()
	parameters["CHESS"]["PLAYER_COLORS"] = ("white","black")
	parameters["CHESS"]["TYPES_OF_CHESS_PIECES"] = ("king","queen","rook","knight","bishop","pawn")
	parameters["CHESS"]["CHESSBOARD_X_ARRAY"] = 8
	parameters["CHESS"]["CHESSBOARD_Y_ARRAY"] = 8

	# Xiangqi
	parameters["XIANGQI"] = dict()
	parameters["XIANGQI"]["PLAYER_COLORS"] = ("red","black")
	parameters["XIANGQI"]["TYPES_OF_CHESS_PIECES"] = ("shuai", "shi", "xiang", "ju", "ma", "pao", "bing")
	parameters["XIANGQI"]["CHESSBOARD_X_ARRAY"] = 9
	parameters["XIANGQI"]["CHESSBOARD_Y_ARRAY"] = 10



	###########################################################
	###					Default state						###
	###########################################################
	global state
	state = dict()

	state["chess_type"] = "CHESS"
	state["position"] = dict()

	state["saved_caption"] = ""
	state["quick_save_position"] = dict()

	state["CHESS"] = dict()
	state["XIANGQI"] = dict()

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
