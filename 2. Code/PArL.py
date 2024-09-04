import string

'''
========================= STATES ========================= 
'''
ERROR = -1                                                  # Error state
START = 0                                                   # Start state

INTEGER_LITERAL = 1                                         # Integer literal state
FLOAT_LITERAL = 2                                           # Float literal state
COLOR_LITERAL = 3                                           # Color literal state

LITERAL = 4                                                 # Literal state
IDENTIFIER = 5                                              # Identifier state

ACTUAL_PARAMETERS = 6                                       # Actual parameters state
FUNCTION_CALL = 7                                           # Function call state

SUB_EXPRESSION = 8                                          # Sub-expression state

UNARY_OPERATION = 9                                         # Unary operation state

FACTOR = 10                                                 # Factor state
TERM = 11                                                   # Term state

SIMPLE_EXPRESSION = 12                                      # Simple expression state
EXPRESSION = 13                                             # Expression state

ASSIGNMENT = 14                                             # Assignment state
VARIABLE_DECLARATION = 15                                   # Variable declaration state

PRINT_STATEMENT = 16                                        # Print statement state
DELAY_STATEMENT = 17                                        # Delay statement state
RETURN_STATEMENT = 18                                       # Return statement state
IF_STATEMENT = 19                                           # If statement state
FOR_STATEMENT = 20                                          # For statement state
WHILE_STATEMENT = 21                                        # While statement state

FORMAL_PARAMETER = 22                                       # Formal parameter state
FORMAL_PARAMETERS = 23                                      # Formal parameters state

FUNCTION_DECLARATION = 24                                   # Function declaration state
STATEMENT = 25                                              # Statement state

FINAL_FLOAT_LITERAL = 26                                    # Final float literal state
WRITE_STATEMENT = 27                                        # Write statement state
WRITE_BOX_STATEMENT = 28                                    # Write box statement state

'''
========================= TOKENS ========================= 
'''
INVALID_TOKEN = '<invalid>'                                 # Token for invalid tokens

FUNCTION_DECLARATION_TOKEN = '<function_declaration>'       # Token for function declarations
STATEMENT_TOKEN = '<statement>'                             # Token for statements
PROGRAM_TOKEN = '<program>'                                 # Token for programs
BLOCK_TOKEN = '<block>'                                     # Token for blocks

WRITE_TOKEN = '<write>'                                     # Token for write
WRITE_BOX_TOKEN = '<write_box>'                             # Token for write box
PRINT_STATEMENT_TOKEN = '<print_statement>'                 # Token for print statements
DELAY_STATEMENT_TOKEN = '<delay_statement>'                 # Token for delay statements
RETURN_STATEMENT_TOKEN = '<return_statement>'               # Token for return statements
IF_STATEMENT_TOKEN = '<if_statement>'                       # Token for if statements
FOR_STATEMENT_TOKEN = '<for_statement>'                     # Token for for statements
WHILE_STATEMENT_TOKEN = '<while_statement>'                 # Token for while statements

INTEGER_LITERAL_TOKEN = '<integer_literal>'                 # Token for integer literals
FLOAT_LITERAL_TOKEN = '<float_literal>'                     # Token for float literals
COLOR_LITERAL_TOKEN = '<color_literal>'                     # Token for color literals

LITERAL_TOKEN = '<literal>'                                 # Token for literals
IDENTIFIER_TOKEN = '<identifier>'                           # Token for identifiers

ACTUAL_PARAMETERS_TOKEN = '<actual_parameters>'             # Token for actual parameters
FUNCTION_CALL_TOKEN = '<function_call>'                     # Token for function calls

UNARY_OPERATION_TOKEN = '<unary_operation>'                 # Token for unary operations
SUB_EXPRESSION_TOKEN = '<sub_expression>'                   # Token for sub-expressions
FACTOR_TOKEN = '<factor>'                                   # Token for factors
TERM_TOKEN = '<term>'                                       # Token for terms

SIMPLE_EXPRESSION_TOKEN = '<simple_expression>'             # Token for simple expressions
EXPRESSION_TOKEN = '<expression>'                           # Token for expressions

ASSIGNMENT_TOKEN = '<assignment>'                           # Token for assignments
VARIABLE_DECLARATION_TOKEN = '<variable_declaration>'       # Token for variable declarations

