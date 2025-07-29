import streamlit as st
import requests
import json
import pandas as pd
import os
from dataclasses import dataclass
from typing import Optional
from datetime import datetime
import base64
from dotenv import load_dotenv
import markdown
from xhtml2pdf import pisa
from io import BytesIO
from demo_data import get_demo_parcel_data, get_demo_research_memo, SAMPLE_APNS
from rentcast_api import fetch_rentcast_property

# Set page config first (must be the first Streamlit command)
st.set_page_config(
    page_title="Commercial Property Research Agent",
    page_icon="🏢",
    layout="wide"
)

# Load environment variables
load_dotenv()

@dataclass
class ParcelModel:
    owner: str
    mailing_address: str
    apn: str
    parcel_size: str
    legal_description: str
    valuation: str
    sale_date: Optional[str]
    sale_price: Optional[int]
    zoning: str
    source_url: str

# OpenAI client setup (unchanged)
client = None
try:
    from openai import OpenAI
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key and api_key != "your_openai_api_key_here":
        client = OpenAI(api_key=api_key)
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": "Test"}],
                max_tokens=5
            )
        except Exception:
            client = None
except Exception:
    client = None

def fetch_property_data(apn: str = None, address: str = None, use_demo: bool = False) -> dict:
    if use_demo:
        st.info("🎭 Using demo data for demonstration purposes.")
        return get_demo_parcel_data(apn or "123-45-678")
    return fetch_rentcast_property(address=address, apn=apn)

def safe_str(val):
    if isinstance(val, dict):
        # Prefer formattedAddress for mailing address dicts
        if 'formattedAddress' in val:
            return val['formattedAddress']
        return ", ".join(f"{k}: {safe_str(v)}" for k, v in val.items())
    if isinstance(val, list):
        return ", ".join(safe_str(v) for v in val)
    if val is None:
        return "Unknown"
    return str(val)

def normalize_parcel_data(raw_data: dict, apn: str = None, address: str = None) -> ParcelModel:
    # Owner
    owner = "Unknown"
    if "owner" in raw_data:
        o = raw_data["owner"]
        if isinstance(o, dict) and "names" in o:
            owner = ", ".join(safe_str(n) for n in o["names"])
        elif isinstance(o, str):
            owner = o
        else:
            owner = safe_str(o)

    # Mailing address
    mailing_address = "Unknown"
    if "owner" in raw_data and isinstance(raw_data["owner"], dict):
        m = raw_data["owner"].get("mailingAddress")
        if m:
            mailing_address = safe_str(m.get("formattedAddress") or m)
    if mailing_address == "Unknown":
        mailing_address = safe_str(raw_data.get("formattedAddress") or f"{raw_data.get('city', '')}, {raw_data.get('state', '')}")

    # APN
    apn_val = safe_str(raw_data.get("assessorID") or raw_data.get("parcel_number") or apn or "Unknown")

    # Parcel size
    lot_size = raw_data.get("lotSize") or raw_data.get("lot_size_sqft")
    parcel_size = f"{safe_str(lot_size)} sqft" if lot_size else "Unknown sqft"

    # Legal description
    legal_description = safe_str(raw_data.get("legalDescription") or raw_data.get("legal_description") or raw_data.get("legal_desc") or "Unknown")

    # Valuation (use latest year in taxAssessments)
    valuation = "Unknown"
    tax_assessments = raw_data.get("taxAssessments")
    if isinstance(tax_assessments, dict) and tax_assessments:
        latest_year = max(tax_assessments.keys(), key=lambda y: int(y))
        val = tax_assessments[latest_year].get("value")
        if val:
            valuation = f"${val:,.0f}"

    # Sale info
    sale_date = safe_str(raw_data.get("lastSaleDate") or raw_data.get("last_sale_date") or "Unknown")
    sale_price = "Unknown"  # Not present in sample

    # Zoning
    zoning = safe_str(raw_data.get("zoning") or raw_data.get("zoning_code") or "Unknown")

    # Source URL (Google Maps link)
    source_url = f"https://www.google.com/maps/search/?api=1&query={requests.utils.quote(raw_data.get('formattedAddress', ''))}" if raw_data.get("formattedAddress") else "https://rentcast.io"

    return ParcelModel(
        owner=owner,
        mailing_address=mailing_address,
        apn=apn_val,
        parcel_size=parcel_size,
        legal_description=legal_description,
        valuation=valuation,
        sale_date=sale_date,
        sale_price=sale_price,
        zoning=zoning,
        source_url=source_url
    )

