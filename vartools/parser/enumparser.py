import logging
from pprint import pprint

import ply.yacc as yacc

from vartools.parser.enumlexer import EnumLexer
from vartools.parser.utils import EnumList, clean_enums


class EnumParser:
    """Parser of C++ headers that extracts information from enums.

    :class:`vartools.parser.utils.Description` tuples are created from
    enum entries and stored in ``members`` dictionary of
    :class:`vartools.parser.utils.EnumList`.

    """

    #: Tokens imported from lexer.
    tokens = EnumLexer.tokens

    def __init__(self, **kwargs):
        #: Logger to output errors and warnings.
        self._logger = logging.getLogger('EnumParser')
        is_debug = kwargs.get('debug', False)
        #: Lexer object.
        self.lexer = EnumLexer(debug=is_debug)
        #: Parser object.
        self.parser = yacc.yacc(module=self, debuglog=self._logger)
        #: Keeps track of index inside enum statement.
        self.current_enum_index = 0

    def parse(self, data):
        """Parse a string.

        :param str data: C++ header
        """
        self.current_enum_index = 0
        return self.parser.parse(data)

    def p_error(self, p):
        self._logger.error('Syntax error at {0}'.format(p.value))

    def p_header(self, p):
        """header : statement_list"""
        p[0] = p[1]

    def p_statement_list(self, p):
        """statement_list : statement_list statement
                          | statement"""
        if not isinstance(p[1], list):
            p[0] = [p[1]]
        else:
            p[0] = p[1]
        if len(p) > 2 and p[2]:
            p[0].append(p[2])

    def p_statement_namespace(self, p):
        """statement : namespace"""
        p[0] = p[1]

    def p_statement_enum(self, p):
        """statement : enum"""
        p[0] = p[1]

    def p_statement_call(self, p):
        """statement : call"""
        pass

    def p_enum(self, p):
        """enum : ENUM ID OPEN_CURLY enum_member_list CLOSE_CURLY SEMICOLON"""
        p[0] = EnumList(*p[2], members=p[4], category=None)
        self.current_enum_index = 0

    def p_enum_member_list1(self, p):
        """enum_member_list : enum_member_list COMMA enum_member"""
        p[0] = p[1]
        p[0].update(p[3])

    def p_enum_member_list2(self, p):
        """enum_member_list : enum_member"""
        p[0] = p[1]

    def p_enum_member(self, p):
        """enum_member : ID
                       | ID ASSIGN INTEGER"""
        if len(p) > 2:
            self.current_enum_index = p[3]
        p[0] = {self.current_enum_index: p[1]}
        self.current_enum_index += 1

    def p_namespace(self, p):
        """namespace : NAMESPACE ID OPEN_CURLY statement_list CLOSE_CURLY"""
        p[0] = p[4]

    def p_call(self, p):
        """call : ID OPEN_PAREN parameter_list CLOSE_PAREN SEMICOLON"""
        pass

    def p_parameter_list(self, p):
        """parameter_list : parameter_list COMMA parameter
                          | parameter"""
        pass

    def p_parameter(self, p):
        """parameter : ID
                     | parameter NAMESPACE_SEPARATOR ID"""
        pass

if __name__ == '__main__':
    import sys
    # check if file name was given
    if len(sys.argv) != 2:
        print("Must provide filename")
        sys.exit()
    parser = EnumParser(debug=True)
    # read test code
    code = open(sys.argv[1], 'r').read()
    # print result
    print()
    for e in clean_enums(parser.parse(code)):
        pprint(e)
        print()