FORMAL_PARAMETER_TOKEN = '<formal_parameter>'               # Token for formal parameter (Singular)
FORMAL_PARAMETERS_TOKEN = '<formal_parameters>'             # Token for formal parameters (Plural)

'''
========================= STATE_CONVERTOR ========================= 
'''
state_convertor = {
    INTEGER_LITERAL: INTEGER_LITERAL_TOKEN,                 # Token for integer literals
    FLOAT_LITERAL: FLOAT_LITERAL_TOKEN,                     # Token for float literals
    COLOR_LITERAL: COLOR_LITERAL_TOKEN,                     # Token for color literals
    LITERAL: LITERAL_TOKEN,                                 # Token for literals
    IDENTIFIER: IDENTIFIER_TOKEN,                           # Token for identifiers
    ACTUAL_PARAMETERS: ACTUAL_PARAMETERS_TOKEN,             # Token for actual parameters
    FUNCTION_CALL: FUNCTION_CALL_TOKEN,                     # Token for function calls
    UNARY_OPERATION: UNARY_OPERATION_TOKEN,                 # Token for unary operations
    SUB_EXPRESSION: SUB_EXPRESSION_TOKEN,                   # Token for sub-expressions
    FACTOR: FACTOR_TOKEN,                                   # Token for factors
    TERM: TERM_TOKEN,                                       # Token for terms
    SIMPLE_EXPRESSION: SIMPLE_EXPRESSION_TOKEN,             # Token for simple expressions
    EXPRESSION: EXPRESSION_TOKEN,                           # Token for expressions
    ASSIGNMENT: ASSIGNMENT_TOKEN,                           # Token for assignments
    VARIABLE_DECLARATION: VARIABLE_DECLARATION_TOKEN,       # Token for variable declarations
    PRINT_STATEMENT: PRINT_STATEMENT_TOKEN,                 # Token for print statements
    DELAY_STATEMENT: DELAY_STATEMENT_TOKEN,                 # Token for delay statements
    RETURN_STATEMENT: RETURN_STATEMENT_TOKEN,               # Token for return statements
    IF_STATEMENT: IF_STATEMENT_TOKEN,                       # Token for if statements
    FOR_STATEMENT: FOR_STATEMENT_TOKEN,                     # Token for for statements
    WHILE_STATEMENT: WHILE_STATEMENT_TOKEN,                 # Token for while statements
    FORMAL_PARAMETER: FORMAL_PARAMETER_TOKEN,               # Token for formal parameters
    FORMAL_PARAMETERS: FORMAL_PARAMETERS_TOKEN,             # Token for formal parameters
    FUNCTION_DECLARATION: FUNCTION_DECLARATION_TOKEN,       # Token for function declarations
    STATEMENT: STATEMENT_TOKEN                              # Token for statements
}

'''
========================= TERMINAL_SYMBOLS ========================= 
'''

LETTER_TOKEN = '<letter>'                                   # Token for letters
DIGIT_TOKEN = '<digit>'                                     # Token for digits
TYPE_TOKEN = '<type>'                                       # Token for types
BOOLEAN_LITERAL_TOKEN = '<boolean_literal>'                 # Token for boolean literals

PAD_WIDTH_TOKEN = '<pad_width>'                             # Token for pad width
PAD_HEIGHT_TOKEN = '<pad_height>'                           # Token for pad height
PAD_READ_TOKEN = '<pad_read>'                               # Token for pad read
PAD_RANDI_TOKEN = '<pad_randi>'                             # Token for pad randi

MULTIPLICATIVE_OP_TOKEN = '<multiplicative_op>'             # Token for multiplicative operators
ADDITIVE_OP_TOKEN = '<additive_op>'                         # Token for additive operators
RELATIONAL_OP_TOKEN = '<relational_op>'                     # Token for relational operators
UNARY_TOKEN = '<unary>'                                     # Token for unary operators

LPAREN_TOKEN = '<lparen>'                                   # Token for left parenthesis
RPAREN_TOKEN = '<rparen>'                                   # Token for right parenthesis
LBRACE_TOKEN = '<lbrace>'                                   # Token for left brace
RBRACE_TOKEN = '<rbrace>'                                   # Token for right brace

