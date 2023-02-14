# swagger_client.ServiceSettingsApi

All URIs are relative to *https://172.25.124.153/*

Method | HTTP request | Description
------------- | ------------- | -------------
[**service_settings_get_network_settings**](ServiceSettingsApi.md#service_settings_get_network_settings) | **GET** /api/v4/networkSettings | Get Backup Appliance Network Settings

# **service_settings_get_network_settings**
> NetworkSettings service_settings_get_network_settings()

Get Backup Appliance Network Settings

The HTTP GET request to the `/networkSettings` endpoint retrieves network settings of the backup appliance.

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
api_instance = swagger_client.ServiceSettingsApi(swagger_client.ApiClient(configuration))

try:
    # Get Backup Appliance Network Settings
    api_response = api_instance.service_settings_get_network_settings()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ServiceSettingsApi->service_settings_get_network_settings: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**NetworkSettings**](NetworkSettings.md)

### Authorization

[Bearer](../README.md#Bearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/problem+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

