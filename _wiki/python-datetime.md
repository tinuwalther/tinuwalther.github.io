---
title: Python datetime
date: '2021-06-18T10:50:44+02:00'
author: Tinu
excerpt: Das Mysterium Python datetime. Was mir in PowerShell simple erscheint, ist
  mir in Python immer noch nicht ganz klar - convert string to datetime und umgekehrt,
  was wann wie und warum?
categories:
- Python
tags:
- Python
- Scripting
image: /assets/wiki/python-e1619608154428.png
wordpress_id: 3383
layout: post
permalink: /wiki/python-datetime/
render_with_liquid: false
---

Das Mysterium Python datetime. Was mir in PowerShell simple erscheint, ist mir in Python immer noch nicht ganz klar - convert string to datetime und umgekehrt, was wann wie und warum?

## Convert string to datetime

Mit diesem Beispiel wandle ich ein String-Datum in ein DateTime-Object um.

```
def convert_string_to_datetime(dt_string, dt_format):
    """Convert string to datetime-object"""
    import datetime as dt
    return dt.datetime.strptime(dt_string, dt_format)

if __name__ =="__main__":
    dt_format = "%Y-%m-%dT%H:%M:%S"
    dt_string = "2021-06-20T09:15:00"
    print(type(dt_string), dt_string)

    dt_object = convert_string_to_datetime(dt_string, dt_format)
    print(type(dt_object), dt_object)
```

**Output:**  
<code>&#60;class &#39;str&#39;&#62; 2021&#45;06&#45;20T09&#58;15&#58;00</code>  
<code>&#60;class &#39;datetime&#46;datetime&#39;&#62; 2021&#45;06&#45;20 09&#58;15&#58;00</code>

## Convert datetime to string

Mit diesem Beispiel extrahiere ich aus dem aktuellen TimeStamp (DateTime-Object) den Wochentag als String.

```
def convert_datetime_to_string(dt_object, dt_format):
    """Convert datetime to string"""
    import datetime as dt
    return dt_object.strftime(dt_format)

if __name__ =="__main__":
    import datetime as dt
    dt_object = dt.datetime.now()
    dt_format = "%A"
    
    dt_string = convert_datetime_to_string(dt_object, dt_format)
    if dt_string == "Saturday" or dt_string == "Sunday":
        print("Thanks good, its weekend:", type(dt_string), dt_string, type(dt_object), dt_object)
    else:
        print("Oh no, it's weekday:", type(dt_string), dt_string, type(dt_object), dt_object)
```

**Output:**  
<code>Oh no&#44; it&#39;s weekday&#58; &#60;class &#39;str&#39;&#62; Friday &#60;class &#39;datetime&#46;datetime&#39;&#62; 2021&#45;06&#45;18 09&#58;22&#58;49&#46;396187</code>

## Kombination aus beiden Methoden

Damit aus einem String-Datum der Wochentag extrahiert werden kann, muss das String-Datum zuerst in ein DateTime-Object umgewandelt werden und danach wieder in ein String.

```
if __name__ =="__main__":
    import datetime as dt
    dt_string = "2021-06-20T09:15:00.123456"
    dt_format = "%Y-%m-%dT%H:%M:%S.%f"

    dt_object = convert_string_to_datetime(dt_string, dt_format)
    print(type(dt_object), dt_object)
    dt_format = "%A"

    dt_string = convert_datetime_to_string(dt_object, dt_format)
    print("Day of week:", type(dt_string), dt_string)
```

**Output:**  
<code>&#60;class &#39;datetime&#46;datetime&#39;&#62; 2021&#45;06&#45;20 09&#58;15&#58;00</code>  
<code>Day of week&#58; &#60;class &#39;str&#39;&#62; Sunday</code>

## File datetime

### What is Python epoch

The epoch time is also called Unix time, POSIX time, and Unix timestamp. The epoch time means the number of seconds that have passed since January 1 1970 excluding leap seconds. The Unix time has 10 digits. Unix time can represent all timezone at once.

```
import os, time
from sys import platform
if platform == "linux" or platform == "linux2":
    home_dir = os.environ['HOME']
elif platform == "darwin":
    home_dir = os.environ['HOME']
elif platform == "win32":
    home_dir  = os.environ['USERPROFILE']
    downloads = os.path.join(home_dir,'downloads')

dt_format = "%Y-%m-%d %H:%M:%S"

# Get the Python epoch (timestamp in seconds) of the file
mod_time_since_epoc = os.path.getctime(os.path.join(downloads, "testfile.txt"))
print("mod_time_since_epoc:", type(mod_time_since_epoc), mod_time_since_epoc)

# Convert the timestamp to string-datetime in localtime
dt_string_mod_time  = time.strftime(dt_format, time.localtime(mod_time_since_epoc))
print("dt_string_mod_time :", type(dt_string_mod_time), dt_string_mod_time)

# Convert string-datetime to datetime-object
dt_file_datetime    = dt.datetime.strptime(dt_string_mod_time, dt_format)
print("dt_file_datetime   :", type(dt_file_datetime), dt_file_datetime)
```

**Output:**  
<code>mod&#95;time&#95;since&#95;epoc&#58; &#60;class &#39;float&#39;&#62; 1624005612&#46;6895187</code>  
<code>dt&#95;string&#95;mod&#95;time &#58; &#60;class &#39;str&#39;&#62; 2021&#45;06&#45;18 10&#58;40&#58;12</code>  
<code>dt&#95;file&#95;datetime   &#58; &#60;class &#39;datetime&#46;datetime&#39;&#62; 2021&#45;06&#45;18 10&#58;40&#58;12</code>

## Time delta

```
import datetime as dt
time_span = dt.datetime.now() - dt.timedelta(days=3)
print(type(time_span), time_span)
```

**Output:**  
<code>&#60;class &#39;datetime&#46;datetime&#39;&#62; 2021&#45;06&#45;15 10&#58;36&#58;45&#46;500677</code>

## References

[Python Examples](https://pythonexamples.org/python-datetime-format/), [Python.org](https://docs.python.org/3/library/datetime.html)