EQUALS_TOKEN = '<equals>'                                   # Token for equals sign
COMMA_TOKEN = '<comma>'                                     # Token for comma
PERIOD_TOKEN = '<period>'                                   # Token for period
SEMICOLON_TOKEN = '<semicolon>'                             # Token for semicolon
COLON_TOKEN = '<colon>'                                     # Token for colon
HASH_TOKEN = '<hash>'                                       # Token for hash symbol
RARROW_TOKEN = '<rarrow>'                                   # Token for right arrow (->)

RETURN_TOKEN = '<return>'                                   # Token for return keyword
IF_TOKEN = '<if>'                                           # Token for if keyword
ELSE_TOKEN = '<else>'                                       # Token for else keyword
FOR_TOKEN = '<for>'                                         # Token for for keyword
WHILE_TOKEN = '<while>'                                     # Token for while keyword

FUN_TOKEN = '<fun>'                                         # Token for fun keyword
LET_TOKEN = '<let>'                                         # Token for let keyword

PRINT_TOKEN = '<print>'                                     # Token for print keyword
DELAY_TOKEN = '<delay>'                                     # Token for delay keyword
WRITE_TOKEN = '<write>'                                     # Token for write keyword
WRITE_BOX_TOKEN = '<write_box>'                             # Token for write box keyword

NONE_TOKEN = '<none>'                                       # Token for none keyword
EOF_TOKEN = '<eof>'                                         # Token for end of file

'''
========================= BASIC_PArL ========================= 
'''
alphabet = list(string.ascii_letters)                       # List of all letters in the alphabet
digits = list(string.digits)                                # List of all digits
hex_ = list(string.hexdigits.upper())                       # List of hex terminals
types = ['float', 'int', 'bool', 'color']                   # Types
boolean_literals = ['True', 'False']                        # Boolean literals

pad_width = ['__width']                                     # Pad width
pad_height = ['__height']                                   # Pad height
pad_read = ['__read']                                       # Pad read
pad_randi = ['__randi']                                     # Pad randi

multiplicative_ops = ['*', '/', 'and']                      # Multiplicative operators
additive_ops = ['+', '-', 'or']                             # Additive operators
relational_ops = ['<', '>', '<=', '>=', '==', '!=']         # Relational operators

unary_ops = ['not', '-']                                    # Unary operators
lparen = ['(']                                              # Left parenthesis
rparen = [')']                                              # Right parenthesis
lbrace = ['{']                                              # Left brace
rbrace = ['}']                                              # Right brace
equals = ['=']                                              # Equals
comma = [',']                                               # Comma
period = ['.']                                              # Period
semicolon = [';']                                           # Semicolon
colon = [':']                                               # Colon
hash_ = ['#']                                               # Hash
rarrow = ['->']                                             # Right arrow

return_ = ['return']                                        # Return
if_ = ['if']                                                # If
else_ = ['else']                                            # Else
for_ = ['for']                                              # For
while_ = ['while']                                          # While
fun = ['fun']                                               # Fun
let = ['let']                                               # Let

print_ = ['__print']                                        # Print
delay = ['__delay']                                         # Delay
write = ['__write']                                         # Write
write_box = ['__write_box']                                 # Write_Box

WHITESPACE = ' '                                            # WHITESPACE

'''
========================= TOKEN() [TASK-1: LEXER] ========================= 
'''
class Token:
    def __init__(self, t_type, value):
        # Initialize the token type and value
        self.t_type = t_type
        self.value = value

    def __str__(self):
        # Convert the token to a string representation
        if self.value:
            # If the token has a value, include it in the tags
            return f"<{self.t_type}>{self.value}</{self.t_type[1:]}>"
        else:
            # If the token has no value, use self-closing tags
            return f"<{self.t_type[:-1]}>/{self.t_type[-1]}"

    def __repr__(self):
        # Use the string representation for the repr function
        return self.__str__()
    
'''
========================= AST_Node() [TASK-2/3: PARSER & Semantic Analysis] ========================= 
'''
class AST_Node:
    def __init__(self, t_type, parameters, children=[], token_count=0, indent =0):
        # Initialize the AST node type, parameters, children, and token count
        self.t_type = t_type
        self.parameters = parameters
        self.children = children
        self.token_count = token_count

    def __repr__(self):
        # Convert the AST node to a string representation
        open_tag = self.t_type
        close_tag = self.t_type[0] + '/' + self.t_type[1:]
        # Include the children nodes in the representation
        return '{} {} {}\n'.format(open_tag, self.children, close_tag)
        
    def __eq__(self, other: object) -> bool:
        # Check if two AST nodes are equal
        if isinstance(other, AST_Node):
            return (
                self.t_type == other.t_type and 
                self.parameters == other.parameters and 
                self.children == other.children
            )
        
