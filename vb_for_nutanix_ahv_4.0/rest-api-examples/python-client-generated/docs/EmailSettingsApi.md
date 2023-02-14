# swagger_client.EmailSettingsApi

All URIs are relative to *https://172.25.124.153/*

Method | HTTP request | Description
------------- | ------------- | -------------
[**email_settings_get_email_settings**](EmailSettingsApi.md#email_settings_get_email_settings) | **GET** /api/v4/emailSettings | Get Email Notification Settings
[**email_settings_update_email_settings**](EmailSettingsApi.md#email_settings_update_email_settings) | **PUT** /api/v4/emailSettings | Modify Email Notification Settings

# **email_settings_get_email_settings**
> EmailNotificationSettings email_settings_get_email_settings()

Get Email Notification Settings

The HTTP GET request to the `/emailSettings` endpoint retrieves email notification settings configured in Veeam Backup for Nutanix AHV.

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
api_instance = swagger_client.EmailSettingsApi(swagger_client.ApiClient(configuration))

try:
    # Get Email Notification Settings
    api_response = api_instance.email_settings_get_email_settings()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EmailSettingsApi->email_settings_get_email_settings: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**EmailNotificationSettings**](EmailNotificationSettings.md)

### Authorization

[Bearer](../README.md#Bearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/problem+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **email_settings_update_email_settings**
> email_settings_update_email_settings(body)

Modify Email Notification Settings

The HTTP PUT request to the `/emailSettings` endpoint configures Veeam Backup for Nutanix AHV to send email notifications.

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
api_instance = swagger_client.EmailSettingsApi(swagger_client.ApiClient(configuration))
body = swagger_client.EmailNotificationSettings() # EmailNotificationSettings | Email settings

try:
    # Modify Email Notification Settings
    api_instance.email_settings_update_email_settings(body)
except ApiException as e:
    print("Exception when calling EmailSettingsApi->email_settings_update_email_settings: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**EmailNotificationSettings**](EmailNotificationSettings.md)| Email settings | 

### Return type

void (empty response body)

### Authorization

[Bearer](../README.md#Bearer)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/problem+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

