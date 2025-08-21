import math
import numexpr
# from src.servers.calculator.model import CalculatorInput, CalculatorOutput
from model import CalculatorInput, CalculatorOutput

def calculator(input: CalculatorInput) -> CalculatorOutput:
    """
    Evaluates a mathematical expression using the python library numexpr
    and returns the result. The input expression can include
    mathematical constants like pi and e.
    Args:
        input (str): A string containing only numbers or mathematical expressions.
    Returns:
        output (str): The result of the expression evaluation.
    Raises:
        Exception: If the evaluation fails, an error message is returned.
    """
    local_dict = {"pi": math.pi, "e": math.e}
    try:
        result = numexpr.evaluate(input.input.strip(), global_dict={}, local_dict=local_dict)
        return CalculatorOutput(output=str(result))
    except Exception as e:
        return CalculatorOutput(output=f"Error: {str(e)}")