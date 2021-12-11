import copy

import moves

def init():
	global state
	state = dict()



class Parameters:
	__instance = None
	__data = None
	def __new__(self):
		if not self.__instance:
			self.__instance = super(Parameters, self).__new__(self)
			self.__instance.__initialize()
		return self.__instance

	def __initialize(self):
		self.__data = dict();
		self.__TypesOfChess = list()

		self.__InitChessParam()
		self.__InitXiangQiParam()

		self.__InitDimensionParam()


	def __InitChessParam(self):
		self.__TypesOfChess.append("Chess")
		self.__data["Chess"] = {
			"PlayerColors"			: ("white", "black"),
			"TypesOfChessPieces"	: ("king", "queen", "rook", "knight", "bishop", "pawn"),
			"ChessboardXArray"		: 8,
			"ChessboardYArray"		: 8,
		}

	def __InitXiangQiParam(self):
		self.__TypesOfChess.append("XiangQi")
		self.__data["XiangQi"] = {
			"PlayerColors"			: ("red", "black"),
			"TypesOfChessPieces"	: ("shuai", "shi", "xiang", "ju", "ma", "pao", "bing"),
			"ChessboardXArray"		: 9,
			"ChessboardYArray"		: 10,
		}

	def __InitDimensionParam(self):
		self.__dimensions = dict()
		self.__dimensions["CanvasSize"] = 700
		self.__dimensions["BoardMargin"] = 0.05 * self.GetCanvasSize()
		self.__dimensions["BoardSize"] = 0.9 * self.GetCanvasSize()

		self.__dimensions["CellSize"] = dict()
		for ChessType in self.__TypesOfChess:
			self.__dimensions["CellSize"][ChessType] = self.GetBoardSize() / max(self.GetChessboardXArray(ChessType), self.GetChessboardYArray(ChessType))
		
		self.__dimensions["ChessPieceSize"] = dict()
		for ChessType, multiplier in {
			"Chess"		: 0.8,
			"XiangQi"	: 0.98,
		}.items():
			self.__dimensions["ChessPieceSize"][ChessType] = multiplier * self.GetCellSize(ChessType)
		

	# Chess parameters
	def GetTypesOfChess(self):
		return self.__TypesOfChess
	def GetPlayerColors(self, ChessType):
		return self.__data[ChessType]["PlayerColors"]
	def GetTypesOfChessPieces(self, ChessType):
		return self.__data[ChessType]["TypesOfChessPieces"]
	def GetChessboardXArray(self, ChessType):
		return self.__data[ChessType]["ChessboardXArray"]
	def GetChessboardYArray(self, ChessType):
		return self.__data[ChessType]["ChessboardYArray"]

	# Dimension parameters
	def GetCanvasSize(self):
		return self.__dimensions["CanvasSize"]
	def GetBoardMargin(self):
		return self.__dimensions["BoardMargin"]
	def GetBoardSize(self):
		return self.__dimensions["BoardSize"]
	def GetCellSize(self, ChessType):
		return self.__dimensions["CellSize"][ChessType]
	def GetChessPieceSize(self, ChessType):
		return self.__dimensions["ChessPieceSize"][ChessType]


class State:
	__instance = None
	__data = None
	def __new__(self):
		if not self.__instance:
			self.__instance = super(State, self).__new__(self)
			self.__instance.__initialize()
		return self.__instance
	
	def __initialize(self):
		self.__data = {
			"ChessType"					: Parameters().GetTypesOfChess()[0],
			"IsGameOngoing"				: True,
			"SelectedPieceToAddToBoard"	: "deselect",
			"SavedCaption"				: "",
			"Position"					: dict(),
			"QuickSavePosition"			: dict(),
		}
		self.ClearMoveList()

	def ClearMoveList(self):
		self.__data["ActiveSquare"] = 0
		self.__data["MoveList"] = list()
		self.__data["PreviousPlayer"] = ""
		self.__data["CurrentMove"] = moves.Moves()
		self.__data["CurrentMoveIndex"] = -1
	

	def SetChessType(self, ChessType):
		self.__data["ChessType"] = ChessType
	def GetChessType(self):
		return self.__data["ChessType"]
	
	def SetGameIsOngoing(self, BoolVal):
		self.__data["IsGameOngoing"] = BoolVal
	def IsGameOngoing(self):
		return self.__data["IsGameOngoing"]

	def SetSelectedPieceToAddToBoard(self, ChessPiece):
		self.__data["SelectedPieceToAddToBoard"] = ChessPiece
	def GetSelectedPieceToAddToBoard(self):
		return self.__data["SelectedPieceToAddToBoard"]

	def SetSavedCaption(self, caption):
		self.__data["SavedCaption"] = caption
	def GetSavedCaption(self):
		return self.__data["SavedCaption"]
	def SetQuickSavePosition(self):
		self.__data["QuickSavePosition"] = copy.deepcopy(self.__data["Position"])
	def GetQuickSavePosition(self):
		return self.__data["QuickSavePosition"]

	def GetActiveSquare(self):
		return self.__data["ActiveSquare"]
	def GetMoveList(self):
		return self.__data["MoveList"]
	def GetPreviousPlayer(self):
		return self.__data["PreviousPlayer"]
	def GetCurrentMove(self):
		return self.__data["CurrentMove"]
	def GetCurrentMoveIndex(self):
		return self.__data["CurrentMoveIndex"]

	def AddChessPieceToPosition(self, ChessPiece, coordinate):
		self.__data["Position"][coordinate] = ChessPiece
	def RemoveChessPieceFromPosition(self, coordinate):
		self.__data["Position"].pop(coordinate)
	def GetChessPieceAtPosition(self, coordinate):
		return self.__data["Position"][coordinate]
	def ClearChessPiecePositions(self):
		self.__data["Position"] = dict()
	def GetChessPiecePositions(self):
		return self.__data["Position"]

	def RecordMove(self, CurrentMove):
		self.__data["CurrentMoveIndex"] += 1
		if (len(self.__data["MoveList"]) > self.__data["CurrentMoveIndex"]):
			self.__data["MoveList"] = self.__data["MoveList"][:self.__data["CurrentMoveIndex"]]
		self.__data["MoveList"].append(CurrentMove)
		self.__data["PreviousPlayer"] = CurrentMove.player_color
		self.__data["CurrentMove"] = moves.Moves()
