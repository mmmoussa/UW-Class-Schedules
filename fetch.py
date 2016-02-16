import requests
import json

uwApiEndpoint = "https://api.uwaterloo.ca/v2/"
apiKey = "YOUR API KEY HERE"

reqUrl = uwApiEndpoint + "terms/1161/courses.json?key=" + apiKey

r = requests.get(reqUrl)
courseListData = r.json()

courseDetailsList = []
print "There are " + str(len(courseListData["data"])) + " courses"
count = 1

for course in courseListData["data"]:
	print "Getting details for course " + str(count)
	reqUrl = uwApiEndpoint + "terms/1161/" + course["subject"] + "/" + course["catalog_number"] + "/schedule.json?key=" + apiKey
	r = requests.get(reqUrl)
	fullCourseData = r.json()
	courseDetailsList.append(fullCourseData)
	count += 1

with open("dirtyClassDetails.json", "w") as outFile:
	outputData = json.dumps(courseDetailsList, indent=4)
	outFile.write(outputData)

