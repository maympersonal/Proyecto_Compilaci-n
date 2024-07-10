from cmp_lex.utils import Grammar
from ast_lex import *
from cmp_lex.chars import r_chars


def RegexGrammar():
    G = Grammar()

    regex = G.NonTerminal('<regex>', startSymbol=True)
    branch, piece, atom, literal = G.NonTerminals('<branch> <piece> <atom> <literal>')
    symbol, char_class_body, char_class_character = G.NonTerminals('<symbol> <char-class-body> <char-class-character>')
    escape_comp = G.NonTerminal("<escape-comp>")

    plus, star, question, bang = G.Terminals('+ * ? !')
    opar, cpar, obrack, cbrack = G.Terminals('( ) [ ]')
    dot, pipe, scape = G.Terminals('. | \\')
    literal_characters = G.Terminals(r_chars)

    quotes = G.Terminals("\' \"")

    regex %= branch, lambda h, s: s[1]

    branch %= piece, lambda h, s: s[1]
    branch %= piece + branch, lambda h, s: ConcatenationNode(left=s[1], right=s[2])
    branch %= piece + pipe + branch, lambda h, s: UnionNode(left=s[1], right=s[3])

    piece %= atom, lambda h, s: s[1]
    piece %= atom + symbol, lambda h, s: s[2](child=s[1]),

    symbol %= plus, lambda h, s: PositiveClausureNode
    symbol %= star, lambda h, s: ClausureNode
    symbol %= question, lambda h, s: OptionalNode
    symbol %= bang, lambda h, s: NotNode

    atom %= literal, lambda h, s: s[1]
    atom %= opar + branch + cpar, lambda h, s: s[2]
    atom %= obrack + char_class_body + cbrack, lambda h, s: s[2]

    whitespace = G.addWhitespace()
    literal %= whitespace, lambda h, s: AtomicNode(value=s[1])

    literal %= scape + escape_comp, lambda h, s: s[2]

    A = [x for x in G.terminals if x.Name == "A"][0]
    escape_comp %= A, lambda h, s: VocabularyNode()

    for v in literal_characters + quotes:
        literal %= v, lambda h, s: AtomicNode(value=s[1])

    for v in [plus, star, question, bang, opar, cpar, obrack, cbrack, pipe, dot, scape]:
        escape_comp %= v, lambda h, s: AtomicNode(value=s[1])

    for v in quotes:
        escape_comp %= v, lambda h, s: AtomicNode(value=s[1])

    char_class_body %= char_class_character, lambda h, s: s[1]
    char_class_body %= char_class_character + char_class_body, lambda h, s: ConcatenationNode(left=s[1], right=s[2])

    char_class_character %= literal, lambda h, s: s[1]
    char_class_character %= literal + dot + dot + literal, lambda h, s: EllipsisNode(left=s[1], right=s[4])

    return G
