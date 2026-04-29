"""
Clinical Trial Protocol Analyzer Agent

This module provides functionality to analyze clinical trial protocols for
discrepancies, missing sections, and common issues. It supports PDF documents
and provides both programmatic and interactive interfaces for protocol analysis.
"""

import pdfplumber
import os
from typing import List, Dict


class ProtocolAnalyzer:
    """
    A class to analyze clinical trial protocols for quality assurance.
    
    This analyzer reads clinical trial protocols in PDF format and checks for
    common issues such as missing sections, undefined endpoints, and 
    inconsistent enrollment criteria. It provides methods to search for 
    specific information and extract sections from the protocol.
    """
    
    def __init__(self):
        """Initialize the ProtocolAnalyzer with empty protocol text."""
        self.protocol_text = ""
        self.protocol_metadata = {}
        
    def load_protocol(self, pdf_path: str) -> str:
        """
        Load and extract text from a clinical trial protocol PDF file.
        
        This method opens a PDF file at the specified path and extracts all
        text content from each page. The extracted text is stored internally
        for use by other methods.
        
        Args:
            pdf_path (str): The file path to the clinical trial protocol PDF.
        
        Returns:
            str: The complete extracted text from the protocol.
        
        Raises:
            FileNotFoundError: If the PDF file does not exist at the given path.
            Exception: If there is an error reading or extracting text from the PDF.
        """
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"Protocol file not found: {pdf_path}")
        
        try:
            with pdfplumber.open(pdf_path) as pdf:
                self.protocol_text = ""
                for page in pdf.pages:
                    self.protocol_text += page.extract_text() + "\n"
            
            page_count = len(pdf.pages)
            print(f"Protocol loaded successfully ({page_count} pages)")
            return self.protocol_text
        except Exception as e:
            raise Exception(f"Error reading PDF: {str(e)}")
    
    def check_discrepancies(self) -> List[Dict]:
        """
        Check the protocol for common discrepancies and missing sections.
        
        This method performs a series of quality checks on the loaded protocol
        to identify common issues. It looks for key sections and required
        information that should be present in a well-structured clinical trial
        protocol according to GCP (Good Clinical Practice) guidelines.
        
        Returns:
            List[Dict]: A list of dictionaries containing discovered issues.
                       Each dictionary has keys: 'severity', 'issue', 
                       'description', and 'recommendation'.
        """
        issues = []
        text = self.protocol_text.lower()
        
        # Check 1: Enrollment criteria consistency
        # Verifies that both inclusion and exclusion criteria are present
        if "inclusion criteria" in text:
            if "exclusion criteria" not in text:
                issues.append({
                    "severity": "high",
                    "issue": "Missing Exclusion Criteria",
                    "description": "Exclusion criteria section not found. All protocols should specify exclusion criteria.",
                    "recommendation": "Add a clear exclusion criteria section"
                })
        
        # Check 2: Primary and secondary endpoints definition
        # Ensures that endpoints are clearly specified
        if "primary endpoint" not in text and "primary outcome" not in text:
            issues.append({
                "severity": "high",
                "issue": "Missing Primary Endpoint",
                "description": "Primary endpoint is not clearly defined",
                "recommendation": "Clearly define the primary efficacy endpoint"
            })
        
        if "secondary endpoint" not in text and "secondary outcome" not in text:
            issues.append({
                "severity": "medium",
                "issue": "Missing Secondary Endpoints",
                "description": "Secondary endpoints are not defined",
                "recommendation": "Define secondary endpoints for exploratory analysis"
            })
        
        # Check 3: Safety and adverse event reporting
        # Verifies that adverse event monitoring is documented
        if "adverse event" not in text and "safety" not in text:
            issues.append({
                "severity": "high",
                "issue": "Missing Adverse Event Definitions",
                "description": "Adverse event monitoring plan is not specified",
                "recommendation": "Include clear AE grading and reporting procedures"
            })
        
        # Check 4: Study population specifications
        # Ensures that the target sample size is specified
        if "sample size" not in text and "n=" not in text and "enrollment" not in text:
            issues.append({
                "severity": "medium",
                "issue": "Sample Size Not Specified",
                "description": "Target sample size or enrollment number is unclear",
                "recommendation": "Specify the target sample size with justification"
            })
        
        # Check 5: Statistical analysis plan details
        # Confirms that statistical methods are documented
        if "statistical analysis" not in text and "analysis plan" not in text:
            issues.append({
                "severity": "medium",
                "issue": "Statistical Analysis Plan",
                "description": "Statistical analysis approach is not detailed",
                "recommendation": "Include a comprehensive statistical analysis plan"
            })
        
        # Check 6: Study duration specification
        # Verifies that follow-up periods are documented
        if "duration" not in text and "follow-up" not in text:
            issues.append({
                "severity": "low",
                "issue": "Study Duration Not Clear",
                "description": "Duration of patient follow-up is not specified",
                "recommendation": "Clearly state the study duration and follow-up periods"
            })
        
        return issues
    
    def search_protocol(self, query: str) -> List[str]:
        """
        Search for specific information within the protocol.
        
        This method performs a case-insensitive search through the protocol text
        to find lines containing the specified query. Useful for locating specific
        information such as inclusion criteria, endpoints, or other protocol details.
        
        Args:
            query (str): The search term or phrase to find in the protocol.
        
        Returns:
            List[str]: A list of lines from the protocol that contain the query.
                      If no matches are found, returns a message indicating no results.
        """
        results = []
        query_lower = query.lower()
        lines = self.protocol_text.split('\n')
        
        # Iterate through each line and check if query matches
        for line in lines:
            if query_lower in line.lower() and len(line.strip()) > 0:
                results.append(line.strip())
        
        # Return results or a message if no matches found
        return results if results else ["No relevant information found for: " + query]
    
    def get_section(self, section_name: str) -> str:
        """
        Extract a specific section from the protocol.
        
        This method locates a section in the protocol by name and extracts
        the text from that section up to the next recognized section heading.
        Useful for isolating portions of the protocol like Methods, Results,
        or Discussion.
        
        Args:
            section_name (str): The name of the section to extract.
        
        Returns:
            str: The text content of the specified section, or a message
                 if the section is not found.
        """
        text_lower = self.protocol_text.lower()
        section_lower = section_name.lower()
        
        # Find the starting index of the requested section
        start_idx = text_lower.find(section_lower)
        if start_idx == -1:
            return f"Section '{section_name}' not found"
        
        # Define common section names to identify section boundaries
        next_sections = ["background", "methods", "results", "discussion", 
                        "references", "appendix", "conclusion", "statistical", "analysis"]
        
        # Find the next section to determine where this section ends
        end_idx = len(self.protocol_text)
        for section in next_sections:
            idx = text_lower.find(section, start_idx + 1)
            if idx != -1 and idx < end_idx:
                end_idx = idx
        
        # Extract and return the section text
        return self.protocol_text[start_idx:end_idx].strip()
    
    def generate_summary(self) -> Dict:
        """
        Generate a summary of the protocol structure.
        
        This method analyzes the loaded protocol and returns a dictionary
        containing information about which key sections and components are
        present in the protocol. This provides a quick overview of the
        protocol's completeness.
        
        Returns:
            Dict: A dictionary with boolean values indicating the presence
                 of key protocol components.
        """
        summary = {
            "has_study_design": "study design" in self.protocol_text.lower(),
            "has_inclusion_criteria": "inclusion" in self.protocol_text.lower(),
            "has_exclusion_criteria": "exclusion" in self.protocol_text.lower(),
            "has_primary_endpoint": "primary" in self.protocol_text.lower(),
            "has_safety_plan": "adverse" in self.protocol_text.lower() or "safety" in self.protocol_text.lower(),
        }
        return summary


