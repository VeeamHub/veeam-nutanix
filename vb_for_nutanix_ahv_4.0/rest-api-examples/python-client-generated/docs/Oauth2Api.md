# swagger_client.Oauth2Api

All URIs are relative to *https://172.25.124.153/*

Method | HTTP request | Description
------------- | ------------- | -------------
[**oauth2_logout**](Oauth2Api.md#oauth2_logout) | **POST** /api/oauth2/logout | Logout
[**oauth2_token**](Oauth2Api.md#oauth2_token) | **POST** /api/oauth2/token | Request Authorization Tokens

# **oauth2_logout**
> oauth2_logout()

Logout

The HTTP POST request to the `/logout` endpoint performs the logout operation for an authorized user.

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
api_instance = swagger_client.Oauth2Api(swagger_client.ApiClient(configuration))

try:
    # Logout
    api_instance.oauth2_logout()
except ApiException as e:
    print("Exception when calling Oauth2Api->oauth2_logout: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

void (empty response body)

### Authorization

[Bearer](../README.md#Bearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/problem+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **oauth2_token**
> TokenModel oauth2_token(grant_type, user_name, password, refresh_token, updater_token, long_lived_refresh_token)

Request Authorization Tokens

The HTTP POST request to the `/token` endpoint allows you to authorize your access to the Veeam Backup for Nutanix AHV REST API.

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
api_instance = swagger_client.Oauth2Api(swagger_client.ApiClient(configuration))
grant_type = swagger_client.GrantType() # GrantType | 
user_name = 'user_name_example' # str | 
password = 'password_example' # str | 
refresh_token = 'refresh_token_example' # str | 
updater_token = 'updater_token_example' # str | 
long_lived_refresh_token = true # bool | 

try:
    # Request Authorization Tokens
    api_response = api_instance.oauth2_token(grant_type, user_name, password, refresh_token, updater_token, long_lived_refresh_token)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling Oauth2Api->oauth2_token: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **grant_type** | [**GrantType**](.md)|  | 
 **user_name** | **str**|  | 
 **password** | [**str**](.md)|  | 
 **refresh_token** | **str**|  | 
 **updater_token** | **str**|  | 
 **long_lived_refresh_token** | **bool**|  | 

### Return type

[**TokenModel**](TokenModel.md)

### Authorization

[Bearer](../README.md#Bearer)

### HTTP request headers

 - **Content-Type**: application/x-www-form-urlencoded
 - **Accept**: application/json, application/problem+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

