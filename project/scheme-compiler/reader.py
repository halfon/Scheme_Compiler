# coding=utf8
import pc
import sexprs

def list_to_pair(s,a):
        if s:
            return sexprs.Pair(s[0],list_to_pair(s[1:],a))
        else:
            return a

ps = pc.ParserStack()

p_line_comment = ps.parser(pc.const(lambda x: x == ';')) \
                 .parser(pc.star(pc.const(lambda x: x != '\n' and x != '\r' and x != '\n\r' and x != '\r\n'))) \
                 .parser(pc.end()) \
                 .parser(pc.const(lambda x: x == '\n' or x == '\r' or x == '\n\r' or x == '\r\n')) \
                 .disj() \
                 .catens(3) \
                 .done()

pSexpr_comment = ps.parser(pc.const(lambda x: x == '#')) \
                    .parser(pc.const(lambda x: x == ';')) \
                    .delayed_parser(lambda: pSexpr) \
                    .catens(3) \
                    .done()

p_skip = ps.parser(pc.pcWhite1) \
        .parser(p_line_comment) \
        .parser(pSexpr_comment) \
        .disjs(3) \
        .star() \
        .done()

true_p = ps.parser(pc.pcWordCI('#t')) \
                .pack(lambda m: sexprs.true()) \
                .done()

false_p = ps.parser(pc.pcWordCI('#f')) \
                .pack(lambda m: sexprs.false()) \
                .done()

boolean_p = ps.parser(true_p) \
            .parser(false_p) \
            .disj() \
            .done()

nat_p = ps.parser(pc.const(lambda x: x=='+')) \
        .parser(pc.plus(pc.pcOneOf('0123456789'))) \
        .caten() \
        .pack(lambda m: sexprs.Integer(int(m[0]+"".join(m[1])))) \
        .parser(pc.plus(pc.pcOneOf('0123456789'))) \
        .pack(lambda m: sexprs.Integer(int("".join(m)))) \
        .disj() \
        .done()
        
neg_p = ps.parser(pc.const(lambda x: x=='-')) \
        .parser(pc.plus(pc.pcOneOf('0123456789'))) \
        .caten() \
        .pack(lambda m: sexprs.Integer(int(m[0]+"".join(m[1])))) \
        .done()

hex_prefix_p = ps.parser(pc.const(lambda x: x=='0')) \
        .parser(pc.const(lambda x: x=='x' or x=='X' or x=='h' or x=='H')) \
        .caten() \
        .pack(lambda m: m) \
        .done() 

hex_p = ps.parser(hex_prefix_p) \
        .parser(pc.plus(pc.pcOneOf('0123456789abcdefABCDEF'))) \
        .caten() \
        .pack(lambda m: sexprs.Integer(int("".join(m[1]),16))) \
        .parser(pc.const(lambda x: x=='+')) \
        .parser(hex_prefix_p) \
        .parser(pc.plus(pc.pcOneOf('0123456789abcdefABCDEF'))) \
        .catens(3) \
        .pack(lambda m: sexprs.Integer(int("".join(m[2]),16))) \
        .parser(pc.const(lambda x: x=='-')) \
        .parser(hex_prefix_p) \
        .parser(pc.plus(pc.pcOneOf('0123456789abcdefABCDEF'))) \
        .catens(3) \
        .pack(lambda m: sexprs.Integer((int(m[0]+"".join(m[2]),16)))) \
        .disjs(3) \
        .done()

hex_not_zero_p = ps.parser(hex_prefix_p) \
                .parser(pc.star(pc.const(lambda x: x=='0')))  \
                .parser(pc.pcOneOf('123456789abcdefABCDEF')) \
                .parser(pc.star(pc.pcOneOf('0123456789abcdefABCDEF'))) \
                .catens(4) \
                .pack(lambda m: sexprs.Integer(int(m[2]+"".join(m[3]),16))) \
                .done()

int_p = ps.parser(hex_p) \
        .parser(nat_p) \
        .parser(neg_p) \
        .disjs(3) \
        .pack(lambda m: m) \
        .done()

