import tkinter

import settings

class Moves:
	def __init__(self):
		self.player_color = ''

		self.start_piece = ''
		self.start_pos = 0

		self.end_piece = ''
		self.end_pos = 0

		self.piece_taken = ''
		self.piece_taken_pos = ''


	def details(self):
		print(self.player_color, self.start_piece, 'from', self.start_pos, 'to', self.end_pos, 'taking', self.piece_taken)


	def update(self, state, coordinate):
		selected_piece = ''
		player_color, piece = '', ''
		if coordinate in state['position']:
			selected_piece = state['position'][coordinate]
			player_color, piece = selected_piece.split('_')
		
		if self.start_piece == '':
			# Select chess piece at specified coordinate
			if selected_piece != '':
				if player_color != state['previous_player']:
					self.player_color = player_color
					self.start_piece = selected_piece
					self.start_pos = coordinate
		else:
			# Change selection to new chess piece at specified coordinate
			if selected_piece != '' and player_color == self.player_color:
				self.start_piece = selected_piece
				self.start_pos = coordinate
			else:
				# Register piece taken
				if selected_piece != '':
					self.piece_taken = selected_piece
					self.piece_taken_pos = coordinate

				# Record end_piece and end_pos
				if self.start_piece == 'white_pawn' and coordinate[1] == 0:
					self.end_piece = self.pawn_promotion('white')
				elif self.start_piece == 'black_pawn' and coordinate[1] == 7:
					self.end_piece = self.pawn_promotion('black')
				else:
					self.end_piece = self.start_piece
				self.end_pos = coordinate

	def pawn_promotion(self, color):
		class promotion_prompt:
			def __init__(self, master):
				self.piece_to_promote_to = ''

				# Create promotion window
				self.promotion_window = tkinter.Toplevel(master)
				self.promotion_window.title('Promotion')

				def callback(chosen_piece):
					self.piece_to_promote_to = chosen_piece
					self.promotion_window.destroy()

				for piece in settings.parameters['CHESS']['TYPES_OF_CHESS_PIECES']:
					if piece != 'king' and piece != 'pawn':
						chess_piece = color + '_' + piece
						img = settings.parameters['CHESS']['IMG'][chess_piece]
						img_size = settings.parameters['CHESS']['PIECE_SIZE']
						tkinter.Button(self.promotion_window, image=img, command=lambda s=chess_piece:callback(s), width=img_size, height=img_size).pack(side=tkinter.LEFT)
				
				master.wait_window(self.promotion_window)

		promotion = promotion_prompt(settings.root)
		return promotion.piece_to_promote_to
