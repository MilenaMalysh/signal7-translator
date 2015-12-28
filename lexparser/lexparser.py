

from switch import switch
from lexycal_tables import symbol_table, large_dividers, constants, indents, find_indent
from token_accumulator import TokenAccumulator, DividerAccumulator, CommentAccumulator


class LexParser(object):
	def __init__(self, filein, fileout):
		self.column = 0
		self.row = 0
		self.filein = filein
		self.fileout = fileout
		self.indent_accumulator = TokenAccumulator([1, 2])
		self.constant_accumulator = TokenAccumulator([1])
		self.large_divider_accumulator = DividerAccumulator([4], large_dividers)
		self.comment_accumulator = CommentAccumulator([3])
		self.token_list = []
		self.error = False

	def parse(self):
		with open(self.filein) as f:
			for line in f:
				self.column = 0
				self.row += 1
				for c in line:
					self.column += 1
					self.parse_char(c)
			if not self.comment_accumulator.is_empty():
				print "Unending comment"
			elif not self.large_divider_accumulator.is_empty():
				self.parse_char('\n')

	def parse_char(self, c):
		char = symbol_table.find(c)
		if not self.comment_accumulator.is_empty():
			comment = self.comment_accumulator.accumulate(char)
			if comment:
				if comment == '(':
					self.print_char_error()
					self.comment_accumulator.reset()
					self.analyse(char)
				elif comment == '(**)':
					self.comment_accumulator.reset()
		elif not self.large_divider_accumulator.is_empty():
			dividers = self.large_divider_accumulator.accumulate(char)
			if dividers:
				if isinstance(dividers, dict):
					self.register(dividers, None, lambda x: x)
				else:
					for d in dividers:
						self.register(d, None, lambda x: {'id': ord(x), 'body': x})
				self.large_divider_accumulator.reset()
				self.analyse(char)
		elif self.indent_accumulator.is_empty() and self.constant_accumulator.is_empty():
			self.analyse(char)
		elif not self.indent_accumulator.is_empty():
			token = self.indent_accumulator.accumulate(char)
			if token:
				if self.analyse(char):
					self.print_ident_error()
				else:
					self.register(token, indents, find_indent)
				self.indent_accumulator.reset()
		elif not self.constant_accumulator.is_empty():
			token = self.constant_accumulator.accumulate(char)
			if token:
				if self.analyse(char):
					self.print_ident_error()
				else:
					self.register(token, constants)
				self.constant_accumulator.reset()

	def analyse(self, char):
		for case in switch(char['id']):
			if case(0):
				break
			if case(1):
				self.constant_accumulator.initial_accumulate(char)
				return True
			if case(2):
				self.indent_accumulator.initial_accumulate(char)
				return True
			if case(3):
				self.comment_accumulator.initial_accumulate(char, self.row, self.column)
				break
			if case(4):
				self.large_divider_accumulator.initial_accumulate(char)
				break
			if case(5):
				self.print_char_error()
				break
		return None

	def register(self, token, table, verifying_function=None):
		if not verifying_function:
			verifying_function = lambda x: table.find(token)
		registered = verifying_function(token)
		if not registered:
			registered = table.register(token)
		registered.update({'row': self.row, 'column': self.column - token.__len__()})
		self.token_list.append(registered)

	def print_ident_error(self):
		self.error = True
		print "Error in identifier on line " + str(self.row) + ", column " + str(self.column)

	def print_char_error(self):
		self.error = True
		print "Error in char on line " + str(self.row) + ", column " + str(self.column)

	def write(self):
		with open(self.fileout, 'w') as f:
			f.writelines([str(token)+'\n' for token in self.token_list])

	@staticmethod
	def update_tables():
		indents.serialize()
		constants.serialize()