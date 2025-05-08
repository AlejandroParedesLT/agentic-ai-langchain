import math
import numexpr
from src.servers.calculator.model import CalculatorInput, CalculatorOutput

def calculator(input: CalculatorInput) -> CalculatorOutput:
    """Evaluate a mathematical expression."""
    local_dict = {"pi": math.pi, "e": math.e}
    try:
        result = numexpr.evaluate(input.input.strip(), global_dict={}, local_dict=local_dict)
        return CalculatorOutput(output=str(result))
    except Exception as e:
        return CalculatorOutput(output=f"Error: {str(e)}")