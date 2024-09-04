from PArL import *

'''
========================= TRANSITION TABLE ========================= 
'''
transition_table = {
    START: [
        # Integer literal
        {i: INTEGER_LITERAL for i in digits},

        # Float literal
        {i: FLOAT_LITERAL for i in digits},

        # Colour literal
        {'#': COLOR_LITERAL},

        # Identifier
        {i: IDENTIFIER for i in alphabet},
    ],

    INTEGER_LITERAL: [
        # Integer literal
        {i: INTEGER_LITERAL for i in digits},
    ],

    FLOAT_LITERAL: [
        # Float literal
        {i: FLOAT_LITERAL for i in digits},

        # Transition to an intermediary state if '.' is encountered, then add another finalizing state which only allows digits
        {'.': FINAL_FLOAT_LITERAL},
    ],

    FINAL_FLOAT_LITERAL: [
        # Float literal
        {i: FINAL_FLOAT_LITERAL for i in digits},
    ],

    COLOR_LITERAL: [
        # Colour literal
        {i: COLOR_LITERAL for i in hex_},
        {i: COLOR_LITERAL for i in digits},
    ],

    IDENTIFIER: [
        # Identifier
        {i: IDENTIFIER for i in alphabet},
        {'_': IDENTIFIER},
        {i: IDENTIFIER for i in digits},
    ],
}

'''
========================= LEXER CLASS ========================= 
'''
class Lexer():
    def __init__(self):
        # Initialize the list of valid states as an empty list
        self.valid_states = []

    table = transition_table  # Transition table for state transitions

    def match(self, symbol, terminal):
        new_states = []

        if terminal:
            # Check if the symbol matches a terminal type and return the corresponding token
            if symbol in types:
                return Token(TYPE_TOKEN, symbol)
            elif symbol in boolean_literals:
                return Token(BOOLEAN_LITERAL_TOKEN, symbol)
            elif symbol in pad_width:
                return Token(PAD_WIDTH_TOKEN, symbol)
            elif symbol in pad_height:
                return Token(PAD_HEIGHT_TOKEN, symbol)
            elif symbol in pad_read:
                return Token(PAD_READ_TOKEN, symbol)
            elif symbol in pad_randi:
                return Token(PAD_RANDI_TOKEN, symbol)
            elif symbol in multiplicative_ops:
                return Token(MULTIPLICATIVE_OP_TOKEN, symbol)
            elif symbol in additive_ops:
                return Token(ADDITIVE_OP_TOKEN, symbol)
            elif symbol in relational_ops:
                return Token(RELATIONAL_OP_TOKEN, symbol)
            elif symbol in unary_ops:
                new_states.append(UNARY_OPERATION)
                return Token(UNARY_OPERATION_TOKEN, symbol)
            elif symbol in lparen:
                return Token(LPAREN_TOKEN, symbol)
            elif symbol in rparen:
                return Token(RPAREN_TOKEN, symbol)
            elif symbol in lbrace:
                return Token(LBRACE_TOKEN, symbol)
            elif symbol in rbrace:
                return Token(RBRACE_TOKEN, symbol)
            elif symbol in equals:
                return Token(EQUALS_TOKEN, symbol)
            elif symbol in comma:
                return Token(COMMA_TOKEN, symbol)
            elif symbol in period:
                return Token(PERIOD_TOKEN, symbol)
            elif symbol in semicolon:
                return Token(SEMICOLON_TOKEN, symbol)
            elif symbol in colon:
                return Token(COLON_TOKEN, symbol)
            elif symbol in hash_:
                return Token(HASH_TOKEN, symbol)
            elif symbol in rarrow:
                return Token(RARROW_TOKEN, symbol)
            elif symbol in return_:
                return Token(RETURN_TOKEN, symbol)
            elif symbol in if_:
                return Token(IF_TOKEN, symbol)
            elif symbol in else_:
                return Token(ELSE_TOKEN, symbol)
            elif symbol in for_:
                return Token(FOR_TOKEN, symbol)
            elif symbol in while_:
                return Token(WHILE_TOKEN, symbol)
            elif symbol in fun:
                return Token(FUN_TOKEN, symbol)
            elif symbol in let:
                return Token(LET_TOKEN, symbol)
            elif symbol in print_:
                return Token(PRINT_TOKEN, symbol)
            elif symbol in delay:
                return Token(DELAY_TOKEN, symbol)
            elif symbol in write:
                return Token(WRITE_TOKEN, symbol)
            elif symbol in write_box:
                return Token(WRITE_BOX_TOKEN, symbol)
        else:
            # If the symbol is not terminal, check state transitions
            for state in self.valid_states:
                for key in self.table[state]:
                    if symbol in key:
                        # Append the new state based on the symbol
                        new_states.append(key[symbol])

            # Update the valid states with the new states
            self.valid_states = new_states

            # Return False as no terminal token was matched
            return False

    '''
    ========================= TOKENIZE() ========================= 
    '''
    def tokenize(self, string):
        # Convert the input string into a single string without any modification initially
        string = ''.join([i for i in string])
        # Define a list of punctuation characters to be tokenized
        punctuation = ['(', ')', '{', '}', ',', '+', '==', '!=', '>=', '<=', ':', ';', '//', '/*', '*/', '\n']
        # Replace each punctuation character in the string with itself surrounded by spaces
        for char in punctuation:
            string = string.replace(char, ' {} '.format(char))
        # Replace newline characters with a special <NEWLINE> token
        string = string.replace('\n', ' <NEWLINE> ')
        # Split the modified string into individual words/tokens
        words = string.split()
        
        # Process the list of words to handle comments
        for i in range(len(words)):
            if words[i] == '//':  # Handle single-line comments
                for j in range(i, len(words)):
                    if words[j] == '<NEWLINE>':
                        for k in range(i, j + 1):
                            words[k] = '<COMMENT>'
                        break

            if words[i] == '/*':  # Handle multi-line comments
                for j in range(i, len(words)):
                    if words[j] == '*/':
                        for k in range(i, j + 1):
                            words[k] = '<COMMENT>'
                        break

        # Remove <NEWLINE> and <COMMENT> tokens from the list of words
        words = [i for i in words if i not in ['<NEWLINE>', '<COMMENT>']]

        tokens = []  # List to store tokens
        commands = []  # List to store final commands

        for token in words:
            COLOR_LITERAL_LIMIT = 6  # Define a limit for color literals
            self.valid_states = [START]  # Initialize valid states with START state
            # Match terminal symbols
            terminal = self.match(token, terminal=True)
            if terminal:
                tokens.append(terminal)
            else:
                # Process each character in the token
                for char in token:
                    self.match(char, terminal=False)

                    # Check if the token is a color literal and has the correct length
                    if COLOR_LITERAL in self.valid_states:
                        if len(token) - 1 != COLOR_LITERAL_LIMIT:
                            self.valid_states.remove(COLOR_LITERAL)
                # If no valid states are left, raise an exception for an invalid token
                if len(self.valid_states) == 0:
                    raise Exception('\033[1;31mInvalid token: "{}"\033[0m'.format(token))
                else:
                    # If valid states are present, append the token to the tokens list
                    tokens.append(Token(state_convertor[self.valid_states[0]], token))

            # Add the processed tokens to the commands list
            commands += tokens
            tokens = []
        # Print a success message
        print("\033[1;32mTokenizer (& Lexer) successful!\033[0m")
        # Return the list of commands
        return commands