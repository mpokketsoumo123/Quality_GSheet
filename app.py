import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import datetime
import re

# Google Sheets Authentication
def authenticate_google_sheets():
    credentials = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=[
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]
    )
    client = gspread.authorize(credentials)
    return client

# Write data to Google Sheets
# Write data to Google Sheets
def write_to_sheet(sheet_name, data, email):
    client = authenticate_google_sheets()
    sheet = client.open(sheet_name).sheet1

    # Get the number of rows already in the sheet
    current_data = sheet.get_all_values()

    # Determine the row index to append data
    row_index = len(current_data) + 1  # Append below the last existing row

    # Convert date and time objects to string
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    data_with_meta = []
    for item in data:
        if isinstance(item, (datetime.date, datetime.datetime)):
            item = item.strftime("%Y-%m-%d")  # Convert to date string format
        elif isinstance(item, datetime.time):
            item = item.strftime("%H:%M:%S")  # Convert to time string format
        data_with_meta.append(item)

    # Add email and date columns to the data
    data_with_meta += [email, current_date]

    # Append the data to the sheet
    sheet.append_row(data_with_meta)

# Streamlit App Configuration
st.set_page_config(page_title="Multi-Page App", layout="wide")

# Session State for Login
# Session State for Login
if "login_email" not in st.session_state:
    st.session_state["login_email"] = None

# Page Navigation
pages = ["Login"]
if st.session_state["login_email"]:
    pages += ["Input Form", "How to Use"]

selected_page = st.sidebar.selectbox("Navigate", pages)

# Login Page
if selected_page == "Login":
    st.title("Login")
    email = st.text_input("Enter your email ID")

    if st.button("Login"):  # When the login button is clicked
        allowed_emails = ["mis.operations@mpokket.com"]  # Example email list
        if email in allowed_emails:
            st.session_state["login_email"] = email
            st.session_state["selected_page"] = "How to Use"  # Set selected page directly after login
            st.success("Login successful! Redirecting to 'How to Use' page...")
        else:
            st.error("Invalid email ID. Please try again.")

# How to Use Page
elif selected_page == "How to Use":
    st.title("How to Use the App")
    st.markdown(
        """
        1. Login with your email ID on the **Login** page and click on login for 2 times.
        2. Navigate to the **Input Form** page using the sidebar.
        3. Fill out the form in the two sections below.
        4. Review the table showing your input.
        5. Use the **Delete Row** button to remove any incorrect rows (plese enter Row+1 in the input place).
        6. Click **Final Submit** to upload the data to Google Sheets.
        """
    )

