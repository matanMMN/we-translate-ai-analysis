import subprocess

def convert_file(input_file:str, output_file:str, from_format:str, to_format:str):
    """
    Convert a file from one format to another using Pandoc.
    
    :param input_file: The path to the input file.
    :param output_file: The path where the output file should be saved.
    :param from_format: The format of the input file (e.g., 'markdown', 'html').
    :param to_format: The format to convert to (e.g., 'pdf', 'docx').
    """
    command = ['pandoc', input_file, '-f', from_format, '-t', to_format, '-o', output_file]
    
    try:
        subprocess.run(command, check=True)
        return True
    except subprocess.CalledProcessError as e:
        return False

