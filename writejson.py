import json

a = [{'1' : '2'},{'2':'3','3' : '555'}]
with open('data.json','w') as fw:
    json.dump(a,fw)