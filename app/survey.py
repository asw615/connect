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
    
    h2 {
      text-align: center;
      margin: 30px 0;
      font-size: 16px;
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

    select {
      width: 100%;
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
    <h2>When asked to name persons, use first names, separated by a comma e.g. Søren, Laura, Liv, Freya</h2>
    <form method="POST" action="">
        <label for="name">Name:</label>
        <input type="text" id="name" name="name" required>
        <label for="class">Class:</label>
        <input type="text" id="class" name="class" required>
        <label for="gender">Gender:</label>
        <select id="gender" name="gender" required>
            <option value="Male">Male</option>
            <option value="Female">Female</option>
            <option value="Other">Other</option>
        </select>
        <label for="social_well_being">How well do you feel socially (from 1-5 where 1 is not so good 5 is great)</label>
        <select id="social_well_being" name="social_well_being" required>
            <option value="1">1</option>
            <option value="2">2</option>
            <option value="3">3</option>
            <option value="4">4</option>
            <option value="5">5</option>
        <label for="work_well">Who do you work well with in group projects? </label>
        <input type="text" id="work_well" name="work_well" required>
        <label for="not_work_well">Are there any classmates you struggle to work with in group projects?</label>
        <input type="text" id="not_work_well" name="not_work_well" required>
        <label for="work_more_with">Is there anyone in class, you would like to work more with on a group project? </label>
        <input type="text" id="work_more_with" name="work_more_with" required>
        <label for="enjoy_talking_to">Who do you most enjoy talking with in class? </label>
        <input type="text" id="enjoy_talking_to" name="enjoy_talking_to" required>
        <label for="difficult_talking_to">Is there anyone in class you find it difficult to talk with? </label>
        <input type="text" id="difficult_talking_to" name="difficult_talking_to" required>
        <label for="get_to_know_better">Is there anyone in class you would like to get to know better? </label>
        <input type="text" id="get_to_know_better" name="get_to_know_better" required>
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
        gender = request.form["gender"]
        social_well_being = request.form["social_well_being"]
        work_well = request.form["work_well"]
        not_work_well = request.form["not_work_well"]
        work_more_with = request.form["work_more_with"]
        enjoy_talking_to = request.form["enjoy_talking_to"]
        difficult_talking_to = request.form["difficult_talking_to"]
        get_to_know_better = request.form["get_to_know_better"]

        # Read the CSV file
        with open(csv_file, mode="r", newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            records = [record for record in reader]

        # Add the new row
        records.append({
            "name": name,
            "class": class_,
            "gender": gender,
            "social_well_being": social_well_being,
            "work_well": work_well,
            "not_work_well": not_work_well,
            "work_more_with": work_more_with,
            "enjoy_talking_to": enjoy_talking_to,
            "difficult_talking_to": difficult_talking_to,
            "get_to_know_better": get_to_know_better,
        })

        # Write the new data to the CSV file
        with open(csv_file, mode="w", newline="") as csvfile:
            fieldnames = ["name", "class", "gender", "social_well_being", "work_well", "not_work_well", "work_more_with", "enjoy_talking_to", "difficult_talking_to", "get_to_know_better"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(records)

        return render_template_string(template, survey_endpoint=request.url_root + "survey")

    else:
        return render_template_string(template, survey_endpoint=request.url_root + "survey")