"""Downloads slides from https://courses.engr.illinois.edu/cs225/sp2021/pages/lectures.html
and stores them in folders by week with name and date"""
import os
from requests import get
from bs4 import BeautifulSoup

URL = "https://courses.engr.illinois.edu/cs225/sp2021/pages/lectures.html"  # target URL

if __name__ == "__main__":
    page_html = get(URL).text
    page = BeautifulSoup(page_html, features="html.parser")
    weeks = page.find_all("div", class_="row flex-column-reverse flex-md-row lecture-row mb-4 mx-2")
    weeks.reverse()
    WEEK_NUM = 0
    for week in weeks:
        WEEK_NUM += 1
        folder_name = f"Week {WEEK_NUM}"
        os.makedirs(folder_name, exist_ok=True)
        days = week.find_all("div", class_="card-body")
        for day in days:
            title = day.find("h5").text
            date = day.find("div").text
            try:    # only checks first block but slide is always the first block
                slide_block = day.find("ul").find("li").find("a")
            except AttributeError as error:
                continue    # The break day does not have slide_block, so the program continues
            link = "https://courses.engr.illinois.edu/" + slide_block.get("href")   # adds base URL
            if "slides" in link:
                file_name = f"{folder_name}/{title} on {date}.pdf"
                print(file_name)
                slide_content = get(link).content
                with open(file_name, "wb") as slide_file:
                    slide_file.write(slide_content)
                print("Downloaded " + file_name)
            else:   # if there are no slides, like for exam days, continue
                continue
