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

		self.disabled_castling = list()


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
				def record_end_piece_and_pos(selected_piece, coordinate):
					self.end_piece = self.start_piece
					self.end_pos = coordinate
					self.piece_taken = selected_piece
					self.piece_taken_pos = coordinate
				# Record end_piece and end_pos

				# King
				if self.start_piece == 'white_king':
					if settings.state['CHESS']['CASTLE']['white_short'] and coordinate == (6,7) and (5,7) not in settings.state['position']:
						self.end_piece = self.start_piece
						self.end_pos = coordinate
					elif settings.state['CHESS']['CASTLE']['white_long'] and coordinate == (2,7) and (1,7) not in settings.state['position'] and (3,7) not in settings.state['position']:
						self.end_piece = self.start_piece
						self.end_pos = coordinate
					elif abs(self.start_pos[0] - coordinate[0]) < 2 and abs(self.start_pos[1] - coordinate[1]) < 2:
						record_end_piece_and_pos(selected_piece, coordinate)
				elif self.start_piece == 'black_king':
					if settings.state['CHESS']['CASTLE']['black_short'] and coordinate == (6,0) and (5,0) not in settings.state['position']:
						self.end_piece = self.start_piece
						self.end_pos = coordinate
					elif settings.state['CHESS']['CASTLE']['black_long'] and coordinate == (2,0) and (1,0) not in settings.state['position'] and (3,0) not in settings.state['position']:
						self.end_piece = self.start_piece
						self.end_pos = coordinate
					elif abs(self.start_pos[0] - coordinate[0]) < 2 and abs(self.start_pos[1] - coordinate[1]) < 2:
						record_end_piece_and_pos(selected_piece, coordinate)
				elif self.start_piece == 'white_pawn':
					if self.start_pos[0] == coordinate[0] and coordinate not in settings.state['position']:
						if self.start_pos[1] == 6 and coordinate[1] == 4:
							self.end_piece = self.start_piece
							self.end_pos = coordinate
						elif self.start_pos[1] == coordinate[1] + 1:
							self.end_piece = self.start_piece
							self.end_pos = coordinate
					elif abs(self.start_pos[0] - coordinate[0]) == 1 and self.start_pos[1] == coordinate[1] + 1:
						if coordinate in settings.state['position'] and settings.state['position'][coordinate].split('_')[0] == 'black':
							record_end_piece_and_pos(selected_piece, coordinate)
						# En passant
						elif self.start_pos[1] == 3 and settings.state['move_list'][-1].start_piece == 'black_pawn' and settings.state['move_list'][-1].end_pos[0] == coordinate[0] and settings.state['move_list'][-1].end_pos[1] == settings.state['move_list'][-1].start_pos[1] + 2:
							self.end_piece = self.start_piece
							self.end_pos = coordinate
							self.piece_taken = 'black_pawn'
							self.piece_taken_pos = (coordinate[0], coordinate[1]+1)
					if self.end_pos != 0 and self.end_pos[1] == 0:
						self.end_piece = self.pawn_promotion('white')
				elif self.start_piece == 'black_pawn':
					if self.start_pos[0] == coordinate[0] and coordinate not in settings.state['position']:
						if self.start_pos[1] == 1 and coordinate[1] == 3:
							record_end_piece_and_pos(selected_piece, coordinate)
						elif self.start_pos[1] == coordinate[1] - 1:
							record_end_piece_and_pos(selected_piece, coordinate)
					elif abs(self.start_pos[0] - coordinate[0]) == 1 and self.start_pos[1] == coordinate[1] - 1:
						if coordinate in settings.state['position'] and settings.state['position'][coordinate].split('_')[0] == 'white':
							record_end_piece_and_pos(selected_piece, coordinate)
						# En passant
						elif self.start_pos[1] == 4 and settings.state['move_list'][-1].start_piece == 'white_pawn' and settings.state['move_list'][-1].end_pos[0] == coordinate[0] and settings.state['move_list'][-1].end_pos[1] == settings.state['move_list'][-1].start_pos[1] - 2:
							self.end_piece = self.start_piece
							self.end_pos = coordinate
							self.piece_taken = 'black_pawn'
							self.piece_taken_pos = (coordinate[0], coordinate[1]-1)
					if self.end_pos != 0 and self.end_pos[1] == 7:
						self.end_piece = self.pawn_promotion('black')
				else:
					record_end_piece_and_pos(selected_piece, coordinate)


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
