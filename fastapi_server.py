from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from API_Detector import API_Detector

app = FastAPI()
api_detector = API_Detector("rules")

@app.get("/{path}")
@app.post("/{path}")
async def catch_all(path: str, request: Request):
    api_request = request
    result = await api_detector.detect_malicious_request(api_request, "fastapi")
    return {"answer": result}
