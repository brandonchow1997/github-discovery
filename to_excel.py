import pymongo
import pandas as pd
client = pymongo.MongoClient('localhost', 27017)
db = client['github_spider']
table = db['Discover_repositories']
data = pd.DataFrame(list(table.find()))
del data['_id']
print(data)
data.to_excel('github_discovery.xls')