unsigned_int_p = ps.parser(hex_p) \
        .parser(nat_p) \
        .disjs(2) \
        .pack(lambda m: m) \
        .done()

frac_p = ps.parser(int_p) \
         .parser(pc.const(lambda x: x=='/')) \
         .parser(hex_not_zero_p) \
         .catens(3)\
         .pack(lambda m: sexprs.Fraction(m[0],m[2])) \
         .parser(int_p) \
         .parser(pc.const(lambda x: x=='/')) \
         .parser(pc.star(pc.const(lambda x: x=='0')))  \
         .parser(unsigned_int_p) \
         .catens(4) \
         .pack(lambda m: sexprs.Fraction(m[0],m[3])) \
         .disj() \
         .done()

number_p =  ps.parser(frac_p) \
            .parser(int_p) \
            .disj() \
            .done() \

symbol_p = ps.parser(pc.pcRange('a','z')) \
           .parser(pc.pcRange('A','Z')) \
           .parser(pc.pcRange('0','9')) \
           .parser(pc.pcOneOf('!$^*-_=+<>/?')) \
           .disjs(4) \
           .plus() \
           .parser(number_p) \
           .butNot() \
           .pack(lambda m: sexprs.Symbol("".join(m).upper())) \
           .done()

'''
string_p = ps.parser(pc.const(lambda x: x=='"')) \
           .parser(pc.const(lambda x: x=="\\")) \
           .parser(pc.pcOneOf('"nrtfl\\')) \
           .caten() \
           .pack(lambda m: m[0]+"".join(m[1])) \
           .parser(pc.const(lambda x: x!='"')) \
           .disj() \
           .star() \
           .parser(pc.const(lambda x: x=='"')) \
           .catens(3) \
           .pack(lambda m: sexprs.String("".join(m[1]))) \
           .done()
'''

string_p = ps.parser(pc.const(lambda x: x=='"')) \
           .parser(pc.const(lambda x: x=="\\")) \
           .parser(pc.pcOneOf('"nrtfl\\')) \
           .caten() \
           .pack(lambda m: {'"':'"','n':'\n','r':'\r','t':'\t','f':'\f','l':chr(0x03bb),'\\':'\\'}[m[1]]) \
           .parser(pc.const(lambda x: x!='"')) \
           .disj() \
           .star() \
           .parser(pc.const(lambda x: x=='"')) \
           .catens(3) \
           .pack(lambda m: sexprs.String("".join(m[1]))) \
           .done()

'''
named_char_p = ps.parser(pc.pcWord("#\\")) \
            .parser(pc.pcWordCI('newline')) \
            .pack(lambda m: chr(10)) \
            .parser(pc.pcWordCI('return')) \
            .pack(lambda m: chr(13)) \
            .parser(pc.pcWordCI('tab')) \
            .pack(lambda m: chr(9)) \
            .parser(pc.pcWordCI('formfeed')) \
            .pack(lambda m: chr(12)) \
            .parser(pc.pcWordCI('lambda')) \
            .pack(lambda m: chr(0x03bb)) \
            .disjs(5) \
            .caten() \
            .pack(lambda m: sexprs.Char(m[1])) \
            .done()
'''

named_char_p = ps.parser(pc.pcWord("#\\")) \
            .parser(pc.pcWordCI('newline')) \
            .parser(pc.pcWordCI('return')) \
            .parser(pc.pcWordCI('tab')) \
            .parser(pc.pcWordCI('page')) \
            .parser(pc.pcWordCI('lambda')) \
            .disjs(5) \
            .caten() \
            .pack(lambda m: sexprs.Char(''.join(m[1]))) \
            .done()


digit_letter_p = ps.parser(pc.pcRange('a','f')) \
           .parser(pc.pcRange('A','F')) \
           .parser(pc.pcRange('0','9')) \
           .disjs(3) \
           .done() \

hex_char_p = ps.parser(pc.pcWord("#\\x")) \
             .parser(digit_letter_p) \
             .parser(digit_letter_p) \
             .parser(digit_letter_p) \
             .parser(digit_letter_p) \
             .catens(5)\
             .pack(lambda m: sexprs.Char(chr(int(m[1]+m[2]+m[3]+m[4],16)))) \
             .parser(pc.pcWord("#\\x")) \
             .parser(digit_letter_p) \
             .parser(digit_letter_p) \
             .catens(3)\
             .pack(lambda m: sexprs.Char(chr(int(m[1]+m[2],16)))) \
             .disj() \
             .done()

