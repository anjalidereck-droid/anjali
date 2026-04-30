# CRA App - Clinical Research Assistant

A user-friendly web application for analyzing clinical trial protocols using AI. Upload your protocol, get intelligent analysis, identify issues, and find specific information instantly.

---

## Project Overview

CRA App is an intelligent assistant designed to help clinical researchers, CRAs (Clinical Research Associates), and protocol reviewers analyze clinical trial protocols efficiently. The application uses AI-powered analysis to identify common discrepancies, missing sections, and quality issues in protocols.

---

## Features

Upload Protocol
- Drag and drop PDF file upload
- Automatic text extraction from PDFs
- Fast processing

Protocol Analysis
- Quality checks and issue detection
- Identify missing sections and endpoints
- Severity-based reporting (High, Medium, Low)

Interactive Search
- Search for specific information in protocols
- Find inclusion criteria, endpoints, adverse events
- Extract specific sections

Summary View
- Protocol completeness overview
- Check presence of key components
- Visual status indicators

User-Friendly Interface
- Tabbed interface for easy navigation
- Responsive design works on desktop and mobile
- No login or authentication required
- Local privacy - data stays on your machine

---

## Technology Stack

Backend
- FastAPI - Modern Python web framework
- Uvicorn - ASGI server
- pdfplumber - PDF text extraction
- Python 3.8+

Frontend
- HTML5 - Structure
- CSS3 - Styling
- JavaScript - Interactivity
- No external UI frameworks required

---

## Installation

Prerequisites
- Python 3.8 or higher
- Windows, Mac, or Linux
- 100MB free disk space

Step 1: Clone Repository
```bash
git clone https://github.com/anjalidereck-droid/anjali.git
cd anjali
```

Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

This installs:
- fastapi
- uvicorn
- pdfplumber
- python-multipart

---

## Running the Application

Start the server:

```bash
python app.py
```

You should see:

```text
Starting CRA App - Clinical Research Assistant
Access the application at: http://127.0.0.1:8001/
```

Open your web browser and go to:

```markdown
[http://127.0.0.1:8001/](http://127.0.0.1:8001/)
```

---

## How to Use

1. Upload Protocol
   - Click the upload area or drag and drop your PDF
   - Select a clinical trial protocol in PDF format

2. View Analysis
   - Protocol Summary tab shows which sections are present
   - Issues tab displays detected quality problems
   - Search tab allows searching for specific information

3. Get Recommendations
   - Each issue includes a recommended fix
   - Severity levels indicate priority

4. Search Protocol
   - Type keywords in the search box
   - Results show relevant text from the protocol

---

## Quality Checks Performed

The application checks for:

High Priority
- Missing or unclear primary endpoints
- Absent adverse event definitions
- Missing enrollment criteria

Medium Priority
- Undefined secondary endpoints
- Missing sample size specifications
- Incomplete statistical analysis plans

Low Priority
- Unclear study duration
- Missing follow-up period details

---

## File Structure

```
c:\Users\anjal\Desktop\git_stuff\
    app.py                      (FastAPI backend server)
    clinical_protocol_agent.py  (Analysis engine)
    index.html                  (Web interface)
    style.css                   (Styling)
    script.js                   (Frontend interactions)
    requirements.txt            (Python dependencies)
    SETUP.md                    (Setup instructions)
    PROTOCOL_AGENT_README.md    (Detailed documentation)
```

---

## API Endpoints

POST /api/upload
- Upload and analyze a protocol PDF
- Returns: Summary, Issues, Page count

GET /api/summary
- Get protocol summary

GET /api/issues
- Get detected issues

POST /api/search
- Search protocol content
- Parameters: query (search term)

GET /api/section
- Extract specific section
- Parameters: section_name

---

## Troubleshooting

Port Already in Use
- Error: Address already in use
- Solution: Close other applications or change port in app.py

Module Not Found
- Error: ModuleNotFoundError
- Solution: Run pip install -r requirements.txt

File Upload Issues
- Only PDF files are supported
- Ensure file is valid and not corrupted

No Results on Search
- Try different keywords
- Search is case-insensitive

---

## System Requirements

Minimum
- 2GB RAM
- 100MB free disk space
- Windows 10, Mac OS 10.14+, or Linux

Recommended
- 4GB RAM
- 500MB free disk space
- Modern web browser (Chrome, Firefox, Edge)

---

## Performance

Typical Analysis Times
- Protocol upload and parsing: 2-5 seconds
- Quality checks: 1-2 seconds
- Search: Less than 1 second
- Total first analysis: 3-7 seconds

File Size Support
- Tested up to 200MB PDF files
- Recommended: Under 50MB for best performance

---

## Future Enhancements

Planned Features
- User accounts and protocol history
- Export analysis reports as PDF
- Integration with ClinicalTrials.gov
- Support for additional document formats
- Advanced LLM integration for deeper analysis
- Multi-language support
- Team collaboration features

---

## Security and Privacy

Data Privacy
- All processing done locally
- No data sent to external servers
- Protocols only stored in memory during analysis
- No data persistence between sessions

Safe to Use
- Open source code
- No user tracking
- No ads or third-party services

---

## Contributing

Found an issue? Have suggestions?
- Report bugs
- Suggest improvements
- Submit pull requests

Contact: anjalidereck@gmail.com

---

## License

Open source - Free to use and modify

---

## About the Developer

Created by: Anjali Dereck
MSc Drug Discovery with Artificial Intelligence
University of Liverpool

CRA App demonstrates expertise in:
- Clinical research knowledge
- Python programming
- Web application development
- AI and healthcare technology
- User interface design

---

## Quick Start Guide

Complete setup instructions available in [SETUP.md](SETUP.md)

For detailed API documentation, see [WEB_APP_GUIDE.md](WEB_APP_GUIDE.md)

For analysis engine details, see [PROTOCOL_AGENT_README.md](PROTOCOL_AGENT_README.md)

---

**Start analyzing protocols today with CRA App!**

Visit: http://localhost:8000

Built with passion for better clinical research.
