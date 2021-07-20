import pandas as pd
import requests
from bs4 import BeautifulSoup

print("Enter search query...")

query = input('>')
jobs_list = []
for i in range(50):
    url = f'https://wuzzuf.net/search/jobs/?a=navbl&q={query}&start={i}'

    html_text = requests.get(url).text
    soup = BeautifulSoup(html_text, 'lxml')

    jobs = soup.find_all('div', class_="css-1gatmva e1v1l3u10")
    if not jobs:
        break
    for job in jobs:
        try:
            job_title = job.find("a", class_="css-o171kl").text
            company_name = job.find('div', class_="css-d7j1kk").find('a').text.strip()
            meta = job.find('div', class_='css-y4udm8')
            years_experience = meta.find('div', attrs={'class': None}).span.text.replace('·', '').strip()
            skills = [skill.text.replace('·', '').strip() for skill in meta.find_all("a", class_="css-5x9pm1")]

            jobs_list.append({
                "job_title": job_title,
                "company_name": company_name,
                "years_experience": years_experience,
                "skills": skills
            })
            print(job_title)
            print(company_name)
            print(years_experience)
            print(skills)
            print()
        except Exception as e:
            continue
jobs_df = pd.DataFrame(jobs_list)
jobs_df.to_csv('test.csv', index=False)