import contextlib
import io
from src.servers.coding.model import CodingInput, CodingOutput

def execute_code(input: CodingInput):
    stdout = io.StringIO()
    try:
        with contextlib.redirect_stdout(stdout):
            exec(input.input, {})
    except Exception as e:
        return CodingOutput(output=f"Error: {e}")
    return CodingOutput(output=stdout.getvalue()) 
