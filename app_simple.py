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
from demo_data import get_demo_parcel_data, SAMPLE_APNS
from rentcast_api import fetch_rentcast_property

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

def fetch_property_data(apn: str = None, address: str = None, use_demo: bool = False) -> dict:
    if use_demo:
        st.info("🎭 Using demo data for demonstration purposes.")
        return get_demo_parcel_data(apn or "123-45-678")
    return fetch_rentcast_property(address=address, apn=apn)

def normalize_parcel_data(raw_data: dict, apn: str = None, address: str = None) -> ParcelModel:
    owner = raw_data.get("owner_name", "Unknown")
    mailing_address = raw_data.get("mailing_address", "Unknown")
    apn_val = raw_data.get("parcel_number", apn or "Unknown")
    parcel_size = f"{raw_data.get('lot_size_sqft', 'Unknown')} sqft"
    legal_description = raw_data.get("legal_description", "Unknown")
    valuation = f"${raw_data.get('property_value', 'Unknown'):,}" if raw_data.get('property_value') else "Unknown"
    sale_date = raw_data.get("last_sale_date", None)
    sale_price = raw_data.get("last_sale_price", None)
    zoning = raw_data.get("zoning", "Unknown")
    source_url = raw_data.get("rentcast_url", "https://rentcast.io")
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
    st.set_page_config(
        page_title="Commercial Property Research Agent (Simple)",
        page_icon="🏢",
        layout="wide"
    )
    st.title("🏢 Commercial Property Ownership Research Agent (Simple Version)")
    st.markdown("---")
    with st.sidebar:
        st.header("🔍 Research Parameters")
        demo_mode = st.checkbox("🎭 Demo Mode (Use sample data)", value=False, help="Check this to use sample data instead of real API calls")
        input_method = st.radio(
            "Select input method:",
            ["Address", "APN"]
        )
        if input_method == "Address":
            address_input = st.text_input(
                "Enter Property Address:",
                placeholder="e.g., 123 Main St, Phoenix, AZ 85001"
            )
            apn_input = None
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
            address_input = None
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
        if apn_input or address_input:
            with st.spinner("🔍 Fetching property data..."):
                raw_data = fetch_property_data(apn=apn_input, address=address_input, use_demo=demo_mode)
                if not raw_data:
                    st.error("Failed to fetch data. Please check your input and try again.")
                    return
                is_real_data = not demo_mode
                if is_real_data:
                    st.success("🎉 Using REAL data from RentCast API!")
                else:
                    st.info("🎭 Using DEMO data for demonstration purposes.")
                parcel_data = normalize_parcel_data(raw_data, apn_input, address_input)
                st.success("✅ Research completed successfully!")
                if is_real_data:
                    st.info("📊 Data Source: RentCast API (Real Data)")
                else:
                    st.info("📊 Data Source: Demo Data (Sample Information)")
                tab1, tab2, tab3 = st.tabs(["📊 Property Data", "📦 Raw API Data"])
                with tab1:
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
                        st.metric("Sale Price", f"${parcel_data.sale_price:,}" if parcel_data.sale_price else "No recent sale")
                        st.metric("Source", "RentCast API")
                    st.markdown("### Mailing Address")
                    st.info(parcel_data.mailing_address)
                    st.markdown("### Legal Description")
                    st.text_area("Legal Description", parcel_data.legal_description, height=100, disabled=True)
                with tab2:
                    st.markdown("## Raw API Data")
                    st.json(raw_data)
    else:
        st.markdown("""
        ## Welcome to the Commercial Property Research Agent (Simple Version)
        
        This is a simplified version that works without OpenAI API requirements.
        
        ### How to use:
        1. **Choose your mode** in the sidebar:
           - 🌐 **Real API Mode** (default): Uses actual RentCast property data
           - 🎭 **Demo Mode**: Uses sample data for testing and demonstration
        2. **Enter a property address** or **APN** (Assessor's Parcel Number)
        3. Click **"🔍 Research Property"** to begin analysis
        4. Review the property data
        5. Download results as PDF or CSV
        
        ### Features:
        - 🔍 **Property Data Retrieval** from RentCast API
        - 📊 **Structured Data Views** for detailed analysis
        - 📥 **Export Options** (PDF & CSV)
        - 🎭 **Demo Mode** for testing without API dependencies
        
        ### Real Address Examples (Arizona):
        - `26823 N 31st Dr, Phoenix, AZ 85083` (Try this first!)
        - `301 W Jefferson St, Phoenix, AZ 85003`
        - `41028 N Congressional Dr, Phoenix, AZ 85086`
        
        ---
        *💡 **Tip**: This version works without OpenAI API keys. For AI-powered analysis, use the full version with OpenAI integration.*
        """)

def create_pdf_download(parcel_data: ParcelModel) -> bytes:
    html_content = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; }}
            h1 {{ color: #2c3e50; border-bottom: 2px solid #3498db; }}
            h2 {{ color: #34495e; margin-top: 30px; }}
            .property-info {{ background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin: 20px 0; }}
            .property-info h3 {{ margin-top: 0; color: #2c3e50; }}
        </style>
    </head>
    <body>
        <h1>Commercial Property Research Memo</h1>
        <div class="property-info">
            <h3>Property Information</h3>
            <p><strong>APN:</strong> {parcel_data.apn}</p>
            <p><strong>Owner:</strong> {parcel_data.owner}</p>
            <p><strong>Valuation:</strong> {parcel_data.valuation}</p>
            <p><strong>Generated:</strong> {datetime.now().strftime('%B %d, %Y')}</p>
        </div>
        <h2>Property Data</h2>
        <ul>
            <li><b>Mailing Address:</b> {parcel_data.mailing_address}</li>
            <li><b>Parcel Size:</b> {parcel_data.parcel_size}</li>
            <li><b>Legal Description:</b> {parcel_data.legal_description}</li>
            <li><b>Sale Date:</b> {parcel_data.sale_date or 'No recent sale'}</li>
            <li><b>Sale Price:</b> {parcel_data.sale_price or 'No recent sale'}</li>
            <li><b>Zoning:</b> {parcel_data.zoning}</li>
            <li><b>Source:</b> {parcel_data.source_url}</li>
        </ul>
    </body>
    </html>
    """
    pdf_buffer = BytesIO()
    pisa.CreatePDF(html_content, pdf_buffer)
    return pdf_buffer.getvalue()

def create_csv_download(parcel_data: ParcelModel) -> str:
    df = pd.DataFrame([{
        'APN': parcel_data.apn,
        'Owner': parcel_data.owner,
        'Mailing_Address': parcel_data.mailing_address,
        'Parcel_Size': parcel_data.parcel_size,
        'Legal_Description': parcel_data.legal_description,
        'Valuation': parcel_data.valuation,
        'Sale_Date': parcel_data.sale_date,
        'Sale_Price': parcel_data.sale_price,
        'Zoning': parcel_data.zoning,
        'Source_URL': parcel_data.source_url
    }])
    csv_buffer = BytesIO()
    df.to_csv(csv_buffer, index=False)
    return csv_buffer.getvalue()

if __name__ == "__main__":
    main()