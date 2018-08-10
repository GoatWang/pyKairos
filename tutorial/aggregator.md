1. avg, count, first, last, least_squares, max, min, sum:
```
"aggregators": [
    {
        "name": "avg",
        "sampling": {
            "value": "3",
            "unit": "days"
            },
        "align_sampling": true
        # "align_start_time": true
        # "align_end_time": true
    }
]
```

2. dev
```
"aggregators": [{
        "name": "dev",
        "sampling": {
            "value": "3",
            "unit": "days",
            },
        "return_type": "value"
        # "return_type": "pos_sd"
        # "return_type": "neg_sd"

    }
],
```


3. diff
```
"aggregators": [{
    "name": "diff"
    }
]
```

4. div
```
"aggregators": [{
    "name": "div",
    "divisor": "1.2"
    }
],
```

5. filter
```
"aggregators": [{
    "name": "filter",
    "filter_op": "equal",
    # "filter_op": "lt",
    # "filter_op": "lte",
    # "filter_op": "gt",
    # "filter_op": "gte",
    "threshold": "25"
    }
],
```

6. percentile
```
"aggregators": [{
    "name": "percentile",
    "sampling": {
        "value": "1",
        "unit": "days"
        },
    "percentile": "0.75"
    }
],
```

7. rate:
```
"aggregators": [{
    "name": "rate",
    "sampling": {
        "unit": "weeks",
        "value": 1
        }
    }
],
```

8. sampler
```
"aggregators": [{
        "name": "sampler",
        "unit": "weeks"
    }
],
```

9. scale
```
"aggregators": [{
        "name": "scale",
        "factor": "0.1"
    }
],
```

10. trim
```
"aggregators": [{
        "name": "trim",
        "trim": "first"
        "trim": "last"
        "trim": "both"
    }
],
```