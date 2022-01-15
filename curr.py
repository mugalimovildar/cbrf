import library
import os.path
import json
import datetime

beginDateObject = library.getDateFromUser('Введите дату начала в формате дд/мм/гггг: ')
endDateObject = library.getDateFromUser('Введите дату конца в формате дд/мм/гггг: ',canInFuture=True)

daysToGet = library.getDatesRange(beginDateObject,endDateObject)

for day in daysToGet:

    if (not os.path.exists('cache/'+day.strftime("%d_%m_%Y")+'.json')) :

        dayInfo = library.getDayData(day)

        with open('cache/'+day.strftime("%d_%m_%Y")+'.json', 'w') as jsonDayFile:

            json.dump(dayInfo,jsonDayFile, indent=4, sort_keys=True, ensure_ascii=False)

    else :

        with open('cache/'+day.strftime("%d_%m_%Y")+'.json', 'r') as jsonDayFile:

            dayInfo = json.load(jsonDayFile)

    print (dayInfo)