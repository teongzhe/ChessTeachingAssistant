import copy

import moves


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

		self.CalculateDimensionParam()


	def __InitChessParam(self):
		self.__TypesOfChess.append("Chess")
		self.__data["Chess"] = {
			"PlayerColors"			: ("white", "black"),
			"TypesOfChessPieces"	: ("king", "queen", "rook", "knight", "bishop", "pawn"),
			"ChessboardXArray"		: 8,
			"ChessboardYArray"		: 8,
			"HighlightColor"		: "red",
		}

	def __InitXiangQiParam(self):
		self.__TypesOfChess.append("XiangQi")
		self.__data["XiangQi"] = {
			"PlayerColors"			: ("red", "black"),
			"TypesOfChessPieces"	: ("shuai", "shi", "xiang", "ju", "ma", "pao", "bing"),
			"ChessboardXArray"		: 9,
			"ChessboardYArray"		: 10,
			"HighlightColor"		: "blue",
		}

	def CalculateDimensionParam(self, CanvasSize = 700):
		self.__dimensions = dict()
		self.__dimensions["CanvasSize"] = CanvasSize
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

		self.__dimensions["BoardXLimits"] = {
			"Chess"		: (self.GetBoardMargin(), self.GetBoardMargin() + self.GetBoardSize()),
			"XiangQi"	: (
				self.GetBoardMargin() + self.GetCellSize("XiangQi") - 0.5*self.GetChessPieceSize("XiangQi"),
				self.GetBoardMargin() - self.GetCellSize("XiangQi") + 0.5*self.GetChessPieceSize("XiangQi") + self.GetBoardSize()
			),
		}
		self.__dimensions["BoardYLimits"] = {
			"Chess"		: (self.GetBoardMargin(), self.GetBoardMargin() + self.GetBoardSize()),
			"XiangQi"	: (
				self.GetBoardMargin() + 0.5*self.GetCellSize("XiangQi") - 0.5*self.GetChessPieceSize("XiangQi"),
				self.GetBoardMargin() - 0.5*self.GetCellSize("XiangQi") + 0.5*self.GetChessPieceSize("XiangQi") + self.GetBoardSize()
			),
		}

		self.__dimensions["CellCenter"] = dict()
		for ChessType, (xOffset, yOffset) in {
			"Chess"		: (0.5, 0.5),
			"XiangQi"	: (1.0, 0.5),
		}.items():
			self.__dimensions["CellCenter"][ChessType] = dict()
			for i in range(self.GetChessboardXArray(ChessType)):
				for j in range(self.GetChessboardYArray(ChessType)):
					self.__dimensions["CellCenter"][ChessType][(i,j)] = (
						(i+xOffset)*self.GetCellSize(ChessType) + self.GetBoardMargin(),
						(j+yOffset)*self.GetCellSize(ChessType) + self.GetBoardMargin()
					)

		self.__dimensions["TextMargin"] = {
			"Chess"		: 10,
			"XiangQi"	: 15,
		}

		for ChessType in self.GetTypesOfChess():
			self.__dimensions["HighlightLinewidth"] = 0.1 * self.GetCellSize(ChessType)
		

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
	def GetTextMargin(self, ChessType):
		return self.__dimensions["TextMargin"][ChessType]
	def GetBoardXLimits(self, ChessType):
		return self.__dimensions["BoardXLimits"][ChessType]
	def GetBoardYLimits(self, ChessType):
		return self.__dimensions["BoardYLimits"][ChessType]
	def GetCellCenter(self, ChessType, coordinate):
		return self.__dimensions["CellCenter"][ChessType][coordinate]

	# Highlight parameters
	def GetHighlightLinewidth(self):
		return self.__dimensions["HighlightLinewidth"]
	def GetHighlightColor(self, ChessType):
		return self.__data[ChessType]["HighlightColor"]


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
