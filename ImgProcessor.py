import tkinter
from PIL import Image, ImageTk

import settings

MainDirectory = "img"


def ReadChessPieceImagesFromFile(ChessType):
	DirectoryPath = MainDirectory + "/" + ChessType + "/"
	settings.parameters[ChessType]["Img"] = dict()
	for color in settings.parameters[ChessType]["PlayerColors"]:
		for piece in settings.parameters[ChessType]["TypesOfChessPieces"]:
			ChessPiece = color + "_" + piece
			try:
				settings.parameters[ChessType]["Img"][ChessPiece] = Image.open(DirectoryPath + ChessPiece + ".png")
			except FileNotFoundError as e:
				tkinter.messagebox.showerror("Error", e)
				exit(1)
			

def ResizeChessPieceImages(ChessType):
	if "Img" not in settings.parameters[ChessType]:
		ReadChessPieceImagesFromFile(ChessType)
	for ChessPiece, img in settings.parameters[ChessType]["Img"].items():
		LongerSide = img.size[0] if img.size[0] > img.size[1] else img.size[1]
		ScalingFactor = settings.parameters["PieceSize"][ChessType] / LongerSide
		ScaledSize = (int(ScalingFactor*img.size[0]), int(ScalingFactor*img.size[1]))
		settings.parameters[ChessType]["Img"][ChessPiece] = img.resize(ScaledSize)


def GetImage(ChessType, ChessPiece):
	return settings.parameters[ChessType]["Img"][ChessPiece]


def GetPhotoImage(ChessType, ChessPiece):
	return ImageTk.PhotoImage(settings.parameters[ChessType]["Img"][ChessPiece])


def InitChessPieceImages():
	for ChessType in settings.parameters["TypesOfChess"]:
		if "img" not in settings.parameters[ChessType].keys():
			ReadChessPieceImagesFromFile(ChessType)
			ResizeChessPieceImages(ChessType)
