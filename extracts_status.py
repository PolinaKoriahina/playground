## imports 
import json
import requests

def form_message(workflow_status, fname, workflow_link):

  if workflow_status == "KO":
    message = {
            "@context": "http://schema.org/extensions",
            "@type": "MessageCard",
            "themeColor": "F35E5E",
            "title": "GitHub Action workflow failed",
            "text": "Link: " + workflow_link
          }

  else:
    with open(fname) as user_file:
      parsed_json = json.load(user_file)

      test_name = parsed_json["summary"]["name"]
      test_status = parsed_json["summary"]["qualityStatus"]
      test_start = parsed_json["summary"]["startDateText"]
      test_end = parsed_json["summary"]["endDateText"]
      test_description = parsed_json["summary"]["description"]

    if test_status == "FAILED":
      color = "F35E5E"
      image = "https://github.com/PolinaKoriahina/playground/raw/main/red.png"
      test_sla = parsed_json["sla_test"]
      
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
          "text": form_sla(test_sla)
        }
      ]
    }

    else:
      color = "57C478"
      image = "https://github.com/PolinaKoriahina/playground/raw/main/green.png"
      message = {
      "@type": "MessageCard",
      "@context": "http://schema.org/extensions",
      "themeColor": color,
      "summary": test_name + ":" + test_status,
      "sections": [
        {
          "activityTitle": test_name + ":" + test_status,
          "activitySubtitle": test_start + " - " + test_end,
          "activityImage": image
        }
      ]
    }

  final_message = str(message).replace("'", "\"")
  return(final_message)

# def send_mesege(workflow_status, fname, workflow_link, webhook):
#   response = requests.post(webhook, form_message(workflow_status, fname, workflow_link))
#   print(response)

def form_sla(sla_json):
    sla = "<table><thead><tr><th>Category</th><th>Name</th><th>KPI</th><th>operator</th><th>value</th><th>Status</th><th>by value</th></tr></thead><tbody>"
    for element in sla_json:
      category = element["element"]["category"]
      name = element["element"]["name"]
      KPI = element["kpi"]
      operator = element["failedThreshold"]["operator"]
      value = element["value"]
      Status = element["status"]
      by_value =element["failedThreshold"]["values"][0]

      sla +=f"<tr><td>{category}</td><td>{name}</td><td>{KPI}</td><td>{operator}</td><td>{value}</td><td>{Status}</td><td>{by_value}</td></tr>"
    sla += """</tbody></table>"""
    return(sla)
