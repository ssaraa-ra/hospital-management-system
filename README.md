# Sistmemi i Menaxhimit të Poliklinikës S.R 
## (Hospital Management System)

This is a simple management system for registering and managing patient, doctor, and prescription data in a polyclinic. The project allows for adding, updating, deleting, and viewing information about patients, doctors, and prescriptions. It also provides the ability to search for data using the patient or doctor's ID.

## Features

### Patient Management:
- Adding new patients.
- Updating existing patient information.
- Deleting patient data.
- Searching for patients by ID.

### Doctor Management:
- Adding new doctors.
- Updating existing doctor information.
- Deleting doctor data.
- Searching for doctors by ID.

### Prescription Management:
- Adding prescriptions for patients.
- Updating existing prescriptions.
- Deleting prescriptions.
- Searching for prescriptions by ID.

## Requirements

### 1. Clone the Repository
Clone this repository to your local machine by running the following command in your terminal:

```bash
git clone https://github.com/sararamadaniii/hospital-management-system.git


```
### 2. Install the Required Dependencies
Navigate to the project directory in your terminal and install the required Python dependencies by running:

```bash
pip install -r requirements.txt

```
### 3. Set Up the Configuration
In the project directory, create a file named config.py and add the following configuration settings:

```bash
# Configuration file for authentication and database settings

password = '<user_authentication_password>'  # User login password (e.g., '1234')
database_name = '<current_database_name>'  # Name of your database (e.g., 'database_1A')
edit_mode_password = '<edit_mode_password>'  # Password for edit mode (e.g., 'allow_edit')

```
Replace the placeholders (<user_authentication_password>, <current_database_name>, etc.) with your actual values.

4. Run the Application
Once you've completed the configuration, navigate to the project directory in your terminal and run the following command to launch the application:

```bash
streamlit run app.py
```
