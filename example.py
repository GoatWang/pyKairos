import os
from datetime import datetime
import pyKairos as pk
from random import randint

host = 'localhost'
port = '18080'
kairos_username = os.environ['KAIROS_USERNAME']
kairos_password = os.environ['KAIROS_PASSWORD']
client = pk.KairosClient(host=host, port=port, username=kairos_username, password=kairos_password)

# query
# aggregator = pk.build_query_metric_aggregator('avg', 2, 'days')
# metric = pk.build_query_metric('temperature_london', [aggregator], {"region":'london'}, limit=100)
# query = pk.build_query([metric], datetime(2005, 1, 1), datetime(2005, 1, 29))
# res = client.query_datapoints(query)
# print(res['queries'][0])

# add
# datapoints = [[datetime(2005, 1, 1, 0, 0), 20.7],
#                 [datetime(2005, 1, 2, 0, 0), 17.9],
#                 [datetime(2005, 1, 3, 0, 0), 18.8],
#                 [datetime(2005, 1, 4, 0, 0), 14.6],
#                 [datetime(2005, 1, 5, 0, 0), 15.8],
#                 [datetime(2005, 1, 6, 0, 0), 15.8],
#                 [datetime(2005, 1, 7, 0, 0), 15.8],
#                 [datetime(2005, 1, 8, 0, 0), 17.4],
#                 [datetime(2005, 1, 9, 0, 0), 21.8],
#                 [datetime(2005, 1, 10, 0, 0), 20.0]]
# datapoints = list(map(lambda x: [x[0], x[1] - randint(0, 5)], datapoints))
# tags = {"type": "temperature","region": "taipei"}
# postdata = pk.build_postdata("temperature_london", tags, datapoints)
# res = client.add_datapoints(postdata)
# print(postdata)
# print(res)



