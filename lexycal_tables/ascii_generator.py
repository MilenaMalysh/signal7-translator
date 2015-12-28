import string



with open("../ascii_table.txt", 'w') as output:
	for num in range(0, 256):
		if chr(num) in string.whitespace:
			output.write(str(num)+" 0\n")
		elif chr(num) in string.digits:
			output.write(str(num)+" 1\n")
		elif chr(num) in string.uppercase:
			output.write(str(num)+" 2\n")
		elif chr(num) is '(':
			output.write(str(num)+" 3\n")
		elif chr(num) in "*&./:;=\\":
			output.write(str(num)+" 4\n")
		else:
			output.write(str(num)+" 5\n")