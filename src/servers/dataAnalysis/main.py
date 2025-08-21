# from src.servers.dataAnalysis.model import DataAnalysisInput, DataAnalysisOutput
# from src.servers.dataAnalysis.utils import statistics
from model import DataAnalysisInput, DataAnalysisOutput
from utils import statistics
from fastapi import FastAPI, UploadFile, File

app = FastAPI()

@app.post("/process", response_model=DataAnalysisOutput)
async def process_data_analysis(file: UploadFile = File(...)) -> DataAnalysisOutput:
    """
    Process a CSV file and return statistical analysis.
    """
    return statistics(file)
