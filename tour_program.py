import streamlit as st
import pandas as pd
import datetime
import calendar
from fpdf import FPDF
from io import BytesIO

# ==================== User Configuration ====================
OFFICER_NAME = "Dinesh Das B"
DESIGNATION = "Assistant Electrical Inspector"
OFFICE_NAME = "Office of the Electrical Inspector"
OFFICE_ADDRESS = "Palakkad"
PEN = "833631"
DEFAULT_OWNERSHIP = "Private"  # Default ownership type: "Government-owned" or "Private"
# ===========================================================

# Function to generate PDF
def generate_pdf(dataframe):
    """Generate a PDF from the tour program DataFrame."""
    pdf = FPDF(orientation='L')  # Landscape orientation
    pdf.add_page()
    
    # Add header with officer details
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 8, OFFICE_NAME, ln=True, align="C")
    pdf.set_font("Arial", "", 10)
    pdf.cell(0, 6, OFFICE_ADDRESS, ln=True, align="C")
    pdf.ln(2)
    
    # Officer details - Name and Designation (left) and PEN (right)
    pdf.set_font("Arial", "", 9)
    pdf.cell(140, 5, f"Name: {OFFICER_NAME}", ln=False, align="L")
    pdf.cell(0, 5, f"PEN: {PEN}", ln=True, align="R")
    pdf.cell(140, 5, f"Designation: {DESIGNATION}", ln=True, align="L")
    
    # Draw horizontal line
    pdf.line(10, pdf.get_y() + 2, pdf.w - 10, pdf.get_y() + 2)
    pdf.ln(5)
    
    # Title
    pdf.set_font("Arial", "B", 11)
    pdf.cell(0, 6, "Monthly Tour Program", ln=True, align="C")
    pdf.ln(3)
    
    # Calculate effective page width
    epw = pdf.w - 2 * pdf.l_margin
    
    # Define column ratios (must sum to 1.0 or 100%)
    col_ratios = {
        "Date": 0.07,
        "Time": 0.05,
        "Day": 0.06,
        "Category": 0.11,
        "Ownership": 0.10,
        "Address": 0.29,
        "Section": 0.12,
        "Remarks": 0.20
    }
    
    # Calculate actual column widths based on ratios
    col_widths = {key: epw * ratio for key, ratio in col_ratios.items()}
    
    # Add table header (single line, smaller font to fit long text)
    pdf.set_font("Arial", "B", 8)
    row_height = 8
    header_specs = [
        ("Date", "Date"),
        ("Time", "Time"),
        ("Day", "Day"),
        ("Category", "Category"),
        ("Ownership", "Ownership"),
        ("Address", "Name & Address of the Installation"),
        ("Section", "Section"),
        ("Remarks", "Remarks"),
    ]
    for key, label in header_specs:
        pdf.cell(col_widths[key], row_height, label, border=1, align="C")
    pdf.ln(row_height)
    
    # Add table rows
    pdf.set_font("Arial", "", 10)
    for idx, row in dataframe.iterrows():
        # Date
        pdf.cell(col_widths["Date"], row_height, str(row["Date"]), border=1, align="C")
        # Time
        time_value = row.get("Time", "")
        time_str = ""
        if pd.notna(time_value) and time_value != "":
            # Format time if it's a time object
            if isinstance(time_value, datetime.time):
                time_str = time_value.strftime("%H:%M")
            else:
                # Try to convert string to time format, fallback to empty if fails
                try:
                    time_str = str(time_value)[:5]  # Extract HH:MM from time string
                except:
                    time_str = ""
        pdf.cell(col_widths["Time"], row_height, time_str, border=1, align="C")
        # Day
        pdf.cell(col_widths["Day"], row_height, str(row["Day"]), border=1, align="C")
        # Category
        pdf.cell(col_widths["Category"], row_height, str(row["Category"])[:20], border=1, align="C")
        # Ownership
        ownership_text = str(row.get("Ownership", "Private"))[:15]
        pdf.cell(col_widths["Ownership"], row_height, ownership_text, border=1, align="C")
        
        # Address - with text wrapping using multi_cell
        x = pdf.get_x()
        y = pdf.get_y()
        address_text = str(row["Address"])[:150]  # Increased limit for wider column
        pdf.multi_cell(col_widths["Address"], row_height, address_text, border=1, align="L")
        
        # Adjust position after multi_cell
        pdf.set_xy(x + col_widths["Address"], y)
        
        # Electrical Section
        pdf.cell(col_widths["Section"], row_height, str(row["Electrical Section"])[:20], border=1, align="C")
        # Remarks
        remarks_text = str(row["Remarks"])[:40]  # Increased for wider column
        pdf.cell(col_widths["Remarks"], row_height, remarks_text, border=1, align="C")
        pdf.ln(row_height)
    
    # Add footer with signature space
    pdf.ln(10)
    pdf.set_font("Arial", "", 10)
    pdf.cell(0, 8, "Signature: ___________________", ln=True)
    pdf.cell(0, 8, "Name/Designation: ___________________", ln=True)
    
    # Return PDF as bytes
    return pdf.output(dest='S').encode('latin-1')

# Set page config
st.set_page_config(
    page_title="Inspector Tour Program",
    layout="wide"
)

# Initialize session state for the DataFrame
if 'tour_data' not in st.session_state:
    st.session_state.tour_data = pd.DataFrame(
        columns=["Date", "Time", "Day", "Place of Inspection", "Address", "Category", "Ownership", "Electrical Section", "Remarks"]
    )

