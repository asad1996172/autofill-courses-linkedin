# Autofill Courses LinkedIn

Auto Fill Courses Section in your LinkedIn Profile from your transcripts.

## Table of Contents
1. [Installation](#installation)
2. [How to Run](#how-to-run)

## Installation

- Clone the repository: `git clone <repository-link>`
- Install dependencies via requirements: `pip install -r requirements.txt` or setup env with conda: `conda env create -f environment.yml`

## How to Run

Step 1: 
 
 Create courses.json with the following format:

 ```json
 {
    "<institure_name>": {
        "course_code": "course_title",
        ...
    },
    ...
}
 ```

 The institute name should be the same as you have in your LinkedIn profile

 To automate the creation of `courses.json`, I took picture of my transcripts and used `ChatOCR` plugin for ChatGPT to parse the text and extract the courses_code to course_title mapping.

Step 2:

Run the script:

 `python main.py --file-path courses.json --delete-existing`
