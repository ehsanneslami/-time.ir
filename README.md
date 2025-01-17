# خزنده time.ir و اسکرپ کردن تاریخ

## پیش نیازها
- پایتون 3
- کتابخانه requests
- کتابخانه bs4
- کتابخانه unicode
برای نصب کتابخانه ها می تونید از دو روش:
### روش اول
```
pip install requests
pip install bs4
pip install Unidecode
```

### یا روش دوم با فایل requirement.txt
```pip install -r requirements.txt```
## شروع به کار

خزنده سایت time.ir، دور زدن csrf و موانع. کل اطلاعات در فایل main.py هست. \
سایت time.ir برای جلوگیری از دسترسی ربات ها در مرحله او از csrf استفاده می کنه. اگه بخوایم اطلاعات سال جاری رو بگیریم هیچ مشکلی وجود نداره.\
ولی برای دریافت سالهای دیگه (کلا از سال 1 تا 3000 رو ساپورت می کنه) باید از متد post بعلاوه یک توکن که از سرور گرفته میشه، استفاده کرد.\
خط 18 تا 22 , 26 تا 32 برای عبور از این موارد نوشته شده.
```
session = requests.session()
primary_request = session.get(url)
soup = BeautifulSoup(primary_request.text, 'html.parser')
view_state = (soup.find('input', attrs={'name': '__VIEWSTATE'}))['value']
cookies = session.cookies
```
```
request = requests.post(url, data={
            '__VIEWSTATE': view_state,
            'ctl00$cphTop$Sampa_Web_View_EventUI_EventYearCalendar10cphTop_3417$txtYear': year
        }, cookies=cookies)
soup = BeautifulSoup(request.text, 'html.parser')
months = soup.findAll('div', class_="dayList")
months_event_text = soup.findAll('div', class_="eventsCurrentMonthWrapper")
```
اطلاعات هر روز ماه (خط 39 تا 60) دریافت میشه.

اطلاعات مناسبت ها هم در خط 62 تا 71 به آرایه مون اضافه میشه.
## ساختار آرایه برگشتی
```
today = {
    'solar': solar,
    'moon': moon,
    'gregorian': gregorian,
    'dayWeek': day_week_name[day_week],
    'holiday': 'holiday' in str(day),
    'event': []
}
```

## در انتها
این مخزن صرفا برای آموزش عملی کتباخانه requests و bs4 ایجاد شده.\
خروجی این پروژه رو می تونید در api رایگان تقویم شمسی که هم مناسبت ها و تعطیلات، و هم اطلاعات تبدیل روز رو میده ببینید. آدرس [مستندات api تقویم شمسی](https://pnldev.com/fa/api-doc/calender) \
ارتباط با من [ehsann.seo@gmail.com](mailto:ehsann.seo@gmail.com)
