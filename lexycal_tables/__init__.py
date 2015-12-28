from lexycal_tables.token_table import IndentTable, TokenTable

symbol_table = TokenTable("ascii_table.txt")
large_dividers = IndentTable("large_dividers.txt", 201)
key_words = IndentTable("key_words.txt", 401)
constants = IndentTable("constants.txt", 501, "constants_table.txt")
indents = IndentTable("indents.txt", 1001, "indent_table.txt")


def find_indent(value):
	token = key_words.find(value)
	if not token:
		token = constants.find(value)
		if not token:
			token = indents.find(value)
	return token