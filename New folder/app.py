from flask import Flask, render_template, request, redirect, url_for, flash, send_file
import pandas as pd
import os
from datetime import datetime
from io import BytesIO

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Load predefined items
def load_predefined_items():
    if os.path.exists("items.xlsx"):
        try:
            df = pd.read_excel("items.xlsx", engine="openpyxl")
            return df["Item"].tolist()
        except Exception as e:
            print(f"Error reading Excel file: {e}")
            return []
    else:
        default_items = pd.DataFrame({"Item": ["Tomato", "Onion", "Potato", "Carrot", "Cucumber"]})
        default_items.to_excel("items.xlsx", index=False, engine="openpyxl")
        return default_items["Item"].tolist()

# Home route
@app.route("/", methods=["GET", "POST"])
def index():
    predefined_items = load_predefined_items()
    if request.method == "POST":
        item = request.form.get("item")
        quantity = request.form.get("quantity")
        amount = request.form.get("amount")
        date = request.form.get("date")

        # Validate inputs
        if not item or not quantity or not amount or not date:
            flash("All fields are required!", "error")
            return redirect(url_for("index"))

        if item not in predefined_items:
            flash("Item not found in the predefined list!", "error")
            return redirect(url_for("index"))

        try:
            quantity = int(quantity)
            amount = float(amount)
        except ValueError:
            flash("Quantity must be a number and Amount must be a decimal!", "error")
            return redirect(url_for("index"))

        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            flash("Date must be in YYYY-MM-DD format!", "error")
            return redirect(url_for("index"))

        # Save to Excel
        if os.path.exists("inventory.xlsx"):
            df = pd.read_excel("inventory.xlsx", engine="openpyxl")
        else:
            df = pd.DataFrame(columns=["Item", "Quantity", "Amount", "Date"])

        new_entry = pd.DataFrame({"Item": [item], "Quantity": [quantity], "Amount": [amount], "Date": [date]})
        df = pd.concat([df, new_entry], ignore_index=True)
        df.to_excel("inventory.xlsx", index=False, engine="openpyxl")

        flash("Entry added successfully!", "success")
        return redirect(url_for("index"))

    # Fetch today's entries
    today = datetime.today().strftime("%Y-%m-%d")
    today_entries = []
    if os.path.exists("inventory.xlsx"):
        df = pd.read_excel("inventory.xlsx", engine="openpyxl")
        df["Date"] = pd.to_datetime(df["Date"]).dt.strftime("%Y-%m-%d")
        today_entries = df[df["Date"] == today].to_dict("records")

    return render_template("index.html", predefined_items=predefined_items, today_entries=today_entries)

# Export data by date range
@app.route("/export", methods=["GET", "POST"])
def export_data():
    if request.method == "POST":
        start_date = request.form.get("start_date")
        end_date = request.form.get("end_date")

        # Validate inputs
        if not start_date or not end_date:
            flash("Both start and end dates are required!", "error")
            return redirect(url_for("export_data"))

        try:
            start_date = datetime.strptime(start_date, "%Y-%m-%d")
            end_date = datetime.strptime(end_date, "%Y-%m-%d")
        except ValueError:
            flash("Dates must be in YYYY-MM-DD format!", "error")
            return redirect(url_for("export_data"))

        # Load inventory data
        if not os.path.exists("inventory.xlsx"):
            flash("No data available to export!", "error")
            return redirect(url_for("export_data"))

        df = pd.read_excel("inventory.xlsx", engine="openpyxl")
        df["Date"] = pd.to_datetime(df["Date"])

        # Filter data by date range
        filtered_data = df[(df["Date"] >= start_date) & (df["Date"] <= end_date)]

        if filtered_data.empty:
            flash("No data found for the selected date range!", "error")
            return redirect(url_for("export_data"))

        # Export to Excel
        output = BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            filtered_data.to_excel(writer, index=False)
        output.seek(0)

        return send_file(
            output,
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            as_attachment=True,
            download_name=f"inventory_{start_date.date()}_to_{end_date.date()}.xlsx"
        )

    return render_template("export.html")

# Run the app
if __name__ == "__main__":
    app.run(debug=True)