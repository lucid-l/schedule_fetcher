import bs4
import requests
import re

def fetch_timetable(
    site_URL: str = "https://ss-ikrsnjavoga-nasice.skole.hr/raspored-sati/",
    timetable_name: str = "GIM-EK",
    schedule_prefference: str = "new"
    ) -> str:
    try:
        site_content = requests.get(site_URL).content
        site_soup = bs4.BeautifulSoup(site_content, 'html.parser')

        all_links = site_soup.find_all('a')
        found_links = []

        for link in all_links:
            link_name = str(link)
            if timetable_name in link_name:
                if "drive" in link_name:
                    id = re.search(r'/d/([^/]+)', link_name).group(1)
                    link = pdf_link = f"https://drive.google.com/uc?export=download&id={id}"
                    link = bs4.BeautifulSoup(f"<a href='{link}'>Download</a>", 'html.parser').a
                    found_links.append(link)
                else:
                    found_links.append(link)
                    
        if len(found_links) > 1:
            old_schedule_link = found_links[0]['href']
            new_schedule_link = found_links[1]['href']
            if schedule_prefference == "new":
                return new_schedule_link
            else:
                return old_schedule_link
        elif len(found_links) == 1:
            return found_links[0]['href']
        else:
            return "No timetable found for the specified class."
    except Exception as e:
        return f"Error fetching timetable: {e}"
