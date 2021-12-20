import tkinter
import copy

from settings import Parameters, State
from ImgProcessor import *


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

	def __str__(self):
		endPosString, pieceTakenString = "", ""
		if self.end_pos != 0:
			endPosString = " to ({},{})".format(self.end_pos[0], self.end_pos[1])
			if self.piece_taken != "":
				pieceTakenString = " taking {} at ({},{})".format(self.piece_taken, self.piece_taken_pos[0], self.piece_taken_pos[1])
		return "{} from ({},{}){}{}".format(self.start_piece, self.start_pos[0], self.start_pos[1], endPosString, pieceTakenString)



	def update(self, coordinate):
		player_color, piece = "", ""
		if coordinate in settings.State().GetChessPiecePositions():
			player_color, piece = settings.State().GetChessPieceAtPosition(coordinate)
		selected_piece = player_color + "_" + piece
		
		if self.start_piece == "":
			# Select chess piece at specified coordinate
			if selected_piece != "":
				if player_color != settings.State().GetPreviousPlayer():
					self.player_color = player_color
					self.start_piece = selected_piece
					self.start_pos = coordinate
		else:
			# Change selection to new chess piece at specified coordinate
			if selected_piece != "" and player_color == self.player_color:
				self.start_piece = selected_piece
				self.start_pos = coordinate
			else:
				if settings.State().GetChessType() == "Chess":
					self.chess_move_checker(selected_piece, coordinate)
				elif settings.State().GetChessType() == "XiangQi":
					self.xiangqi_move_checker(selected_piece, coordinate)
					
	def record_end_piece_and_pos(self, selected_piece, coordinate):
		self.end_piece = self.start_piece
		self.end_pos = coordinate
		self.piece_taken = selected_piece
		self.piece_taken_pos = coordinate
		


	###########################################################
	###						Chess							###
	###########################################################
	def chess_move_checker(self, selected_piece, coordinate):
		# King
		if self.start_piece == "white_king":
			if settings.state["CHESS"]["CASTLE"]["white_short"] and coordinate == (6,7) and (5,7) not in settings.State().GetChessPiecePositions():
				self.end_piece = self.start_piece
				self.end_pos = coordinate
			elif settings.state["CHESS"]["CASTLE"]["white_long"] and coordinate == (2,7) and (1,7) not in settings.State().GetChessPiecePositions() and (3,7) not in settings.State().GetChessPiecePositions():
				self.end_piece = self.start_piece
				self.end_pos = coordinate
			elif abs(self.start_pos[0] - coordinate[0]) < 2 and abs(self.start_pos[1] - coordinate[1]) < 2:
				self.record_end_piece_and_pos(selected_piece, coordinate)
		elif self.start_piece == "black_king":
			if settings.state["CHESS"]["CASTLE"]["black_short"] and coordinate == (6,0) and (5,0) not in settings.State().GetChessPiecePositions():
				self.end_piece = self.start_piece
				self.end_pos = coordinate
			elif settings.state["CHESS"]["CASTLE"]["black_long"] and coordinate == (2,0) and (1,0) not in settings.State().GetChessPiecePositions() and (3,0) not in settings.State().GetChessPiecePositions():
				self.end_piece = self.start_piece
				self.end_pos = coordinate
			elif abs(self.start_pos[0] - coordinate[0]) < 2 and abs(self.start_pos[1] - coordinate[1]) < 2:
				self.record_end_piece_and_pos(selected_piece, coordinate)
		
		# Queen
		elif self.start_piece.split("_")[1] == "queen":
			invalid_move = False
			if self.start_pos[0] == coordinate[0] and self.start_pos[1] != coordinate[1]:
				for i in range(min(self.start_pos[1],coordinate[1])+1, max(self.start_pos[1],coordinate[1])):
					if (self.start_pos[0], i) in settings.State().GetChessPiecePositions():
						invalid_move = True
			elif self.start_pos[1] == coordinate[1] and self.start_pos[0] != coordinate[0]:
				for i in range(min(self.start_pos[0],coordinate[0])+1, max(self.start_pos[0],coordinate[0])):
					if (i, self.start_pos[1]) in settings.State().GetChessPiecePositions():
						invalid_move = True
			elif abs(self.start_pos[0]-coordinate[0]) == abs(self.start_pos[1]-coordinate[1]):
				x, y = self.start_pos
				x_dir = 1 if self.start_pos[0] < coordinate[0] else -1
				y_dir = 1 if self.start_pos[1] < coordinate[1] else -1
				for i in range(1, abs(self.start_pos[0]-coordinate[0])):
					if (x+i*x_dir, y+i*y_dir) in settings.State().GetChessPiecePositions():
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
					if (self.start_pos[0], i) in settings.State().GetChessPiecePositions():
						invalid_move = True
			elif self.start_pos[1] == coordinate[1]:
				for i in range(min(self.start_pos[0],coordinate[0])+1, max(self.start_pos[0],coordinate[0])):
					if (i, self.start_pos[1]) in settings.State().GetChessPiecePositions():
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
					if (x+i*x_dir, y+i*y_dir) in settings.State().GetChessPiecePositions():
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
			if 3 <= coordinate[0] <= 5 and coordinate[1] < 3 and abs(self.start_pos[0] - coordinate[0]) == abs(self.start_pos[1] - coordinate[1]) == 1:
				self.record_end_piece_and_pos(selected_piece, coordinate)
		
		# Xiang
		elif self.start_piece == "red_xiang":
			if coordinate[1] > 4 and abs(self.start_pos[0] - coordinate[0]) == abs(self.start_pos[1] - coordinate[1]) == 2 and ((self.start_pos[0]+coordinate[0])//2, (self.start_pos[1]+coordinate[1])//2) not in settings.State().GetChessPiecePositions():
				self.record_end_piece_and_pos(selected_piece, coordinate)
		elif self.start_piece == "black_xiang":
			if coordinate[1] < 6 and abs(self.start_pos[0] - coordinate[0]) == abs(self.start_pos[1] - coordinate[1]) == 2 and ((self.start_pos[0]+coordinate[0])//2, (self.start_pos[1]+coordinate[1])//2) not in settings.State().GetChessPiecePositions():
				self.record_end_piece_and_pos(selected_piece, coordinate)

		# Ju
		elif self.start_piece.split("_")[1] == "ju":
			invalid_move = False
			if self.start_pos[0] == coordinate[0]:
				for i in range(min(self.start_pos[1],coordinate[1])+1, max(self.start_pos[1],coordinate[1])):
					if (self.start_pos[0], i) in settings.State().GetChessPiecePositions():
						invalid_move = True
			elif self.start_pos[1] == coordinate[1]:
				for i in range(min(self.start_pos[0],coordinate[0])+1, max(self.start_pos[0],coordinate[0])):
					if (i, self.start_pos[1]) in settings.State().GetChessPiecePositions():
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
					if (self.start_pos[0], i) in settings.State().GetChessPiecePositions():
						obstacles += 1
				if selected_piece == '' and obstacles == 0 :
					self.record_end_piece_and_pos(selected_piece, coordinate)
				elif selected_piece != '' and obstacles == 1:
					self.record_end_piece_and_pos(selected_piece, coordinate)
			elif self.start_pos[1] == coordinate[1]:
				obstacles = 0
				for i in range(min(self.start_pos[0],coordinate[0])+1, max(self.start_pos[0],coordinate[0])):
					if (i, self.start_pos[1]) in settings.State().GetChessPiecePositions():
						obstacles += 1
				if selected_piece == '' and obstacles == 0 :
					self.record_end_piece_and_pos(selected_piece, coordinate)
				elif selected_piece != '' and obstacles == 1:
					self.record_end_piece_and_pos(selected_piece, coordinate)

		# Ma
		elif self.start_piece.split("_")[1] == "ma":
			x_diff = abs(self.start_pos[0] - coordinate[0])
			y_diff = abs(self.start_pos[1] - coordinate[1])

			if x_diff == 1 and y_diff == 2 and (self.start_pos[0],(self.start_pos[1]+coordinate[1])//2) not in settings.State().GetChessPiecePositions():
				self.record_end_piece_and_pos(selected_piece, coordinate)
			elif x_diff == 2 and y_diff == 1 and ((self.start_pos[0]+coordinate[0])//2,self.start_pos[1]) not in settings.State().GetChessPiecePositions():
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


class Move:
	def __init__(self):
		self.__PlayerColor = None
		self.__StartPiece = None
		self.__StartPos = None
		self.__EndPiece = None
		self.__EndPos = None
		self.__TakenPiece = None
		self.__TakenPiecePos = None
		self.__DisabledCastleTypes = list()

	def __str__(self):
		EndPosString, PieceTakenString = "", ""
		if self.GetEndPos() != None:
			EndPosString = " to {}".format(self.GetEndPos())
			if self.GetPieceTaken() != None:
				PieceTakenString = " taking {} at {}".format(self.GetPieceTaken(), self.GetPieceTakenPos())
		return "{} {} from {}{}{}".format(self.GetPlayerColor(), self.GetStartPiece(), self.GetStartPos(), EndPosString, PieceTakenString)

	def GetPlayerColor(self):
		return self.__PlayerColor
	def GetStartPiece(self):
		return self.__StartPiece
	def GetStartPos(self):
		return self.__StartPos
	def GetEndPiece(self):
		return self.__EndPiece
	def GetEndPos(self):
		return self.__EndPos
	def GetPieceTaken(self):
		return self.__TakenPiece
	def GetPieceTakenPos(self):
		return self.__TakenPiecePos
	def GetDisabledCastleTypes(self):
		return self.__DisabledCastleTypes

	def SetStartPieceAndPos(self, PlayerColor, PieceType, Position):
		self.__PlayerColor = PlayerColor
		self.__StartPiece = PieceType
		self.__StartPos = Position
	def SetEndPiece(self, PieceType):
		self.__EndPiece = PieceType
	def SetEndPos(self, Position):
		if State().GetChessPieceAtPosition(Position) != None:
			self.SetTakenPieceAndPos(State().GetChessPieceAtPosition(Position), Position)
		self.__EndPiece = self.GetStartPiece()
		self.__EndPos = Position
	def SetTakenPieceAndPos(self, PieceType, Position):
		self.__TakenPiece = PieceType
		self.__TakenPiecePos = Position
	def SetTakenPieceAndPos(self, PieceType, Position):
		self.__TakenPiece = PieceType
		self.__TakenPiecePos = Position
	def SetDisabledCastleTypes(self, CastleType):
		self.__DisabledCastleTypes.append(CastleType)


class MoveHandler:
	__instance = None
	__data = None
	def __new__(self, chessboard = None):
		if not self.__instance:
			if chessboard != None:
				self.__instance = super(MoveHandler, self).__new__(self)
				self.__ChessBoard = chessboard
				self.__instance.__initialize()
			else:
				print("Failed to initialize MoveHandler, please initiate chessboard first and pass as argument!")
				exit(1)
		return self.__instance

	def __initialize(self):
		self.__data = {
			"Castling"		: dict(),
			"MoveList"		: list(),
			"MoveIndex"		: 0,
			"CurrentMove"	: Move(),
		}
		self.ResetCastlingStatus()


	def ResetCastlingStatus(self):
		for color, KingYCoordinate in {"white": 7, "black": 0}.items():
			KingPiece = State().GetChessPieceAtPosition((4, KingYCoordinate))
			if KingPiece["PlayerColor"] == color and KingPiece["PieceType"] == "king":
				for CastleType, RookXCoordinate in {"Long": 0, "Short": 7}.items():
					RookPiece = State().GetChessPieceAtPosition((RookXCoordinate, KingYCoordinate))
					if RookPiece["PlayerColor"] == color and RookPiece["PieceType"] == "rook":
						self.SetCastlingStatus(color, CastleType, True)
					else:
						self.SetCastlingStatus(color, CastleType, False)
			else:
				for CastleType in ("Long", "Short"):
					self.SetCastlingStatus(color,  CastleType, False)
		
	def SetCastlingStatus(self, PlayerColor, CastleType, Status):
		self.__data["Castling"][(PlayerColor, CastleType)] = Status
	def GetCastlingStatus(self, PlayerColor, CastleType):
		return self.__data["Castling"][(PlayerColor, CastleType)]

	def GetPreviousMove(self):
		index = self.GetMoveIndex()
		if index == 0:
			return None
		return self.__data["MoveList"][index-1]
	def GetCurrentMove(self):
		return self.__data["CurrentMove"]

	def IncrementMoveIndex(self):
		self.__data["MoveIndex"] += 1
	def DecrementMoveIndex(self):
		self.__data["MoveIndex"] -= 1
	def GetMoveIndex(self):
		return self.__data["MoveIndex"]


	def Process(self, coordinate):
		SelectedPiece = State().GetChessPieceAtPosition(coordinate)
		PlayerColor = SelectedPiece["PlayerColor"]
		PieceType = SelectedPiece["PieceType"]

		if self.GetCurrentMove().GetStartPiece() == None:
			if PieceType != None and (self.GetMoveIndex() == 0 or self.GetPreviousMove().GetPlayerColor() != PlayerColor):
				self.GetCurrentMove().SetStartPieceAndPos(PlayerColor, PieceType, coordinate)
				self.__ChessBoard.remove_highlights()
				self.__ChessBoard.add_highlight(coordinate)
		else:
			if PieceType != None and PlayerColor == self.GetCurrentMove().GetPlayerColor():
				self.GetCurrentMove().SetStartPieceAndPos(PlayerColor, PieceType, coordinate)
				self.__ChessBoard.remove_highlights()
				self.__ChessBoard.add_highlight(coordinate)
			else:
				ChessType = State().GetChessType()
				if ChessType == "Chess":
					self.ChessMove(coordinate)
				elif ChessType == "XiangQi":
					self.XiangQiMove(coordinate)


	def ChessMove(self, coordinate):
		StartPiece = self.GetCurrentMove().GetStartPiece()
		if StartPiece == None:
			print("An error occured when getting StartPiece for CurrentMove in MoveHandler!")
			exit(1)

		isValidMove = False
		if StartPiece == "king":
			isValidMove = self.KingMove(coordinate)
		elif StartPiece == "queen":
			isValidMove = self.QueenMove(coordinate)
		elif StartPiece == "rook":
			isValidMove = self.RookMove(coordinate)
		elif StartPiece == "bishop":
			isValidMove = self.BishopMove(coordinate)
		elif StartPiece == "knight":
			isValidMove = self.KnightMove(coordinate)
		elif StartPiece == "pawn":
			isValidMove = self.PawnMove(coordinate)

		if isValidMove:
			self.RegisterMove()

	def XiangQiMove(self, coordinate):
		print("XiangQi move validator")


	def TakeBackMove(self):
		print("Take back move")

	def UndoTakeBack(self):
		print("Undo take back")

	def RegisterMove(self):
		CurrentMove = self.GetCurrentMove()
		self.__ChessBoard.RemovePieceFromBoard(CurrentMove.GetPieceTakenPos())
		self.__ChessBoard.RemovePieceFromBoard(CurrentMove.GetStartPos())
		self.__ChessBoard.AddPieceToBoard(CurrentMove.GetPlayerColor(), CurrentMove.GetEndPiece(), CurrentMove.GetEndPos())
		self.__ChessBoard.add_highlight(CurrentMove.GetEndPos())

		self.__data["MoveList"].append(copy.deepcopy(self.GetCurrentMove()))
		self.__data["CurrentMove"] = Move()
		self.IncrementMoveIndex()


	def KingMove(self, coordinate):
		CurrentMove = self.GetCurrentMove()
		PlayerColor = CurrentMove.GetPlayerColor()
		isValidMove = False

		if abs(coordinate[0] - CurrentMove.GetStartPos()[0]) <= 1 and abs(coordinate[1] - CurrentMove.GetStartPos()[1]) <= 1:
			isValidMove = True
		elif abs(coordinate[0] - CurrentMove.GetStartPos()[0]) == 2 and coordinate[1] == CurrentMove.GetStartPos()[1]:
			CastleType = {2: "Long", 6: "Short"}
			RookPos = {"Long": 0, "Short": 7}
			if coordinate[0] in CastleType.keys():
				if self.GetCastlingStatus(PlayerColor, CastleType[coordinate[0]]):
					isBlocked = False
					CheckRange = (coordinate[0], RookPos[CastleType[coordinate[0]]])
					CheckRange = (min(CheckRange), max(CheckRange))
					for i in range(CheckRange[0] + 1, CheckRange[1]):
						if State().GetChessPieceAtPosition((i, coordinate[1])) != None:
							isBlocked = True
							break
					
					if not isBlocked:
						self.__ChessBoard.RemovePieceFromBoard((RookPos[CastleType[coordinate[0]]], coordinate[1]))
						RookEndCoordinate = ((coordinate[0] + CurrentMove.GetStartPos()[0]) // 2, coordinate[1])
						self.__ChessBoard.AddPieceToBoard(PlayerColor, "rook", RookEndCoordinate)
						isValidMove = True

		if isValidMove:
			for CastleType in ("Long", "Short"):
				self.SetCastlingStatus(PlayerColor, CastleType, False)
				self.GetCurrentMove().SetDisabledCastleTypes(CastleType)
			self.GetCurrentMove().SetEndPos(coordinate)
			return True
		return False

	def QueenMove(self, coordinate):
		CurrentMove = self.GetCurrentMove()
		isValidMove = False

		if coordinate[0] == CurrentMove.GetStartPos()[0]:
			isValidMove = True
			CheckRange = (coordinate[1], CurrentMove.GetStartPos()[1])
			CheckRange = (min(CheckRange), max(CheckRange))
			for i in range(CheckRange[0] + 1, CheckRange[1]):
				if State().GetChessPieceAtPosition((coordinate[0], i))["PieceType"] != None:
					isValidMove = False
					break
		elif coordinate[1] == CurrentMove.GetStartPos()[1]:
			isValidMove = True
			CheckRange = (coordinate[0], CurrentMove.GetStartPos()[0])
			CheckRange = (min(CheckRange), max(CheckRange))
			for i in range(CheckRange[0] + 1, CheckRange[1]):
				if State().GetChessPieceAtPosition((i, coordinate[1]))["PieceType"] != None:
					isValidMove = False
					break
		elif abs(coordinate[0] - CurrentMove.GetStartPos()[0]) == abs(coordinate[1] - CurrentMove.GetStartPos()[1]):
			isValidMove = True
			x, y = CurrentMove.GetStartPos()
			xDirection = 1 if CurrentMove.GetStartPos()[0] < coordinate[0] else -1
			yDirection = 1 if CurrentMove.GetStartPos()[1] < coordinate[1] else -1
			for i in range(1, abs(CurrentMove.GetStartPos()[0] - coordinate[0])):
				if State().GetChessPieceAtPosition((x+i*xDirection, y+i*yDirection))["PieceType"] != None:
					isValidMove = False
					break

		if isValidMove:
			self.GetCurrentMove().SetEndPos(coordinate)
			return True
		return False

	def RookMove(self, coordinate):
		CurrentMove = self.GetCurrentMove()
		PlayerColor = CurrentMove.GetPlayerColor()
		isValidMove = False

		if coordinate[0] == CurrentMove.GetStartPos()[0]:
			isValidMove = True
			CheckRange = (coordinate[1], CurrentMove.GetStartPos()[1])
			CheckRange = (min(CheckRange), max(CheckRange))
			for i in range(CheckRange[0] + 1, CheckRange[1]):
				if State().GetChessPieceAtPosition((coordinate[0], i))["PieceType"] != None:
					isValidMove = False
					break
		elif coordinate[1] == CurrentMove.GetStartPos()[1]:
			isValidMove = True
			CheckRange = (coordinate[0], CurrentMove.GetStartPos()[0])
			CheckRange = (min(CheckRange), max(CheckRange))
			for i in range(CheckRange[0] + 1, CheckRange[1]):
				if State().GetChessPieceAtPosition((i, coordinate[1]))["PieceType"] != None:
					isValidMove = False
					break

		if isValidMove:
			self.GetCurrentMove().SetEndPos(coordinate)
			if CurrentMove().GetStartPos()[0] == 0 and self.GetCastlingStatus(PlayerColor, "Long"):
				self.SetCastlingStatus(PlayerColor, "Long", False)
				self.GetCurrentMove().SetDisabledCastleTypes("Long")
			elif CurrentMove().GetStartPos()[0] == 7 and self.GetCastlingStatus(PlayerColor, "Short"):
				self.SetCastlingStatus(PlayerColor, "Short", False)
				self.GetCurrentMove().SetDisabledCastleTypes("Short")
			return True
		return False

	def BishopMove(self, coordinate):
		CurrentMove = self.GetCurrentMove()
		isValidMove = False

		if abs(coordinate[0] - CurrentMove.GetStartPos()[0]) == abs(coordinate[1] - CurrentMove.GetStartPos()[1]):
			isValidMove = True
			x, y = CurrentMove.GetStartPos()
			xDirection = 1 if CurrentMove.GetStartPos()[0] < coordinate[0] else -1
			yDirection = 1 if CurrentMove.GetStartPos()[1] < coordinate[1] else -1
			for i in range(1, abs(CurrentMove.GetStartPos()[0] - coordinate[0])):
				if State().GetChessPieceAtPosition((x+i*xDirection, y+i*yDirection))["PieceType"] != None:
					isValidMove = False
					break

		if isValidMove:
			self.GetCurrentMove().SetEndPos(coordinate)
			return True
		return False

	def KnightMove(self, coordinate):
		CurrentMove = self.GetCurrentMove()
		isValidMove = False
		xDiff = abs(coordinate[0] - CurrentMove.GetStartPos()[0])
		yDiff = abs(coordinate[1] - CurrentMove.GetStartPos()[1])
		if xDiff == 1 and yDiff == 2:
			isValidMove = True
		elif xDiff == 2 and yDiff == 1:
			isValidMove = True

		if isValidMove:
			self.GetCurrentMove().SetEndPos(coordinate)
			return True
		return False
	
	def PawnMove(self, coordinate):
		PieceType = "pawn"
		CurrentMove = self.GetCurrentMove()
		PlayerColor = CurrentMove.GetPlayerColor()
		isValidMove = False
		if PlayerColor == "white":
			StartingRow = 6
			MoveDirection = -1
		else:
			StartingRow = 1
			MoveDirection = 1

		# Check if pawn is moving straight
		if coordinate[0] == CurrentMove.GetStartPos()[0]:
			StepsTaken = coordinate[1] - CurrentMove.GetStartPos()[1]
			if StepsTaken == MoveDirection:
				isValidMove = True
			elif CurrentMove.GetStartPos()[1] == StartingRow and StepsTaken == MoveDirection * 2:
				isValidMove = True

		# Check if pawn is taking another piece
		elif abs(coordinate[0] - CurrentMove.GetStartPos()[0]) == 1 and coordinate[1] - CurrentMove.GetStartPos()[1] == MoveDirection:
			TakenPiece = State().GetChessPieceAtPosition(coordinate)
			if TakenPiece["PieceType"] != None:
				isValidMove = True
			# En passant
			else:
				EnPassantEndingRow = {"white": 2, "black": 5}
				if coordinate[1] == EnPassantEndingRow[PlayerColor]:
					EnemyPawnPos = (coordinate[0], CurrentMove.GetStartPos()[1])
					EnemyPawn = State().GetChessPieceAtPosition(EnemyPawnPos)
					if EnemyPawn["PlayerColor"] != PlayerColor and EnemyPawn["PieceType"] == PieceType:
						if self.GetMoveIndex() == 0:
							self.GetCurrentMove().SetTakenPiecePos(PieceType, coordinate)
							isValidMove = True
						elif self.GetPreviousMove().GetStartPiece() == PieceType and self.GetPreviousMove().GetEndPos()[0] == coordinate[0] and abs(self.GetPreviousMove().GetStartPos()[1] - self.GetPreviousMove().GetEndPos()[1]) == 2:
							self.GetCurrentMove().SetTakenPieceAndPos(PieceType, EnemyPawnPos)
							isValidMove = True

		def PawnPromotion(color):
			class PromotionPrompt:
				def __init__(self, root):
					self.PieceToPromoteTo = None

					self.PromotionWindow = tkinter.Toplevel(root)
					self.PromotionWindow.title("Promotion")

					def callback(ChosenPiece):
						self.PieceToPromoteTo = ChosenPiece
						self.PromotionWindow.destroy()
					
					for PieceType in Parameters().GetTypesOfChessPieces("Chess"):
						if PieceType != "king" and PieceType != "pawn":
							ImgName = color + "_" + PieceType
							ButtonSize = Parameters().GetCellSize("Chess")
							img = ImgProcessor().GetPhotoImage("Chess", ImgName)
							bt = tkinter.Button(self.PromotionWindow, image = img, command = lambda s = PieceType : callback(s), width = ButtonSize, height = ButtonSize)
							bt.image = img
							bt.pack(side = tkinter.LEFT)

					root.wait_window(self.PromotionWindow)

			promotion = PromotionPrompt(Parameters().GetRoot())
			if promotion.PieceToPromoteTo == None:
				return "queen"
			return promotion.PieceToPromoteTo

		if isValidMove:
			self.GetCurrentMove().SetEndPos(coordinate)
			PromotionRow = {"white": 0, "black": 7}
			if coordinate[1] == PromotionRow[PlayerColor]:
				self.GetCurrentMove().SetEndPiece(PawnPromotion(PlayerColor))
			return True
		return False
