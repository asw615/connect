from flask import Blueprint, request, render_template_string
import csv
import os

survey_blueprint = Blueprint('survey', __name__)

template = """
<!DOCTYPE html>
<html>
<head>
        <!-- style css -->
    <link rel="stylesheet" type="text/css" href="css/style.css">
    <title>Survey Form</title>
    <style>
    body {
      font-family: Arial, sans-serif;
      margin: 0;
      padding: 0;
    }

    h1 {
      text-align: center;
      margin: 30px 0;
      font-size: 36px;
    }

    form {
      max-width: 600px;
      margin: 0 auto;
      padding: 20px;
      border: 1px solid #ccc;
      border-radius: 10px;
      background-color: #f9f9f9;
      box-shadow: 0px 0px 10px #ccc;
    }

    label {
      display: block;
      margin-bottom: 10px;
      font-weight: bold;
      font-size: 18px;
    }

    input[type="text"] {
      width: 95%;
      padding: 10px;
      margin-bottom: 20px;
      font-size: 16px;
      border: 1px solid #ccc;
      border-radius: 5px;
    }

    input[type="submit"] {
        background-color: #a258ed;
        color: #fff;
        padding: 10px 20px;
        border: none;
        border-radius: 5px;
        font-size: 16px;
        cursor: pointer;
    }

    input[type="submit"]:hover {
        background-color: #3674f2;
    }
    </style>
</head>
<body>
    <h1>Please answer the questions</h1>
    <form method="POST" action="">
        <label for="name">Name:</label>
        <input type="text" id="name" name="name" required>
        <label for="class">Class:</label>
        <input type="text" id="class" name="class" required>
        <label for="work_well">Who do you work well with? (first names, separated by a comma e.g. Søren, Laura, Liv, Freya)</label>
        <input type="text" id="work_well" name="work_well" required>
        <label for="not_work_well">Who do you not work well with? (first names, seperated by a comma e.g. Søren, Laura, Liv, Freya)</label>
        <input type="text" id="not_work_well" name="not_work_well" required>
        <input type="submit" name="submit" value="Submit">
    </form>
</body>
</html>
"""

@survey_blueprint.route("/survey", methods=["GET", "POST"])
def survey_form():
    csv_file = "app/static/data/survey.csv"

    if request.method == "POST":
        name = request.form["name"]
        class_ = request.form["class"]
        work_well = request.form["work_well"]
        not_work_well = request.form["not_work_well"]

        # Read the CSV file
        with open(csv_file, mode="r", newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            records = [record for record in reader]

        # Add the new row
        records.append({
            "name": name,
            "class": class_,
            "work_well": work_well,
            "not_work_well": not_work_well,
        })

        # Write the new data to the CSV file
        with open(csv_file, mode="w", newline="") as csvfile:
            fieldnames = ["name", "class", "work_well", "not_work_well"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(records)

        return render_template_string(template, survey_endpoint=request.url_root + "survey")

    else:
        return render_template_string(template, survey_endpoint=request.url_root + "survey")



           
