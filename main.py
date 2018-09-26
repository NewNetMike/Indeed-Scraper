import requests
from bs4 import BeautifulSoup


class IndeedJob:
    def __init__(self, title, company, link):
        self.title = title
        self.company = company
        self.link = link


url = "https://www.indeed.com/jobs?l=Los+Angeles,+CA&jt=parttime"
num_pages = 8


def extract_job_title_from_result(soup):
    jobs = []
    for div in soup.find_all(name="div", attrs={"class":"row"}):
        for a in div.find_all(name="a", attrs={"data-tn-element":"jobTitle"}):
            jobs.append(a["title"])
    return jobs


def extract_company_from_result(soup):
    companies = []
    for div in soup.find_all(name="div", attrs={"class":"row"}):
        company = div.find_all(name="span", attrs={"class":"company"})
        if len(company) > 0:
            for b in company:
                companies.append(b.text.strip())
        else:
            sec_try = div.find_all(name="span", attrs={"class":"result-link-source"})
            for span in sec_try:
                companies.append(span.text.strip())
    return companies


def extract_links(soup):
    links = []
    divs = soup.findAll("div", attrs={"class": "result"})
    a_tags = []
    for d in divs:
        links.append("https://indeed.com" + d.find_all("a", href=True)[0]['href'])

    return links


counter = 0
indeedjobs = []

for i in range(num_pages):
    URL = "{}&start={}".format(url, i*10)
    page = requests.get(URL)
    soup = BeautifulSoup(page.text, "html.parser")

    jobs = extract_job_title_from_result(soup)
    companies = extract_company_from_result(soup)
    links = extract_links(soup)

    for n in range(len(jobs)):
        occurrences = [i for i, x in enumerate(indeedjobs) if x.title == jobs[n] and x.company == companies[n]]
        if len(occurrences) == 0:
            indeedjobs.append(IndeedJob(jobs[n], companies[n], links[n]))
    print("Scraped page {}..".format(i+1))

print("\n{:>75} | {:<52} {}\n".format("JOB TITLE", "EMPLOYER", "LINK:"))

for ij in indeedjobs:
    print("{:>75} | {:<52} {}".format(ij.title, ij.company, ij.link))