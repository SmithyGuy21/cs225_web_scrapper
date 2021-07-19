import os
from requests import get
from bs4 import BeautifulSoup

URL = "https://courses.engr.illinois.edu/cs225/sp2021/pages/lectures.html"  # target URL

if __name__ == "__main__":
    page_html = get(URL).text
    page = BeautifulSoup(page_html, features="html.parser")
    weeks = page.find_all("div", class_="row flex-column-reverse flex-md-row lecture-row mb-4 mx-2")
    weeks.reverse()
    week_num = 0
    for week in weeks:
        week_num += 1
        folder_name = f"week{week_num}"
        os.makedirs(folder_name, exist_ok=True)
        days = week.find_all("div", class_="card-body")
        for day in days:
            title = day.find("h5").text
            date = day.find("div").text            
            try:
                slide_block = day.find("ul").find("li").find("a")   # only checks first block but slide is always the first block
            except AttributeError as e: # break day has not slide_block, in which case, the program continues
                continue
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