'''
========================= INSTRUCTION_SET [TASK-4: Code Generation] ========================= 
'''
PAR_PUSH = 'push'                                           # Push a value onto the stack
PAR_PUSH_DOT = 'push .'                                     # Push the top value from the stack onto the stack again
PAR_PUSH_HASH = 'push #'                                    # Push a specific constant value onto the stack
PAR_PUSH_STACK = 'push ['                                   # Push the entire stack
PAR_ST = 'st'                                               # Store a value

PAR_NOP = 'nop'                                             # No operation, do nothing
PAR_DROP = 'drop'                                           # Drop the top value from the stack
PAR_DUP = 'dup'                                             # Duplicate the top value on the stack

PAR_ADD = 'add'                                             # Add the top two values on the stack
PAR_SUB = 'sub'                                             # Subtract the top two values on the stack
PAR_MUL = 'mul'                                             # Multiply the top two values on the stack
PAR_DIV = 'div'                                             # Divide the top two values on the stack
PAR_MOD = 'mod'                                             # Modulus of the top two values on the stack
PAR_INC = 'inc'                                             # Increment the top value on the stack
PAR_DEC = 'dec'                                             # Decrement the top value on the stack
PAR_MAX = 'max'                                             # Get the maximum of the top two values on the stack
PAR_MIN = 'min'                                             # Get the minimum of the top two values on the stack
PAR_IRND = 'irnd'                                           # Generate a random integer
PAR_AND = 'and'                                             # Logical AND of the top two values on the stack
PAR_OR = 'or'                                               # Logical OR of the top two values on the stack
PAR_NOT = 'not'                                             # Logical NOT of the top value on the stack

PAR_LT = 'lt'                                               # Less than comparison of the top two values on the stack
PAR_LE = 'le'                                               # Less than or equal to comparison of the top two values on the stack
PAR_GT = 'gt'                                               # Greater than comparison of the top two values on the stack
PAR_GE = 'ge'                                               # Greater than or equal to comparison of the top two values on the stack
PAR_EQ = 'eq'                                               # Equality comparison of the top two values on the stack

PAR_JMP = 'jmp'                                             # Unconditional jump
PAR_CJMP = 'cjmp'                                           # Conditional jump based on the top value on the stack
PAR_CJMP_2 = 'cjmp2'                                        # Conditional jump [2] based on the top value on the stack - EXTRA

PAR_CALL = 'call'                                           # Call a subroutine
PAR_RET = 'ret'                                             # Return from a subroutine
PAR_HALT = 'halt'                                           # Halt the execution
PAR_OFRAME = 'oframe'                                       # Open a frame for data
PAR_CFRAME = 'cframe'                                       # Close the current frame
PAR_ALLOC = 'alloc'                                         # Allocate memory

PAR_DELAY = 'delay'                                         # Delay execution for a given time
PAR_WRITE = 'write'                                         # Write instruction
PAR_WRITE_BOX = 'write_box'                                 # Write box instruction
PAR_CLEAR = 'clear'                                         # Clear the display
PAR_WIDTH = 'width'                                         # Set the width of an element
PAR_HEIGHT = 'height'                                       # Set the height of an element
PAR_PRINT = 'print'                                         # Print a value or message

'''
========================= INSTRUCTION SET [TASK-5: Code Generation w/Arrays] ========================= 
'''
PAR_DUPA = 'dupa'                                           # Pops v (value) and c (count) from the OpS and pushes back to OpS the value v for c times.
PAR_STA = 'sta'                                             # Pops a (memory level), b (frame index), c (count) values from OpS and for i=0 to c-1 times, pops value from OpS and writes it to b+i
PAR_PUSHA = 'pusha ['                                       # Pushes the values in an array size c (popped from OpS), and pushes to OpS values starting at index i of the frame at stack level l.
PAR_PUSH_PLUS = 'push +'                                    # Pops offset o from OpS and pushes back to OpS the value x located at index i+o of the frame at stack level l.
PAR_PRINTA = 'printa'                                       # Pops c (count) from OpS and prints to the logs section c popped values from the OpS.
PAR_RETA = 'reta'                                           # Pops c (count) and c values from OpS and pushes them back in reverse order to OpS. Used to return an array.