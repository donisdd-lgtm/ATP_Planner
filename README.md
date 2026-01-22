# ATP_Planner
App to Plan my monthly ATP

## Overview
This is a Streamlit-based application designed to help Electrical Inspectors plan and manage their monthly tour programs. The application allows you to:
- Schedule inspection visits
- Track installation ownership types
- Generate PDF reports of tour programs
- Prevent scheduling conflicts (duplicate dates, Sundays, second Saturdays)

## Features

### Installation Ownership Classification
Each tour entry includes an **Ownership** field that classifies the installation as either:
- **Government-owned** - For government facilities and installations
- **Private** - For private sector installations

#### Configuration
The default ownership type can be set in the configuration section at the top of `tour_program.py`:

```python
DEFAULT_OWNERSHIP = "Private"  # Options: "Government-owned" or "Private"
```

When creating a new tour entry, the ownership dropdown will be pre-populated with this default value, but you can change it as needed.

#### Required Field
The ownership field is **required** for all tour entries. The form will not submit without selecting an ownership type.

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
streamlit run tour_program.py
```

## Configuration
You can customize the application by editing the configuration section at the top of `tour_program.py`:

- `OFFICER_NAME` - Name of the officer
- `DESIGNATION` - Officer's designation
- `OFFICE_NAME` - Name of the office
- `OFFICE_ADDRESS` - Office address
- `PEN` - Personal Employee Number
- `DEFAULT_OWNERSHIP` - Default ownership type for new entries

## Usage

1. **Add Tour Entries**: Use the sidebar form to add new inspection entries
2. **Edit Entries**: Use the data editor in the main view to modify existing entries
3. **Generate PDF**: Click the download button to generate a formatted PDF report

## Validation Rules

- No duplicate dates allowed
- Warns against scheduling on Sundays
- Warns against scheduling on Second Saturdays
- Ownership field is mandatory for all entries