# Display title header
st.title("📋 Monthly Tour Program for Electrical Inspectors")

# Display letterhead
st.markdown(f"""
<div style='text-align: center; padding: 20px; background-color: #f0f2f6; border-radius: 10px; margin-bottom: 20px;'>
    <h2 style='margin: 0; color: #1f77b4;'>{OFFICE_NAME}</h2>
    <p style='margin: 5px 0; font-size: 16px;'>{OFFICE_ADDRESS}</p>
    <hr style='margin: 10px auto; width: 50%; border: 1px solid #1f77b4;'>
    <div style='display: flex; justify-content: space-between; max-width: 600px; margin: 10px auto;'>
        <div style='text-align: left;'>
            <strong>Name:</strong> {OFFICER_NAME}<br>
            <strong>Designation:</strong> {DESIGNATION}
        </div>
        <div style='text-align: right;'>
            <strong>PEN:</strong> {PEN}
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Sidebar - Add Tour Entry Form
with st.sidebar:
    st.header("Add Tour Entry")
    
    with st.form("tour_entry_form"):
        # Date Input
        entry_date = st.date_input(
            "Date",
            value=datetime.date.today()
        )
        
        # Time Input
        entry_time = st.time_input(
            "Time of Inspection",
            value=datetime.time(9, 0)  # Default to 9:00 AM
        )
        
        # Category Selectbox
        category = st.selectbox(
            "Category",
            options=['HT Installation', 'EHT Installation', 'Non HT installations', 'MV Installations', 'Lift Inspection', 'AC Check at AC Cinema halls', 'Quality control inspections', 'X-Ray/Neon', 'Office Work', 'Leave']
        )
        
        # Ownership Selectbox (REQUIRED)
        ownership = st.selectbox(
            "Ownership *",
            options=['Government-owned', 'Private'],
            index=0 if DEFAULT_OWNERSHIP == 'Government-owned' else 1,
            help="Select the ownership type of the installation (required)"
        )
        
        # Name & Address of the Installation
        address = st.text_area("Name & Address of the Installation")
        
        # Place of Inspection
        place_of_inspection = st.text_input("Place of Inspection")
        
        # Name of Electrical Section
        electrical_section = st.text_input("Name of Electrical Section")
        
        # Remarks
        remarks = st.text_area("Remarks")
        
        # Submit Button
        submit_button = st.form_submit_button("Submit")
        
        if submit_button:
            # Validation checks
            validation_passed = True
            
            # Validate ownership field is selected
            if not ownership:
                st.error("❌ Ownership is required!")
                validation_passed = False
            
            # Check if date already exists in DataFrame
            if len(st.session_state.tour_data) > 0:
                date_exists = entry_date in st.session_state.tour_data["Date"].values
                if date_exists:
                    st.warning("⚠️ Date already booked!")
                    validation_passed = False
            
            # Check if selected date is a Sunday
            if entry_date.weekday() == 6:  # Sunday is 6
                st.warning("⚠️ Warning: Selected date is a Sunday.")
                validation_passed = False
            
            # Check if date is the Second Saturday of the month
            first_day = entry_date.replace(day=1)
            first_saturday = first_day + datetime.timedelta(days=(5 - first_day.weekday()) % 7)
            second_saturday = first_saturday + datetime.timedelta(days=7)
            
            if entry_date == second_saturday:
                st.warning("⚠️ Warning: Second Saturday.")
                validation_passed = False
            
            # Proceed with entry only if validation passed
            if validation_passed:
                # Calculate the day from the date
                day_name = calendar.day_name[entry_date.weekday()]
                
                # Create new entry as a dictionary
                new_entry = {
                    "Date": entry_date,
                    "Time": entry_time,
                    "Day": day_name,
                    "Place of Inspection": place_of_inspection,
                    "Address": address,
                    "Category": category,
                    "Ownership": ownership,
                    "Electrical Section": electrical_section,
                    "Remarks": remarks
                }
                
                # Append to session state DataFrame
                st.session_state.tour_data = pd.concat(
                    [st.session_state.tour_data, pd.DataFrame([new_entry])],
                    ignore_index=True
                )
                
                # Display success message
                st.success("✅ Tour entry added successfully!")

# Main Page - Display Tour Program Data
st.markdown("---")

# Sort the DataFrame by Date
sorted_data = st.session_state.tour_data.sort_values(by="Date", ascending=True) if len(st.session_state.tour_data) > 0 else st.session_state.tour_data

# Create two columns
col1, col2 = st.columns([3, 1])

with col1:
    st.subheader("Tour Program Schedule")
    
    # Data Editor
    edited_data = st.data_editor(
        sorted_data,
        key="tour_data_editor",
        use_container_width=True,
        num_rows="dynamic"
    )
    
    # Update session state with edited data
    st.session_state.tour_data = edited_data

with col2:
    st.subheader("Summary Statistics")
    
    # Calculate metrics
    total_inspections = len(edited_data)
    unique_places = edited_data["Place of Inspection"].nunique() if len(edited_data) > 0 else 0
    
    # Display metrics
    st.metric("Total Inspections", total_inspections)
    st.metric("Unique Places Visited", unique_places)

# Download PDF Button
st.markdown("---")
if len(edited_data) > 0:
    pdf_bytes = generate_pdf(edited_data)
    st.download_button(
        label="📥 Download Tour Program PDF",
        data=pdf_bytes,
        file_name="tour_program.pdf",
        mime="application/pdf"
    )
else:
    st.info("Add entries to generate PDF")
