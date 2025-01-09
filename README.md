# Restaurant Inventory Management System

A Flask-based web application for managing restaurant inventory. It allows users to add entries, view today's entries, and export data by date range.

---

## Features

1. **Add Entry**:
   - Add new inventory entries with details like item name, quantity, amount, and date.
   - Autocomplete for item names from a predefined list.

2. **Today's Entries**:
   - Display all entries added today in a table on the right side of the page.

3. **Export Data**:
   - Export inventory data for a specific date range as an Excel file.
   - Includes a **Back Button** to return to the main page.

4. **Responsive Design**:
   - The application is designed to work seamlessly on both desktop and mobile devices.

---

## Prerequisites

Before running the application, ensure you have the following installed:

- Python 3.x
- Flask
- Pandas
- Openpyxl

---

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/restaurant-inventory.git
   cd restaurant-inventory

   pip install flask pandas openpyxl
   python app.py


   restaurant_inventory/
│
├── app.py                # Flask application
├── templates/
│   ├── index.html        # Main page template
│   └── export.html       # Export page template
├── static/
│   └── styles.css        # CSS styles
└── items.xlsx            # Predefined items list
