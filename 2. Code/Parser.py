from PArL import *

'''
========================= PARSER CLASS ========================= 
'''
class Parser:
    def __init__(self):
        self.program_node = None

    ''''
    ========================= PARSE() ========================= 
    '''
    def parse(self, tokens):
        # Parse the tokens starting from the 'program' rule
        node = self.program(tokens)

        # Check if the resulting node indicates invalid syntax
        if node == AST_Node(INVALID_TOKEN, None):
            # Extract the next 20 tokens starting from the point of error
            output = [token.value for token in tokens[node.token_count:node.token_count + 20]]
            # Join the extracted tokens into a string
            output = ' '.join(output)
            # Raise an exception with the invalid syntax message
            raise Exception(f'Invalid syntax at {output} ...')
        else:
            # If the syntax is valid, set the program node
            self.program_node = node
            # Print a success message
            print("\033[1;32mParser successful!\033[0m")

        # Return the parsed program node
        return self.program_node
    
    '''
    ========================= PROGRAM() ========================= 
    '''
    def program(self, tokens):
        OFFSET_TOKEN = 0

        # If the number of tokens is less than 2, return an invalid node
        if len(tokens) < 2:
            return AST_Node(INVALID_TOKEN, None, [], OFFSET_TOKEN)

        statements = []
        node = self.statement(tokens[OFFSET_TOKEN:], turbo=False)

        # If the first statement is valid, proceed to parse further statements
        if node.t_type == STATEMENT_TOKEN:
            statements.append(node)
            OFFSET_TOKEN += node.token_count
            node = self.statement(tokens[OFFSET_TOKEN:], turbo=False)
            
            # Check for invalid syntax after a valid statement
            if OFFSET_TOKEN < len(tokens) and node.t_type == INVALID_TOKEN:
                output = ' '.join([token.value for token in tokens[OFFSET_TOKEN:OFFSET_TOKEN + 20]])
                raise Exception(f'Invalid syntax at {output} ...')

            # Parse additional statements
            while node.t_type == STATEMENT_TOKEN:
                statements.append(node)
                OFFSET_TOKEN += node.token_count
                node = self.statement(tokens[OFFSET_TOKEN:], turbo=False)

                # Check for invalid syntax in subsequent statements
                if OFFSET_TOKEN < len(tokens) and node.t_type == INVALID_TOKEN:
                    output = ' '.join([token.value for token in tokens[OFFSET_TOKEN:OFFSET_TOKEN + 20]])
                    raise Exception(f'Invalid syntax at {output} ...')
            return AST_Node(PROGRAM_TOKEN, None, statements, OFFSET_TOKEN)

        # Return an invalid node if the first statement is not valid
        return AST_Node(INVALID_TOKEN, None, [], OFFSET_TOKEN)

    '''
    ========================= BLOCK() ========================= 
    '''
    def block(self, tokens):
        OFFSET_TOKEN = 0

        # If the number of tokens is less than 2, return an invalid node
        if len(tokens) < 2:
            return AST_Node(INVALID_TOKEN, None, [], OFFSET_TOKEN)

        statements = []

        # Check for the opening brace '{'
        if tokens[OFFSET_TOKEN].t_type == LBRACE_TOKEN:
            OFFSET_TOKEN += 1
            statement_node = self.statement(tokens[OFFSET_TOKEN:])
            
            # Parse statements inside the block
            while statement_node.t_type == STATEMENT_TOKEN:
                statements.append(statement_node)
                OFFSET_TOKEN += statement_node.token_count
                statement_node = self.statement(tokens[OFFSET_TOKEN:])
            
            # Check for the closing brace '}'
            if tokens[OFFSET_TOKEN].t_type == RBRACE_TOKEN:
                OFFSET_TOKEN += 1
                return AST_Node(BLOCK_TOKEN, None, statements, OFFSET_TOKEN)

        # Return an invalid node if the block is not valid
        return AST_Node(INVALID_TOKEN, None, [], OFFSET_TOKEN)

    '''
    ========================= VARIABLE_DECL() ========================= 
    '''
    def variable_decl(self, tokens):
        OFFSET_TOKEN = 0

        # If the number of tokens is less than 6, return an invalid node
        if len(tokens) < 6:
            return AST_Node(INVALID_TOKEN, None, [], OFFSET_TOKEN)

        iden_1 = None
        type_1 = None
        expr_1 = None

        # Parse the variable declaration
        if tokens[OFFSET_TOKEN].t_type == LET_TOKEN:
            OFFSET_TOKEN += 1
            if tokens[OFFSET_TOKEN].t_type == IDENTIFIER_TOKEN:
                iden_1 = AST_Node('identifier', parameters=tokens[OFFSET_TOKEN].value)
                OFFSET_TOKEN += 1
                if tokens[OFFSET_TOKEN].t_type == COLON_TOKEN:
                    OFFSET_TOKEN += 1
                    if tokens[OFFSET_TOKEN].t_type == TYPE_TOKEN:
                        type_1 = AST_Node('type', parameters=tokens[OFFSET_TOKEN].value)
                        OFFSET_TOKEN += 1
                        if tokens[OFFSET_TOKEN].t_type == EQUALS_TOKEN:
                            OFFSET_TOKEN += 1
                            randi_node = self.randi(tokens[OFFSET_TOKEN:])
                            if randi_node.t_type == PAD_RANDI_TOKEN:
                                expr_1 = randi_node
                                OFFSET_TOKEN += randi_node.token_count
                                return AST_Node(VARIABLE_DECLARATION_TOKEN, None, [iden_1, type_1, expr_1], OFFSET_TOKEN)
                            else:
                                expr_node = self.expr(tokens[OFFSET_TOKEN:])
                                if expr_node.t_type == EXPRESSION_TOKEN:
                                    expr_1 = expr_node
                                    OFFSET_TOKEN += expr_node.token_count
                                    return AST_Node(VARIABLE_DECLARATION_TOKEN, None, [iden_1, type_1, expr_1], OFFSET_TOKEN)

        # Return an invalid node if the variable declaration is not valid
        return AST_Node(INVALID_TOKEN, None, [], OFFSET_TOKEN)

    '''
    ========================= STATEMENT() ========================= 
    '''   
    def statement(self, tokens, turbo=False):
        OFFSET_TOKEN = 0

        # If there are no tokens, return an invalid node
        if len(tokens) < 1:
            return AST_Node(INVALID_TOKEN, None, [], OFFSET_TOKEN)

        # Turbo mode for direct statement parsing
        if turbo:
            node = None

            # Identify the statement type and parse accordingly
            if tokens[OFFSET_TOKEN].t_type == LET_TOKEN:
                node = self.variable_decl(tokens[0:])
            elif tokens[OFFSET_TOKEN].t_type == IDENTIFIER_TOKEN:
                node = self.assignment(tokens[0:])
            elif tokens[OFFSET_TOKEN].t_type == PRINT_TOKEN:
                node = self.print_statement(tokens[0:])
            elif tokens[OFFSET_TOKEN].t_type == DELAY_TOKEN:
                node = self.delay_statement(tokens[0:])
            elif tokens[OFFSET_TOKEN].t_type == IF_TOKEN:
                node = self.if_statement(tokens[0:])
            elif tokens[OFFSET_TOKEN].t_type == FOR_TOKEN:
                node = self.for_statement(tokens[0:])
            elif tokens[OFFSET_TOKEN].t_type == WHILE_TOKEN:
                node = self.while_statement(tokens[0:])
            elif tokens[OFFSET_TOKEN].t_type == RETURN_TOKEN:
                node = self.return_statement(tokens[0:])
            elif tokens[OFFSET_TOKEN].t_type == FUN_TOKEN:
                node = self.function_decl(tokens[0:])
            elif tokens[OFFSET_TOKEN].t_type == LBRACE_TOKEN:
                node = self.block(tokens[0:])
            elif tokens[OFFSET_TOKEN].t_type == WRITE_TOKEN:
                node = self.write_statement(tokens[0:])
            elif tokens[OFFSET_TOKEN].t_type == WRITE_BOX_TOKEN:
                node = self.write_box_statement(tokens[0:])

            # Return the parsed statement node or an invalid node
            if node:
                return AST_Node(STATEMENT_TOKEN, None, [node], node.token_count)
            else:
                return AST_Node(INVALID_TOKEN, None, [], OFFSET_TOKEN)
        else:
            # Non-turbo mode: try each statement type until a valid one is found
            stmt_types = [
                self.variable_decl(tokens[0:]),
                self.assignment(tokens[0:]),
                self.print_statement(tokens[0:]),
                self.delay_statement(tokens[0:]),
                self.if_statement(tokens[0:]),
                self.for_statement(tokens[0:]),
                self.while_statement(tokens[0:]),
                self.return_statement(tokens[0:]),
                self.function_decl(tokens[0:]),
                self.block(tokens[0:]),
                self.write_statement(tokens[0:]),
                self.write_box_statement(tokens[0:])
            ]

            for stmt in stmt_types:
                if stmt.t_type != INVALID_TOKEN:
                    OFFSET_TOKEN += stmt.token_count
                    if stmt.t_type in [IF_STATEMENT_TOKEN, FOR_STATEMENT_TOKEN, WHILE_STATEMENT_TOKEN, FUNCTION_DECLARATION_TOKEN, BLOCK_TOKEN]:
                        return AST_Node(STATEMENT_TOKEN, None, [stmt], OFFSET_TOKEN)
                    elif tokens[OFFSET_TOKEN].t_type == SEMICOLON_TOKEN:
                        OFFSET_TOKEN += 1
                        return AST_Node(STATEMENT_TOKEN, None, [stmt], OFFSET_TOKEN)

            return AST_Node(INVALID_TOKEN, None, [], OFFSET_TOKEN)
        
    '''
    ========================= ASSIGNMENT() ========================= 
    ''' 
    def assignment(self, tokens):
        OFFSET_TOKEN = 0

        # If the number of tokens is less than 3, return an invalid node
        if len(tokens) < 3:
            return AST_Node(INVALID_TOKEN, None, [], OFFSET_TOKEN)

        iden_1 = None
        expr_1 = None

        # Parse the assignment statement
        if tokens[OFFSET_TOKEN].t_type == IDENTIFIER_TOKEN:
            iden_1 = AST_Node('identifier', parameters=tokens[OFFSET_TOKEN].value)
            OFFSET_TOKEN += 1
            if tokens[OFFSET_TOKEN].t_type == EQUALS_TOKEN:
                OFFSET_TOKEN += 1
                randi_node = self.randi(tokens[OFFSET_TOKEN:])
                if randi_node.t_type == PAD_RANDI_TOKEN:
                    expr_1 = randi_node
                    OFFSET_TOKEN += randi_node.token_count
                    return AST_Node(ASSIGNMENT_TOKEN, None, [iden_1, expr_1], OFFSET_TOKEN)
                
                expr_node = self.expr(tokens[OFFSET_TOKEN:])
                if expr_node.t_type == EXPRESSION_TOKEN:
                    expr_1 = expr_node
                    OFFSET_TOKEN += expr_node.token_count
                    return AST_Node(ASSIGNMENT_TOKEN, None, [iden_1, expr_1], OFFSET_TOKEN)

        # Return an invalid node if the assignment is not valid
        return AST_Node(INVALID_TOKEN, None, [], OFFSET_TOKEN)
    
    '''
    ========================= WRITE() ========================= 
    '''
    def write_statement(self, tokens):
        OFFSET_TOKEN = 0

        # If the number of tokens is less than 4, return an invalid node
        if len(tokens) < 4:
            return AST_Node(INVALID_TOKEN, None, [], OFFSET_TOKEN)

        # Parse the write statement
        if tokens[OFFSET_TOKEN].t_type == WRITE_TOKEN:
            OFFSET_TOKEN += 1
            expr1 = self.expr(tokens[OFFSET_TOKEN:])
            if expr1.t_type == EXPRESSION_TOKEN:
                OFFSET_TOKEN += expr1.token_count
                if tokens[OFFSET_TOKEN].t_type == COMMA_TOKEN:
                    OFFSET_TOKEN += 1
                    expr2 = self.expr(tokens[OFFSET_TOKEN:])
                    if expr2.t_type == EXPRESSION_TOKEN:
                        OFFSET_TOKEN += expr2.token_count
                        if tokens[OFFSET_TOKEN].t_type == COMMA_TOKEN:
                            OFFSET_TOKEN += 1
                            expr3 = self.expr(tokens[OFFSET_TOKEN:])
                            if expr3.t_type == EXPRESSION_TOKEN:
                                OFFSET_TOKEN += expr3.token_count
                                return AST_Node(WRITE_TOKEN, None, [expr1, expr2, expr3], OFFSET_TOKEN)

        # Return an invalid node if the write statement is not valid
        return AST_Node(INVALID_TOKEN, None, [], OFFSET_TOKEN)

    '''
    ========================= WRITE_BOX() ========================= 
    '''
    def write_box_statement(self, tokens):
        OFFSET_TOKEN = 0

        # If the number of tokens is less than 6, return an invalid node
        if len(tokens) < 6:
            return AST_Node(INVALID_TOKEN, None, [], OFFSET_TOKEN)

        # Parse the write box statement
        if tokens[OFFSET_TOKEN].t_type == WRITE_BOX_TOKEN:
            OFFSET_TOKEN += 1
            expr1 = self.expr(tokens[OFFSET_TOKEN:])
            if expr1.t_type == EXPRESSION_TOKEN:
                OFFSET_TOKEN += expr1.token_count
                if tokens[OFFSET_TOKEN].t_type == COMMA_TOKEN:
                    OFFSET_TOKEN += 1
                    expr2 = self.expr(tokens[OFFSET_TOKEN:])
                    if expr2.t_type == EXPRESSION_TOKEN:
                        OFFSET_TOKEN += expr2.token_count
                        if tokens[OFFSET_TOKEN].t_type == COMMA_TOKEN:
                            OFFSET_TOKEN += 1
                            expr3 = self.expr(tokens[OFFSET_TOKEN:])
                            if expr3.t_type == EXPRESSION_TOKEN:
                                OFFSET_TOKEN += expr3.token_count
                                if tokens[OFFSET_TOKEN].t_type == COMMA_TOKEN:
                                    OFFSET_TOKEN += 1
                                    expr4 = self.expr(tokens[OFFSET_TOKEN:])
                                    if expr4.t_type == EXPRESSION_TOKEN:
                                        OFFSET_TOKEN += expr4.token_count
                                        if tokens[OFFSET_TOKEN].t_type == COMMA_TOKEN:
                                            OFFSET_TOKEN += 1
                                            expr5 = self.expr(tokens[OFFSET_TOKEN:])
                                            if expr5.t_type == EXPRESSION_TOKEN:
                                                OFFSET_TOKEN += expr5.token_count
                                                return AST_Node(WRITE_BOX_TOKEN, None, [expr1, expr2, expr3, expr4, expr5], OFFSET_TOKEN)

        # Return an invalid node if the write box statement is not valid
        return AST_Node(INVALID_TOKEN, None, [], OFFSET_TOKEN)

    '''
    ========================= PRINT() ========================= 
    ''' 
    def print_statement(self, tokens):
        OFFSET_TOKEN = 0

        # If the number of tokens is less than 2, return an invalid node
        if len(tokens) < 2:
            return AST_Node(INVALID_TOKEN, None, [], OFFSET_TOKEN)

        expr_1 = None

        # Parse the print statement
        if tokens[OFFSET_TOKEN].t_type == PRINT_TOKEN:
            OFFSET_TOKEN += 1
            expr_node = self.expr(tokens[OFFSET_TOKEN:])
            if expr_node.t_type == EXPRESSION_TOKEN:
                expr_1 = expr_node
                OFFSET_TOKEN += expr_node.token_count
                return AST_Node(PRINT_STATEMENT_TOKEN, None, [expr_1], OFFSET_TOKEN)

        # Return an invalid node if the print statement is not valid
        return AST_Node(INVALID_TOKEN, None, [], OFFSET_TOKEN)

    '''
    ========================= DELAY() ========================= 
    '''  
    def delay_statement(self, tokens):
        OFFSET_TOKEN = 0

        # If the number of tokens is less than 2, return an invalid node
        if len(tokens) < 2:
            return AST_Node(INVALID_TOKEN, None, [], OFFSET_TOKEN)

        expr_1 = None

        # Parse the delay statement
        if tokens[OFFSET_TOKEN].t_type == DELAY_TOKEN:
            OFFSET_TOKEN += 1
            expr_node = self.expr(tokens[OFFSET_TOKEN:])
            if expr_node.t_type == EXPRESSION_TOKEN:
                expr_1 = expr_node
                OFFSET_TOKEN += expr_node.token_count
                return AST_Node(DELAY_STATEMENT_TOKEN, None, [expr_1], OFFSET_TOKEN)

        # Return an invalid node if the delay statement is not valid
        return AST_Node(INVALID_TOKEN, None, [], OFFSET_TOKEN)

    '''
    ========================= IF() ========================= 
    '''
    def if_statement(self, tokens):
        OFFSET_TOKEN = 0

        # If the number of tokens is less than 5, return an invalid node
        if len(tokens) < 5:
            return AST_Node(INVALID_TOKEN, None, [], OFFSET_TOKEN)

        expr_1 = None
        BLOCK_1 = None
        BLOCK_2 = None

        # Parse the if statement
        if tokens[OFFSET_TOKEN].t_type == IF_TOKEN:
            OFFSET_TOKEN += 1
            if tokens[OFFSET_TOKEN].t_type == LPAREN_TOKEN:
                OFFSET_TOKEN += 1
                expr_node = self.expr(tokens[OFFSET_TOKEN:])
                if expr_node.t_type == EXPRESSION_TOKEN:
                    expr_1 = expr_node
                    OFFSET_TOKEN += expr_node.token_count
                    if tokens[OFFSET_TOKEN].t_type == RPAREN_TOKEN:
                        OFFSET_TOKEN += 1
                        block_node = self.block(tokens[OFFSET_TOKEN:])
                        if block_node.t_type == BLOCK_TOKEN:
                            BLOCK_1 = block_node
                            OFFSET_TOKEN += block_node.token_count
                            if OFFSET_TOKEN < len(tokens):
                                if tokens[OFFSET_TOKEN].t_type == ELSE_TOKEN:
                                    OFFSET_TOKEN += 1
                                    else_block_node = self.block(tokens[OFFSET_TOKEN:])
                                    if else_block_node.t_type == BLOCK_TOKEN:
                                        BLOCK_2 = else_block_node
                                        OFFSET_TOKEN += else_block_node.token_count
                                        return AST_Node(IF_STATEMENT_TOKEN, None, [expr_1, BLOCK_1, BLOCK_2], OFFSET_TOKEN)
                                else:
                                    return AST_Node(IF_STATEMENT_TOKEN, None, [expr_1, BLOCK_1], OFFSET_TOKEN)
                            else:
                                return AST_Node(IF_STATEMENT_TOKEN, None, [expr_1, BLOCK_1], OFFSET_TOKEN)

        # Return an invalid node if the if statement is not valid
        return AST_Node(INVALID_TOKEN, None, [], OFFSET_TOKEN)

    '''
    ========================= FOR() ========================= 
    '''
    def for_statement(self, tokens):
        OFFSET_TOKEN = 0

        # If there are no tokens, return an invalid node
        if len(tokens) < 1:
            return AST_Node(INVALID_TOKEN, None, [], OFFSET_TOKEN)

        # Parse the for statement
        if tokens[OFFSET_TOKEN].t_type == FOR_TOKEN:
            OFFSET_TOKEN += 1
            if OFFSET_TOKEN < len(tokens) and tokens[OFFSET_TOKEN].t_type == LPAREN_TOKEN:
                OFFSET_TOKEN += 1
                init_node = self.statement(tokens[OFFSET_TOKEN:])
                if init_node.t_type != INVALID_TOKEN:
                    OFFSET_TOKEN += init_node.token_count
                    if OFFSET_TOKEN < len(tokens) and tokens[OFFSET_TOKEN].t_type == SEMICOLON_TOKEN:
                        OFFSET_TOKEN += 1
                        condition_node = self.expr(tokens[OFFSET_TOKEN:])
                        if condition_node.t_type != INVALID_TOKEN:
                            OFFSET_TOKEN += condition_node.token_count
                            if OFFSET_TOKEN < len(tokens) and tokens[OFFSET_TOKEN].t_type == SEMICOLON_TOKEN:
                                OFFSET_TOKEN += 1
                                post_node = self.statement(tokens[OFFSET_TOKEN:])
                                if post_node.t_type != INVALID_TOKEN:
                                    OFFSET_TOKEN += post_node.token_count
                                    if OFFSET_TOKEN < len(tokens) and tokens[OFFSET_TOKEN].t_type == RPAREN_TOKEN:
                                        OFFSET_TOKEN += 1
                                        block_node = self.block(tokens[OFFSET_TOKEN:])
                                        if block_node.t_type == BLOCK_TOKEN:
                                            OFFSET_TOKEN += block_node.token_count
                                            return AST_Node(FOR_STATEMENT_TOKEN, None, [init_node, condition_node, post_node, block_node], OFFSET_TOKEN)

        # Return an invalid node if the for statement is not valid
        return AST_Node(INVALID_TOKEN, None, [], OFFSET_TOKEN)
    
    '''
    ========================= WHILE() ========================= 
    '''
    def while_statement(self, tokens):
        OFFSET_TOKEN = 0

        # If the number of tokens is less than 5, return an invalid node
        if len(tokens) < 5:
            return AST_Node(INVALID_TOKEN, None, [], OFFSET_TOKEN)

        expr_1 = None
        block_1 = None

        # Parse the while statement
        if tokens[OFFSET_TOKEN].t_type == WHILE_TOKEN:
            OFFSET_TOKEN += 1
            if tokens[OFFSET_TOKEN].t_type == LPAREN_TOKEN:
                OFFSET_TOKEN += 1
                expr_node = self.expr(tokens[OFFSET_TOKEN:])
                if expr_node.t_type == EXPRESSION_TOKEN:
                    expr_1 = expr_node
                    OFFSET_TOKEN += expr_node.token_count
                    if tokens[OFFSET_TOKEN].t_type == RPAREN_TOKEN:
                        OFFSET_TOKEN += 1
                        block_node = self.block(tokens[OFFSET_TOKEN:])
                        if block_node.t_type == BLOCK_TOKEN:
                            block_1 = block_node
                            OFFSET_TOKEN += block_node.token_count
                            return AST_Node(WHILE_STATEMENT_TOKEN, None, [expr_1, block_1], OFFSET_TOKEN)

        # Return an invalid node if the while statement is not valid
        return AST_Node(INVALID_TOKEN, None, [], OFFSET_TOKEN)

    '''
    ========================= RETURN() ========================= 
    '''
    def return_statement(self, tokens):
        OFFSET_TOKEN = 0

        # If the number of tokens is less than 2, return an invalid node
        if len(tokens) < 2:
            return AST_Node(INVALID_TOKEN, None, [], OFFSET_TOKEN)

        expr_1 = None

        # Parse the return statement
        if tokens[OFFSET_TOKEN].t_type == RETURN_TOKEN:
            OFFSET_TOKEN += 1
            expr_node = self.expr(tokens[OFFSET_TOKEN:])
            if expr_node.t_type == EXPRESSION_TOKEN:
                expr_1 = expr_node
                OFFSET_TOKEN += expr_node.token_count
                return AST_Node(RETURN_STATEMENT_TOKEN, None, [expr_1], OFFSET_TOKEN)

        # Return an invalid node if the return statement is not valid
        return AST_Node(INVALID_TOKEN, None, [], OFFSET_TOKEN)

    '''
    ========================= FUNC_DECLARATION() ========================= 
    '''
    def function_decl(self, tokens):
        OFFSET_TOKEN = 0

        # If the number of tokens is less than 8, return an invalid node
        if len(tokens) < 8:
            return AST_Node(INVALID_TOKEN, None, [], OFFSET_TOKEN)

        iden_1 = None
        parameters_1 = None
        type_1 = None
        BLOCK_1 = None

        # Parse the function declaration
        if tokens[OFFSET_TOKEN].t_type == FUN_TOKEN:
            OFFSET_TOKEN += 1
            if tokens[OFFSET_TOKEN].t_type == IDENTIFIER_TOKEN:
                iden_1 = AST_Node('identifier', parameters=tokens[OFFSET_TOKEN].value)
                OFFSET_TOKEN += 1
                if tokens[OFFSET_TOKEN].t_type == LPAREN_TOKEN:
                    OFFSET_TOKEN += 1
                    parameters_node = self.formal_params(tokens[OFFSET_TOKEN:])
                    if parameters_node.t_type == FORMAL_PARAMETERS_TOKEN:
                        parameters_1 = parameters_node
                        OFFSET_TOKEN += parameters_node.token_count
                        if tokens[OFFSET_TOKEN].t_type == RPAREN_TOKEN:
                            OFFSET_TOKEN += 1
                            if tokens[OFFSET_TOKEN].t_type == RARROW_TOKEN:
                                OFFSET_TOKEN += 1
                                if tokens[OFFSET_TOKEN].t_type == TYPE_TOKEN:
                                    type_1 = AST_Node('type', parameters=tokens[OFFSET_TOKEN].value)
                                    OFFSET_TOKEN += 1
                                    BLOCK_1 = self.block(tokens[OFFSET_TOKEN:])
                                    if BLOCK_1.t_type == BLOCK_TOKEN:
                                        OFFSET_TOKEN += BLOCK_1.token_count
                                        return AST_Node(FUNCTION_DECLARATION_TOKEN, None, [iden_1, parameters_1, type_1, BLOCK_1], OFFSET_TOKEN)
                    else:
                        if tokens[OFFSET_TOKEN].t_type == RPAREN_TOKEN:
                            OFFSET_TOKEN += 1
                            if tokens[OFFSET_TOKEN].t_type == RARROW_TOKEN:
                                OFFSET_TOKEN += 1
                                if tokens[OFFSET_TOKEN].t_type == TYPE_TOKEN:
                                    type_1 = AST_Node('type', parameters=tokens[OFFSET_TOKEN].value)
                                    OFFSET_TOKEN += 1
                                    BLOCK_1 = self.block(tokens[OFFSET_TOKEN:])
                                    if BLOCK_1.t_type == BLOCK_TOKEN:
                                        OFFSET_TOKEN += BLOCK_1.token_count
                                        return AST_Node(FUNCTION_DECLARATION_TOKEN, None, [iden_1, type_1, BLOCK_1], OFFSET_TOKEN)

        # Return an invalid node if the function declaration is not valid
        return AST_Node(INVALID_TOKEN, None, [], OFFSET_TOKEN)

    '''
    ========================= FORM_PARMS() (PLURAL) ========================= 
    '''
    def formal_params(self, tokens):
        OFFSET_TOKEN = 0

        # If the number of tokens is less than 2, return an invalid node
        if len(tokens) < 2:
            return AST_Node(INVALID_TOKEN, None, [], OFFSET_TOKEN)

        formalParams = []
        formal_params_ = []

        # Parse the formal parameters
        param_node = self.formal_param(tokens[OFFSET_TOKEN:])
        if param_node.t_type == FORMAL_PARAMETER_TOKEN:
            formalParams.append(param_node)
            OFFSET_TOKEN += param_node.token_count
            while OFFSET_TOKEN < len(tokens) and tokens[OFFSET_TOKEN].t_type == COMMA_TOKEN:
                OFFSET_TOKEN += 1
                param_node = self.formal_param(tokens[OFFSET_TOKEN:])
                if param_node.t_type == FORMAL_PARAMETER_TOKEN:
                    formalParams.append(param_node)
                    OFFSET_TOKEN += param_node.token_count
                else:
                    return AST_Node(INVALID_TOKEN, None, [], OFFSET_TOKEN)

            return AST_Node(FORMAL_PARAMETERS_TOKEN, None, formalParams, OFFSET_TOKEN)

        # Return an invalid node if the formal parameters are not valid
        return AST_Node(INVALID_TOKEN, None, [], OFFSET_TOKEN)

    '''
    ========================= FORM_PARM() (SINGULAR) ========================= 
    '''
    def formal_param(self, tokens):
        OFFSET_TOKEN = 0

        # If the number of tokens is less than 2, return an invalid node
        if len(tokens) < 2:
            return AST_Node(INVALID_TOKEN, None, [], OFFSET_TOKEN)

        iden_1 = None
        type_1 = None

        # Parse a single formal parameter
        if tokens[OFFSET_TOKEN].t_type == IDENTIFIER_TOKEN:
            iden_1 = AST_Node('identifier', parameters=tokens[OFFSET_TOKEN].value)
            OFFSET_TOKEN += 1
            if tokens[OFFSET_TOKEN].t_type == COLON_TOKEN:
                OFFSET_TOKEN += 1
                if tokens[OFFSET_TOKEN].t_type == TYPE_TOKEN:
                    type_1 = AST_Node('type', parameters=tokens[OFFSET_TOKEN].value)
                    OFFSET_TOKEN += 1
                    return AST_Node(FORMAL_PARAMETER_TOKEN, None, [iden_1, type_1], OFFSET_TOKEN)

        # Return an invalid node if the formal parameter is not valid
        return AST_Node(INVALID_TOKEN, None, [], OFFSET_TOKEN)

    '''
    ========================= UNARY() ========================= 
    '''
    def unary(self, tokens):
        OFFSET_TOKEN = 0

        # If the number of tokens is less than 2, return an invalid node
        if len(tokens) < 2:
            return AST_Node(INVALID_TOKEN, None, [], OFFSET_TOKEN)

        # Parse the unary operation
        if tokens[OFFSET_TOKEN].t_type == UNARY_TOKEN:
            unary_op = AST_Node('unary_op', parameters=tokens[OFFSET_TOKEN].value)
            OFFSET_TOKEN += 1
            expr_node = self.expr(tokens[OFFSET_TOKEN:])
            if expr_node.t_type == EXPRESSION_TOKEN:
                OFFSET_TOKEN += expr_node.token_count
                return AST_Node(UNARY_OPERATION_TOKEN, None, [unary_op, expr_node], OFFSET_TOKEN)

        # Return an invalid node if the unary operation is not valid
        return AST_Node(INVALID_TOKEN, None, [], OFFSET_TOKEN)

    '''
    ========================= FACTOR() ========================= 
    '''
    def factor(self, tokens):
        OFFSET_TOKEN = 0

        # If there are no tokens, return an invalid node
        if len(tokens) < 1:
            return AST_Node(INVALID_TOKEN, None, [], OFFSET_TOKEN)

        # Parse a literal
        literal_node = self.literal(tokens[OFFSET_TOKEN:])
        if literal_node.t_type == LITERAL_TOKEN:
            OFFSET_TOKEN += literal_node.token_count
            return AST_Node(FACTOR_TOKEN, None, [literal_node], OFFSET_TOKEN)

        # Parse an identifier
        if tokens[OFFSET_TOKEN].t_type == IDENTIFIER_TOKEN:
            identifier_node = AST_Node('identifier', parameters=tokens[OFFSET_TOKEN].value)
            OFFSET_TOKEN += 1
            return AST_Node(FACTOR_TOKEN, None, [identifier_node], OFFSET_TOKEN)

        # Parse a function call
        function_call_node = self.function_call(tokens[OFFSET_TOKEN:])
        if function_call_node.t_type == FUNCTION_CALL_TOKEN:
            OFFSET_TOKEN += function_call_node.token_count
            return AST_Node(FACTOR_TOKEN, None, [function_call_node], OFFSET_TOKEN)

        # Parse a sub-expression
        sub_expr_node = self.sub_expr(tokens[OFFSET_TOKEN:])
        if sub_expr_node.t_type == SUB_EXPRESSION_TOKEN:
            OFFSET_TOKEN += sub_expr_node.token_count
            return AST_Node(FACTOR_TOKEN, None, [sub_expr_node], OFFSET_TOKEN)

        # Parse a unary operation
        unary_node = self.unary(tokens[OFFSET_TOKEN:])
        if unary_node.t_type == UNARY_OPERATION_TOKEN:
            OFFSET_TOKEN += unary_node.token_count
            return AST_Node(FACTOR_TOKEN, None, [unary_node], OFFSET_TOKEN)

        # Parse PAD operations
        if tokens[OFFSET_TOKEN].t_type in {PAD_RANDI_TOKEN, PAD_WIDTH_TOKEN, PAD_HEIGHT_TOKEN, PAD_READ_TOKEN}:
            pad_node = AST_Node(tokens[OFFSET_TOKEN].t_type, parameters=tokens[OFFSET_TOKEN].value)
            OFFSET_TOKEN += 1
            return AST_Node(FACTOR_TOKEN, None, [pad_node], OFFSET_TOKEN)

        # Return an invalid node if no valid factor is found
        return AST_Node(INVALID_TOKEN, None, [], OFFSET_TOKEN)

    '''
    ========================= TERM() ========================= 
    '''
    def term(self, tokens):
        OFFSET_TOKEN = 0

        # If there are no tokens, return an invalid node
        if len(tokens) < 1:
            return AST_Node(INVALID_TOKEN, None, [], OFFSET_TOKEN)

        factors = []
        multiplicative_ops = []

        # Parse the first factor
        factor_node = self.factor(tokens[OFFSET_TOKEN:])
        if factor_node.t_type == FACTOR_TOKEN:
            factors.append(factor_node)
            OFFSET_TOKEN += factor_node.token_count

            # Parse additional factors and multiplicative operations
            while OFFSET_TOKEN < len(tokens) and tokens[OFFSET_TOKEN].t_type == MULTIPLICATIVE_OP_TOKEN:
                multiplicative_op_node = AST_Node('multiplicative_op', parameters=tokens[OFFSET_TOKEN].value)
                multiplicative_ops.append(multiplicative_op_node)
                OFFSET_TOKEN += 1
                factor_node = self.factor(tokens[OFFSET_TOKEN:])
                if factor_node.t_type == FACTOR_TOKEN:
                    factors.append(factor_node)
                    OFFSET_TOKEN += factor_node.token_count
                else:
                    return AST_Node(INVALID_TOKEN, None, [], OFFSET_TOKEN)

            # If there is only one factor, return it as the term
            if len(factors) == 1:
                return AST_Node(TERM_TOKEN, None, factors, OFFSET_TOKEN)
            else:
                # Stack the operations for multiple factors
                def stack_operations(factors, multiplicative_ops):
                    if len(factors) == 2:
                        return AST_Node(MULTIPLICATIVE_OP_TOKEN, {'OP': multiplicative_ops[0].parameters}, [factors[0], factors[1]], 0)
                    else:
                        return AST_Node(MULTIPLICATIVE_OP_TOKEN, {'OP': multiplicative_ops[0].parameters}, [factors[0], stack_operations(factors[1:], multiplicative_ops[1:])], 0)

                operations = stack_operations(factors, multiplicative_ops)
                return AST_Node(TERM_TOKEN, None, [operations], OFFSET_TOKEN)

        # Return an invalid node if no valid term is found
        return AST_Node(INVALID_TOKEN, None, [], OFFSET_TOKEN)
    
    '''
    ========================= SIMPLE_EXPRESSION() ========================= 
    '''
    def simple_expr(self, tokens):
        OFFSET_TOKEN = 0

        # If there are no tokens, return an invalid node
        if len(tokens) < 1:
            return AST_Node(INVALID_TOKEN, None, [], OFFSET_TOKEN)

        terms = []
        additive_ops = []

        # Parse the first term
        term_node = self.term(tokens[OFFSET_TOKEN:])
        if term_node.t_type == TERM_TOKEN:
            terms.append(term_node)
            OFFSET_TOKEN += term_node.token_count

            # Parse additional terms and additive operations
            while OFFSET_TOKEN < len(tokens) and tokens[OFFSET_TOKEN].t_type == ADDITIVE_OP_TOKEN:
                additive_op_node = AST_Node('additive_op', parameters=tokens[OFFSET_TOKEN].value)
                additive_ops.append(additive_op_node)
                OFFSET_TOKEN += 1
                term_node = self.term(tokens[OFFSET_TOKEN:])
                if term_node.t_type == TERM_TOKEN:
                    terms.append(term_node)
                    OFFSET_TOKEN += term_node.token_count
                else:
                    return AST_Node(INVALID_TOKEN, None, [], OFFSET_TOKEN)

            # If there is only one term, return it as the simple expression
            if len(terms) == 1:
                return AST_Node(SIMPLE_EXPRESSION_TOKEN, None, terms, OFFSET_TOKEN)
            else:
                # Stack the operations for multiple terms
                def stack_operations(terms, additive_ops):
                    if len(terms) == 2:
                        return AST_Node(ADDITIVE_OP_TOKEN, {'OP': additive_ops[0].parameters}, [terms[0], terms[1]], 0)
                    else:
                        return AST_Node(ADDITIVE_OP_TOKEN, {'OP': additive_ops[0].parameters}, [terms[0], stack_operations(terms[1:], additive_ops[1:])], 0)

                operations = stack_operations(terms, additive_ops)
                return AST_Node(SIMPLE_EXPRESSION_TOKEN, None, [operations], OFFSET_TOKEN)

        # Return an invalid node if no valid simple expression is found
        return AST_Node(INVALID_TOKEN, None, [], OFFSET_TOKEN)

    '''
    ========================= RANDI() ========================= 
    '''
    def randi(self, tokens):
        OFFSET_TOKEN = 0

        # If there are no tokens, return an invalid node
        if len(tokens) < 1:
            return AST_Node(INVALID_TOKEN, None, [], OFFSET_TOKEN)

        expr_1 = None
        # Parse the PAD_RANDI operation
        if tokens[OFFSET_TOKEN].t_type == PAD_RANDI_TOKEN:
            OFFSET_TOKEN += 1
            expr_node = self.expr(tokens[OFFSET_TOKEN:])
            if expr_node.t_type == EXPRESSION_TOKEN:
                expr_1 = expr_node
                OFFSET_TOKEN += expr_node.token_count
                return AST_Node(PAD_RANDI_TOKEN, None, [expr_1], OFFSET_TOKEN)

        # Return an invalid node if PAD_RANDI operation is not valid
        return AST_Node(INVALID_TOKEN, None, [], OFFSET_TOKEN)

    '''
    ========================= EXPRESSION() (NOT SIMPLE) ========================= 
    '''
    def expr(self, tokens):
        OFFSET_TOKEN = 0

        # If there are no tokens, return an invalid node
        if len(tokens) < 1:
            return AST_Node(INVALID_TOKEN, None, [], OFFSET_TOKEN)

        smp_exprs = []
        rel_ops = []
        simple_exprs = []
        relational_ops = []

        # Parse the first simple expression
        simple_expr_node = self.simple_expr(tokens[OFFSET_TOKEN:])
        if simple_expr_node.t_type == SIMPLE_EXPRESSION_TOKEN:
            smp_exprs.append(simple_expr_node)
            OFFSET_TOKEN += simple_expr_node.token_count

            # Parse additional simple expressions and relational operations
            while OFFSET_TOKEN < len(tokens) and tokens[OFFSET_TOKEN].t_type == RELATIONAL_OP_TOKEN:
                relational_op_node = AST_Node('relational_op', parameters=tokens[OFFSET_TOKEN].value)
                rel_ops.append(relational_op_node)
                OFFSET_TOKEN += 1
                simple_expr_node = self.simple_expr(tokens[OFFSET_TOKEN:])
                if simple_expr_node.t_type == SIMPLE_EXPRESSION_TOKEN:
                    smp_exprs.append(simple_expr_node)
                    OFFSET_TOKEN += simple_expr_node.token_count
                else:
                    return AST_Node(INVALID_TOKEN, None, [], OFFSET_TOKEN)

            # If there is only one simple expression, return it as the expression
            if len(smp_exprs) == 1:
                return AST_Node(EXPRESSION_TOKEN, None, smp_exprs, OFFSET_TOKEN)
            else:
                # Stack the operations for multiple simple expressions
                def stack_operations(simple_exprs, relational_ops):
                    if len(simple_exprs) == 2:
                        return AST_Node(RELATIONAL_OP_TOKEN, {'OP': relational_ops[0].parameters}, [simple_exprs[0], simple_exprs[1]], 0)
                    else:
                        return AST_Node(RELATIONAL_OP_TOKEN, {'OP': relational_ops[0].parameters}, [simple_exprs[0], stack_operations(simple_exprs[1:], relational_ops[1:])], 0)

                operations = stack_operations(smp_exprs, rel_ops)
                return AST_Node(EXPRESSION_TOKEN, None, [operations], OFFSET_TOKEN)

        # Return an invalid node if no valid expression is found
        return AST_Node(INVALID_TOKEN, None, [], OFFSET_TOKEN)

    '''
    ========================= LITERAL() ========================= 
    '''
    def literal(self, tokens):
        OFFSET_TOKEN = 0

        # If there are no tokens, return an invalid node
        if len(tokens) < 1:
            return AST_Node(INVALID_TOKEN, None, [], OFFSET_TOKEN)

        # Parse the literal value
        if tokens[0].t_type in {
            BOOLEAN_LITERAL_TOKEN, INTEGER_LITERAL_TOKEN, FLOAT_LITERAL_TOKEN,
            COLOR_LITERAL_TOKEN, PAD_WIDTH_TOKEN, PAD_HEIGHT_TOKEN, PAD_READ_TOKEN
        }:
            literal_node = AST_Node(tokens[0].t_type, parameters=tokens[0].value)
            OFFSET_TOKEN += 1
            return AST_Node(LITERAL_TOKEN, None, [literal_node], OFFSET_TOKEN)

        # Return an invalid node if no valid literal is found
        return AST_Node(INVALID_TOKEN, None, [], OFFSET_TOKEN)

    '''
    ========================= CALL FUNCTION (function_call()) ========================= 
    '''
    def function_call(self, tokens):
        OFFSET_TOKEN = 0

        # If the number of tokens is less than 4, return an invalid node
        if len(tokens) < 4:
            return AST_Node(INVALID_TOKEN, None, [], OFFSET_TOKEN)

        iden_1 = None
        actual_parameters_1 = None

        # Parse the function call
        if tokens[OFFSET_TOKEN].t_type == IDENTIFIER_TOKEN:
            iden_1 = AST_Node('identifier', parameters=tokens[OFFSET_TOKEN].value)
            OFFSET_TOKEN += 1
            if tokens[OFFSET_TOKEN].t_type == LPAREN_TOKEN:
                OFFSET_TOKEN += 1
                actual_params_node = self.actual_params(tokens[OFFSET_TOKEN:])
                if actual_params_node.t_type == ACTUAL_PARAMETERS_TOKEN:
                    actual_parameters_1 = actual_params_node
                    OFFSET_TOKEN += actual_params_node.token_count
                    if tokens[OFFSET_TOKEN].t_type == RPAREN_TOKEN:
                        OFFSET_TOKEN += 1
                        return AST_Node(FUNCTION_CALL_TOKEN, None, [iden_1, actual_parameters_1], OFFSET_TOKEN)
                elif tokens[OFFSET_TOKEN].t_type == RPAREN_TOKEN:
                    OFFSET_TOKEN += 1
                    return AST_Node(FUNCTION_CALL_TOKEN, None, [iden_1], OFFSET_TOKEN)

        # Return an invalid node if the function call is not valid
        return AST_Node(INVALID_TOKEN, None, [], OFFSET_TOKEN)

    '''
    ========================= ACTUAL_PARMS() ========================= 
    '''
    def actual_params(self, tokens):
        OFFSET_TOKEN = 0

        # If there are no tokens, return an invalid node
        if len(tokens) < 1:
            return AST_Node(INVALID_TOKEN, None, [], OFFSET_TOKEN)

        exprs = []
        expressions = []

        # Parse the first expression
        expr_node = self.expr(tokens[OFFSET_TOKEN:])
        if expr_node.t_type == EXPRESSION_TOKEN:
            exprs.append(expr_node)
            OFFSET_TOKEN += expr_node.token_count

            # Parse additional expressions separated by commas
            while OFFSET_TOKEN < len(tokens) and tokens[OFFSET_TOKEN].t_type == COMMA_TOKEN:
                OFFSET_TOKEN += 1
                expr_node = self.expr(tokens[OFFSET_TOKEN:])
                if expr_node.t_type == EXPRESSION_TOKEN:
                    exprs.append(expr_node)
                    OFFSET_TOKEN += expr_node.token_count
                else:
                    return AST_Node(INVALID_TOKEN, None, [], OFFSET_TOKEN)

            return AST_Node(ACTUAL_PARAMETERS_TOKEN, None, exprs, OFFSET_TOKEN)

        # Return an invalid node if no valid actual parameters are found
        return AST_Node(INVALID_TOKEN, None, [], OFFSET_TOKEN)

    '''
    ========================= SUB_EXPRESSION() ========================= 
    '''
    def sub_expr(self, tokens):
        OFFSET_TOKEN = 0

        # If the number of tokens is less than 3, return an invalid node
        if len(tokens) < 3:
            return AST_Node(INVALID_TOKEN, None, [], OFFSET_TOKEN)

        # Parse the sub-expression
        if tokens[OFFSET_TOKEN].t_type == LPAREN_TOKEN:
            OFFSET_TOKEN += 1
            expr_node = self.expr(tokens[OFFSET_TOKEN:])
            if expr_node.t_type == EXPRESSION_TOKEN:
                OFFSET_TOKEN += expr_node.token_count
                if OFFSET_TOKEN < len(tokens) and tokens[OFFSET_TOKEN].t_type == RPAREN_TOKEN:
                    OFFSET_TOKEN += 1
                    return AST_Node(SUB_EXPRESSION_TOKEN, None, [expr_node], OFFSET_TOKEN)

        # Return an invalid node if the sub-expression is not valid
        return AST_Node(INVALID_TOKEN, None, [], OFFSET_TOKEN)