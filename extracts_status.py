import re
fname = "./report_dc3078d8-ee29-4411-b4ef-fa0f0f0203f2.html"
x = re.search("Status: (.*?)<", open(fname, 'r', encoding='utf-8').read())
print(x.group(1))
