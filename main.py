import requests
from bs4 import BeautifulSoup
import re
import time
from unidecode import unidecode #pip install Unidecode

day_week_name = {
    0: 'ش',
    1: 'ی',
    2: 'د',
    3: 'س',
    4: 'چ',
    5: 'پ',
    6: 'ج',
}

url = "https://www.time.ir/fa/eventyear-%d8%aa%d9%82%d9%88%db%8c%d9%85-%d8%b3%d8%a7%d9%84%db%8c%d8%a7%d9%86%d9%87"
session = requests.session()
primary_request = session.get(url)
soup = BeautifulSoup(primary_request.text, 'html.parser')
view_state = (soup.find('input', attrs={'name': '__VIEWSTATE'}))['value']
cookies = session.cookies

for year in range(1, 3001):
    print(year)
    request = requests.post(url, data={
            '__VIEWSTATE': view_state,
            'ctl00$cphTop$Sampa_Web_View_EventUI_EventYearCalendar10cphTop_3417$txtYear': year
        }, cookies=cookies)
    soup = BeautifulSoup(request.text, 'html.parser')
    months = soup.findAll('div', class_="dayList")
    months_event_text = soup.findAll('div', class_="eventsCurrentMonthWrapper")
    full_calender = {}
    month_counter = 1
    for month in months:
        full_calender[month_counter] = {}
        days = month.findChildren("div" , recursive=False)
        day_week = 0
        for day in days:
            if 'disabled' not in str(day):
                solar = unidecode(re.sub('\D', '', day.find('div', class_="jalali").text))
                moon = unidecode(re.sub('\D', '', day.find('div', class_="qamari").text))
                if moon != '':
                    moon = int(moon)
                gregorian = unidecode(re.sub('\D', '', day.find('div', class_="miladi").text))

                today = {
                    'solar': solar,
                    'moon': moon,
                    'gregorian': gregorian,
                    'dayWeek': day_week_name[day_week],
                    'holiday': 'holiday' in str(day),
                    'event': []
                }
                full_calender[month_counter][solar] = today

            if day_week >= 6:
                day_week = 0
            else:
                day_week += 1
        
        this_month_event_text = months_event_text[month_counter - 1].findAll('li')
        for event in this_month_event_text:
            spans = event.findAll('span')
            day = unidecode(re.sub('\D', '', spans[0].text))
            event_text = (spans[0].next_sibling).replace('\r', '').replace('\n', '').strip()
            if (spans[1].text).replace('\r', '').replace('\n', '').strip() != '':
                event_text += ' ' + (spans[1].text).replace('\r', '').replace('\n', '').strip()

            
            full_calender[month_counter][day]['event'].append(event_text)
        
        month_counter += 1

    view_state = (soup.find('input', attrs={'name': '__VIEWSTATE'}))['value']
    time.sleep(1)