def main():
    st.title("🏢 Commercial Property Ownership Research Agent")
    st.markdown("---")
    
    with st.sidebar:
        st.header("🔍 Research Parameters")
        demo_mode = st.checkbox("🎭 Demo Mode (Use sample data)", value=False, help="Check this to use sample data instead of real API calls")
        input_method = st.radio(
            "Select input method:",
            ["Address", "APN"]
        )
        address_input = None
        apn_input = None
        if input_method == "Address":
            address_input = st.text_input(
                "Enter Property Address:",
                placeholder="e.g., 123 Main St, Phoenix, AZ 85001"
            )
            if demo_mode:
                st.markdown("**Sample Addresses:**")
                sample_addresses = [
                    "26823 N 31st Dr, Phoenix, AZ 85083",
                    "301 W Jefferson St, Phoenix, AZ 85003",
                    "41028 N Congressional Dr, Phoenix, AZ 85086"
                ]
                for addr in sample_addresses:
                    if st.button(f"Use {addr[:30]}...", key=f"addr_{addr[:10]}"):
                        address_input = addr
                        st.rerun()
        else:
            apn_input = st.text_input(
                "Enter APN (Assessor's Parcel Number):",
                placeholder="e.g., 205-03-224"
            )
            if demo_mode:
                st.markdown("**Sample APNs:**")
                for apn in SAMPLE_APNS:
                    if st.button(f"Use {apn}", key=f"apn_{apn}"):
                        apn_input = apn
                        st.rerun()
        research_button = st.button("🔍 Research Property", type="primary")
        st.markdown("---")
        st.markdown("**API Status:**")
        if demo_mode:
            st.markdown("🎭 Demo Mode Active")
            st.markdown("📝 Using sample data")
        else:
            st.markdown("🌐 Real API Mode")
            st.markdown("✅ RentCast API")
            st.markdown("💡 Try real addresses or APNs")
    if research_button:
        if not apn_input and not address_input:
            st.error("Please enter either an address or APN.")
            return
        # Guarantee only one is set
        if input_method == "Address":
            raw_data = fetch_property_data(apn=None, address=address_input, use_demo=demo_mode)
        else:
            raw_data = fetch_property_data(apn=apn_input, address=None, use_demo=demo_mode)
        if not raw_data:
            st.error("Failed to fetch data. Please check your input and try again.")
            return
        is_real_data = not demo_mode
        if is_real_data:
            st.success("🎉 Using REAL data from RentCast API!")
        else:
            st.info("🎭 Using DEMO data for demonstration purposes.")
        parcel_data = normalize_parcel_data(raw_data, apn_input, address_input)
        with st.spinner("🤖 Generating research memo..."):
            memo_content = generate_research_memo(parcel_data, raw_data, use_demo=demo_mode)
        st.success("✅ Research completed successfully!")
        if is_real_data:
            st.info("📊 Data Source: RentCast API (Real Data)")
        else:
            st.info("📊 Data Source: Demo Data (Sample Information)")
        tab1, tab2, tab3 = st.tabs(["📄 Research Memo", "📊 Property Data", "📦 Raw API Data"])
        with tab1:
            st.markdown("## Research Memo")
            st.markdown(memo_content)
            col1, col2 = st.columns(2)
            with col1:
                pdf_data = create_pdf_download(memo_content, parcel_data)
                st.download_button(
                    label="📥 Download PDF",
                    data=pdf_data,
                    file_name=f"property_research_{parcel_data.apn.replace('-', '_')}.pdf",
                    mime="application/pdf"
                )
            with col2:
                csv_data = create_csv_download(parcel_data)
                st.download_button(
                    label="📥 Download CSV",
                    data=csv_data,
                    file_name=f"property_data_{parcel_data.apn.replace('-', '_')}.csv",
                    mime="text/csv"
                )
        with tab2:
            st.markdown("## Property Information")
            col1, col2 = st.columns(2)
            with col1:
                st.metric("APN", parcel_data.apn)
                st.metric("Owner", parcel_data.owner)
                st.metric("Valuation", parcel_data.valuation)
                st.metric("Zoning", parcel_data.zoning)
            with col2:
                st.metric("Parcel Size", parcel_data.parcel_size)
                st.metric("Sale Date", parcel_data.sale_date or "No recent sale")
                # Robust sale price formatting
                if isinstance(parcel_data.sale_price, (int, float)):
                    sale_price_display = f"${parcel_data.sale_price:,}"
                elif parcel_data.sale_price and parcel_data.sale_price not in ("Unknown", "None"):
                    sale_price_display = str(parcel_data.sale_price)
                else:
                    sale_price_display = "No recent sale"
                st.metric("Sale Price", sale_price_display)
                st.metric("Source", "RentCast API")
            st.markdown("### Mailing Address")
            st.info(parcel_data.mailing_address)
            st.markdown("### Legal Description")
            st.text_area("Legal Description", parcel_data.legal_description, height=100, disabled=True)
        with tab3:
            st.markdown("## Raw API Data")
            st.json(raw_data)
            st.markdown("---")
            st.markdown("> **Debug: Raw RentCast Property Dict**")
            st.code(json.dumps(raw_data, indent=2))
    else:
        st.markdown("""
        ## Welcome to the Commercial Property Research Agent
        
        This application helps commercial real estate professionals quickly research property ownership, 
        valuation, and legal information using the RentCast API.
        
        ### How to use:
        1. **Choose your mode** in the sidebar:
           - 🌐 **Real API Mode** (default): Uses actual RentCast property data
           - 🎭 **Demo Mode**: Uses sample data for testing
        2. **Enter a property address** or **APN** (Assessor's Parcel Number)
        3. Click **"🔍 Research Property"** to begin analysis
        4. Review the AI-generated research memo
        5. Download results as PDF or CSV
        
        ### Features:
        - 🔍 **Property Data Retrieval** from RentCast API
        - 🤖 **AI-Powered Analysis** using GPT-4o
        - 📄 **Professional Research Memos** with citations
        - 📊 **Structured Data Views** for detailed analysis
        - 📥 **Export Options** (PDF & CSV)
        
        ### Real Address Examples (Arizona):
        - `26823 N 31st Dr, Phoenix, AZ 85083` (Try this first!)
        - `301 W Jefferson St, Phoenix, AZ 85003`
        - `41028 N Congressional Dr, Phoenix, AZ 85086`
        
        ### Demo Mode Features:
        - 🎭 **Sample Data**: Pre-populated with realistic property information
        - 🔄 **Quick Testing**: Instant results without API calls
        - 📊 **Full Functionality**: All features work with demo data
        
        ---
        *💡 **Tip**: Start with Real API Mode to see actual RentCast property data. If you encounter issues, switch to Demo Mode for testing.*
        """)

