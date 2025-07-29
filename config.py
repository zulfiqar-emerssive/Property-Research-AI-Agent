"""
Configuration settings for the Commercial Property Research Agent
"""

# Application Settings
APP_TITLE = "Commercial Property Ownership Research Agent"
APP_ICON = "🏢"
PAGE_LAYOUT = "wide"

# API Settings
MARICOPA_API_BASE_URL = "https://mcassessor.maricopa.gov/api/v1"
OPENAI_MODEL = "gpt-4o"
OPENAI_MAX_TOKENS = 1500
OPENAI_TEMPERATURE = 0.3

# Demo Settings
DEFAULT_DEMO_MODE = True
DEFAULT_DEMO_APN = "123-45-678"

# UI Settings
SIDEBAR_TITLE = "🔍 Research Parameters"
RESEARCH_BUTTON_TEXT = "🔍 Research Property"
SUCCESS_MESSAGE = "✅ Research completed successfully!"

# Tab Labels
TAB_MEMO = "📄 Research Memo"
TAB_DATA = "📊 Property Data"
TAB_RAW = "📦 Raw API Data"

# Download Settings
PDF_FILENAME_PREFIX = "property_research_"
CSV_FILENAME_PREFIX = "property_data_"

# Sample APNs for demo
SAMPLE_APNS = [
    "123-45-678",
    "456-78-901", 
    "789-01-234",
    "321-54-876",
    "654-87-210"
]

# GPT Prompt Template
GPT_PROMPT_TEMPLATE = """
You are a commercial real estate analyst. Given this property data from Maricopa County, generate a concise 1-page research memo including ownership summary, deed insights, valuation context, and any legal red flags. Cite data fields explicitly.

Property Data:
- APN: {apn}
- Owner: {owner}
- Mailing Address: {mailing_address}
- Parcel Size: {parcel_size}
- Legal Description: {legal_description}
- Valuation: {valuation}
- Sale Date: {sale_date}
- Sale Price: {sale_price}
- Zoning: {zoning}
- Source: {source_url}

Raw API Data for additional context:
{raw_data}

Please format your response as a professional research memo with clear sections for:
1. Executive Summary
2. Ownership Analysis
3. Property Details
4. Valuation Analysis
5. Legal Considerations
6. Recommendations

Use markdown formatting for better readability.
"""

# PDF Styling
PDF_STYLE = """
body { font-family: Arial, sans-serif; margin: 40px; }
h1 { color: #2c3e50; border-bottom: 2px solid #3498db; }
h2 { color: #34495e; margin-top: 30px; }
.property-info { background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin: 20px 0; }
.property-info h3 { margin-top: 0; color: #2c3e50; }
""" 