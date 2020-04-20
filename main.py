import os
import csv
import requests
from bs4 import BeautifulSoup

os.system("clear")
alba_url = "http://www.alba.co.kr"


def get_data(html):
    link = html.find('a')
    name = link.find('span', {'class': 'company'}).string
    return {'links': link["href"],
            'name': name}


def extract_link():
    datas = []
    result = requests.get(alba_url)
    soup = BeautifulSoup(result.text, 'html.parser')
    brand_list = soup.find("div", {"id": "MainSuperBrand"}).find(
        'ul', {'class': 'goodsBox'}).find_all('li', {'class': 'impact'})
    for brand in brand_list:
        data = get_data(brand)
        datas.append(data)
    return datas


def extract_job(things):
    place = things.find('td', {'class': 'local'}).find_next(string=True)
    place = place.replace(u'\xa0', u' ')
    title = things.find('td', {'class': 'title'}).find(
        'span', {'class': 'company'}).string
    time = things.find('td', {'class': 'data'}).find('span', {'class': 'time'})
    if time:
        time = time.string
    else:
        time = None
    pay1 = things.find('td', {'class': 'pay'}).find(
        'span', {'class': 'payIcon'}).string
    pay2 = things.find('td', {'class': 'pay'}).find(
        'span', {'class': 'number'}).string
    date = things.find('td', {'class': 'regDate'}).find_next(string=True)
    return {'place': place,
            'title': title,
            'time': time,
            'pay': pay1+pay2,
            'date': date
            }


def extract_jobs(links):
    jobs_list = []
    # for i in range(2):
    for i in range(len(links)):
        jobs = []
        name = links[i]['name']
        print(f"scrapping jobs of {name}")
        result = requests.get(f"{links[i]['links']}")
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find('tbody').find_all('tr', {'class': ['', 'divide']})
        for things in results:
            job = extract_job(things)
            jobs.append(job)
        jobs_list.append(jobs)
    return jobs_list


def save_to_file(jobs, links):
    # for i in range(2):
    for i in range(len(links)):
        name = links[i]['name']
        file = open(f"{name}.csv", mode="w")
        writer = csv.writer(file)
        writer.writerow(["place", "title", "time", "pay", "date"])
        for job in jobs[i]:
            writer.writerow(list(job.values()))
    return


link = extract_link()
jobs = extract_jobs(link)
save_to_file(jobs, link)
