import json
from datetime import datetime
import requests
from requests.auth import HTTPBasicAuth
import gzip
import pandas as pd

def to_kairos_time(python_time):
    return python_time.timestamp() * 1e3

def to_python_time(kairos_time):
    return datetime.fromtimestamp(kairos_time / 1e3)

def build_postdata(metric, tags, datapoints):
    '''
    metric: str type, metric name
    tags: dict type, {tag_key1:tag_value1, tag_key2:tag_value2, ....}
    datapoints: list type, [[python_dateime1, value1], [python_dateime2, value2], ...], this datetime should be local time
    '''
    #TODO: build strong class of Query
    #TODO: metric type validate
    #TODO: valid datapoints lambda x:type(x[0]) == datetime
    #TODO: valid datapoints lambda x:type(x[1])
    #TODO: valid len(datapoints) != 0
    for d in datapoints:
        assert (type(d[0]) == datetime or type(d[0]) == pd.Timestamp), 'type of first element in each data should be python datetime'

    if type(d[0]) == datetime:
        datapoints = list(map(lambda x:[to_kairos_time(x[0]), x[1]], datapoints))
    elif type(d[0]) == pd.Timestamp:
        datapoints = list(map(lambda x:[to_kairos_time(x[0].to_pydatetime()), x[1]], datapoints))

    postdata = {
        "name": metric,
        "datapoints": datapoints,
        "tags": tags
    }
    return postdata

def build_query_metric_aggregator(name, num, unit, align="none"):
    '''
    name: str type, "avg", "count", "dev", "diff", "div", "filter", "first", "gaps", "last", "least_squares", "max", "min", "percentile", "rate", "sampler", "save_as", "scale", "sum", "trim"
    num: int type, number of unit
    unit: str type, "years", "months", "weeks", "days", "hours", "minutes", "seconds", "milliseconds"
    align: str type, "none", "sample", "start", "end"
    '''
    name_candidate = ["avg", "count", "dev", "diff", "div", "filter", "first", "gaps", "last", "least_squares", "max", "min", "percentile", "rate", "sampler", "save_as", "scale", "sum", "trim"]
    assert name in name_candidate, "name should be in " + str(name_candidate) 
    assert type(num) == int,  "num should be int type " 
    unit_candidate = ["years", "months", "weeks", "days", "hours", "minutes", "seconds", "milliseconds"]
    assert unit in unit_candidate, "name should be in " + str(unit_candidate) 
    align_candidate = ["none", "sample", "start", "end"]
    assert align in align_candidate, "name should be in " + str(align_candidate) 

    aggregator = {}
    aggregator['name'] = name
    aggregator['sampling'] = {"value":str(num), "unit":unit}
    if align != "none":
        if align == 'sample': aggregator['align_sampling']=True
        if align == 'start': aggregator['align_end_time']=True
        if align == 'end': aggregator['align_end_time']=True
    return aggregator
            
def build_query_metric(name, aggragators, tags={}, limit=None):
    '''
    name: str type, metric name
    tags: dict type, {tag_key1:tag_value1, tag_key2:tag_value2, ....}
    aggregators: list type [aggregator1, aggregator2, ...], it's recommended to generate aggragator by pyKairos.build_query_metric_aggregator. If number of input aggregatprs are more than one, it's hierachical concept for aggregating. 
    limit: int type, limitation on return rows.
    '''
    assert type(limit) == int,  "limit should be int type " 

    metric = {}
    metric['name'] = name
    metric['tags'] = tags
    metric['aggragators'] = aggragators
    if limit != None:
        metric['limit'] = limit
    return metric

def build_query(metrics, starttime, endtime=None, cache_time=0):
    '''
    metrics: dict type, it's recommended to generate aggragator by pyKairos.build_query_metric.
    cache_time: int type, int seconds.
    starttime: python datetime type(local time)
    endtime: python datetime type(local time)
    '''
    query = {}
    query['metrics'] = metrics
    query['plugins'] = []
    query['cache_time'] = cache_time
    query['start_absolute'] = to_kairos_time(starttime)
    if endtime != None:
        query['end_absolute'] = to_kairos_time(endtime)
    return query

class KairosClient():
    def __init__(self, host='localhost', port='8080', **kwargs):
        '''kwargs: username, password'''
        self.username = kwargs['username'] if 'username' in kwargs.keys() else None
        self.password = kwargs['password'] if 'password' in kwargs.keys() else None
        self.url = "http://" + str(host) + ":" + str(port) + "/"
    
    def get_all_metrics(self):
        path = self.url + "api/v1/metricnames"
        if self.username == None or self.password == None:
            res = requests.get(path)
        else:
            res = requests.get(path, auth=HTTPBasicAuth(self.username, self.password))
        return json.loads(res.text)['results']
    
    def get_all_tagkeys(self):
        path = self.url + "api/v1/tagnames"
        if self.username == None or self.password == None:
            res = requests.get(path)
        else:
            res = requests.get(path, auth=HTTPBasicAuth(self.username, self.password))
        return json.loads(res.text)['results']

    def get_all_tagvalues(self):
        path = self.url + "api/v1/tagvalues"
        if self.username == None or self.password == None:
            res = requests.get(path)
        else:
            res = requests.get(path, auth=HTTPBasicAuth(self.username, self.password))
        return json.loads(res.text)['results']
    
    def add_datapoints(self, postdatas):
        '''
        queries: list type, [query1, query2, ...], it's recommended to buid query using pyKairos.build_postdata
        '''
        gzipped = gzip.compress(bytes(json.dumps(postdatas), 'UTF-8'))
        headers = {'content-type': 'application/gzip'}
        path = self.url + "api/v1/datapoints"
        if self.username == None or self.password == None:
            res = requests.post(path, gzipped, headers=headers)
        else:
            res = requests.post(path, gzipped, headers=headers, auth=HTTPBasicAuth(self.username, self.password))
        
        if res.status_code == 204:
            return 'success'
        else:
            return 'fail, status code: ' + str(res.status_code)
    
    def query_datapoints(self, query):
        path = self.url + "api/v1/datapoints/query"
        if self.username == None or self.password == None:
            res = requests.post(path, data=json.dumps(query))
        else:
            res = requests.post(path, data=json.dumps(query), auth=HTTPBasicAuth(self.username, self.password))
        return json.loads(res.text)
        