import argparse
import json
import logging
import os
import time
from typing import Dict

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from color_logger import setup_logger

options = webdriver.EdgeOptions()
options.use_chromium = True
driver = webdriver.Edge(options=options)

logging.getLogger("selenium").setLevel(logging.ERROR)
log = setup_logger()


def add_course(course_name: str, course_code: str, associated_with: str) -> None:
    """
    Add a course to LinkedIn profile.

    Args:
        course_name (str): The name of the course.
        course_code (str): The code of the course.
        associated_with (str): The associated institution or program for the course.
    """

    driver.get(
        (
            "https://www.linkedin.com/in/asad1996172/details/courses"
            "/edit/forms/new/?profileFormEntryPoint=PROFILE_SECTION"
        )
    )
    time.sleep(5)

    label = driver.find_element(By.XPATH, "//label[text()='Course name']")
    input_id = label.get_attribute("for")
    input_element = driver.find_element(By.ID, input_id)
    input_element.send_keys(course_name)

    label = driver.find_element(By.XPATH, "//label[text()='Number']")
    input_id = label.get_attribute("for")
    input_element = driver.find_element(By.ID, input_id)
    input_element.send_keys(course_code)

    label = driver.find_element(By.XPATH, "//label[text()='Associated with']")
    select_id = label.get_attribute("for")
    select_element = driver.find_element(By.ID, select_id)
    select = Select(select_element)
    select.select_by_value(associated_with)

    save_button = driver.find_element(By.XPATH, "//button[span[text()='Save']]")
    save_button.click()


def delete_courses() -> None:
    """
    Deletes all courses from the LinkedIn profile.
    """

    time.sleep(5)

    ul_element = driver.find_element(By.CLASS_NAME, "pvs-list ")
    all_div_elements = ul_element.find_elements(
        By.CLASS_NAME, "pvs-entity__action-container"
    )
    a_hrefs = [
        a.get_attribute("href")
        for div in all_div_elements
        for a in div.find_elements(By.TAG_NAME, "a")
        if a.get_attribute("href")
    ]

    for index, a_href in enumerate(a_hrefs, start=1):
        print(f"Deleting course {index}/{len(a_hrefs)} ...")
        driver.get(a_href)
        time.sleep(5)

        delete_course_button = driver.find_element(
            By.XPATH, "//button[span[text()='Delete course']]"
        )
        delete_course_button.click()
        time.sleep(5)
        delete_button = driver.find_element(By.XPATH, "//button[span[text()='Delete']]")
        delete_button.click()


def read_courses_json(file_path: str) -> Dict:
    """
    Reads the courses from the provided JSON file.

    Args:
        file_path (str): Path to the JSON file.

    Returns:
        dict: Dictionary containing the courses if the file exists.
    """

    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            courses = json.load(file)
        return courses
    else:
        log.info(f"File {file_path} does not exist!")
        return {}


def setup_linkedin() -> None:
    """
    Navigate to LinkedIn, prompt the user to log in and go to courses section.
    """
    driver.get("https://www.linkedin.com/")
    input("\nLog in to your LinkedIn and press enter to continue...")
    driver.get("https://www.linkedin.com/in/asad1996172/details/courses/")
    time.sleep(5)


def main(args: argparse.Namespace) -> None:
    """
    Main function to handle LinkedIn course operations.

    Args:
        args (argparse.Namespace): Command-line arguments.
    """

    all_courses = read_courses_json(args.file_path)
    log.info("Courses read from JSON file:")
    log.info(json.dumps(all_courses, indent=4))

    setup_linkedin()

    if args.delete_existing:
        log.info("Deleting existing courses from LinkedIn")
        delete_courses()

    for associated_with, courses in all_courses.items():
        for course_code, course_name in courses.items():
            log.info(f"Adding course: {course_name} ({course_code})")
            add_course(course_name, course_code, associated_with)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Read courses from a JSON file.")
    parser.add_argument("--file-path", type=str, help="Path to the courses.json file.")
    parser.add_argument(
        "--delete-existing",
        action="store_true",
        help="Flag to delete existing courses from LinkedIn.",
    )

    args = parser.parse_args()
    main(args)
