import json
import plotly
from plotly.graph_objs import Bar, Layout


STUDENTS_ON_CAMPUS = 30731

def cleanWeekdays(weekdaysStr):
	weekdaysList = []
	if "Th" in weekdaysStr:
		weekdaysList.append("Th")
		weekdaysStr.replace("Th", "")
	if "M" in weekdaysStr:
		weekdaysList.append("M")
		weekdaysStr.replace("M", "")
	if "T" in weekdaysStr:
		weekdaysList.append("T")
		weekdaysStr.replace("T", "")
	if "W" in weekdaysStr:
		weekdaysList.append("W")
		weekdaysStr.replace("W", "")
	if "F" in weekdaysStr:
		weekdaysList.append("F")
		weekdaysStr.replace("F", "")
	if "S" in weekdaysStr:
		weekdaysList.append("S")
		weekdaysStr.replace("S", "")
	return weekdaysList

def createTimes():
	daysOfTheWeek = ["Su", "M", "T", "W", "Th", "F", "S"]

	timeList = []

	for day in daysOfTheWeek:
		hour = 11
		minute = 0
		count = 1

		while count <= 288:
			sTime = day + " " + str((hour % 12) + 1).zfill(2) + ":" + str(minute).zfill(2)
			if hour < 23:
				sTime += "AM"
			else:
				sTime += "PM"
			timeList.append(sTime)
			minute += 5
			if minute == 60:
				minute = 0
				hour += 1
			count += 1

	return timeList


with open("dirtyClassDetails.json", "r") as dirtyClassDetailsFile:
	dirtyClassDetailsData = json.load(dirtyClassDetailsFile)

classDetailsList = []
count = 1

for course in dirtyClassDetailsData:
	courseData = course["data"]
	for section in courseData:
		for classSet in section["classes"]:
			if classSet["date"]["weekdays"]:
				weekdays = cleanWeekdays(classSet["date"]["weekdays"])
				if classSet["date"]["start_time"] and classSet["date"]["end_time"] and (len(weekdays) > 0):
					for weekday in weekdays:
						classDetailsList.append({
							"catalog_number": section["catalog_number"],
							"class_number": section["class_number"],
							"subject": section["subject"],
							"title": section["title"],
							"section": section["section"],
							"academic_level": section["academic_level"],
							"enrollment_total": section["enrollment_total"],
							"start_time": classSet["date"]["start_time"],
							"end_time": classSet["date"]["end_time"],
							"weekday": weekday,
						})
	count += 1

with open("classDetails.json", "w") as outFile:
	outputData = json.dumps(classDetailsList, indent=4)
	outFile.write(outputData)


times = createTimes()
inClassValues = [0] * len(times)

for idx, timeStr in enumerate(times):
	splitTime = timeStr.split()
	timeStrWeekday = splitTime[0]
	timeStrHour = int(splitTime[1][:2])
	timeStrMin = int(splitTime[1][3:5])

	if splitTime[1][-2:] == "PM" and not (timeStrHour == 12):
		timeStrHour += 12
	elif splitTime[1][-2:] == "AM" and timeStrHour == 12:
		timeStrHour = 0
	
	for classTime in classDetailsList:
		if timeStrWeekday == classTime["weekday"]:
			classStartHour = int(classTime["start_time"][:2])
			classStartMin = int(classTime["start_time"][-2:])
			classEndHour = int(classTime["end_time"][:2])
			classEndMin = int(classTime["end_time"][-2:])

			if (timeStrHour > classStartHour) and (timeStrHour < classEndHour):
				inClassValues[idx] += classTime["enrollment_total"]
			elif (timeStrHour == classStartHour) and (timeStrMin >= classStartMin) and (timeStrHour < classEndHour):
				inClassValues[idx] += classTime["enrollment_total"]
			elif (timeStrHour > classStartHour) and (timeStrMin <= classEndMin) and (timeStrHour == classEndHour):
				inClassValues[idx] += classTime["enrollment_total"]
			elif (timeStrHour == classStartHour) and (timeStrMin >= classStartMin) and (timeStrMin <= classEndMin) and (timeStrHour == classEndHour):
				inClassValues[idx] += classTime["enrollment_total"]

percentValues = [(100.0 * x) / STUDENTS_ON_CAMPUS for x in inClassValues]

graphData = [
    Bar (
        x = times,
        y = percentValues,
        text = [str(x) + " students" for x in inClassValues]
    )
]

plotly.offline.plot({
	"data": graphData,
	"layout": Layout (
	    title = "UW Class Schedules",
	    yaxis = dict(
	    	title = "Percentage of students supposed to be in class",
	    )
	)
},
show_link=False, filename='uw-class-schedules.html')