visible_char_p = ps.parser(pc.pcWord("#\\")) \
                 .parser(pc.const(lambda ch: ch > ' ')) \
                 .caten() \
                 .pack(lambda m: sexprs.Char(m[1])) \
                 .done()

char_p = ps.parser(named_char_p) \
         .parser(hex_char_p) \
         .parser(visible_char_p) \
         .disjs(3) \
         .done()

nil_p = ps.parser(pc.const(lambda x: x=='(')) \
        .parser(p_skip) \
        .parser(pc.const(lambda x: x==')')) \
        .catens(3) \
        .pack(lambda m: sexprs.Nil()) \
        .done()

proper_p = ps.parser(pc.const(lambda x: x=='(')) \
           .delayed_parser(lambda: pSexpr) \
           .star() \
           .parser(pc.const(lambda x: x==')')) \
           .catens(3) \
           .pack(lambda m: list_to_pair(m[1],sexprs.Nil())) \
           .done()

improper_p = ps.parser(pc.const(lambda x: x=='(')) \
           .delayed_parser(lambda: pSexpr) \
           .plus() \
           .parser(pc.const(lambda x: x=='.')) \
           .delayed_parser(lambda: pSexpr) \
           .parser(pc.const(lambda x: x==')')) \
           .catens(5) \
           .pack(lambda m: list_to_pair(m[1],m[3])) \
           .done()
            

pair_p = ps.parser(proper_p) \
         .parser(improper_p) \
         .disj() \
         .done()

vector_p = ps.parser(pc.const(lambda x: x=='#')) \
           .parser(pc.const(lambda x: x=='(')) \
           .delayed_parser(lambda: pSexpr) \
           .star() \
           .parser(pc.const(lambda x: x==')')) \
           .catens(4) \
           .pack(lambda m: sexprs.Vector(m[2])) \
           .done()

quoted_p = ps.parser(pc.const(lambda x: x=="'")) \
           .delayed_parser(lambda: pSexpr) \
           .caten() \
           .pack(lambda m: sexprs.Pair(sexprs.Symbol("quote"),sexprs.Pair(m[1],sexprs.Nil()))) \
           .done()

qquoted_p = ps.parser(pc.const(lambda x: x=="`")) \
           .delayed_parser(lambda: pSexpr) \
           .caten() \
           .pack(lambda m: sexprs.Pair(sexprs.Symbol("quasiquote"),sexprs.Pair(m[1],sexprs.Nil()))) \
           .done()

unquoted_spliced_p = ps.parser(pc.pcWord(",@")) \
           .delayed_parser(lambda: pSexpr) \
           .caten() \
           .pack(lambda m: sexprs.Pair(sexprs.Symbol("unquote-splicing"),sexprs.Pair(m[1],sexprs.Nil()))) \
           .done()

unquoted_p = ps.parser(pc.const(lambda x: x==",")) \
           .delayed_parser(lambda: pSexpr) \
           .caten() \
           .pack(lambda m: sexprs.Pair(sexprs.Symbol("unquote"),sexprs.Pair(m[1],sexprs.Nil()))) \
           .done()

quote_like_p = ps.parser(quoted_p) \
               .parser(qquoted_p) \
               .parser(unquoted_spliced_p) \
               .parser(unquoted_p) \
               .disjs(4) \
               .done()

pSexpr = ps.parser(p_skip) \
    .parser(nil_p) \
    .parser(boolean_p)\
    .parser(number_p) \
    .parser(string_p) \
    .parser(char_p) \
    .parser(pair_p) \
    .parser(vector_p) \
    .parser(quote_like_p) \
    .parser(symbol_p) \
    .parser(pc.end()).pack(lambda m: "") \
    .disjs(10) \
    .parser(p_skip) \
    .catens(3) \
    .pack(lambda m: m[1]) \
    .done()
