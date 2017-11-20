Log Analysis
============

Prerequisites:
  * docker
  * docker-compose
  * python3 (for computing average size)


Start Graylog:
`docker-compose up -d`


To access Graylog, go to `http://localhost:9000`. Log in with user "admin" and password "admin".


Set up an Input to accept Raw/Plain Text on port 5555.


Set up a Grok type Extractor for this input. Use the following for the pattern:
```
(?<x_forwarded_for>%{IPORHOST}|-)(?<other_forwards>(?:, %{IPORHOST}|-)*) %{HTTPDUSER:ident} %{USER:auth} \[%{HTTPDATE:timestamp}\] "(?:%{WORD:verb} %{NOTSPACE:request}(?: HTTP/%{NUMBER:httpversion})?|%{DATA:rawrequest})" %{NUMBER:response} (?:%{INT:response_size}|-) %{QS:referrer} %{QS:agent} (?:%{WORD:imagereader_source}|-) (?:%{NUMBER:php_time_microsec}|-) %{NUMBER:total_request_time}
```


Run the `insert-data.sh` script to add the logs into Graylog.




Computing Average Size of Successful Response
---------------------------------------------

Graylog was not showing/computing the median of the `response_size` field, so I had to take matters into my own hands. This included:
  - Open the Chrome Dev Tools and go to the "Network" tab
  - Search for the items you need and look for the request (note: there will be a lot of requests)
  - Right click the request -> Copy -> Copy as cURL
  - Run that cURL command and output to `success.json`. This includes pasting the command in the terminal and appending " > success.json" to the end of the command
  - Run the `average-response-size.py` script to get the average values

