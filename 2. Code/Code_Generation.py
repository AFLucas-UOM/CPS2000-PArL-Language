from PArL import *

'''
========================= CODEGenerator ========================= 
'''
class CodeGenerator:
    def __init__(self):
        # Initialize stack, return value, frame index, and stack level
        self.stack = [{}]
        self.return_ = None

        self.frame_index = 0  
        self.stack_level = 0  # for SoF 

        self.code_blocks = []
        self.code = ''

        self.padheight = 8
        self.padwidth = 8
        self.padrandi = 2

        self.add_code = True  # Flag to control code addition

    '''
    ========================= program() ========================= 
    '''
    def program(self, program):
        main = []
        other = []

        # Separate main and function declarations
        for node in program.children:
            if isinstance(node, AST_Node):
                if node.t_type != 'FUNCTION_DECLARATION':
                    main.append(node)
                else:
                    other.append(node)

        # Generate code for function declarations
        for node in other:
            self.add_code = True
            self.generate(node)

        # Generate code for main function
        self.add_code = True
        self.code_blocks.append([])
        self.code_blocks[-1].append('.main\n')

        # Count number of variable declarations (always declare at least 1)
        var_declarations = 1
        for node in main:
            if node.t_type == 'VARIABLE_DECLARATION':
                var_declarations += 1

        # Allocate space for variables
        if var_declarations > 0:
            self.add_command(PAR_PUSH, var_declarations)
            self.add_command(PAR_OFRAME)
        self.add_command(PAR_PUSH, '#ffffff')
        self.add_command(PAR_CLEAR)

        # Initialize stack level and frame index
        self.stack_level = 0
        self.frame_index = 0

        # Generate code for main block
        for node in main:
            self.add_code = True
            self.generate(node)

        # Add HALT command
        self.add_code = True
        self.add_command(PAR_HALT)

        # Join all code blocks into a single string
        self.code = ''.join([''.join(block) for block in self.code_blocks])
        print("\033[92m\033[1mCode Generation successful! - Check 'output.txt'\033[0m")

    '''
    ========================= generate() ========================= 
    '''
    def generate(self, node):
        if isinstance(node, AST_Node):
            if node.t_type == 'VARIABLE_DECLARATION':
                self.variable_decl(node)
            elif node.t_type == 'ASSIGNMENT':
                self.assignment(node)
            elif node.t_type == 'PRINT_STATEMENT':
                self.print_statement(node)
            elif node.t_type == 'DELAY_STATEMENT':
                self.delay_statement(node)
            elif node.t_type == 'IF_STATEMENT':
                self.if_statement(node)
            elif node.t_type == 'FOR_STATEMENT':
                self.for_statement(node)
            elif node.t_type == 'WHILE_STATEMENT':
                self.while_statement(node)
            elif node.t_type == 'RETURN_STATEMENT':
                self.return_statement(node)
            elif node.t_type == 'FUNCTION_DECLARATION':
                self.function_decl(node)
            elif node.t_type == 'WRITE_TOKEN':
                self.write_statement(node)
            elif node.t_type == 'WRITE_BOX_TOKEN':
                self.write_box_statement(node)

    default = {
        'int': 1,
        'float': 1.0,
        'bool': True,
        'color': '#FFFFFF',
    }

    '''
    ========================= stack_get() ========================= 
    '''
    def stack_get(self, node):
        # Retrieve a variable from the stack
        for frame in reversed(self.stack):
            if node.text in frame:
                return frame[node.parameters]
        return False

    '''
    ========================= stack_set() ========================= 
    '''
    def stack_set(self, node, value):
        # Set a variable in the stack
        for frame in self.stack:
            if node.parameters in frame:
                if isinstance(value, list):
                    frame[node.parameters] = value
                else:
                    frame[node.parameters][1] = value
                return True

        if isinstance(value, list):
            self.stack[-1][node.parameters] = value
        else:
            type_ = type(value).__name__
            self.stack[-1][node.parameters] = [type_, value]

    '''
    ========================= add_command() ========================= 
    '''
    def add_command(self, operator, operand=None):
        # Add a command to the current code block
        if self.add_code and operator is not None:
            if operand is not None:
                if isinstance(operand, list):
                    if operator == PAR_PUSH_STACK:
                        self.code_blocks[-1].append(f"{operator}[{operand[0]}:{operand[1]}]\n")
                else:
                    operand = str(operand)
                    if operator == PAR_OFRAME:
                        pass
                    if operator == PAR_PUSH_DOT:
                        operand = operand.lower()
                        self.code_blocks[-1].append(f"{operator}{operand}\n")
                    elif operator == PAR_PUSH_STACK:
                        self.code_blocks[-1].append(f"{operator}[{operand}]\n")
                    else:
                        self.code_blocks[-1].append(f"{operator} {operand}\n")
            else:
                self.code_blocks[-1].append(f"{operator}\n")

    '''
    ========================= variable_decl() ========================= 
    '''
    def variable_decl(self, node):
        identifier = node.children[0]
        type_ = node.children[1]
        expr = node.children[2]
        val = self.code_evaluate(expr)
        self.stack_set(identifier, [type_.parameters, val, self.frame_index, self.stack_level])

        # Push the value onto the stack
        if val is not None and val not in ['__height', '__width', '__randi']:
            self.add_command(PAR_PUSH, val)
        self.add_command(PAR_PUSH, self.frame_index)
        self.add_command(PAR_PUSH, self.stack_level)
        self.add_command(PAR_ST)

        self.frame_index += 1

    '''
    ========================= assignment() ========================= 
    '''
    def assignment(self, node):
        identifier = node.children[0]
        expr = node.children[1]
        val = self.code_evaluate(expr)
        mem_loc = self.stack_get(identifier)

        # Push the value and memory location onto the stack
        self.add_command(PAR_PUSH, val)
        self.add_command(PAR_PUSH, mem_loc[2])  # frame index
        self.add_command(PAR_PUSH, mem_loc[3])  # level in SoF
        self.add_command(PAR_ST)
        self.stack_set(identifier, val)

    '''
    ========================= print_statement() ========================= 
    '''
    def print_statement(self, node):
        expr = node.children[0]
        val = self.code_evaluate(expr)

        # Push the value and print
        if val:
            self.add_command(PAR_PUSH, val)
        self.add_command(PAR_PRINT)

    '''
    ========================= delay_statement() ========================= 
    '''
    def delay_statement(self, node):
        expr = node.children[0]
        val = self.code_evaluate(expr)

        # Push the value and delay
        if val:
            self.add_command(PAR_PUSH, val)
        self.add_command(PAR_DELAY)

    '''
    ========================= if_statement() ========================= 
    '''
    def if_statement(self, node):
        start_index = len(self.code_blocks[-1])

        self.add_stack_frame()

        # Count number of variable declarations
        num_declarations = 0
        for statement in node.children[1].children:
            if isinstance(statement, AST_Node) and statement.t_type == 'VARIABLE_DECLARATION':
                num_declarations += 1

        self.add_command(PAR_PUSH, num_declarations)
        self.add_command(PAR_OFRAME)

        condition = node.children[0]
        block = node.children[1]
        else_ = None

        if len(node.children) > 2:
            else_ = node.children[2]

        # Evaluate condition and add conditional jump
        self.code_evaluate(condition)
        self.add_command(PAR_PUSH, 0)
        self.add_command(PAR_EQ)
        self.add_command(PAR_CJMP)

        original_frame_index = self.frame_index
        for statement in block.children:
            self.generate(statement)

        if_end_index = len(self.code_blocks[-1])

        self.frame_index = original_frame_index

        if else_:
            else_start_index = len(self.code_blocks[-1])
            for statement in else_.children:
                self.generate(statement)
            else_end_index = len(self.code_blocks[-1])

        # Insert jump commands
        if else_:
            self.code_blocks[-1].insert(start_index, f"push #PC+{else_start_index - start_index + 3}\n")
        else:
            self.code_blocks[-1].insert(start_index, f"push #PC+{if_end_index - start_index + 2}\n")

        if else_:
            self.code_blocks[-1].insert(if_end_index + 1, f"push #PC+{else_end_index + 1 - else_start_index + 1}\n")
            self.code_blocks[-1].insert(if_end_index + 2, PAR_JMP + "\n")

        self.remove_stack_frame()

    '''
    ========================= add_stack_frame() ========================= 
    '''
    def add_stack_frame(self):
        # Add a new stack frame
        self.stack.append({})
        self.stack_level = 0
        self.frame_index = 0

        for frame in self.stack[:-1]:
            for variable in frame:
                frame[variable][-1] += 1

    '''
    ========================= remove_stack_frame() ========================= 
    '''
    def remove_stack_frame(self):
        # Remove the current stack frame
        for frame in self.stack[:-1]:
            for variable in frame:
                frame[variable][-1] -= 1

        self.stack.pop()
        self.stack_level -= 1
        self.return_ = None
        self.add_command(PAR_CFRAME)

    '''
    ========================= for_statement() ========================= 
    '''
    def for_statement(self, node):
        self.add_stack_frame()

        # Count number of variable declarations
        variable_decl_count = 0
        for statement in node.children[3].children:
            if isinstance(statement, AST_Node) and statement.t_type == 'VARIABLE_DECLARATION':
                variable_decl_count += 1

        self.add_command(PAR_PUSH, 1 + variable_decl_count)
        self.add_command(PAR_OFRAME)

        for_start_index = len(self.code_blocks[-1])

        variable_decl_ = node.children[0]
        if variable_decl_:
            self.variable_decl(variable_decl_)

        condition = node.children[1]
        assignment = node.children[2]
        block = node.children[3]

        # Evaluate condition and add loop commands
        self.code_evaluate(condition)
        self.add_command(PAR_PUSH, 0)
        self.add_command(PAR_EQ)
        self.add_command(PAR_CJMP)
        for_condition_index = len(self.code_blocks[-1]) - 1
        for statement in block.children:
            self.generate(statement)

        self.generate(assignment)
        self.add_command(PAR_JMP)

        for_end_index = len(self.code_blocks[-1]) - 1

        # Insert jump commands
        self.code_blocks[-1].insert(for_condition_index, f"push #PC+{for_end_index - for_condition_index + 3}\n")
        for_end_index += 1
        self.code_blocks[-1].insert(for_end_index, f"push #PC-{for_end_index - for_condition_index + 5}\n")
        self.remove_stack_frame()

    '''
    ========================= while_statement() ========================= 
    '''
    def while_statement(self, node):
        self.add_stack_frame()

        # Count number of variable declarations
        variable_decl_count = 0
        for statement in node.children[1].children:
            if isinstance(statement, AST_Node) and statement.t_type == 'VARIABLE_DECLARATION':
                variable_decl_count += 1
        self.add_command(PAR_PUSH, 1 + variable_decl_count)
        self.add_command(PAR_OFRAME)

        while_start_index = len(self.code_blocks[-1])

        condition = node.children[0]
        block = node.children[1]

        # Evaluate condition and add loop commands
        self.code_evaluate(condition)
        self.add_command(PAR_PUSH, 0)
        self.add_command(PAR_EQ)
        self.add_command(PAR_CJMP)
        while_condition_index = len(self.code_blocks[-1]) - 1

        for statement in block.children:
            self.generate(statement)

        self.add_command(PAR_JMP)

        while_end_index = len(self.code_blocks[-1]) - 1

        # Insert jump commands
        self.code_blocks[-1].insert(while_condition_index, f"push #PC+{while_end_index - while_condition_index + 3}\n")
        while_end_index += 1
        self.code_blocks[-1].insert(while_end_index, f"push #PC-{while_end_index - while_condition_index + 5}\n")

        self.remove_stack_frame()

    '''
    ========================= return_statement() ========================= 
    '''
    def return_statement(self, node):
        expr = node.children[0]
        ret = self.code_evaluate(expr)

        # Add return commands
        if ret:
            self.add_command(PAR_PUSH, ret)
        self.add_command(PAR_RET)

    '''
    ========================= function_decl() ========================= 
    '''
    def function_decl(self, node):
        self.add_stack_frame()

        self.code_blocks.append([])

        identifier = node.children[0]
        if len(node.children) == 4:
            parameters = node.children[1].children
            type_ = node.children[2]
            block = node.children[3]
        else:
            parameters = []
            type_ = node.children[1]
            block = node.children[2]

        self.code_blocks[-1].append(f".{identifier.parameters.lower()}\n")

        # Count number of variable declarations
        variable_decl_count = 0
        for statement in block.children:
            if isinstance(statement, AST_Node) and statement.t_type == 'VARIABLE_DECLARATION':
                variable_decl_count += 1

        self.add_command(PAR_PUSH, len(parameters) + variable_decl_count)
        self.add_command(PAR_ALLOC)

        # Check if the function already exists
        if self.stack_get(identifier):
            print(f"Function {identifier.parameters} already exists")
        else:
            for parameter in parameters:
                param_identifier = parameter.children[0]
                param_type_ = parameter.children[1]
                self.stack_set(param_identifier, [
                               param_type_.parameters, self.default[param_type_.parameters], self.frame_index, self.stack_level])
                self.frame_index += 1

        for statement in block.children:
            self.generate(statement)

        self.stack_set(
            identifier, [type_.parameters, parameters, block, self.frame_index, self.stack_level])

    '''
    ========================= function_call() ========================= 
    '''
    def function_call(self, node):
        identifier = node.children[0]
        if len(node.children) == 2:
            arguments = node.children[1].children
        else:
            arguments = []

        # Push arguments onto the stack
        if len(arguments) > 0:
            for argument in reversed(arguments):
                argument = self.code_evaluate(argument)
                if argument:
                    self.add_command(PAR_PUSH, argument)
            self.add_command(PAR_PUSH, len(arguments))
        self.add_command(PAR_PUSH_DOT, identifier.parameters)
        self.add_command(PAR_CALL)

    '''
    ========================= write_statement() ========================= 
    '''
    def write_statement(self, node):
        # Handle __write statement
        for child in node.children:
            val = self.code_evaluate(child)
            if val:
                self.add_command(PAR_PUSH, val)
        self.add_command(PAR_WRITE)

    '''
    ========================= write_box_statement() ========================= 
    '''
    def write_box_statement(self, node):
        # Handle __write_box statement
        for child in node.children:
            val = self.code_evaluate(child)
            if val:
                self.add_command(PAR_PUSH, val)
        self.add_command(PAR_WRITE_BOX)

    '''
    ========================= code_evaluate() ========================= 
    '''
    def code_evaluate(self, node, iden=True):
        if isinstance(node, AST_Node):
            if node.t_type == 'IDENTIFIER':
                if iden:
                    self.add_command(PAR_PUSH_STACK, self.stack_get(node)[2:4])
                return self.stack_get(node)
            if node.t_type == 'PAD_HEIGHT':
                self.add_command(PAR_HEIGHT)
                return '__height'
            elif node.t_type == 'PAD_WIDTH':
                self.add_command(PAR_WIDTH)
                return '__width'
            elif node.t_type == 'PAD_RANDI':
                val = self.code_evaluate(node.children[0])
                if isinstance(val, int):
                    self.add_command(PAR_PUSH, node.children[0].parameters)
                self.add_command(PAR_IRND)
            elif node.t_type == 'INTEGER_LITERAL':
                return int(node.parameters)
            elif node.t_type == 'FLOAT_LITERAL':
                return float(node.parameters)
            elif node.t_type == 'BOOLEAN_LITERAL':
                return True if node.parameters == 'true' else False
            elif node.t_type == 'COLOR_LITERAL':
                return node.parameters
            elif node.t_type == 'FUNCTION_CALL':
                self.function_call(node)
            else:
                right = self.code_evaluate(node.children[1], False)
                left = self.code_evaluate(node.children[0], False)

                l_command = PAR_PUSH
                r_command = PAR_PUSH

                if left == '__height':
                    l_command = PAR_HEIGHT
                    left = None
                    self.code_blocks[-1].pop()
                elif left == '__width':
                    l_command = PAR_WIDTH
                    left = None
                    self.code_blocks[-1].pop()
                elif left == '__randi':
                    l_command = None
                    left = None

                if right == '__height':
                    r_command = PAR_HEIGHT
                    right = None
                    self.code_blocks[-1].pop()
                elif right == '__width':
                    r_command = PAR_WIDTH
                    right = None
                    self.code_blocks[-1].pop()
                elif right == '__randi':
                    r_command = None
                    right = None

                l_iden = left
                r_iden = right

                if node.children[0].t_type == 'IDENTIFIER':
                    l_iden = self.stack_get(node.children[0])[2:4]
                    l_command = PAR_PUSH_STACK
                if node.children[1].t_type == 'IDENTIFIER':
                    r_iden = self.stack_get(node.children[1])[2:4]
                    r_command = PAR_PUSH_STACK

                if node.t_type == 'RELATIONAL_OP':
                    if node.parameters == '<':
                        self.add_command(r_command, r_iden)
                        self.add_command(l_command, l_iden)
                        self.add_command(PAR_LT)
                    elif node.parameters == '>':
                        self.add_command(r_command, r_iden)
                        self.add_command(l_command, l_iden)
                        self.add_command(PAR_GT)
                    elif node.parameters == '==':
                        self.add_command(r_command, r_iden)
                        self.add_command(l_command, l_iden)
                        self.add_command(PAR_EQ)
                    elif node.parameters == '!=':
                        self.add_command(r_command, r_iden)
                        self.add_command(l_command, l_iden)
                        self.add_command(PAR_EQ)
                    elif node.parameters == '<=':
                        self.add_command(r_command, r_iden)
                        self.add_command(l_command, l_iden)
                        self.add_command(PAR_LE)
                    elif node.parameters == '>=':
                        self.add_command(r_command, r_iden)
                        self.add_command(l_command, l_iden)
                        self.add_command(PAR_GE)
                elif node.t_type == 'ADDITIVE_OP':
                    if node.parameters == '+':
                        self.add_command(r_command, r_iden)
                        self.add_command(l_command, l_iden)
                        self.add_command(PAR_ADD)
                    elif node.parameters == '-':
                        self.add_command(r_command, r_iden)
                        self.add_command(l_command, l_iden)
                        self.add_command(PAR_SUB)
                elif node.t_type == 'MULTIPLICATIVE_OP':
                    if node.parameters == '*':
                        self.add_command(r_command, r_iden)
                        self.add_command(l_command, l_iden)
                        self.add_command(PAR_MUL)
                    elif node.parameters == '/':
                        self.add_command(r_command, r_iden)
                        self.add_command(l_command, l_iden)
                        self.add_command(PAR_DIV)
                    elif node.parameters == 'and':
                        pass

    '''
    ========================= evaluate() ========================= 
    '''
    def evaluate(self, node):
        if isinstance(node, AST_Node):
            if node.t_type == 'FUNCTION_CALL':
                self.function_call(node)
                return self.return_
            elif node.t_type == 'PAD_HEIGHT':
                return '__height'
            elif node.t_type == 'PAD_WIDTH':
                return '__width'
            elif node.t_type == 'IDENTIFIER':
                if not self.stack_get(node):
                    raise Exception(f"Variable {node.parameters} does not exist")
                else:
                    iden = self.stack_get(node)
                    return iden[1]
            elif node.t_type == 'pad_randi':
                return '__randi'
            elif node.t_type == 'INTEGER_LITERAL':
                return int(node.parameters)
            elif node.t_type == 'FLOAT_LITERAL':
                return float(node.parameters)
            elif node.t_type == 'BOOLEAN_LITERAL':
                return True if node.parameters == 'true' else False
            elif node.t_type == 'COLOR_LITERAL':
                return node.parameters


