import sys
import os

from PArL import * # PArL Basic Structure [TASKS 1-5]

# Import the required classes from the modules
from Lexer import Lexer # TASK-1
from Parser import Parser # TASK-2
from Semantic_Analysis import SemanticAnalysis # TASK-3
from Code_Generation import CodeGenerator, ArrayCodeGenerator # TASK-4 & 5

def main():
    # Check if the correct number of command-line arguments is provided
    if len(sys.argv) != 2:
        # Print the usage message in bold and red if incorrect arguments are provided
        
        # Example: python3 ./Assignment/Main.py ./Assignment/source.txt  
        print("\n\033[1;31mUsage: python3 Main.py /path/to/source.txt\033[0m\n")
        sys.exit(1)
    # Retrieve the path to the source file from the command-line arguments
    source_file_path = sys.argv[1]

    try:
        # Open the source file and read its contents
        with open(source_file_path, 'r', encoding='utf-8') as source_file:
            source_code = source_file.read()

        # Create a Lexer object and tokenize the source code
        lexer = Lexer()
        tokens = lexer.tokenize(source_code)

        # Create a Parser object and parse the tokens
        parser = Parser() 
        parser.parse(tokens)

        # Set the AST root node to the program node
        ast_root = parser.program_node

        # Create a SemanticAnalysis object and perform semantic analysis
        semantic_analysis = SemanticAnalysis()
        semantic_analysis.program(ast_root)

        # Create a CodeGenerator object and generate code
        code_generator = CodeGenerator()
        code_generator.program(ast_root)

        # Create a ArrayCodeGenerator object and generate code
        code_generatorARRAY = ArrayCodeGenerator()
        code_generatorARRAY.program(ast_root)

        # Get the directory of the current script - same DIR
        current_directory = os.path.dirname(__file__)
        output_file_path = os.path.join(current_directory, 'output.txt')
        output_file_path2 = os.path.join(current_directory, 'output2.txt')

        # Write the generated code to the output file
        with open(output_file_path, 'w', encoding='utf-8') as f:
            for code_block in code_generator.code_blocks:
                f.write(''.join(code_block))

        # Write the generated code to the output2 [ARRAY] file
        with open(output_file_path2, 'w', encoding='utf-8') as f:
            for code_block in code_generatorARRAY.code_blocks:
                f.write(''.join(code_block))

    except FileNotFoundError:
        # Handle the case where the source file is not found
        print(f"Error: File '{source_file_path}' not found.")
    except Exception as e:
        # Handle any other exceptions that occur during the process
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    main()