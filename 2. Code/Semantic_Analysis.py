from PArL import *

'''
========================= FLATTEN (error-fix) ========================= 
'''
def flatten(lst):
    # Flattens a nested list structure
    for item in lst:
        if isinstance(item, list):
            yield from flatten(item)
        else:
            yield item

'''
========================= Semantic Analysis ========================= 
'''
class SemanticAnalysis:
    def __init__(self):
        # Initialize stack and default values
        self.stack = [{}]
        self.return_ = None
        self.defaults = {
            'int': 0,
            'float': 0.0,
            'boolean': False,
            'color': '#000000'
        }

    '''
    ========================= program() ========================= 
    '''
    def program(self, program_node):
        # Check if the program node has children
        if not hasattr(program_node, 'children'):
            raise ValueError("program_node does not have 'children' attribute")
        
        # Flatten the children of the program node
        program_node.children = list(flatten(program_node.children))
        
        # Analyze each child node
        for node in program_node.children:
            self.analyse(node)
        
        # Print success message
        print("\033[1;32mSemantic Analysis successful!\033[0m")

    '''
    ========================= analyse() ========================= 
    '''
    def analyse(self, node):
        # Check if the node is an instance of AST_Node
        if isinstance(node, AST_Node):
            tag = '<' + node.t_type + '>'
            # Identify the node type and call the appropriate method
            if tag == VARIABLE_DECLARATION_TOKEN:
                self.variable_decl(node)
            elif tag == ASSIGNMENT_TOKEN:
                self.assignment(node)
            elif tag == PRINT_STATEMENT_TOKEN:
                self.print_statement(node)
            elif tag == DELAY_STATEMENT_TOKEN:
                self.delay_statement(node)
            elif tag == IF_STATEMENT_TOKEN:
                self.if_statement(node)
            elif tag == FOR_STATEMENT_TOKEN:
                self.for_statement(node)
            elif tag == WHILE_STATEMENT_TOKEN:
                self.while_statement(node)
            elif tag == RETURN_STATEMENT_TOKEN:
                self.return_statement(node)
            elif tag == FUNCTION_DECLARATION_TOKEN:
                self.function_decl(node)
            else:
                # Flatten and analyze each child node
                node.children = list(flatten(node.children))
                for child in node.children:
                    self.analyse(child)
        else:
            raise ValueError(f"Expected AST_Node, got {type(node)}")

    '''
    ========================= stack_get ========================= 
    '''
    def stack_get(self, node, current_scope_only=False):
        # Look for the variable in the current scope
        if node.parameters in self.stack[-1]:
            return self.stack[-1][node.parameters]
        
        # Look for the variable in all scopes if not restricted to current scope
        if not current_scope_only:
            for frame in reversed(self.stack[:-1]):
                if node.parameters in frame:
                    return frame[node.parameters]
        return False

    '''
    ========================= stack_set ========================= 
    '''
    def stack_set(self, node, value):
        # Set the variable in the current scope
        if isinstance(value, list):
            self.stack[-1][node.parameters] = value
        else:
            type_ = type(value).__name__
            self.stack[-1][node.parameters] = [type_, value]

    '''
    ========================= variable_decl ========================= 
    '''
    def variable_decl(self, node):
        identifier = node.children[0]
        type_ = node.children[1]
        expr = node.children[2]
        val = self.evaluate(expr)

        # Check for type mismatches
        if type_.parameters == 'int' and type(val) != int:
            raise ValueError(f"Type mismatch: expected int, got {type(val)}")
        elif type_.parameters == 'float' and type(val) != float:
            if type(val) == int:
                val = float(val)
            else:
                raise ValueError(f"Type mismatch: expected float, got {type(val)}")
        elif type_.parameters == 'boolean' and type(val) != bool:
            raise ValueError(f"Type mismatch: expected boolean, got {type(val)}")
        elif type_.parameters == 'color' and type(val) not in [str, int]:
            raise ValueError(f"Type mismatch: expected color, got {type(val)}")

        # Check for variable re-declaration in the current scope
        if self.stack_get(identifier, current_scope_only=True):
            raise ValueError(f"Variable '{identifier.parameters}' already declared in the current scope")
        else:
            self.stack[-1][identifier.parameters] = [type_.parameters, val]

    '''
    ========================= assignment ========================= 
    '''
    def assignment(self, node):
        identifier = node.children[0]
        expr = node.children[1]

        val = self.evaluate(expr)

        # Check if the variable exists before assignment
        if not self.stack_get(identifier):
            raise ValueError(f"Variable '{identifier.parameters}' does not exist")
        else:
            type_ = self.stack_get(identifier)[0]
            # Check for type mismatches
            if type_ == 'int' and type(val) != int:
                raise ValueError(f"Type mismatch: expected int, got {type(val)}")
            elif type_ == 'float' and type(val) != float:
                if type(val) == int:
                    val = float(val)
                else:
                    raise ValueError(f"Type mismatch: expected float, got {type(val)}")
            elif type_ == 'boolean' and type(val) != bool:
                raise ValueError(f"Type mismatch: expected boolean, got {type(val)}")
            elif type_ == 'color' and type(val) != str:
                raise ValueError(f"Type mismatch: expected color, got {type(val)}")

            self.stack_set(identifier, val)

    '''
    ========================= print_statement ========================= 
    '''
    def print_statement(self, node):
        expr = node.children[0]
        val = self.evaluate(expr)
        print(val)

    '''
    ========================= delay_statement ========================= 
    '''
    def delay_statement(self, node):
        expr = node.children[0]
        val = self.evaluate(expr)

    '''
    ========================= if_statement ========================= 
    '''
    def if_statement(self, node):
        condition = node.children[0]
        condition_val = self.evaluate(condition)

        # Analyze the appropriate block based on the condition value
        if condition_val:
            self.analyse(node.children[1])
        else:
            if len(node.children) == 3:
                self.analyse(node.children[2])

    '''
    ========================= for_statement ========================= 
    '''
    def for_statement(self, node):
        self.stack.append({})  # Enter a new scope

        variable_decl_ = node.children[0]
        if variable_decl_:
            self.variable_decl(variable_decl_)

        condition = node.children[1]
        assignment = node.children[2]
        block = node.children[3]

        # Loop while the condition is true
        while self.evaluate(condition):
            for statement in block.children:
                self.analyse(statement)

            if assignment:
                self.assignment(assignment)

        self.stack.pop()  # Exit the scope
        self.return_ = None

    '''
    ========================= while_statement ========================= 
    '''
    def while_statement(self, node):
        self.stack.append({})  # Enter a new scope

        condition = node.children[0]
        block = node.children[1]

        # Loop while the condition is true
        while self.evaluate(condition):
            for statement in block.children:
                self.analyse(statement)

        self.stack.pop()  # Exit the scope
        self.return_ = None

    '''
    ========================= return_statement ========================= 
    '''
    def return_statement(self, node):
        expr = node.children[0]
        val = self.evaluate(expr)
        self.stack.pop()  # Exit the current scope
        self.return_ = val

    '''
    ========================= function_decl ========================= 
    '''
    def function_decl(self, node):
        if len(node.children) == 4:
            identifier = node.children[0]
            parameters = node.children[1]
            type_ = node.children[2]
            block = node.children[3]
        else:
            identifier = node.children[0]
            parameters = []
            type_ = node.children[1]
            block = node.children[2]

        # Check for function re-declaration
        if self.stack_get(identifier):
            raise ValueError(f"Function '{identifier.parameters}' already exists")
        else:
            self.stack_set(identifier, [type_.parameters, parameters, block])

        self.stack.append({})  # Enter a new function scope

        # Add parameters to the function scope
        for parameter in parameters.children:
            param_identifier = parameter.children[0]
            if self.stack_get(param_identifier, current_scope_only=True):
                raise ValueError(f"Variable '{param_identifier.parameters}' already exists")
            param_type_ = parameter.children[1]
            self.stack_set(param_identifier, [param_type_.parameters, self.defaults[param_type_.parameters]])

        self.analyse(block)

        if self.return_ is None:
            raise ValueError(f"Function '{identifier.parameters}' does not have a return statement")
        elif type(self.return_).__name__ != type_.parameters:
            raise ValueError(f"Function '{identifier.parameters}' does not return '{type_.parameters}'")

        self.stack.pop()  # Exit the function scope
        self.return_ = None

    '''
    ========================= function_call ========================= 
    '''
    def function_call(self, node):
        if len(node.children) == 2:
            identifier = node.children[0]
            arguments = node.children[1]
        else:
            identifier = node.children[0]
            arguments = []

        function = self.stack_get(identifier)
        if not function:
            raise ValueError(f"Function '{identifier.parameters}' does not exist")
        else:
            func_params = function[1].children
            if len(arguments.children) != len(func_params):
                raise ValueError(f"Function '{identifier.parameters}' requires {len(func_params)} arguments")
            else:
                self.stack.append({})  # Enter a new scope for the function call
                for i in range(len(arguments.children)):
                    argument = arguments.children[i]
                    argument_type = func_params[i].children[1].parameters
                    argument_val = self.evaluate(argument)
                    if type(argument_val).__name__ != argument_type:
                        raise ValueError(f"Type mismatch: expected {argument_type}, got {type(argument_val).__name__}")
                    self.stack_set(func_params[i].children[0], [argument_type, argument_val])

                for statement in function[2].children:
                    self.analyse(statement)

                self.stack.pop()  # Exit the function call scope

    '''
    ========================= evaluate() ========================= 
    '''
    def evaluate(self, node):
        if node.t_type == 'function_call':
            self.function_call(node)
            return self.return_
        elif node.t_type == 'identifier':
            var = self.stack_get(node)
            if not var:
                raise ValueError(f"Variable '{node.parameters}' does not exist")
            else:
                return var[1]
        elif node.t_type == 'integer_literal':
            return int(node.parameters)
        elif node.t_type == 'float_literal':
            return float(node.parameters)
        elif node.t_type == 'boolean_literal':
            return True if node.parameters == 'true' else False
        elif node.t_type == 'color_literal':
            return node.parameters
        elif node.t_type == 'pad_randi':
            return 0
        elif node.t_type == 'pad_width':
            return 0
        elif node.t_type == 'pad_height':
            return 0
        elif node.t_type == 'additive_op':
            left = self.evaluate(node.children[0])
            right = self.evaluate(node.children[1])
            if node.parameters['OP'] == '+':
                return left + right
            elif node.parameters['OP'] == '-':
                return left - right
            elif node.parameters['OP'] == 'or':
                return left or right
        elif node.t_type == 'multiplicative_op':
            left = self.evaluate(node.children[0])
            right = self.evaluate(node.children[1])
            if node.parameters['OP'] == '*':
                return left * right
            elif node.parameters['OP'] == '/':
                return left / right
            elif node.parameters['OP'] == 'and':
                return left and right
        elif node.t_type == 'relational_op':
            left = self.evaluate(node.children[0])
            right = self.evaluate(node.children[1])
            if node.parameters['OP'] == '<':
                return left < right
            elif node.parameters['OP'] == '>':
                return left > right
            elif node.parameters['OP'] == '==':
                return left == right
            elif node.parameters['OP'] == '!=':
                return left != right
            elif node.parameters['OP'] == '<=':
                return left <= right
            elif node.parameters['OP'] == '>=':
                return left >= right
        elif node.t_type == 'write':
            if len(node.children) != 3:
                raise ValueError("Write instruction requires 3 arguments")
            arg1 = self.evaluate(node.children[0])
            arg2 = self.evaluate(node.children[1])
            arg3 = self.evaluate(node.children[2])
            if not isinstance(arg1, int):
                raise ValueError("First argument to write must be an int")
            if not isinstance(arg2, int):
                raise ValueError("Second argument to write must be an int")
            if not isinstance(arg3, str):
                raise ValueError("Third argument to write must be a color (string)")
            return
        else:
            raise ValueError(f"Unexpected t_type: {node.t_type}")