


class TokenAccumulator(object):
	def __init__(self, codes):
		self.line = ''
		self.codes = codes

	def accumulate(self, char):
		if self.check(char):
			return False
		else:
			return self.line

	def check(self, char):
		if char['id'] in self.codes:
			self.line += char['body']
			return True
		else:
			return False

	def initial_accumulate(self, char):
		self.line = ''
		return self.accumulate(char)

	def is_empty(self):
		return self.line.__len__() == 0

	def reset(self):
		self.line = ''


class DividerAccumulator(TokenAccumulator):
	def __init__(self, codes, divider_table):
		super(DividerAccumulator, self).__init__(codes)
		self.divider_table = divider_table

	def accumulate(self, char):
		if super(DividerAccumulator, self).accumulate(char):
			token = self.divider_table.find(self.line)
			if token:
				return token
			else:
				return [divider for divider in self.line]
		else:
			return False


class CommentAccumulator(TokenAccumulator):
	def __init__(self, codes):
		super(CommentAccumulator, self).__init__(codes)
		self.column = 0
		self.row = 0

	def initial_accumulate(self, char, row, column):
		super(CommentAccumulator, self).initial_accumulate(char)
		self.row = row
		self.column = column

	def check(self, char):
		if (char['id'] in self.codes and self.line == '') or (char['body'] == '*' and (self.line == '(' or self.line == '(*')):
			self.line += char['body']
			return True
		elif self.line == '(*':
			return True
		elif self.line == '(**' and char['body'] == ')':
			self.line += char['body']
			return False
		elif self.line == '(**':
			self.line = '(*'
			return True
		else:
			return False