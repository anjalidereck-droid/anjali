# Quick Start Guide 

## Clinical Trial Protocol Analyzer Agent

### Installation (5 minutes)

#### 1. Clone or Download the Project
```bash
git clone https://github.com/anjalidereck-droid/clinical-ai-agent
cd clinical-ai-agent
```

#### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 3. Prepare Your Protocol
- Place your clinical trial protocol PDF in the same directory
- Rename it to `protocol.pdf` (or update the filename in `clinical_protocol_agent.py`)

### Running the Agent

#### Option A: Interactive Mode
```bash
python clinical_protocol_agent.py
```

This will:
1. Load your protocol
2. Display a quality check report
3. Allow you to ask questions about the protocol

#### Option B: Example Usage
```bash
python example_usage.py
```

See how the agent works with a sample protocol

#### Option C: Use as a Library
```python
from clinical_protocol_agent import ProtocolAnalyzer

analyzer = ProtocolAnalyzer()
analyzer.load_protocol("my_protocol.pdf")

# Check for issues
issues = analyzer.check_discrepancies()

# Search for information
results = analyzer.search_protocol("primary endpoint")

# Get summary
summary = analyzer.generate_summary()
```

### What the Agent Can Do

 **Analyze Protocol Structure**
- Checks for presence of key sections
- Identifies missing components

 **Quality Assurance**
- Detects common discrepancies
- Flags potential issues
- Provides recommendations

 **Information Retrieval**
- Search for specific information
- Extract particular sections
- Answer questions about the protocol

 **Protocol Summary**
- Quick overview of protocol components
- Verification of completeness

### Example Output

```
 Protocol loaded successfully (45 pages)
 Protocol Summary:
  • total_pages_approx: 45
  • has_study_design: True
  • has_inclusion_criteria: True
  • has_exclusion_criteria: False  ← Issue!
  • has_primary_endpoint: True
  • has_safety_plan: True

 Quality Check - Potential Issues:
  
  1. [HIGH] Missing Exclusion Criteria
     Issue: Exclusion criteria section not found
     Recommendation: Add a clear exclusion criteria section
  
  2. [MEDIUM] Missing Secondary Endpoints
     Issue: Secondary endpoints are not defined
     Recommendation: Define secondary endpoints
```

### Troubleshooting

**Q: "ModuleNotFoundError: No module named 'pdfplumber'"**
```bash
pip install pdfplumber
```

**Q: "FileNotFoundError: Protocol file not found"**
- Ensure your PDF is in the same directory as the script
- Check the filename matches exactly (case-sensitive on Linux/Mac)

**Q: PDF has special formatting and text extraction is poor**
- Some PDFs have embedded formatting issues
- Try converting to a standard PDF or text format first

### Next Steps

 **Extend the Agent:**
- Add support for PDF annotations
- Integrate with clinical trial databases
- Add compliance checking for regulatory standards
- Connect to LLMs for advanced analysis

 **Use Cases:**
- Protocol review and QA
- Regulatory compliance checking
- Training materials for CRAs
- Protocol comparison and analysis

### Need Help?

- Check [PROTOCOL_AGENT_README.md](PROTOCOL_AGENT_README.md) for detailed documentation
- Review [clinical_protocol_agent.py](clinical_protocol_agent.py) for code
- Run [example_usage.py](example_usage.py) to see it in action

---

**Built by:** Anjali | MSc Drug Discovery with AI | University of Liverpool

*Demonstrating: Clinical Research Expertise + AI/Python Implementation + Healthcare Data Processing*