def main():
    """
    Main function to run the protocol analyzer.
    
    This function demonstrates the protocol analyzer functionality. It loads
    a protocol PDF, generates a summary, checks for discrepancies, and enters
    an interactive mode where users can ask questions about the protocol.
    """
    print("=" * 60)
    print("Clinical Trial Protocol Analyzer Agent")
    print("=" * 60)
    
    analyzer = ProtocolAnalyzer()
    
    # Define the protocol file to analyze
    pdf_file = "protocol.pdf"
    
    try:
        if os.path.exists(pdf_file):
            # Load the protocol from PDF
            analyzer.load_protocol(pdf_file)
            
            # Generate and display protocol summary
            print("\nProtocol Summary:")
            summary = analyzer.generate_summary()
            for key, value in summary.items():
                print(f"  {key}: {value}")
            
            # Perform quality checks and display issues
            print("\nQuality Check - Potential Issues:")
            issues = analyzer.check_discrepancies()
            if issues:
                for i, issue in enumerate(issues, 1):
                    print(f"\n  {i}. [{issue['severity'].upper()}] {issue['issue']}")
                    print(f"     Issue: {issue['description']}")
                    print(f"     Recommendation: {issue['recommendation']}")
            else:
                print("  No major issues detected")
            
            # Enter interactive question-answering mode
            print("\n" + "=" * 60)
            print("Ask questions about the protocol (type 'quit' to exit)")
            print("=" * 60)
            
            while True:
                user_query = input("\nYour question: ").strip()
                if user_query.lower() in ['quit', 'exit', 'q']:
                    break
                
                # Search for relevant information in the protocol
                results = analyzer.search_protocol(user_query)
                print("\nRelevant Information:")
                for result in results[:3]:
                    print(f"  {result}")
        
        else:
            # Handle case where protocol file is not found
            print(f"\nFile '{pdf_file}' not found")
            print(f"Please place your clinical trial protocol PDF in the same directory")
            print(f"and name it '{pdf_file}'")
            print("\nExample usage:")
            print("  1. Place your protocol.pdf in this directory")
            print("  2. Run this script")
            print("  3. The agent will analyze the protocol and answer your questions")
    
    except Exception as e:
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    main()
