"""
FastAPI backend for Clinical Trial Protocol Analyzer

This module provides REST API endpoints for the protocol analyzer,
allowing users to upload protocols and interact with the analysis
through HTTP requests.
"""

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
import tempfile
from clinical_protocol_agent import ProtocolAnalyzer
from typing import Dict, List

app = FastAPI(title="Clinical Trial Protocol Analyzer API")

# Enable CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global analyzer instance
current_analyzer = None


@app.post("/api/upload")
async def upload_protocol(file: UploadFile = File(...)) -> Dict:
    """
    Upload and process a clinical trial protocol PDF.
    
    This endpoint accepts a PDF file, extracts text from it, and prepares
    it for analysis. Returns basic protocol information and detected issues.
    
    Args:
        file (UploadFile): The PDF protocol file to upload.
    
    Returns:
        Dict: Contains protocol summary, detected issues, and page count.
    
    Raises:
        HTTPException: If the file is not a valid PDF or cannot be processed.
    """
    global current_analyzer
    
    # Validate file type
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")
    
    try:
        # Create a temporary file to store the upload
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            contents = await file.read()
            tmp_file.write(contents)
            tmp_path = tmp_file.name
        
        # Initialize analyzer with the uploaded file
        current_analyzer = ProtocolAnalyzer()
        current_analyzer.load_protocol(tmp_path)
        
        # Generate summary and check for issues
        summary = current_analyzer.generate_summary()
        issues = current_analyzer.check_discrepancies()
        
        # Clean up temporary file
        os.unlink(tmp_path)
        
        return {
            "status": "success",
            "message": "Protocol uploaded and analyzed successfully",
            "summary": summary,
            "issues": issues,
            "page_count": len(current_analyzer.protocol_text.split('\n')) // 30
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")


@app.get("/api/summary")
def get_summary() -> Dict:
    """
    Get the summary of the currently loaded protocol.
    
    Returns:
        Dict: Protocol summary information including presence of key sections.
    
    Raises:
        HTTPException: If no protocol is currently loaded.
    """
    if current_analyzer is None:
        raise HTTPException(status_code=400, detail="No protocol loaded. Please upload a protocol first.")
    
    summary = current_analyzer.generate_summary()
    return {"status": "success", "summary": summary}


@app.get("/api/issues")
def get_issues() -> Dict:
    """
    Get the list of detected issues in the current protocol.
    
    Returns:
        Dict: List of detected issues with severity levels and recommendations.
    
    Raises:
        HTTPException: If no protocol is currently loaded.
    """
    if current_analyzer is None:
        raise HTTPException(status_code=400, detail="No protocol loaded. Please upload a protocol first.")
    
    issues = current_analyzer.check_discrepancies()
    return {"status": "success", "issues": issues}


@app.post("/api/search")
def search_protocol(query: Dict) -> Dict:
    """
    Search for specific information in the current protocol.
    
    This endpoint searches the loaded protocol for lines containing
    the specified query term.
    
    Args:
        query (Dict): Dictionary containing 'query' key with search term.
    
    Returns:
        Dict: List of relevant lines from the protocol matching the query.
    
    Raises:
        HTTPException: If no protocol is loaded or query is missing.
    """
    if current_analyzer is None:
        raise HTTPException(status_code=400, detail="No protocol loaded. Please upload a protocol first.")
    
    if 'query' not in query:
        raise HTTPException(status_code=400, detail="Missing 'query' parameter")
    
    search_query = query['query'].strip()
    if not search_query:
        raise HTTPException(status_code=400, detail="Search query cannot be empty")
    
    results = current_analyzer.search_protocol(search_query)
    return {"status": "success", "query": search_query, "results": results}


@app.get("/api/section")
def get_section(section_name: str) -> Dict:
    """
    Extract a specific section from the protocol.
    
    Args:
        section_name (str): Name of the section to extract (e.g., "Methods").
    
    Returns:
        Dict: The extracted section text.
    
    Raises:
        HTTPException: If no protocol is loaded or section not found.
    """
    if current_analyzer is None:
        raise HTTPException(status_code=400, detail="No protocol loaded. Please upload a protocol first.")
    
    if not section_name:
        raise HTTPException(status_code=400, detail="Section name is required")
    
    section_text = current_analyzer.get_section(section_name)
    return {"status": "success", "section_name": section_name, "content": section_text}


@app.get("/")
def read_root():
    """Serve the main HTML page."""
    return FileResponse("index.html")


if __name__ == "__main__":
    import uvicorn
    print("Starting Clinical Trial Protocol Analyzer Server")
    print("Access the application at: http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)
