# swagger_client.TimezonesApi

All URIs are relative to *https://172.25.124.153/*

Method | HTTP request | Description
------------- | ------------- | -------------
[**timezones_get_current_timezone_info**](TimezonesApi.md#timezones_get_current_timezone_info) | **GET** /api/v4/timezones/info | Get Current Time Zone

# **timezones_get_current_timezone_info**
> CurrentTimeZoneInfo timezones_get_current_timezone_info()

Get Current Time Zone

The HTTP GET request to the `/timezones/info` endpoint retrieves the current time zone of the Veeam Backup for Nutanix AHV appliance.

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# Configure API key authorization: Bearer
configuration = swagger_client.Configuration()
configuration.api_key['Authorization'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Authorization'] = 'Bearer'

# create an instance of the API class
api_instance = swagger_client.TimezonesApi(swagger_client.ApiClient(configuration))

try:
    # Get Current Time Zone
    api_response = api_instance.timezones_get_current_timezone_info()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TimezonesApi->timezones_get_current_timezone_info: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**CurrentTimeZoneInfo**](CurrentTimeZoneInfo.md)

### Authorization

[Bearer](../README.md#Bearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/problem+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

