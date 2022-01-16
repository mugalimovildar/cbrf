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



    resultList.append({
        'date':day.strftime("%d/%m/%Y"),
        params['curr_1']:{
            'value':float(dayInfo[params['curr_1']]["Value"]) / float(dayInfo[params['curr_1']]["Nominal"]),
            'delta':1
        },
        params['curr_2']:{
            'value':float(dayInfo[params['curr_2']]["Value"]) / float(dayInfo[params['curr_2']]["Nominal"]),
            'delta':1
        }
    })

with open('result.json', 'w') as jsonResultFile:

    json.dump(resultList,jsonResultFile, indent=4, sort_keys=True, ensure_ascii=False)