def generate_research_memo(parcel_data: ParcelModel, raw_data: dict, use_demo: bool = False) -> str:
    if use_demo or client is None:
        return get_demo_research_memo()
    prompt = f"""
    You are a commercial real estate analyst. Given this property data, generate a concise 1-page research memo including ownership summary, deed insights, valuation context, and any legal red flags. Cite data fields explicitly.\n\nProperty Data:\n- APN: {parcel_data.apn}\n- Owner: {parcel_data.owner}\n- Mailing Address: {parcel_data.mailing_address}\n- Parcel Size: {parcel_data.parcel_size}\n- Legal Description: {parcel_data.legal_description}\n- Valuation: {parcel_data.valuation}\n- Sale Date: {parcel_data.sale_date or 'No recent sale data'}\n- Sale Price: {parcel_data.sale_price or 'No recent sale data'}\n- Zoning: {parcel_data.zoning}\n- Source: {parcel_data.source_url}\n\nRaw API Data for additional context:\n{json.dumps(raw_data, indent=2)}\n\nPlease format your response as a professional research memo with clear sections for:\n1. Executive Summary\n2. Ownership Analysis\n3. Property Details\n4. Valuation Analysis\n5. Legal Considerations\n6. Recommendations\n\nUse markdown formatting for better readability.\n"""
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a professional commercial real estate analyst with expertise in property research and analysis."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1500,
            temperature=0.3
        )
        return response.choices[0].message.content
    except Exception as e:
        st.warning(f"Error generating memo with OpenAI: {str(e)}")
        st.info("Using demo memo for demonstration purposes.")
        return get_demo_research_memo()