# Input Form Page
elif selected_page == "Input Form":
    st.title("Input Form")

    # Data storage
    if "input_table" not in st.session_state:
        st.session_state["input_table"] = []

    # Split the form into two columns using st.columns
    col1, col2 = st.columns(2)

    # Section 1 (Left Column)
    with col1:

        # Date of Birth input (DOB)
        LOB = st.selectbox("LOB:", ["SE", "SIB", "SIC", "Student"])

        # Center selection
        center = st.selectbox("Select your Center:",
                              ["Bhopal", "Indore", "Vijaywada", "MYS", "Noida", "Kolkata", "Coimbatore", "Ranchi"])

        # Partner Name (List format)
        partner_name = st.selectbox("Select Partner Name:",
                                    ["Tarus", "TTBS", "MAGNUM", "ICCS", "INHOUSE", "HRH NEXT", "AYUDA"])

        # Date of Audit (Date format)
        date_of_audit = st.date_input("Enter Date of Audit:")

        # Week (List format)
        week = st.selectbox("Select Week:", ["Week 1", "Week 2", "Week 3", "Week 4", "Week 5"])

        # Audit Category (List format)
        audit_category = st.selectbox("Select Audit Category:", ["Floor", "RCA"])

        # EMP ID (Non-numeric validation)
        emp_id = st.text_input("Enter EMP ID:")

        # Login ID (Numeric validation)
        login_id = st.text_input("Enter Login ID:")

        # Agent Name (No validation)
        agent_name = st.text_input("Enter Agent Name:")

        # Team Leader (No validation)
        team_leader = st.text_input("Enter Team Leader Name:")

        # Audit Name (No validation)
        audit_name = st.text_input("Enter Audit Name:")

        # Auditor Center (List validation)
        auditor_center = st.selectbox("Select Auditor Center:",
                                      ["Indore", "Vijaywada", "Mysore", "Bhopal", "Noida", "Kolkata", "Coimbatore",
                                       "HYD", "Ranchi"])

        # Auditor Designation (List validation)
        auditor_designation = st.selectbox("Select Auditor Designation:", ["TL", "Trainer"])

        # User Register Number (Numeric validation)
        user_register_number = st.text_input("Enter User Register Number:")

        # Calling Number (Numeric validation)
        calling_number = st.text_input("Enter Calling Number:")

        # Date of Call (Date format validation)
        date_of_call = st.date_input("Enter Date of Call:")

        # Call Time Slot (Time format validation)
        call_time_slot = st.time_input("Enter Call Time Slot:")

        # Bucket (List format)
        bucket = st.selectbox("Select Bucket:", ["Bucket 1", "Bucket 2", "Bucket 3", "Bucket 4"])

        # Energetic Opening and Closing (Yes/No validation)
        energetic_opening_closing = st.selectbox("Energetic Opening and Closing?", ["Yes", "No"])

        # Motive of the Call (Yes/No validation)
        motive_of_call = st.selectbox("Motive of the Call?", ["Yes", "No"])

        # Probe / Confirm User's Profession (Yes/No validation)
        probe_confirm_user_profession = st.selectbox("Probe / Confirm User's Profession?", ["Yes", "No", "NA"])

        # Current Profile Stage / Previous Interaction
        Current_Profile_Stage_Previous_Interaction = st.selectbox("Current Profile Stage / Previous Interaction",
                                                                  ["Yes", "No", "FATAL"])

        Probe_If_User_have_any_doc_releated_Profession_Study_Business = st.selectbox(
            "Current Profile Stage / Previous Interaction", ["Yes", "No", "NA"])

        Guide_User_with_required_documents_One_by_one = st.selectbox("Current Profile Stage / Previous Interaction",
                                                                     ["Yes", "Fatal", "NA"])

        Urgency = st.selectbox("Urgency", ["Yes", "Fatal", "NA"])

        Objection_Handling = st.selectbox("Objection Handling", ["Yes", "Fatal", "NA"])



    # Section 2 (Right Column)
    with col2:
        Explained_user_how_to_take_first_loan = st.selectbox("Explained user how to take first loan",
                                                             ["Yes", "Fatal", "NA"])

        Reconfirmation_Call_back_script = st.selectbox("Reconfirmation / Call back script", ["Yes", "Fatal", "NA"])
        Energetic_Tone_and_Clear_articulation=st.selectbox("Energetic Tone and Clear articulation", ["Yes","No"])

        Two_way_communication = st.selectbox("Two way communication", ["Yes", "NO"])

        Active_listening_and_Dead_Air = st.selectbox("Active listening and Dead Air", ["Yes", "NO"])

        Professional_Communication = st.selectbox("Professional Communication", ["Yes", "NO"])

        Information = st.selectbox("Information", ["Yes", "NO"])

        Follow_Up = st.selectbox("Follow Up", ["Yes", "NO"])

        Tagging = st.selectbox("Tagging", ["Yes", "NA", "NO"])
        Benefits= st.selectbox("Tagging", ["Informed","Not Informed"])

        Fatal = st.selectbox("Fatal", ["Yes", "NO"])

        Remarks = st.text_input("Remarks:")

        Agent_Feedback_Status = st.selectbox("Agent Feedback Status", ["Closed", "Open"])

        Profile_completion_status_prior_to_call = st.selectbox("Profile completion status prior to call",
                                                               ["Blank profile", "Partially complete",
                                                                "Almost complete"])

        PIP_SFA_Status = st.selectbox("PIP/SFA Status", ["Correct", "Incorrect", "NA"])

        VOC = st.text_input("VOC")

        AOI = st.text_input("AOI")

        call_duration = st.text_input("Enter Call Duration (HH:mm:ss):")

        KYC_type = st.selectbox("KYC Type", ["Not Updated", "OKYC", "VKYC", "CKYC"])

        Disposition_Accuracy = st.selectbox("Disposition Accuracy", ["Correct", "Incorrect", "Not Done"])

        DCS_Tagging_L1 = st.text_input("Enter DCS Tagging L1")

        DCS_Tagging_L2 = st.text_input("Enter DCS Tagging L2")

        DCS_Tagging_L3 = st.text_input("Enter DCS Tagging L3")

        Actual_Tagging_L1 = st.text_input("Actual Tagging L1")

        Actual_Tagging_L2 = st.text_input("Actual Tagging L2")

        Actual_Tagging_L3 = st.text_input("Actual Tagging L3")

    # Add Row Button
    if st.button("Add Row"):
        data = {
            "LOB": LOB,
            "Center": center,
            "Partner Name": partner_name,
            "Date of Audit": date_of_audit,
            "Week": week,
            "Audit Category": audit_category,
            "EMP ID": emp_id,
            "Login ID": login_id,
            "Agent Name": agent_name,
            "Team Leader": team_leader,
            "Audit Name": audit_name,
            "Auditor Center": auditor_center,
            "Auditor Designation": auditor_designation,
            "User Register Number": user_register_number,
            "Calling Number": calling_number,
            "Date of Call": date_of_call,
            "Call Time Slot": call_time_slot,
            "Bucket": bucket,
            "Energetic Opening and Closing": energetic_opening_closing,
            "Motive of the Call": motive_of_call,
            "Probe / Confirm User's Profession": probe_confirm_user_profession,
            "Current Profile Stage / Previous Interaction": Current_Profile_Stage_Previous_Interaction,
            "Probe If User has Doc Related to Profession/Study/Business": Probe_If_User_have_any_doc_releated_Profession_Study_Business,
            "Guide User with Required Documents": Guide_User_with_required_documents_One_by_one,
            "Urgency": Urgency,
            "Objection Handling": Objection_Handling,
            "Explained User How to Take First Loan": Explained_user_how_to_take_first_loan,
            "Reconfirmation Call Back Script": Reconfirmation_Call_back_script,
            "Energetic Tone and Clear articulation":Energetic_Tone_and_Clear_articulation,
            "Two-way Communication": Two_way_communication,
            "Active Listening and Dead Air": Active_listening_and_Dead_Air,
            "Professional Communication": Professional_Communication,
            "Information": Information,
            "Follow Up": Follow_Up,
            "Tagging": Tagging,
            "Benefits":Benefits,
            "Fatal": Fatal,
            "Remarks": Remarks,
            "Agent Feedback Status": Agent_Feedback_Status,
            "Profile Completion Status Prior to Call": Profile_completion_status_prior_to_call,
            "PIP/SFA Status": PIP_SFA_Status,
            "VOC": VOC,
            "AOI": AOI,
            "Call Duration": call_duration,
            "KYC Type": KYC_type,
            "Disposition Accuracy": Disposition_Accuracy,
            "DCS Tagging L1": DCS_Tagging_L1,
            "DCS Tagging L2": DCS_Tagging_L2,
            "DCS Tagging L3": DCS_Tagging_L3,
            "Actual Tagging L1": Actual_Tagging_L1,
            "Actual Tagging L2": Actual_Tagging_L2,
            "Actual Tagging L3": Actual_Tagging_L3
        }
        st.session_state["input_table"].append(data)

    # Display Table
    if st.session_state["input_table"]:
        st.write("Your Input Table:")
        df = pd.DataFrame(st.session_state["input_table"])
        st.dataframe(df)

        # Delete Row
        row_to_delete = st.number_input(
            "Enter Row Number to Delete (1-based index):",
            min_value=1,
            max_value=len(df),
            step=1
        )
        if st.button("Delete Row"):
            # Adjust for 1-based index
            st.session_state["input_table"].pop(row_to_delete - 1)

    # Final Submit Button
    if st.session_state["input_table"] and st.button("Final Submit"):
        try:
            for row in st.session_state["input_table"]:
                write_to_sheet(
                    "Quality_Requirment",
                    list(row.values()),
                    st.session_state["login_email"]
                )
            st.success("Data successfully written to Google Sheets!")
            st.session_state["input_table"] = []  # Clear after submission
        except Exception as e:
            st.error(f"An error occurred: {e}")
