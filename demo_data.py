"""
Demo data module for testing and fallback scenarios
"""

def get_demo_parcel_data(apn: str) -> dict:
    """
    Returns demo parcel data for testing purposes
    """
    return {
        "owner_details": {
            "owner_name": "DEMO PROPERTY LLC",
            "mailing_address": "1234 DEMO STREET, PHOENIX, AZ 85001",
            "owner_type": "LLC",
            "tax_exempt": False
        },
        "valuation": {
            "total_value": 2500000,
            "land_value": 800000,
            "improvement_value": 1700000,
            "sales": [
                {
                    "sale_date": "2023-06-15",
                    "sale_price": 2400000,
                    "deed_type": "WARRANTY DEED",
                    "buyer": "DEMO PROPERTY LLC",
                    "seller": "PREVIOUS OWNER INC"
                }
            ],
            "tax_year": 2024,
            "assessment_ratio": 0.18
        },
        "legal": {
            "legal_description": "LOT 1, BLOCK 2, DEMO SUBDIVISION, MARICOPA COUNTY, ARIZONA",
            "parcel_size": "2.5 acres",
            "zoning": "C-2 (Commercial)",
            "land_use": "Commercial Retail",
            "subdivision": "DEMO SUBDIVISION",
            "section": "15",
            "township": "2N",
            "range": "3E"
        },
        "raw_data": {
            "owner_response": '{"owner_name": "DEMO PROPERTY LLC", "mailing_address": "1234 DEMO STREET, PHOENIX, AZ 85001"}',
            "valuation_response": '{"total_value": 2500000, "land_value": 800000, "improvement_value": 1700000}',
            "legal_response": '{"legal_description": "LOT 1, BLOCK 2, DEMO SUBDIVISION", "parcel_size": "2.5 acres"}'
        }
    }

def get_demo_research_memo() -> str:
    """
    Returns a demo research memo for testing purposes
    """
    return """
# Commercial Property Research Memo

## Executive Summary
This memo provides a comprehensive analysis of the subject property located at APN: 123-45-678 in Maricopa County, Arizona. The property is currently owned by DEMO PROPERTY LLC and has a total assessed value of $2,500,000.

## Ownership Analysis
- **Current Owner**: DEMO PROPERTY LLC
- **Mailing Address**: 1234 DEMO STREET, PHOENIX, AZ 85001
- **Owner Type**: Limited Liability Company
- **Tax Exempt Status**: No

The property was acquired on June 15, 2023, for $2,400,000 through a warranty deed transaction. The previous owner was PREVIOUS OWNER INC.

## Property Details
- **APN**: 123-45-678
- **Legal Description**: LOT 1, BLOCK 2, DEMO SUBDIVISION, MARICOPA COUNTY, ARIZONA
- **Parcel Size**: 2.5 acres
- **Zoning**: C-2 (Commercial)
- **Land Use**: Commercial Retail
- **Subdivision**: DEMO SUBDIVISION

## Valuation Analysis
- **Total Assessed Value**: $2,500,000
- **Land Value**: $800,000 (32% of total)
- **Improvement Value**: $1,700,000 (68% of total)
- **Assessment Ratio**: 18%
- **Tax Year**: 2024

The property shows a 4.2% increase in value from the 2023 sale price of $2,400,000 to the current assessed value of $2,500,000, indicating positive market appreciation.

## Legal Considerations
- **Zoning Compliance**: The C-2 zoning classification allows for commercial retail use, which aligns with the current land use designation.
- **Subdivision Status**: The property is part of a recorded subdivision, providing clear legal boundaries.
- **Title History**: Recent warranty deed transfer indicates clear title with no apparent encumbrances.

## Recommendations
1. **Due Diligence**: Conduct a thorough title search to verify all liens and encumbrances.
2. **Zoning Verification**: Confirm current zoning regulations and any pending changes.
3. **Environmental Assessment**: Consider Phase I environmental assessment for commercial properties.
4. **Market Analysis**: Evaluate comparable sales in the area for investment potential.
5. **Tax Planning**: Review property tax implications and potential exemptions.

## Risk Factors
- **Market Volatility**: Commercial real estate values can fluctuate based on economic conditions.
- **Zoning Changes**: Future zoning modifications could affect property value and use.
- **Environmental Liabilities**: Commercial properties may have environmental considerations.

---
*This memo is based on data from the Maricopa County Assessor's Office and is intended for informational purposes only. Professional legal and financial advice should be obtained before making investment decisions.*
"""

# Sample APNs for testing
SAMPLE_APNS = [
    "123-45-678",
    "456-78-901", 
    "789-01-234",
    "321-54-876",
    "654-87-210"
] 