# Clinical Trial Protocol Analyzer Agent

## Overview
An AI-powered agent that analyzes clinical trial protocols to identify issues, discrepancies, and protocol details through question answering. This project demonstrates clinical research knowledge and AI implementation.

## Features
- PDF protocol upload and text extraction.
- Quality checks for common protocol discrepancies.
- Interactive question answering based on the uploaded protocol.
- Issue detection for missing endpoints, safety plans, and eligibility criteria.
- Section extraction from specific parts of the protocol.
- Automatic protocol summary generation.

## Detected Issues
The agent checks for:
- Missing or unclear inclusion criteria.
- Missing or unclear exclusion criteria.
- Undefined primary and secondary endpoints.
- Absent adverse event definitions.
- Missing sample size specifications.
- Incomplete statistical analysis plans.
- Unclear study duration.

## Installation

### 1. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 2. Prepare Your Protocol
- Place your clinical trial protocol PDF in the project directory.
- Name it `protocol.pdf`, or update the filename in the script.

### 3. Run the Agent
```bash
python clinical_protocol_agent.py
```

## Usage Example
```python
from clinical_protocol_agent import ProtocolAnalyzer

analyzer = ProtocolAnalyzer()

analyzer.load_protocol("my_protocol.pdf")

issues = analyzer.check_discrepancies()
for issue in issues:
    print(f"[{issue['severity']}] {issue['issue']}")

results = analyzer.search_protocol("inclusion criteria")

summary = analyzer.generate_summary()
```

## API Functions

### `load_protocol(pdf_path: str) -> str`
Loads and extracts text from a clinical trial protocol PDF.

### `check_discrepancies() -> List[Dict]`
Analyzes the protocol for common issues and returns a list of discrepancies.

### `search_protocol(query: str) -> List[str]`
Searches for specific information within the protocol.

### `get_section(section_name: str) -> str`
Extracts a specific section, such as `Methods` or `Inclusion Criteria`.

### `generate_summary() -> Dict`
Returns a summary of the protocol structure and key components.

## Technical Stack
- Python 3.8+
- `pdfplumber` for PDF text extraction
- `langchain` for agent framework and LLM integration
- Regular expressions for protocol pattern matching

## Future Enhancements
- Integrate free LLMs such as Ollama or Hugging Face.
- Extract structured data such as enrollment numbers and study duration.
- Generate compliance reports.
- Support multiple document formats.
- Add machine learning models for endpoint prediction.
- Integrate with the ClinicalTrials.gov API.

## Skills Demonstrated
- Clinical research protocol analysis.
- Python programming.
- PDF processing and text analysis.
- AI and ML agent development.
- Data extraction and quality assurance.
- Healthcare data handling.

## License
Open source project for educational and research use.

---

Built by Anjali  
MSc Drug Discovery with AI  
University of Liverpool