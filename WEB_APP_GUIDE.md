Web Application Setup and Launch Guide

FEATURES
========
- Upload clinical trial protocols as PDF files
- Get intelligent protocol analysis
- Identify common discrepancies and issues
- Search for specific information
- View protocol quality summary
- User-friendly interface with no login required
- Local setup for privacy and data security


INSTALLATION
============

Step 1: Install Dependencies
    Open PowerShell in the project directory and run:
    pip install -r requirements.txt

Step 2: Files Required
    The following files should be in the same directory:
    - app.py (FastAPI backend)
    - index.html (Frontend page)
    - style.css (Styling)
    - script.js (JavaScript interactions)
    - clinical_protocol_agent.py (Analysis engine)


RUNNING THE APPLICATION
=======================

Start the Server
    Open PowerShell and navigate to the project directory:
    cd c:\Users\anjal\Desktop\git_stuff

    Start the FastAPI server:
    python app.py

    You should see:
    Starting Clinical Trial Protocol Analyzer Server
    Access the application at: http://localhost:8000

Open in Browser
    Once the server is running, open your web browser and go to:
    http://localhost:8000

Upload Protocol
    1. Click the upload area or drag and drop your protocol PDF
    2. Wait for the analysis to complete
    3. View results in different tabs

Interact with Results
    Summary Tab: See which protocol sections are present
    Issues Tab: Review quality issues and recommendations
    Search Tab: Search for specific information in the protocol


API ENDPOINTS
=============

POST /api/upload
    Upload and analyze a PDF protocol
    Parameters: file (PDF file)
    Returns: Summary, Issues, Page count

GET /api/summary
    Get protocol summary

GET /api/issues
    Get detected issues

POST /api/search
    Search for information in protocol
    Parameters: query (search term)

GET /api/section
    Extract specific section
    Parameters: section_name


STOPPING THE SERVER
===================

Press Ctrl+C in the PowerShell window where the server is running.


TROUBLESHOOTING
===============

Port Already in Use
    If port 8000 is already in use, you can change it in app.py
    Change: uvicorn.run(app, host="0.0.0.0", port=8000)
    To: uvicorn.run(app, host="0.0.0.0", port=8001)

Module Not Found Errors
    Make sure all dependencies are installed:
    pip install -r requirements.txt

File Upload Issues
    Only PDF files are supported
    Check file size and ensure it's a valid PDF

Browser Cache Issues
    Clear browser cache or use Ctrl+Shift+Delete
    Or open in an incognito/private window


FILE STRUCTURE
==============

c:\Users\anjal\Desktop\git_stuff\
    app.py                          (FastAPI backend)
    clinical_protocol_agent.py      (Analysis engine)
    index.html                      (Frontend page)
    style.css                       (Styling)
    script.js                       (Interactions)
    requirements.txt                (Dependencies)
    protocol.pdf                    (Your protocol - upload this)


ADVANCED USAGE
==============

Deploy to Cloud
    The application can be deployed to cloud services:
    - Heroku
    - AWS Lambda
    - Google Cloud
    - Azure App Service

Add Authentication
    To add user authentication, integrate:
    - Auth0
    - Firebase
    - Custom JWT implementation

Enable HTTPS
    For production deployment:
    - Get SSL certificate
    - Configure HTTPS in FastAPI
    - Update frontend API_URL


TIPS
====

1. Keep browser developer tools open (F12) to see any errors
2. Use Chrome, Firefox, or Edge for best compatibility
3. Protocols can be large; processing may take a few seconds
4. Search is case-insensitive
5. For best results, ensure PDF is properly formatted


SUPPORT
=======

For issues or questions:
1. Check the console (F12) for error messages
2. Review the API response in Network tab (F12)
3. Ensure all dependencies are installed
4. Verify files are in correct directory
5. Check that FastAPI server is running


Created by: Anjali Dereck
MSc Drug Discovery with AI, University of Liverpool
