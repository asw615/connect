<?php
require 'vendor/autoload.php';

use League\Csv\Reader;
use League\Csv\Writer;

if (isset($_POST['submit'])) {
    // Get the form data
    $name = $_POST['name'];
    $class = $_POST['class'];
    $work_well = $_POST['work_well'];
    $not_work_well = $_POST['not_work_well'];

    // Read the CSV file
    $csv_file = "data/survey.csv";
    $csv = Reader::createFromPath($csv_file, 'r');
    $csv->setHeaderOffset(0);

    // Get the records
    $records = $csv->getRecords();

    // Create a new array with the existing records
    $new_data = [];
    foreach ($records as $record) {
        $new_data[] = $record;
    }

    // Add the new row
    $new_data[] = [
        'name' => $name,
        'class' => $class,
        'work_well' => $work_well,
        'not_work_well' => $not_work_well,
    ];

    // Write the new data to the CSV file
    $writer = Writer::createFromPath($csv_file, 'w');
    $writer->insertOne(['name', 'class', 'work_well', 'not_work_well']);
    $writer->insertAll($new_data);
}
?>

<!DOCTYPE html>
<html>
<head>
    <!-- style css -->
    <link rel="stylesheet" type="text/css" href="css/style.css">
    <title>Survey Form</title>
</head>
<head>
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
      width: 100%;
      padding: 10px;
      margin-bottom: 20px;
      font-size: 16px;
      border: 1px solid #ccc;
      border-radius: 5px;
    }

    input[type="submit"] {
      background-color: #0445af;
      color: #fff;
      padding: 10px 20px;
      font-size: 18px;
      font-weight: bold;
      border: none;
      border-radius: 5px;
      cursor: pointer;
    }

    input[type="submit"]:hover {
      background-color: #03308a;
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
