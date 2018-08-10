import os
import pyKairos as pk
host = 'localhost'
port = '18080'
kairos_username = os.environ['KAIROS_USERNAME']
kairos_password = os.environ['KAIROS_PASSWORD']
client = pk.KairosClient(host=host, port=port, username=kairos_username, password=kairos_password)

# add
from datetime import datetime
datapoints = [[datetime(2015, 1, 1, 0, 0), 20.7],
                [datetime(2015, 1, 2, 0, 0), 17.9],
                [datetime(2015, 1, 3, 0, 0), 18.8],
                [datetime(2015, 1, 4, 0, 0), 14.6],
                [datetime(2015, 1, 5, 0, 0), 15.8],
                [datetime(2015, 1, 6, 0, 0), 15.8],
                [datetime(2015, 1, 7, 0, 0), 15.8],
                [datetime(2015, 1, 8, 0, 0), 17.4],
                [datetime(2015, 1, 9, 0, 0), 21.8],
                [datetime(2015, 1, 10, 0, 0), 20.0]]
tags = {"type": "temperature","region": "london"}
postdata = pk.build_postdata("temperature", tags, datapoints)
res = client.add_datapoints(postdata)
print("add data")
print(postdata)
print(res)
print("-------------------------")

# query
aggregator = pk.build_query_metric_aggregator('avg', 2, 'days')
metric = pk.build_query_metric('temperature', [aggregator], {"region":'london'}, limit=5)
query = pk.build_query([metric], datetime(2015, 1, 1), datetime(2015, 1, 9))
res = client.query_datapoints(query)
print("query data")
print(res)
print("-------------------------")

# delete
metric = pk.build_query_metric('temperature', tags={"region":'london'})
query = pk.build_query([metric], datetime(2015, 1, 1))
res = client.delete_datapoints(query)
print("delete data")
print(res)
print("-------------------------")

