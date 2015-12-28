


def parse_ascii(name):
	with open(name, 'rb') as f:
		return [dict([('id', int(line.split()[1])), ('body', chr(int(line.split()[0])))]) for line in f]


def parse_table(name):
	with open(name, 'rb') as f:
		return [dict([('id', int(line.split()[1])), ('body', line.split()[0])]) for line in f]