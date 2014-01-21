#/usr/bin/env python3

import ply.lex as lex

from vartools.parser.utils import Description

class EnumLexer:
    states = (
        ('comment', 'exclusive'),
    )

    reserved = {
        'namespace' : 'NAMESPACE',
        'enum' : 'ENUM',
    }
    
    tokens = [
        'MACROS', 'LINE_COMMENT', 'NON_ASTERISK', 'ASTERISK', 
        'START_MULTILINE_COMMENT', 'END_MULTILINE_COMMENT',
        'ASSIGN', 'COMMA', 'SEMICOLON', 'OPEN_CURLY', 'CLOSE_CURLY',
        'OPEN_PAREN', 'CLOSE_PAREN', 'NAMESPACE_SEPARATOR',
        'ID', 'HEX_INTEGER', 'INTEGER',
    ] + list(reserved.values())

    t_ANY_ignore = ' \t\n'

    t_ASSIGN = r'='
    t_COMMA = r','
    t_SEMICOLON = r';'
    t_OPEN_CURLY = r'{'
    t_CLOSE_CURLY = r'}'
    t_OPEN_PAREN = r'\('
    t_CLOSE_PAREN = r'\)'
    t_NAMESPACE_SEPARATOR = r'::'

    # skip illegal char on error
    def t_ANY_error(self, token):
        print('Illegal character "{}"'.format(token.value[0]))
        self.lexer.skip(1)

    def t_MACROS(self, token):
        r'\#.*'
        #return t

    def t_LINE_COMMENT(self, token):
        r'//[\*! ]*(.*)'
        self.last_line_comment = self.lexer.lexmatch.group(3)

    def t_ID(self, token):
        r'[a-zA-Z_][a-zA-Z_0-9]*'
        # change token type if it maches reserved word
        token.type = self.reserved.get(token.value, 'ID')
        token.value = Description(name=token.value, 
                                  comment=self.last_line_comment)
        self.last_line_comment = ''
        return token

    def t_HEX_INTEGER(self, token):
        r'0x[0-9a-f]+'
        token.type = 'INTEGER'
        token.value = int(token.value[2:], 16)
        return token

    def t_INTEGER(self, token):
        r'[0-9]+'
        token.value = int(token.value)
        return token

    def t_START_MULTILINE_COMMENT(self, token):
        r'/\*'
        self.last_line_comment = ''
        self.lexer.push_state('comment')

    def t_comment_NON_ASTERISK(self, token):
        r'[^\*]+'

    def t_comment_END_MULTILINE_COMMENT(self, token):
        r'\*/'
        self.lexer.pop_state()

    def t_comment_ASTERISK(self, token):
        r'\*'

    # build the lexer
    def build(self, **kwargs):
        self.last_line_comment = ''
        self.lexer = lex.lex(module=self, **kwargs)
    
    # print output
    def test(self, data):
        self.lexer.input(data)
        while True:
             tok = self.lexer.token()
             if not tok: break
             print(tok)

if __name__ == '__main__':
    import sys
    # check if file name was given
    if len(sys.argv) != 2:
        print("Must provide filename")
        sys.exit()
    # create lexer
    lexer = EnumLexer()
    lexer.build(debug=True)
    # read test code
    code = open(sys.argv[1], 'r').read()
    # print lexemes
    print()
    lexer.test(code)
    print()
