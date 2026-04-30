CRA App - Quick Setup Instructions

WHAT IS CRA APP?
================
CRA App is your Clinical Research Assistant. Upload clinical trial protocols
and get instant AI-powered analysis.


INSTALLATION (First Time Only)
==============================

Step 1: Open PowerShell
    Click Start Menu and search for "PowerShell"
    Right-click and choose "Run as Administrator"

Step 2: Navigate to Project Folder
    Type this in PowerShell:
    cd c:\Users\anjal\Desktop\git_stuff

Step 3: Install All Dependencies
    Type this in PowerShell:
    pip install -r requirements.txt

    Wait for it to finish (this takes 2-3 minutes)
    You will see: "Successfully installed..."


RUNNING THE APP (Every Time)
=============================

Step 1: Open PowerShell
    Click Start Menu and search for "PowerShell"

Step 2: Navigate to Project Folder
    Type this in PowerShell:
    cd c:\Users\anjal\Desktop\git_stuff

Step 3: Start the App
    Type this in PowerShell:
    python app.py

    You should see:
    Starting CRA App - Clinical Research Assistant
    Access the application at: http://localhost:8000

Step 4: Open in Browser
    Open Google Chrome, Firefox, or Edge
    Go to: http://localhost:8000
    
    The CRA App will load in your browser


USING CRA APP
=============

1. Click the upload area or drag your protocol PDF
2. Wait for analysis (shows loading spinner)
3. View results in different tabs:
   - Summary: Which protocol sections are present
   - Issues: Quality problems and recommendations
   - Search: Find specific information


STOPPING THE APP
================

In PowerShell, press: Ctrl+C

This stops the app. To run it again, repeat the "RUNNING THE APP" section.


COMMON ISSUES
=============

Issue: "Command not found: pip"
    Solution: Python is not installed properly
    Try: python -m pip install -r requirements.txt

Issue: "Port 8000 already in use"
    Solution: Another app is using that port
    Try: python app.py (restart your computer)

Issue: "Module not found"
    Solution: Dependencies not installed
    Run: pip install -r requirements.txt

Issue: "Cannot connect to http://localhost:8000"
    Solution: Check if app.py is running in PowerShell
    Should see: "Uvicorn running on http://0.0.0.0:8000"


FILE STRUCTURE
==============
c:\Users\anjal\Desktop\git_stuff\
    app.py                      (Main app - run this)
    requirements.txt            (List of dependencies)
    index.html                  (Website interface)
    style.css                   (Styling)
    script.js                   (Interactive features)
    clinical_protocol_agent.py  (Analysis engine)


SUMMARY
=======

Installation (1 time):
    pip install -r requirements.txt

Running (every time):
    python app.py
    Then open: http://localhost:8000


That's it! Enjoy using CRA App!

Created by: Anjali
CRA App - Clinical Research Assistant
