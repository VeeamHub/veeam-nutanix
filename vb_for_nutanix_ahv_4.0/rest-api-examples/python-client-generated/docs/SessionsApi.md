# swagger_client.SessionsApi

All URIs are relative to *https://172.25.124.153/*

Method | HTTP request | Description
------------- | ------------- | -------------
[**sessions_get_base_info**](SessionsApi.md#sessions_get_base_info) | **GET** /api/v4/sessions | Get Collection of Sessions
[**sessions_get_by_id**](SessionsApi.md#sessions_get_by_id) | **GET** /api/v4/sessions/{id} | Get Session Data
[**sessions_stop**](SessionsApi.md#sessions_stop) | **POST** /api/v4/sessions/{id}/stop | Stop Session Processing

# **sessions_get_base_info**
> PageOfSessionBaseInfo sessions_get_base_info(_from=_from, to=to, offset=offset, limit=limit, filter=filter, sort=sort)

Get Collection of Sessions

For each performed operation (VM backup, restore, snapshot creation and so on) Veeam Backup for Nutanix AHV starts a new session. The HTTP GET request to the `/sessions` endpoint retrieves a list of sessions stored in the Veeam Backup for Nutanix AHV database.

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
api_instance = swagger_client.SessionsApi(swagger_client.ApiClient(configuration))
_from = '2013-10-20T19:20:30+01:00' # datetime | Returns only sessions run after the specified date and time. (optional)
to = '2013-10-20T19:20:30+01:00' # datetime | Returns only sessions run before the specified date and time. (optional)
offset = 0 # int | Excludes from a response the first N items of a resource collection. (optional) (default to 0)
limit = 100 # int | Specifies the maximum number of items of a resource collection to return in a response. (optional) (default to 100)
filter = swagger_client.FilterParameter() # FilterParameter | Specifies the criteria for items to be returned in a response. For more information, see the Veeam Backup for Nutanix AHV REST API Reference Overview, section [Filter Parameters](https://helpcenter.veeam.com/docs/van/rest/filter.html?ver=40). (optional)
sort = swagger_client.SortParameter() # SortParameter | Specifies the order of items in the response. For more information, see the Veeam Backup for Nutanix AHV REST API Reference Overview, section [Sort Parameters](https://helpcenter.veeam.com/docs/van/rest/sort.html?ver=40). (optional)

try:
    # Get Collection of Sessions
    api_response = api_instance.sessions_get_base_info(_from=_from, to=to, offset=offset, limit=limit, filter=filter, sort=sort)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SessionsApi->sessions_get_base_info: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **_from** | **datetime**| Returns only sessions run after the specified date and time. | [optional] 
 **to** | **datetime**| Returns only sessions run before the specified date and time. | [optional] 
 **offset** | **int**| Excludes from a response the first N items of a resource collection. | [optional] [default to 0]
 **limit** | **int**| Specifies the maximum number of items of a resource collection to return in a response. | [optional] [default to 100]
 **filter** | [**FilterParameter**](.md)| Specifies the criteria for items to be returned in a response. For more information, see the Veeam Backup for Nutanix AHV REST API Reference Overview, section [Filter Parameters](https://helpcenter.veeam.com/docs/van/rest/filter.html?ver&#x3D;40). | [optional] 
 **sort** | [**SortParameter**](.md)| Specifies the order of items in the response. For more information, see the Veeam Backup for Nutanix AHV REST API Reference Overview, section [Sort Parameters](https://helpcenter.veeam.com/docs/van/rest/sort.html?ver&#x3D;40). | [optional] 

### Return type

[**PageOfSessionBaseInfo**](PageOfSessionBaseInfo.md)

### Authorization

[Bearer](../README.md#Bearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/problem+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **sessions_get_by_id**
> Session sessions_get_by_id(id)

Get Session Data

The HTTP GET request to the `/session/{id}` endpoint retrieves information on a session with the specified ID.

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
api_instance = swagger_client.SessionsApi(swagger_client.ApiClient(configuration))
id = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | Specifies the system ID of a session in the Veeam Backup for Nutanix AHV.

try:
    # Get Session Data
    api_response = api_instance.sessions_get_by_id(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SessionsApi->sessions_get_by_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | [**str**](.md)| Specifies the system ID of a session in the Veeam Backup for Nutanix AHV. | 

### Return type

[**Session**](Session.md)

### Authorization

[Bearer](../README.md#Bearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/problem+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **sessions_stop**
> sessions_stop(id)

Stop Session Processing

The HTTP POST request to the `/sessions/{id}/stop` endpoint stops processing of a session with the specified ID.

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
api_instance = swagger_client.SessionsApi(swagger_client.ApiClient(configuration))
id = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | Specifies the system ID assigned of a session in the Veeam Backup for Nutanix AHV.

try:
    # Stop Session Processing
    api_instance.sessions_stop(id)
except ApiException as e:
    print("Exception when calling SessionsApi->sessions_stop: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | [**str**](.md)| Specifies the system ID assigned of a session in the Veeam Backup for Nutanix AHV. | 

### Return type

void (empty response body)

### Authorization

[Bearer](../README.md#Bearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/problem+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

