import tkinter

def run_program():
	#######################################
	###			Common settings			###
	#######################################
	CHESS_TYPE = "XIANGQI"
	# CHESS_TYPE = "CHESS"

	BOARD_SIZE, BOARD_MARGIN = 600, 50
	CANVAS_SIZE = BOARD_SIZE + 2 * BOARD_MARGIN
	TEXT_MARGIN = 10

	#######################################
	###			Update chessboard		###
	#######################################
	data_plot_objects = []
	def update_chessboard():
		for object in data_plot_objects:
			chessboard.delete(object)

		if CHESS_TYPE == "XIANGQI":
			CHESSBOARD_X_ARRAY = 9
			CHESSBOARD_Y_ARRAY = 10
			CELL_SIZE = BOARD_SIZE / CHESSBOARD_Y_ARRAY
			LINEWIDTH = 2

			# Draw squares
			for i in range(CHESSBOARD_X_ARRAY):
				if i == 0 or i == CHESSBOARD_X_ARRAY-1:
					data_plot_objects.append(chessboard.create_line(BOARD_MARGIN + CELL_SIZE + i*CELL_SIZE, BOARD_MARGIN + CELL_SIZE/2, BOARD_MARGIN + CELL_SIZE + i*CELL_SIZE, BOARD_MARGIN + BOARD_SIZE - CELL_SIZE/2, width=LINEWIDTH))
				else:
					data_plot_objects.append(chessboard.create_line(BOARD_MARGIN + CELL_SIZE + i*CELL_SIZE, BOARD_MARGIN + CELL_SIZE/2, BOARD_MARGIN + CELL_SIZE + i*CELL_SIZE, BOARD_MARGIN + BOARD_SIZE/2 - CELL_SIZE/2, width=LINEWIDTH))
					data_plot_objects.append(chessboard.create_line(BOARD_MARGIN + CELL_SIZE + i*CELL_SIZE, BOARD_MARGIN + BOARD_SIZE/2 + CELL_SIZE/2, BOARD_MARGIN + CELL_SIZE + i*CELL_SIZE, BOARD_MARGIN + BOARD_SIZE - CELL_SIZE/2, width=LINEWIDTH))
			for i in range(CHESSBOARD_Y_ARRAY):
				data_plot_objects.append(chessboard.create_line(BOARD_MARGIN + CELL_SIZE - LINEWIDTH/2, BOARD_MARGIN + CELL_SIZE/2 + i*CELL_SIZE, BOARD_MARGIN + BOARD_SIZE - CELL_SIZE + LINEWIDTH/2, BOARD_MARGIN + CELL_SIZE/2 + i*CELL_SIZE, width=LINEWIDTH))

			# Draw 'X'
			data_plot_objects.append(chessboard.create_line(BOARD_MARGIN + BOARD_SIZE/2 - CELL_SIZE, BOARD_MARGIN + CELL_SIZE/2, BOARD_MARGIN + BOARD_SIZE/2 + CELL_SIZE, BOARD_MARGIN + CELL_SIZE/2 + 2*CELL_SIZE, width=LINEWIDTH))
			data_plot_objects.append(chessboard.create_line(BOARD_MARGIN + BOARD_SIZE/2 - CELL_SIZE, BOARD_MARGIN + CELL_SIZE/2 + 2*CELL_SIZE, BOARD_MARGIN + BOARD_SIZE/2 + CELL_SIZE, BOARD_MARGIN + CELL_SIZE/2, width=LINEWIDTH))
			data_plot_objects.append(chessboard.create_line(BOARD_MARGIN + BOARD_SIZE/2 - CELL_SIZE, BOARD_MARGIN + BOARD_SIZE - CELL_SIZE/2, BOARD_MARGIN + BOARD_SIZE/2 + CELL_SIZE, BOARD_MARGIN + BOARD_SIZE - CELL_SIZE/2 - 2*CELL_SIZE, width=LINEWIDTH))
			data_plot_objects.append(chessboard.create_line(BOARD_MARGIN + BOARD_SIZE/2 - CELL_SIZE, BOARD_MARGIN + BOARD_SIZE - CELL_SIZE/2 - 2*CELL_SIZE, BOARD_MARGIN + BOARD_SIZE/2 + CELL_SIZE, BOARD_MARGIN + BOARD_SIZE - CELL_SIZE/2, width=LINEWIDTH))

		elif CHESS_TYPE == "CHESS":
			CHESSBOARD_X_ARRAY = 8
			CHESSBOARD_Y_ARRAY = 8
			CELL_SIZE = BOARD_SIZE / CHESSBOARD_X_ARRAY

			# Draw chessboard squares
			for i in range(CHESSBOARD_X_ARRAY):
				for j in range(CHESSBOARD_Y_ARRAY):
					cell_color = "black" if (i+j)%2 == 0 else "white"
					x = BOARD_MARGIN + i * CELL_SIZE
					y = BOARD_MARGIN + j * CELL_SIZE
					data_plot_objects.append(chessboard.create_rectangle(x, y, x+CELL_SIZE, y+CELL_SIZE, fill=cell_color))

			# Insert alphabets and numbers for notation
			alphabets = ('a','b','c','d','e','f','g','h')
			for i in range(CHESSBOARD_X_ARRAY):
				data_plot_objects.append(chessboard.create_text(BOARD_MARGIN + CELL_SIZE/2 + i*CELL_SIZE, BOARD_MARGIN - TEXT_MARGIN, text=alphabets[i], font=12))
				data_plot_objects.append(chessboard.create_text(BOARD_MARGIN + CELL_SIZE/2 + i*CELL_SIZE, BOARD_MARGIN + BOARD_SIZE + TEXT_MARGIN, text=alphabets[i], font=12, angle=180))
				data_plot_objects.append(chessboard.create_text(BOARD_MARGIN - TEXT_MARGIN, BOARD_MARGIN + CELL_SIZE/2 + i*CELL_SIZE, text=i+1, font=12))
				data_plot_objects.append(chessboard.create_text(BOARD_MARGIN + BOARD_SIZE + TEXT_MARGIN, BOARD_MARGIN + CELL_SIZE/2 + i*CELL_SIZE, text=i+1, font=12, angle=180))

		chessboard.scale("all", BOARD_MARGIN, BOARD_MARGIN + BOARD_SIZE/2, 1, -1)


	#######################################
	###			Create window			###
	#######################################
	window = tkinter.Tk()
	window.title("Chess Teaching Assistant")


	#######################################
	###		Create left panel			###
	#######################################
	left_panel = tkinter.Frame(window, borderwidth=5)
	left_panel.pack(side=tkinter.LEFT)

	chess_piece = tkinter.Frame(left_panel)
	chess_piece.pack(side=tkinter.TOP)
	tkinter.Label(chess_piece, text="Pieces").pack(side=tkinter.LEFT)


	#######################################
	###			Draw chessboard			###
	#######################################
	chessboard = tkinter.Canvas(window, bg="white", width=CANVAS_SIZE, height=CANVAS_SIZE)
	chessboard.pack(side=tkinter.LEFT)


	#######################################
	###		Create right panel			###
	#######################################
	right_panel = tkinter.Frame(window, borderwidth=5)
	right_panel.pack(side=tkinter.LEFT)

	save_function_frame = tkinter.Frame(right_panel)
	save_function_frame.pack(side=tkinter.TOP)
	tkinter.Label(save_function_frame, text="Test").pack(side=tkinter.LEFT)



	#######################################
	###		Keep watch for actions		###
	#######################################
	update_chessboard()
	window.mainloop()



if __name__ == "__main__":
	run_program()