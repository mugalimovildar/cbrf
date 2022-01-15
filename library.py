import datetime
from dateutil.rrule import rrule, DAILY
from xml.dom import minidom
import requests

# Получает дату из пользовательского ввода, проверяет на корректность
# Параметр dateDelimiter устанавливает разделитель дня, месяца и года
# Параметр canInFuture (bool) указывает, корректна ли дата, находящаяся в будущем относительно сегодняшнего дня

def getDateFromUser(queryText,dateDelimiter='/',canInFuture=False):

    while True:

        date_input = input(queryText).strip().split(dateDelimiter)

        # Проверка корректности формата введенной даты

        if (len(date_input) != 3):
            print ('Формат введенной даты некорректен')
            continue
        
        if (not date_input[0].isnumeric() or not date_input[1].isnumeric() or not date_input[2].isnumeric()):
            print ('Формат введенной даты некорректен')
            continue

        try:

            date_object = datetime.datetime(int(date_input[2]),int(date_input[1]),int(date_input[0]))

        except:

            print ('Формат введенной даты некорректен')
            continue

        # Проверка на дату в будущем

        if (not canInFuture):

            today_date_object = datetime.datetime.today()

            if ((today_date_object - date_object).days < 0) :
                print ('Дата начала не может быть в будущем')
                continue

        return (date_object)

def getDatesRange (start_date, end_date):

    days_list = []

    for dt in rrule(DAILY, dtstart=start_date, until=end_date):

        days_list.append(dt);

    return (days_list)

def getDayData (day):

    url = 'http://www.cbr.ru/scripts/XML_daily.asp?date_req='

    currUrl = url + day.strftime("%d/%m/%Y")

    try:

        currXmlData = requests.get(currUrl)

    except:

        return False

    if (currXmlData.status_code == 404):

        return False

    try:

        minidomObject = minidom.parseString(currXmlData.content)

    except:

        return False

    tagsValute = minidomObject.getElementsByTagName('Valute')

    dayDataList = {}

    for currency in tagsValute:

        dayDataList[currency.getElementsByTagName('CharCode')[0].firstChild.nodeValue] = {
            'NumCode':currency.getElementsByTagName('NumCode')[0].firstChild.nodeValue,
            'Nominal':currency.getElementsByTagName('Nominal')[0].firstChild.nodeValue,
            'Name':currency.getElementsByTagName('Name')[0].firstChild.nodeValue,
            'Value':currency.getElementsByTagName('Value')[0].firstChild.nodeValue
        }

    return (dayDataList)