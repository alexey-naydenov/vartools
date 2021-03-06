import logging
import ply.lex as lex

import vartools.common as vtc


class EnumLexer:
    """C++ header lexer for extracting contents of enum.

    This is a lazy implementation of C++ header parser. It is only
    interested in parsing enum structures, most other C statements
    will cause error. In particular operators and multiline macros are
    not allowed.

    .. note:: ply uses docstrings to match a regular expression to a token.

    .. method:: t_ID(token)

       Change type of reserved tokens and attach comments to non
       reserved ids. To reduce number of token rules reserved words
       parsed as ids and separated from real ids in this
       function. This method also attaches last encountered single
       line comment to non reserved id.

    """

    def __init__(self, **kwargs):
        #: Logger to output errors and warnings.
        self._logger = logging.getLogger('EnumLexer')
        #: Store last one line comment to document identifiers.
        self.last_line_comment = None
        #: Actual lexer object.
        self.lexer = lex.lex(module=self, debuglog=self._logger, **kwargs)

    #: Special lexer name, used by to eliminate multiline comments.
    states = (
        ('comment', 'exclusive'),
    )

    #: Eliminate the need to define rules for keywords, see :meth:`t_ID`.
    reserved = {
        'namespace': 'NAMESPACE',
        'enum': 'ENUM',
    }

    #: Tokens produced by the lexer.
    tokens = [
        'ASSIGN', 'COMMA', 'SEMICOLON', 'OPEN_CURLY', 'CLOSE_CURLY',
        'OPEN_PAREN', 'CLOSE_PAREN', 'NAMESPACE_SEPARATOR',
        'ID', 'INTEGER',
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

    def t_ANY_error(self, token):
        self._logger.error('Illegal character "{}"'.format(token.value[0]))
        self.lexer.skip(1)

    def t_MACROS(self, token):
        r'\#.*'

    def t_LINE_COMMENT(self, _):
        r'//[\*! ]*(.*)'
        self.last_line_comment = self.lexer.lexmatch.group(3)

    def t_ID(self, token):
        r'[a-zA-Z_][a-zA-Z_0-9]*'
        if token.value in self.reserved:
            token.type = self.reserved[token.value]
        else:
            token.type = 'ID'
            comment = self.last_line_comment if self.last_line_comment else ''
            token.value = vtc.Description(name=token.value, comment=comment)
            self.last_line_comment = None
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

    def t_START_MULTILINE_COMMENT(self, _):
        r'/\*'
        self.last_line_comment = ''
        self.lexer.push_state('comment')

    def t_comment_NON_ASTERISK(self, token):
        r'[^\*]+'

    def t_comment_END_MULTILINE_COMMENT(self, _):
        r'\*/'
        self.lexer.pop_state()

    def t_comment_ASTERISK(self, token):
        r'\*'
