## imports 
import re
import json

fname = "./raw_data_dc3078d8-ee29-4411-b4ef-fa0f0f0203f2.json"

import json

with open(fname) as user_file:
  parsed_json = json.load(user_file)

test_name = parsed_json["summary"]["name"]
test_status = parsed_json["summary"]["qualityStatus"]
test_start = parsed_json["summary"]["startDateText"]
test_end = parsed_json["summary"]["endDateText"]
test_description = parsed_json["summary"]["description"]
test_sla = parsed_json["sla_test"]

if test_status == "FAILED":
  color = "F35E5E"
  image = "./red.png"
else:
  color = "57C478"
  image = "./green.png"

sla = []
for element in test_sla:
    sla.append({"name": {element["element"]["category"] + ":" + element["element"]["name"]},"value": {element["status"]}})

message = {
  "@type": "MessageCard",
  "@context": "http://schema.org/extensions",
  "themeColor": color,
  "summary": test_name + ":" + test_status,
  "sections": [
    {
      "activityTitle": test_name + ":" + test_status,
      "activitySubtitle": test_start + " - " + test_end,
      "activityImage": image,
      "facts": [
        {
          "name": "Description",
          "value": test_description
        },
      ]
    },
    {
      "title": "SLA",
      "facts":
      sla
    }
  ]
}

print(str(message))
