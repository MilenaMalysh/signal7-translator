from lexparser.lexparser import LexParser
from semanparser.semanparser import SemanParser
import syntparser.syntparser as SyntParser


import sys


def main():
    parser = LexParser(sys.argv[1], sys.argv[2])
    parser.parse()
    parser.update_tables()
    parser.write()
    P = parser.token_list
    S = SyntParser.Synt_p(P,sys.argv[3])
    S.parse()
    sem_parser = SemanParser(S.tree)
    sem_parser.parse()
    print sem_parser.text
    pass
if __name__ == '__main__':
    main()
