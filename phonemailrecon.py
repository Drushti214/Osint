# get phone numbers and emails from a website

import re, requests, json

target = "https://timesinternet.in/"

text = requests.get(target).text.replace(" ","").replace("\n\n","").replace("\n","").replace(">",">\n")
emails = list(set(re.findall(r'\w+@\w+\.{1}\w+', text)))
phones = list(set(re.findall(r"(?:\+\d{2})?\d{3,4}\D?\d{3}\D?\d{3}", text)))
print(json.dumps({"emails" : emails, "phones" : phones}, indent=4))
