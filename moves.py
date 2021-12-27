import tkinter
import copy

from settings import Parameters, State
from ImgProcessor import *


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
			if self.GetTakenPiecePos() != None:
				PieceTaken = self.GetTakenPiece()
				PieceTakenString = " taking {} {} at {}".format(PieceTaken["PlayerColor"], PieceTaken["PieceType"], self.GetTakenPiecePos())
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
	def GetTakenPiece(self):
		return self.__TakenPiece
	def GetTakenPiecePos(self):
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
		ChessPiece = State().GetChessPieceAtPosition(Position)
		if ChessPiece != None:
			self.SetTakenPieceAndPos(ChessPiece, Position)
		self.__EndPiece = self.GetStartPiece()
		self.__EndPos = Position
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
					if RookPiece == None:
						continue
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
	def GetMoveListLength(self):
		return len(self.__data["MoveList"])

	def IncrementMoveIndex(self):
		self.__data["MoveIndex"] += 1
	def DecrementMoveIndex(self):
		self.__data["MoveIndex"] -= 1
	def GetMoveIndex(self):
		return self.__data["MoveIndex"]
	def GetMoveFromIndex(self):
		return self.__data["MoveList"][self.GetMoveIndex()-1]

	def GetCastleTypeFromXCoordinate(self, xCoordinate):
		if xCoordinate == 2:
			return "Long"
		if xCoordinate == 6:
			return "Short"
		return None
	def GetPlayerColorFromYCoordinate(self, yCoordinate):
		if yCoordinate == 7:
			return Parameters().GetPlayerColors()[0]
		if yCoordinate == 0:
			return Parameters().GetPlayerColors()[1]
		return None


	def Process(self, coordinate):
		SelectedPiece = State().GetChessPieceAtPosition(coordinate)
		PlayerColor, PieceType = None, None
		if SelectedPiece != None:
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
		StartPiece = self.GetCurrentMove().GetStartPiece()
		if StartPiece == None:
			print("An error occured when getting StartPiece for CurrentMove in MoveHandler!")
			exit(1)
		
		isValidMove = False
		if StartPiece == "shuai":
			isValidMove = self.ShuaiMove(coordinate)
		elif StartPiece == "shi":
			isValidMove = self.ShiMove(coordinate)
		elif StartPiece == "xiang":
			isValidMove = self.XiangMove(coordinate)
		elif StartPiece == "ju":
			isValidMove = self.JuMove(coordinate)
		elif StartPiece == "pao":
			isValidMove = self.PaoMove(coordinate)
		elif StartPiece == "ma":
			isValidMove = self.MaMove(coordinate)
		elif StartPiece == "bing":
			isValidMove = self.BingMove(coordinate)
		
		if isValidMove:
			self.RegisterMove()


	def TakeBackMove(self):
		if self.GetMoveIndex() > 0:
			move = self.GetMoveFromIndex()
			self.DecrementMoveIndex()

			# Check for castling
			if move.GetStartPiece() == "king" and abs(move.GetStartPos()[0] - move.GetEndPos()[0]) == 2:
				RookPos = ((move.GetStartPos()[0] + move.GetEndPos()[0]) // 2, move.GetStartPos()[1])
				self.__ChessBoard.RemovePieceFromBoard(RookPos)

				CastleType = self.GetCastleTypeFromXCoordinate(move.GetEndPos())
				if CastleType == "Long":
					RookPos = (0, RookPos[1])
				else:
					RookPos = (7, RookPos[1])
				self.__ChessBoard.AddPieceToBoard(move.GetPlayerColor(), "rook", RookPos)
			
			# Reverse move
			self.__ChessBoard.RemovePieceFromBoard(move.GetEndPos())
			self.__ChessBoard.AddPieceToBoard(move.GetPlayerColor(), move.GetStartPiece(), move.GetStartPos())

			TakenPiece = move.GetTakenPiece()
			if TakenPiece != None:
				self.__ChessBoard.AddPieceToBoard(TakenPiece["PlayerColor"], TakenPiece["PieceType"], move.GetTakenPiecePos())
			
			for CastleType in move.GetDisabledCastleTypes():
				self.SetCastlingStatus(move.GetPlayerColor(), CastleType, True)
			
			self.__ChessBoard.remove_highlights()
			self.__ChessBoard.add_highlight(move.GetStartPos())
			self.__ChessBoard.add_highlight(move.GetEndPos())

	def UndoTakeBack(self):
		index = self.GetMoveIndex()
		if index < self.GetMoveListLength():
			self.IncrementMoveIndex()
			move = self.GetMoveFromIndex()

			if move.GetStartPiece() == "king" and abs(move.GetStartPos()[0] - move.GetEndPos()[0]) == 2:
				RookPos = ((move.GetStartPos()[0] + move.GetEndPos()[0]) // 2, move.GetStartPos()[1])
				self.__ChessBoard.AddPieceToBoard(move.GetPlayerColor(), "rook", RookPos)

				CastleType = self.GetCastleTypeFromXCoordinate(move.GetEndPos())
				if CastleType == "Long":
					RookPos = (0, RookPos[1])
				else:
					RookPos = (7, RookPos[1])
				self.__ChessBoard.RemovePieceFromBoard(RookPos)

			# Forward move
			TakenPiece = move.GetTakenPiece()
			if TakenPiece != None:
				self.__ChessBoard.RemovePieceFromBoard(move.GetTakenPiecePos())
			self.__ChessBoard.RemovePieceFromBoard(move.GetStartPos())
			self.__ChessBoard.AddPieceToBoard(move.GetPlayerColor(), move.GetEndPiece(), move.GetEndPos())

			for CastleType in move.GetDisabledCastleTypes():
				self.SetCastlingStatus(move.GetPlayerCOlor(), CastleType, False)
			
			self.__ChessBoard.remove_highlights()
			self.__ChessBoard.add_highlight(move.GetStartPos())
			self.__ChessBoard.add_highlight(move.GetEndPos())

	def RegisterMove(self):
		CurrentMove = self.GetCurrentMove()
		self.__ChessBoard.RemovePieceFromBoard(CurrentMove.GetTakenPiecePos())
		self.__ChessBoard.RemovePieceFromBoard(CurrentMove.GetStartPos())
		self.__ChessBoard.AddPieceToBoard(CurrentMove.GetPlayerColor(), CurrentMove.GetEndPiece(), CurrentMove.GetEndPos())
		self.__ChessBoard.add_highlight(CurrentMove.GetEndPos())

		self.__data["MoveList"] = self.__data["MoveList"][:self.GetMoveIndex()]
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
			if coordinate[0] in CastleType.keys() and self.GetCastlingStatus(PlayerColor, CastleType[coordinate[0]]):
				isBlocked = False
				CheckRange = (coordinate[0], RookPos[CastleType[coordinate[0]]])
				CheckRange = (min(CheckRange), max(CheckRange))
				for i in range(CheckRange[0] + 1, CheckRange[1]):
					if State().PieceExistsAtPosition((i, coordinate[1])):
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
				if State().GetChessPieceAtPosition((coordinate[0], i)) != None:
					isValidMove = False
					break
		elif coordinate[1] == CurrentMove.GetStartPos()[1]:
			isValidMove = True
			CheckRange = (coordinate[0], CurrentMove.GetStartPos()[0])
			CheckRange = (min(CheckRange), max(CheckRange))
			for i in range(CheckRange[0] + 1, CheckRange[1]):
				if State().PieceExistsAtPosition((i, coordinate[1])):
					isValidMove = False
					break
		elif abs(coordinate[0] - CurrentMove.GetStartPos()[0]) == abs(coordinate[1] - CurrentMove.GetStartPos()[1]):
			isValidMove = True
			x, y = CurrentMove.GetStartPos()
			xDirection = 1 if CurrentMove.GetStartPos()[0] < coordinate[0] else -1
			yDirection = 1 if CurrentMove.GetStartPos()[1] < coordinate[1] else -1
			for i in range(1, abs(CurrentMove.GetStartPos()[0] - coordinate[0])):
				if State().GetChessPieceAtPosition((x+i*xDirection, y+i*yDirection)) != None:
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
				if State().PieceExistsAtPosition((coordinate[0], i)):
					isValidMove = False
					break
		elif coordinate[1] == CurrentMove.GetStartPos()[1]:
			isValidMove = True
			CheckRange = (coordinate[0], CurrentMove.GetStartPos()[0])
			CheckRange = (min(CheckRange), max(CheckRange))
			for i in range(CheckRange[0] + 1, CheckRange[1]):
				if State().PieceExistsAtPosition((i, coordinate[1])):
					isValidMove = False
					break

		if isValidMove:
			self.GetCurrentMove().SetEndPos(coordinate)
			if CurrentMove.GetStartPos()[0] == 0 and self.GetCastlingStatus(PlayerColor, "Long"):
				self.SetCastlingStatus(PlayerColor, "Long", False)
				self.GetCurrentMove().SetDisabledCastleTypes("Long")
			elif CurrentMove.GetStartPos()[0] == 7 and self.GetCastlingStatus(PlayerColor, "Short"):
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
				if State().GetChessPieceAtPosition((x+i*xDirection, y+i*yDirection)) != None:
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
			if State().PieceExistsAtPosition(coordinate):
				isValidMove = True
			# En passant
			else:
				EnPassantEndingRow = {"white": 2, "black": 5}
				if coordinate[1] == EnPassantEndingRow[PlayerColor]:
					EnemyPawnPos = (coordinate[0], CurrentMove.GetStartPos()[1])
					EnemyPawn = State().GetChessPieceAtPosition(EnemyPawnPos)
					if EnemyPawn != None and EnemyPawn["PlayerColor"] != PlayerColor and EnemyPawn["PieceType"] == PieceType:
						if self.GetMoveIndex() == 0:
							self.GetCurrentMove().SetTakenPieceAndPos(PieceType, coordinate)
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

	
	def ShuaiMove(self, coordinate):
		ChessType = "XiangQi"
		CurrentMove = self.GetCurrentMove()
		PlayerColor = CurrentMove.GetPlayerColor()
		isValidMove = False

		xCoordinateLim = (3, 5)
		yCoordinateLim = (0, 2)
		if PlayerColor == Parameters().GetPlayerColors(ChessType)[0]:
			yCoordinateLim = (
				Parameters().GetChessboardYArray(ChessType)-1 - yCoordinateLim[1],
				Parameters().GetChessboardYArray(ChessType)-1 - yCoordinateLim[0]
			)
		if abs(coordinate[0] - CurrentMove.GetStartPos()[0]) == 1 and coordinate[1] == CurrentMove.GetStartPos()[1] and xCoordinateLim[0] <= coordinate[0] <= xCoordinateLim[1]:
			isValidMove = True
		elif abs(coordinate[1] - CurrentMove.GetStartPos()[1]) == 1 and coordinate[0] == CurrentMove.GetStartPos()[0] and yCoordinateLim[0] <= coordinate[1] <= yCoordinateLim[1]:
			isValidMove = True
		else:
			EnemyKing = State().GetChessPieceAtPosition(coordinate)
			if EnemyKing != None and EnemyKing["PlayerColor"] != CurrentMove.GetPlayerColor() and EnemyKing["PieceType"] == "shuai":
				isBlocked = False
				CheckRange = (coordinate[1], CurrentMove.GetStartPos()[1])
				CheckRange = (min(CheckRange), max(CheckRange))
				for i in range(CheckRange[0] + 1, CheckRange[1]):
					if State().PieceExistsAtPosition((coordinate[0], i)):
						isBlocked = True
						break
				if not isBlocked:
					isValidMove = True

		if isValidMove:
			self.GetCurrentMove().SetEndPos(coordinate)
			return True
		return False

	def ShiMove(self, coordinate):
		ChessType = "XiangQi"
		CurrentMove = self.GetCurrentMove()
		PlayerColor = CurrentMove.GetPlayerColor()
		isValidMove = False

		xCoordinateLim = (3, 5)
		yCoordinateLim = (0, 2)
		if PlayerColor == Parameters().GetPlayerColors(ChessType)[0]:
			yCoordinateLim = (
				Parameters().GetChessboardYArray(ChessType)-1 - yCoordinateLim[1],
				Parameters().GetChessboardYArray(ChessType)-1 - yCoordinateLim[0]
			)
		if (abs(coordinate[0] - CurrentMove.GetStartPos()[0]) == 1 and abs(coordinate[1] - CurrentMove.GetStartPos()[1]) == 1 and xCoordinateLim[0] <= coordinate[0] <= xCoordinateLim[1] and yCoordinateLim[0] <= coordinate[1] <= yCoordinateLim[1]):
			isValidMove = True

		if isValidMove:
			self.GetCurrentMove().SetEndPos(coordinate)
			return True
		return False
	
	def XiangMove(self, coordinate):
		ChessType = "XiangQi"
		CurrentMove = self.GetCurrentMove()
		PlayerColor = CurrentMove.GetPlayerColor()
		isValidMove = False

		yCoordinateLim = (0, 4)
		if PlayerColor == Parameters().GetPlayerColors(ChessType)[0]:
			yCoordinateLim = (
				Parameters().GetChessboardYArray(ChessType)-1 - yCoordinateLim[1],
				Parameters().GetChessboardYArray(ChessType)-1 - yCoordinateLim[0]
			)
		if (abs(coordinate[0] - CurrentMove.GetStartPos()[0]) == 2 and abs(coordinate[1] - CurrentMove.GetStartPos()[1]) == 2 and yCoordinateLim[0] <= coordinate[1] <= yCoordinateLim[1]):
			midpoint = ((coordinate[0] + CurrentMove.GetStartPos()[0]) // 2,
						(coordinate[1] + CurrentMove.GetStartPos()[1]) // 2)
			if State().GetChessPieceAtPosition(midpoint) == None:
				isValidMove = True

		if isValidMove:
			self.GetCurrentMove().SetEndPos(coordinate)
			return True
		return False

	def JuMove(self, coordinate):
		CurrentMove = self.GetCurrentMove()
		isValidMove = False

		if (coordinate[0] == CurrentMove.GetStartPos()[0]):
			isValidMove = True
			CheckRange = (coordinate[1], CurrentMove.GetStartPos()[1])
			CheckRange = (min(CheckRange), max(CheckRange))
			for i in range(CheckRange[0] + 1, CheckRange[1]):
				if State().PieceExistsAtPosition((coordinate[0], i)):
					isValidMove = False
					break
		elif (coordinate[1] == CurrentMove.GetStartPos()[1]):
			isValidMove = True
			CheckRange = (coordinate[0], CurrentMove.GetStartPos()[0])
			CheckRange = (min(CheckRange), max(CheckRange))
			for i in range(CheckRange[0] + 1, CheckRange[1]):
				if State().PieceExistsAtPosition((i, coordinate[1])):
					isValidMove = False
					break
		
		if isValidMove:
			self.GetCurrentMove().SetEndPos(coordinate)
			return True
		return False

	def PaoMove(self, coordinate):
		CurrentMove = self.GetCurrentMove()
		isValidMove = False

		if (coordinate[0] == CurrentMove.GetStartPos()[0]):
			CollisionCount = 0
			CheckRange = (coordinate[1], CurrentMove.GetStartPos()[1])
			CheckRange = (min(CheckRange), max(CheckRange))
			for i in range(CheckRange[0] + 1, CheckRange[1]):
				if State().PieceExistsAtPosition((coordinate[0], i)):
					CollisionCount += 1
					if CollisionCount >= 2:
						return False
			
			if not State().PieceExistsAtPosition(coordinate):
				if CollisionCount == 0:
					isValidMove = True
			elif CollisionCount == 1:
					isValidMove = True

		elif (coordinate[1] == CurrentMove.GetStartPos()[1]):
			CollisionCount = 0
			CheckRange = (coordinate[0], CurrentMove.GetStartPos()[0])
			CheckRange = (min(CheckRange), max(CheckRange))
			for i in range(CheckRange[0] + 1, CheckRange[1]):
				if State().PieceExistsAtPosition((i, coordinate[1])):
					CollisionCount += 1
					if CollisionCount >= 2:
						return False
			
			if not State().PieceExistsAtPosition(coordinate):
				if CollisionCount == 0:
					isValidMove = True
			elif CollisionCount == 1:
				isValidMove = True

		if isValidMove:
			self.GetCurrentMove().SetEndPos(coordinate)
			return True
		return False
	
	def MaMove(self, coordinate):
		CurrentMove = self.GetCurrentMove()
		isValidMove = False
		
		xDiff = abs(coordinate[0] - CurrentMove.GetStartPos()[0])
		yDiff = abs(coordinate[1] - CurrentMove.GetStartPos()[1])

		if xDiff == 1 and yDiff == 2:
			BlockPos = (CurrentMove.GetStartPos()[0], (coordinate[1] + CurrentMove.GetStartPos()[1]) // 2)
			if not State().PieceExistsAtPosition(BlockPos):
				isValidMove = True
		elif xDiff == 2 and yDiff == 1:
			BlockPos = ((coordinate[0] + CurrentMove.GetStartPos()[0]) // 2, CurrentMove.GetStartPos()[1])
			if not State().PieceExistsAtPosition(BlockPos):
				isValidMove = True

		if isValidMove:
			self.GetCurrentMove().SetEndPos(coordinate)
			return True
		return False

	def BingMove(self, coordinate):
		ChessType = "XiangQi"
		CurrentMove = self.GetCurrentMove()
		PlayerColor = CurrentMove.GetPlayerColor()
		isValidMove = False

		yCoordinateLim = (5, 9)
		direction = 1
		if PlayerColor == Parameters().GetPlayerColors(ChessType)[0]:
			yCoordinateLim = (
				Parameters().GetChessboardYArray(ChessType)-1 - yCoordinateLim[1],
				Parameters().GetChessboardYArray(ChessType)-1 - yCoordinateLim[0]
			)
			direction = -1

		if coordinate[0] == CurrentMove.GetStartPos()[0] and coordinate[1] == CurrentMove.GetStartPos()[1] + direction:
			isValidMove = True
		elif coordinate[1] == CurrentMove.GetStartPos()[1] and abs(coordinate[0] - CurrentMove.GetStartPos()[0]) == 1 and yCoordinateLim[0] <= coordinate[1] <= yCoordinateLim[1]:
			isValidMove = True
		
		if isValidMove:
			self.GetCurrentMove().SetEndPos(coordinate)
			return True
		return False
