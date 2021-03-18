# credential-as-a-proxy

Following are instrucutions for testing the proxy. gcloud CLI is used for procuring an access token: https://cloud.google.com/sdk/gcloud/reference

1. Starts the proxy:
```console
$ ./google_certificate_proxy.py
```

2. Sends a GET request via the proxy:
```console
curl -H "Authorization: Bearer `gcloud auth print-access-token`" -H "GOOG_SERVICE_URL: https://bigquery.googleapis.com/bigquery/v2/projects/yaoliu-test/jobs" http://localhost:10000
```

3. Sends a POST request via the proxy:
```console
curl -X POST -H "Content-type: application/json" -H "Authorization: Bearer `gcloud auth print-access-token`" -H "GOOGLE_SERVICE_URL: https://bigquery.googleapis.com/bigquery/v2/projects/yaoliu-test/queries" --data '{"query":"SELECT 1"}' http://localhost:10000
```