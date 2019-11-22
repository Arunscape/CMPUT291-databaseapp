from parser import Parser


line = input("Enter command")

if line is not None:
    p = Parser(line)
    p.parse()


