# 🏢 Commercial Property Ownership Research Agent

A Streamlit web application that demonstrates an AI-powered commercial property research tool using the RentCast API and OpenAI GPT-4o.

## 🎯 Overview

This application allows commercial real estate professionals to:
- Input property addresses or APNs (parcel numbers)
- Fetch comprehensive property data from the RentCast API
- Generate AI-powered research memos using OpenAI
- Export results as PDF and CSV files

## 🏗️ Architecture

```
User Browser
     │
     ▼
Streamlit UI
     │
     ▼
RentCast API Connector ─▶ Normalizer ─▶ OpenAI Prompt Engine
     │                                │
     ▼                                ▼
Download Buttons (PDF / CSV)       Research Memo
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- RentCast API key (required for property data)
- OpenAI API key (optional - for AI features)
- Internet connection for API calls

### Installation

1. **Clone or download the project files**

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   - Copy `env_template.txt` to `.env`
   - Add your API keys:
     ```
     RENTCAST_API_KEY=your_rentcast_api_key_here
     OPENAI_API_KEY=your_openai_api_key_here
     ```

4. **Run the application:**
   
   **Simple Version (No OpenAI required):**
   ```bash
   streamlit run app_simple.py
   ```
   
   **Full Version (With OpenAI integration):**
   ```bash
   streamlit run app.py
   ```

5. **Open your browser** and navigate to `http://localhost:8501`

## 📋 Features

### 🔍 Property Research
- **Address Input**: Direct property address lookup
- **APN Input**: Assessor's Parcel Number lookup
- **Real-time API Integration**: RentCast API
- **Data Normalization**: Structured property data model

### 🤖 AI-Powered Analysis
- **OpenAI Integration**: Professional research memo generation
- **Structured Output**: Executive summary, ownership analysis, valuation insights
- **Legal Considerations**: Red flags and recommendations

### 📊 Data Visualization
- **Tabbed Interface**: Research memo, property data, and raw API responses
- **Metrics Display**: Key property information at a glance
- **Expandable Sections**: Detailed API response inspection

### 📥 Export Options
- **PDF Export**: Professional research memo with styling
- **CSV Export**: Structured property data for analysis

## 🛠️ Technical Details

### API Endpoints Used
The application uses the RentCast API:
- `GET /properties?address=...` - Lookup by address
- `GET /properties?parcel_number=...` - Lookup by APN

**Data Sources**: RentCast provides comprehensive property data including:
- Owner information and mailing addresses
- Assessment and market values
- Sale history
- Legal descriptions and zoning
- Building characteristics

### Data Model
```python
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
```

### Dependencies
- **Streamlit**: Web application framework
- **OpenAI**: GPT-4o API integration (v1.0.0+)
- **Requests**: HTTP client for API calls
- **Pandas**: Data manipulation and CSV export
- **xhtml2pdf**: PDF generation
- **python-dotenv**: Environment variable management

## 🎮 Usage Guide

### Step 1: Choose Your Mode
- **🌐 Real API Mode** (default): Uses actual RentCast property data
- **🎭 Demo Mode**: Uses sample data for testing and demonstration

### Step 2: Input Property Information
- Select input method (Address or APN)
- Enter the property identifier
- Click **"🔍 Research Property"**

### Step 3: Review Results
- **Research Memo Tab**: AI-generated analysis with citations (full version)
- **Property Data Tab**: Structured property information
- **Raw API Data Tab**: Complete API responses

### Step 4: Export Results
- Download PDF for professional reports
- Download CSV for data analysis

## 🔧 Configuration

### Environment Variables
- `RENTCAST_API_KEY`: Your RentCast API key for property data access
- `OPENAI_API_KEY`: Your OpenAI API key for GPT-4o access (optional)

### Customization Options
- Modify the GPT prompt in `generate_research_memo()` function
- Adjust PDF styling in `create_pdf_download()` function
- Customize data normalization in `normalize_parcel_data()` function

## 🚨 Important Notes

### Demo Mode Features
- **Sample Data**: Pre-populated with realistic property information
- **Quick Testing**: Instant results without API calls
- **Full Functionality**: All features work with demo data
- **No API Dependencies**: Works without external API access

### Production Considerations
- **API Rate Limits**: RentCast API has usage limits
- **Error Handling**: Add comprehensive error handling for API failures
- **Caching**: Add response caching for better performance
- **User Authentication**: Add user management and access controls
- **Data Validation**: Implement input validation and sanitization

## 🐛 Troubleshooting

### Common Issues

1. **RentCast API Error**
   - Verify your API key is correct
   - Check your RentCast account has sufficient credits
   - Ensure internet connectivity
   - Verify the property address/APN format

2. **OpenAI API Error**
   - Verify your API key is correct
   - Check your OpenAI account has sufficient credits
   - Ensure internet connectivity
   - Make sure you're using OpenAI v1.0.0+ format

3. **PDF Generation Error**
   - Install required system dependencies for xhtml2pdf
   - Check file permissions for temporary files

### Error Messages
- "Error fetching data from RentCast API" - API connectivity issue
- "Error generating memo with OpenAI" - OpenAI API issue
- "No real data found for this property" - Property not found in database

## 📞 Support

For technical support or questions:
- Check the troubleshooting section above
- Review the code comments for implementation details
- Ensure all dependencies are properly installed
- Use Demo Mode if API connectivity issues persist

## 📄 License

This is a proof-of-concept demonstration application. Please ensure compliance with:
- RentCast API terms of service
- OpenAI API usage policies
- Local data protection regulations

---

**Built with ❤️ for commercial real estate professionals** 