'''
========================= ARRAY CODE GENERATOR - [TASK-5] ========================= 
'''
class ArrayCodeGenerator(CodeGenerator):
    def __init__(self):
        super().__init__()

    '''
    ========================= program() ========================= 
    '''
    def program(self, program):
        main = []
        other = []

        for node in program.children:
            if isinstance(node, AST_Node):
                if node.t_type != 'FUNCTION_DECLARATION':
                    main.append(node)
                else:
                    other.append(node)

        # Generate code for function declarations
        for node in other:
            self.add_code = True
            self.generate(node)

        # Generate code for main function
        self.add_code = True
        self.code_blocks.append([])
        self.code_blocks[-1].append('.main\n')

        # Count number of variable declarations (always declare at least 1)
        var_declarations = 1
        for node in main:
            if node.t_type == 'VARIABLE_DECLARATION':
                var_declarations += 1

        # Allocate space for variables
        if var_declarations > 0:
            self.add_command(PAR_PUSH, var_declarations)
            self.add_command(PAR_OFRAME)
        self.add_command(PAR_PUSH, '#ffffff')
        self.add_command(PAR_CLEAR)

        # Initialize stack level and frame index
        self.stack_level = 0
        self.frame_index = 0

        # Generate code for main block
        for node in main:
            self.add_code = True
            self.generate(node)

        # Add HALT command
        self.add_code = True
        self.add_command(PAR_HALT)

        # Join all code blocks into a single string
        self.code = ''.join([''.join(block) for block in self.code_blocks])
        print("\033[92m\033[1mCode Generation [Array] successful! - Check 'output2.txt'\033[0m")

    '''
    ========================= generate() ========================= 
    '''
    def generate(self, node):
        if isinstance(node, AST_Node):
            if node.t_type == 'ARRAY_DECLARATION':
                self.array_decl(node)
            elif node.t_type == 'ARRAY_ASSIGNMENT':
                self.array_assignment(node)
            elif node.t_type == 'ARRAY_ACCESS':
                self.array_access(node)
            else:
                super().generate(node)

    '''
    ========================= array_decl() ========================= 
    '''
    def array_decl(self, node):
        identifier = node.children[0]
        size_expr = node.children[1]
        size = self.code_evaluate(size_expr)

        # Allocate space for array
        self.stack_set(identifier, [size, self.frame_index, self.stack_level])
        self.add_command(PAR_PUSH, size)
        self.add_command(PAR_DUPA)

        self.frame_index += size

    '''
    ========================= array_assignment() ========================= 
    '''
    def array_assignment(self, node):
        identifier = node.children[0]
        index_expr = node.children[1]
        value_expr = node.children[2]
        
        index = self.code_evaluate(index_expr)
        value = self.code_evaluate(value_expr)
        array_info = self.stack_get(identifier)

        # Calculate memory location and assign value
        self.add_command(PAR_PUSH, value)
        self.add_command(PAR_PUSH, array_info[1] + index)
        self.add_command(PAR_PUSH, array_info[2])
        self.add_command(PAR_STA)

    '''
    ========================= array_access() ========================= 
    '''
    def array_access(self, node):
        identifier = node.children[0]
        index_expr = node.children[1]

        index = self.code_evaluate(index_expr)
        array_info = self.stack_get(identifier)

        # Calculate memory location and access value
        self.add_command(PAR_PUSH, array_info[1] + index)
        self.add_command(PAR_PUSH, array_info[2])
        self.add_command(PAR_PUSHA)

    '''
    ========================= add_command() ========================= 
    '''
    def add_command(self, operator, operand=None):
        if self.add_code and operator is not None:
            if operand is not None:
                if isinstance(operand, list):
                    if operator == PAR_PUSH_STACK:
                        self.code_blocks[-1].append(f"{operator}[{operand[0]}:{operand[1]}]\n")
                else:
                    operand = str(operand)
                    if operator == PAR_OFRAME:
                        pass
                    if operator == PAR_PUSH_DOT:
                        operand = operand.lower()
                        self.code_blocks[-1].append(f"{operator}{operand}\n")
                    elif operator == PAR_PUSH_STACK:
                        self.code_blocks[-1].append(f"{operator}[{operand}]\n")
                    else:
                        self.code_blocks[-1].append(f"{operator} {operand}\n")
            else:
                self.code_blocks[-1].append(f"{operator}\n")
                
    '''
    ========================= code_evaluate() - [FOR ARRAYS] ========================= 
    '''
    def code_evaluate(self, node, iden=True):
        if isinstance(node, AST_Node):
            if node.t_type == 'IDENTIFIER':
                if iden:
                    self.add_command(PAR_PUSH_STACK, self.stack_get(node)[2:4])
                return self.stack_get(node)
            if node.t_type == 'PAD_HEIGHT':
                self.add_command(PAR_HEIGHT)
                return '__height'
            elif node.t_type == 'PAD_WIDTH':
                self.add_command(PAR_WIDTH)
                return '__width'
            elif node.t_type == 'PAD_RANDI':
                val = self.code_evaluate(node.children[0])
                if isinstance(val, int):
                    self.add_command(PAR_PUSH, node.children[0].parameters)
                self.add_command(PAR_IRND)
            elif node.t_type == 'INTEGER_LITERAL':
                return int(node.parameters)
            elif node.t_type == 'FLOAT_LITERAL':
                return float(node.parameters)
            elif node.t_type == 'BOOLEAN_LITERAL':
                return True if node.parameters == 'true' else False
            elif node.t_type == 'COLOR_LITERAL':
                return node.parameters
            elif node.t_type == 'FUNCTION_CALL':
                self.function_call(node)
            else:
                right = self.code_evaluate(node.children[1], False)
                left = self.code_evaluate(node.children[0], False)

                l_command = PAR_PUSH
                r_command = PAR_PUSH

                if left == '__height':
                    l_command = PAR_HEIGHT
                    left = None
                    self.code_blocks[-1].pop()
                elif left == '__width':
                    l_command = PAR_WIDTH
                    left = None
                    self.code_blocks[-1].pop()
                elif left == '__randi':
                    l_command = None
                    left = None

                if right == '__height':
                    r_command = PAR_HEIGHT
                    right = None
                    self.code_blocks[-1].pop()
                elif right == '__width':
                    r_command = PAR_WIDTH
                    right = None
                    self.code_blocks[-1].pop()
                elif right == '__randi':
                    r_command = None
                    right = None

                l_iden = left
                r_iden = right

                if node.children[0].t_type == 'IDENTIFIER':
                    l_iden = self.stack_get(node.children[0])[2:4]
                    l_command = PAR_PUSH_STACK
                if node.children[1].t_type == 'IDENTIFIER':
                    r_iden = self.stack_get(node.children[1])[2:4]
                    r_command = PAR_PUSH_STACK

                # Add commands for relational, additive, and multiplicative operations
                if node.t_type == 'RELATIONAL_OP':
                    if node.parameters == '<':
                        self.add_command(r_command, r_iden)
                        self.add_command(l_command, l_iden)
                        self.add_command(PAR_LT)
                    elif node.parameters == '>':
                        self.add_command(r_command, r_iden)
                        self.add_command(l_command, l_iden)
                        self.add_command(PAR_GT)
                    elif node.parameters == '==':
                        self.add_command(r_command, r_iden)
                        self.add_command(l_command, l_iden)
                        self.add_command(PAR_EQ)
                    elif node.parameters == '!=':
                        self.add_command(r_command, r_iden)
                        self.add_command(l_command, l_iden)
                        self.add_command(PAR_EQ)
                    elif node.parameters == '<=':
                        self.add_command(r_command, r_iden)
                        self.add_command(l_command, l_iden)
                        self.add_command(PAR_LE)
                    elif node.parameters == '>=':
                        self.add_command(r_command, r_iden)
                        self.add_command(l_command, l_iden)
                        self.add_command(PAR_GE)
                elif node.t_type == 'ADDITIVE_OP':
                    if node.parameters == '+':
                        self.add_command(r_command, r_iden)
                        self.add_command(l_command, l_iden)
                        self.add_command(PAR_ADD)
                    elif node.parameters == '-':
                        self.add_command(r_command, r_iden)
                        self.add_command(l_command, l_iden)
                        self.add_command(PAR_SUB)
                elif node.t_type == 'MULTIPLICATIVE_OP':
                    if node.parameters == '*':
                        self.add_command(r_command, r_iden)
                        self.add_command(l_command, l_iden)
                        self.add_command(PAR_MUL)
                    elif node.parameters == '/':
                        self.add_command(r_command, r_iden)
                        self.add_command(l_command, l_iden)
                        self.add_command(PAR_DIV)
                    elif node.parameters == 'and':
                        pass