import library
import os.path
import json
import sys

if (len(sys.argv) != 5):
    exit ('Ошибка. Параметры запуска: curr.py [дата начала в формате дд/мм/гггг] [дата конца в формате дд/мм/гггг] [код первой валюты] [код второй валюты]')

params = {
    'date_begin':sys.argv[1],
    'date_end':sys.argv[2],
    'curr_1':sys.argv[3],
    'curr_2':sys.argv[4]
}

beginDateObject = library.getDateFromUser(params['date_begin'])
endDateObject = library.getDateFromUser(params['date_end'], canInFuture=True)

if ((not beginDateObject) or (not endDateObject)):
    exit ('Ошибка. Параметры запуска: curr.py [дата начала в формате дд/мм/гггг] [дата конца в формате дд/мм/гггг] [код первой валюты] [код второй валюты]')

if ((endDateObject - beginDateObject).days < 0):
    exit ('Ошибка. Дата конца не может быть раньше даты начала')

usedCurrencies = [
    "AUD",
    "BYR",
    "CAD",
    "CHF",
    "CNY",
    "DKK",
    "EUR",
    "GBP",
    "ISK",
    "JPY",
    "KZT",
    "NOK",
    "SEK",
    "SGD",
    "TRY",
    "UAH",
    "USD",
    "XDR"
]

if (params['curr_1'] not in usedCurrencies or params['curr_2'] not in usedCurrencies):
    print ('Ошибка, валюта не найдена. Возможные варианты:')
    exit (', '.join(usedCurrencies))

daysToGet = library.getDatesRange(beginDateObject,endDateObject)

resultList = []

for day in daysToGet:

    if (not os.path.exists('cache/'+day.strftime("%d_%m_%Y")+'.json')) :

        dayInfo = library.getDayData(day)

        with open('cache/'+day.strftime("%d_%m_%Y")+'.json', 'w') as jsonDayFile:

            json.dump(dayInfo,jsonDayFile, indent=4, sort_keys=True, ensure_ascii=False)

    else :

        with open('cache/'+day.strftime("%d_%m_%Y")+'.json', 'r') as jsonDayFile:

            dayInfo = json.load(jsonDayFile)

    try:

        priceBefore_1 = currPrice_1
        priceBefore_2 = currPrice_2

    except:

        priceBefore_1 = float(dayInfo[params['curr_1']]["Value"]) / float(dayInfo[params['curr_1']]["Nominal"])
        priceBefore_2 = float(dayInfo[params['curr_2']]["Value"]) / float(dayInfo[params['curr_2']]["Nominal"])

    currPrice_1 = float(dayInfo[params['curr_1']]["Value"]) / float(dayInfo[params['curr_1']]["Nominal"])
    currPrice_2 = float(dayInfo[params['curr_2']]["Value"]) / float(dayInfo[params['curr_2']]["Nominal"])

    resultList.append({
        'date':day.strftime("%d/%m/%Y"),
        params['curr_1']:{
            'value': currPrice_1,
            'delta': currPrice_1 - priceBefore_1
        },
        params['curr_2']:{
            'value': currPrice_2,
            'delta': currPrice_2 - priceBefore_2
        }
    })

with open('result.json', 'w') as jsonResultFile:

    json.dump(resultList,jsonResultFile, indent=4, sort_keys=True, ensure_ascii=False)