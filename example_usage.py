"""
Example usage of the Clinical Trial Protocol Analyzer Agent

This script demonstrates how to use the ProtocolAnalyzer class to analyze
clinical trial protocols. It shows various features including loading protocols,
checking for discrepancies, searching for information, and generating summaries.
"""

from clinical_protocol_agent import ProtocolAnalyzer


def example_usage():
    """
    Demonstrate the functionality of the protocol analyzer.
    
    This function shows how to:
    1. Initialize the analyzer
    2. Load a protocol (or use sample text for demonstration)
    3. Generate a summary
    4. Check for quality issues
    5. Search for specific information
    """
    
    print("=" * 70)
    print("EXAMPLE: Clinical Trial Protocol Analyzer Agent")
    print("=" * 70)
    
    # Step 1: Initialize the analyzer
    analyzer = ProtocolAnalyzer()
    
    # Step 2: Load a protocol
    print("\nStep 1: Loading protocol...")
    try:
        # Replace with your actual PDF path
        analyzer.load_protocol("your_protocol.pdf")
    except FileNotFoundError:
        print("   No protocol.pdf found. Using sample protocol for demonstration...")
        
        # For demonstration, use a sample protocol text
        analyzer.protocol_text = """
        Clinical Trial Protocol: A Phase III Study of Treatment X
        
        1. BACKGROUND
        This is a study of a new treatment for disease Y.
        
        2. INCLUSION CRITERIA
        Patients must meet all of the following criteria:
        - Age between 18 and 75 years
        - Confirmed diagnosis of disease Y
        - Willing to participate in the study
        
        3. STUDY METHODS
        The primary endpoint will be measured at week 12.
        Secondary endpoints include safety and tolerability measures.
        
        4. ADVERSE EVENTS
        All adverse events will be recorded and classified 
        according to severity and relationship to treatment.
        
        5. STATISTICAL ANALYSIS
        Statistical analysis will be performed using standard methods.
        """
        print("   Sample protocol loaded for demonstration")
    
    # Step 3: Generate protocol summary
    print("\nStep 2: Protocol Summary")
    print("-" * 70)
    summary = analyzer.generate_summary()
    for key, value in summary.items():
        status = "PRESENT" if value else "MISSING"
        print(f"   {key}: {status}")
    
    # Step 4: Check for quality issues
    print("\nStep 3: Quality Check - Identified Issues")
    print("-" * 70)
    issues = analyzer.check_discrepancies()
    
    if issues:
        for i, issue in enumerate(issues, 1):
            print(f"\n   Issue {i}: {issue['issue']}")
            print(f"   Severity: {issue['severity'].upper()}")
            print(f"   Description: {issue['description']}")
            print(f"   Recommendation: {issue['recommendation']}")
    else:
        print("   No major issues detected")
    
    # Step 5: Demonstrate search functionality
    print("\nStep 4: Search Example")
    print("-" * 70)
    
    # Define sample search queries
    search_queries = [
        "inclusion criteria",
        "primary endpoint",
        "adverse events"
    ]
    
    # Perform searches and display results
    for query in search_queries:
        print(f"\n   Query: '{query}'")
        results = analyzer.search_protocol(query)
        for result in results[:2]:
            truncated = result[:80] + "..." if len(result) > 80 else result
            print(f"   Result: {truncated}")
    
    # Step 6: Display usage instructions
    print("\n" + "=" * 70)
    print("HOW TO USE WITH YOUR OWN PROTOCOL:")
    print("=" * 70)
    print("""
    1. Place your clinical trial protocol PDF in the same directory
    2. Update the filename in the script if needed (default: "protocol.pdf")
    3. Run the agent:
       
       python clinical_protocol_agent.py
    
    4. The agent will:
       - Load and analyze your protocol
       - Check for common discrepancies
       - Answer your questions about the protocol
       - Extract specific sections on demand
    
    5. Interactive mode features:
       - Type any question about the protocol
       - The agent searches for relevant information
       - Type 'quit' to exit
    """)
    
    # Step 7: Display API examples
    print("\nAPI EXAMPLES:")
    print("-" * 70)
    print("""
    from clinical_protocol_agent import ProtocolAnalyzer
    
    # Create analyzer instance
    analyzer = ProtocolAnalyzer()
    
    # Load a protocol
    analyzer.load_protocol("my_protocol.pdf")
    
    # Check for issues
    issues = analyzer.check_discrepancies()
    
    # Search for specific information
    results = analyzer.search_protocol("inclusion criteria")
    
    # Extract a section
    methods = analyzer.get_section("Methods")
    
    # Get protocol summary
    summary = analyzer.generate_summary()
    """)

if __name__ == "__main__":
    example_usage()
