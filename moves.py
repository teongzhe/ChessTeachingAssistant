class Moves:
	def __init__(self):
		self.player_color = ''
		self.moved_piece = ''
		self.start_pos = 0
		self.end_pos = 0
		self.piece_taken = ''
		self.piece_taken_pos = ''
		self.promoted_to = ''
	
	def details(self):
		print(self.player_color, self.moved_piece, 'from', self.start_pos, 'to', self.end_pos, 'taking', self.piece_taken)