def create_pdf_download(memo_content: str, parcel_data: ParcelModel) -> bytes:
    # Robust sale price formatting for PDF
    if isinstance(parcel_data.sale_price, (int, float)):
        sale_price_display = f"${parcel_data.sale_price:,}"
    elif parcel_data.sale_price and parcel_data.sale_price not in ("Unknown", "None"):
        sale_price_display = str(parcel_data.sale_price)
    else:
        sale_price_display = "No recent sale"
    html_content = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 32px; }}
            h1 {{ color: #2c3e50; border-bottom: 2px solid #3498db; margin-bottom: 12px; }}
            h2 {{ color: #34495e; margin-top: 18px; margin-bottom: 8px; }}
            .section {{ margin-bottom: 18px; }}
            .property-table {{ border-collapse: collapse; width: 100%; margin-top: 6px; }}
            .property-table th, .property-table td {{ border: 1px solid #ddd; padding: 6px 8px; vertical-align: top; }}
            .property-table th {{ background-color: #f2f2f2; text-align: left; width: 160px; }}
            .label {{ font-weight: bold; color: #2c3e50; }}
            .property-table td a {{
                color: #1a0dab;
                word-break: break-all;
                white-space: pre-wrap;
                text-decoration: underline;
            }}
            .property-table td {{
                word-break: break-all;
                white-space: pre-wrap;
            }}
            /* Reduce spacing in markdown */
            .section p, .section ul, .section ol, .section li {{
                margin-top: 2px;
                margin-bottom: 2px;
            }}
        </style>
    </head>
    <body>
        <h1>Commercial Property Research Memo</h1>
        <div class="section">
            <h2>Property Information</h2>
            <table class="property-table">
                <tr><th class="label">APN</th><td>{parcel_data.apn}</td></tr>
                <tr><th class="label">Owner</th><td>{parcel_data.owner}</td></tr>
                <tr><th class="label">Valuation</th><td>{parcel_data.valuation}</td></tr>
                <tr><th class="label">Zoning</th><td>{parcel_data.zoning}</td></tr>
                <tr><th class="label">Parcel Size</th><td>{parcel_data.parcel_size}</td></tr>
                <tr><th class="label">Sale Date</th><td>{parcel_data.sale_date or 'No recent sale'}</td></tr>
                <tr><th class="label">Sale Price</th><td>{sale_price_display}</td></tr>
                <tr><th class="label">Mailing Address</th><td>{parcel_data.mailing_address}</td></tr>
                <tr><th class="label">Legal Description</th><td>{parcel_data.legal_description}</td></tr>
                <tr><th class="label">Source</th><td><a href='{parcel_data.source_url}'>{parcel_data.source_url}</a></td></tr>
            </table>
        </div>
        <div class="section">
            <h2>Research Memo</h2>
            <div style="margin:0; padding:0;">
                {markdown.markdown(memo_content, extensions=['extra'])}
            </div>
        </div>
    </body>
    </html>
    """
    pdf_buffer = BytesIO()
    pisa.CreatePDF(html_content, pdf_buffer)
    return pdf_buffer.getvalue()

def create_csv_download(parcel_data: ParcelModel) -> str:
    # Robust sale price formatting for CSV
    if isinstance(parcel_data.sale_price, (int, float)):
        sale_price_display = f"${parcel_data.sale_price:,}"
    elif parcel_data.sale_price and parcel_data.sale_price not in ("Unknown", "None"):
        sale_price_display = str(parcel_data.sale_price)
    else:
        sale_price_display = "No recent sale"
    df = pd.DataFrame([{
        'APN': parcel_data.apn,
        'Owner': parcel_data.owner,
        'Mailing_Address': parcel_data.mailing_address,
        'Parcel_Size': parcel_data.parcel_size,
        'Legal_Description': parcel_data.legal_description,
        'Valuation': parcel_data.valuation,
        'Sale_Date': parcel_data.sale_date,
        'Sale_Price': sale_price_display,
        'Zoning': parcel_data.zoning,
        'Source_URL': parcel_data.source_url
    }])
    csv_buffer = BytesIO()
    df.to_csv(csv_buffer, index=False)
    return csv_buffer.getvalue()

if __name__ == "__main__":
    main() 