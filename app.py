"""
FastAPI backend for Clinical Trial Protocol Analyzer.

This module provides REST API endpoints for uploading a clinical trial protocol,
running analysis, and querying results.
"""

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from clinical_protocol_agent import ProtocolAnalyzer
from typing import Dict
import os
import tempfile

app = FastAPI(title="CRA App - Clinical Research Assistant")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

current_analyzer = None


@app.post("/api/upload")
async def upload_protocol(file: UploadFile = File(...)) -> Dict:
    global current_analyzer

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")

    tmp_path = None

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            contents = await file.read()
            tmp_file.write(contents)
            tmp_path = tmp_file.name

        current_analyzer = ProtocolAnalyzer()
        current_analyzer.load_protocol(tmp_path)

        summary = current_analyzer.generate_summary()
        issues = current_analyzer.check_discrepancies()

        page_count = 0
        if hasattr(current_analyzer, "protocol_text") and current_analyzer.protocol_text:
            page_count = max(1, len(current_analyzer.protocol_text.split("\n")) // 30)

        return {
            "status": "success",
            "message": "Protocol uploaded and analyzed successfully",
            "summary": summary,
            "issues": issues,
            "page_count": page_count,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")

    finally:
        if tmp_path and os.path.exists(tmp_path):
            os.unlink(tmp_path)


@app.get("/api/summary")
def get_summary() -> Dict:
    if current_analyzer is None:
        raise HTTPException(status_code=400, detail="No protocol loaded. Please upload a protocol first.")

    summary = current_analyzer.generate_summary()
    return {"status": "success", "summary": summary}


@app.get("/api/issues")
def get_issues() -> Dict:
    if current_analyzer is None:
        raise HTTPException(status_code=400, detail="No protocol loaded. Please upload a protocol first.")

    issues = current_analyzer.check_discrepancies()
    return {"status": "success", "issues": issues}


@app.post("/api/search")
def search_protocol(query: Dict) -> Dict:
    if current_analyzer is None:
        raise HTTPException(status_code=400, detail="No protocol loaded. Please upload a protocol first.")

    if "query" not in query:
        raise HTTPException(status_code=400, detail="Missing 'query' parameter")

    search_query = query["query"].strip()
    if not search_query:
        raise HTTPException(status_code=400, detail="Search query cannot be empty")

    results = current_analyzer.search_protocol(search_query)
    return {"status": "success", "query": search_query, "results": results}


@app.get("/api/section")
def get_section(section_name: str) -> Dict:
    if current_analyzer is None:
        raise HTTPException(status_code=400, detail="No protocol loaded. Please upload a protocol first.")

    if not section_name:
        raise HTTPException(status_code=400, detail="Section name is required")

    section_text = current_analyzer.get_section(section_name)
    return {"status": "success", "section_name": section_name, "content": section_text}


@app.get("/")
def read_root():
    return FileResponse("index.html")


if __name__ == "__main__":
    import uvicorn
    print("Starting CRA App - Clinical Research Assistant")
    print("Access the application at: http://localhost:8001")
    uvicorn.run(app, host="0.0.0.0", port=8001)