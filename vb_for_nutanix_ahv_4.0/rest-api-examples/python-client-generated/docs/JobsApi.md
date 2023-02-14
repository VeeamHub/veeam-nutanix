# swagger_client.JobsApi

All URIs are relative to *https://172.25.124.153/*

Method | HTTP request | Description
------------- | ------------- | -------------
[**jobs_add**](JobsApi.md#jobs_add) | **POST** /api/v4/jobs | Create Backup job
[**jobs_delete**](JobsApi.md#jobs_delete) | **DELETE** /api/v4/jobs/{id} | Delete Job
[**jobs_disable**](JobsApi.md#jobs_disable) | **POST** /api/v4/jobs/{id}/disable | Disable Job
[**jobs_enable**](JobsApi.md#jobs_enable) | **POST** /api/v4/jobs/{id}/enable | Enable Job
[**jobs_get_by_id**](JobsApi.md#jobs_get_by_id) | **GET** /api/v4/jobs/{id} | Get Job Data
[**jobs_get_page**](JobsApi.md#jobs_get_page) | **GET** /api/v4/jobs | Get Collection of Jobs
[**jobs_get_settings**](JobsApi.md#jobs_get_settings) | **GET** /api/v4/jobs/{id}/settings | Get Job Setting
[**jobs_start**](JobsApi.md#jobs_start) | **POST** /api/v4/jobs/{id}/start | Starts Job
[**jobs_stop**](JobsApi.md#jobs_stop) | **POST** /api/v4/jobs/{id}/stop | Stop Job
[**jobs_update_settings**](JobsApi.md#jobs_update_settings) | **PUT** /api/v4/jobs/{id}/settings | Modify Job Settings

# **jobs_add**
> JobsAddResponse jobs_add(body)

Create Backup job

The HTTP POST request to the `/jobs` endpoint creates a new job.

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
api_instance = swagger_client.JobsApi(swagger_client.ApiClient(configuration))
body = swagger_client.JobSettings() # JobSettings | Backup job Object

try:
    # Create Backup job
    api_response = api_instance.jobs_add(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling JobsApi->jobs_add: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**JobSettings**](JobSettings.md)| Backup job Object | 

### Return type

[**JobsAddResponse**](JobsAddResponse.md)

### Authorization

[Bearer](../README.md#Bearer)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json, application/problem+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **jobs_delete**
> jobs_delete(id)

Delete Job

The HTTP DELETE request to the `/jobs/{id}` endpoint deletes a job with the specified ID.

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
api_instance = swagger_client.JobsApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | iSystem ID assigned to a job in Veeam Backup for Nutanix AHV.

try:
    # Delete Job
    api_instance.jobs_delete(id)
except ApiException as e:
    print("Exception when calling JobsApi->jobs_delete: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| iSystem ID assigned to a job in Veeam Backup for Nutanix AHV. | 

### Return type

void (empty response body)

### Authorization

[Bearer](../README.md#Bearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/problem+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **jobs_disable**
> jobs_disable(id)

Disable Job

The HTTP POST request to the `/jobs/{id}/disable` endpoint disables an enabled job with the specified ID.

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
api_instance = swagger_client.JobsApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | System ID assigned to a job in Veeam Backup for Nutanix AHV.

try:
    # Disable Job
    api_instance.jobs_disable(id)
except ApiException as e:
    print("Exception when calling JobsApi->jobs_disable: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| System ID assigned to a job in Veeam Backup for Nutanix AHV. | 

### Return type

void (empty response body)

### Authorization

[Bearer](../README.md#Bearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/problem+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **jobs_enable**
> jobs_enable(id)

Enable Job

The HTTP POST request to the `/jobs/{id}/enable` endpoint enables a disabled job with the specified ID.

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
api_instance = swagger_client.JobsApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | System ID assigned to a job in Veeam Backup for Nutanix AHV.

try:
    # Enable Job
    api_instance.jobs_enable(id)
except ApiException as e:
    print("Exception when calling JobsApi->jobs_enable: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| System ID assigned to a job in Veeam Backup for Nutanix AHV. | 

### Return type

void (empty response body)

### Authorization

[Bearer](../README.md#Bearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/problem+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **jobs_get_by_id**
> Job jobs_get_by_id(id)

Get Job Data

The HTTP GET request to the `/jobs/{id}` endpoint retrieves configuration of a job with the specified ID.

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
api_instance = swagger_client.JobsApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | System ID assigned to a job in Veeam Backup for Nutanix AHV.

try:
    # Get Job Data
    api_response = api_instance.jobs_get_by_id(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling JobsApi->jobs_get_by_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| System ID assigned to a job in Veeam Backup for Nutanix AHV. | 

### Return type

[**Job**](Job.md)

### Authorization

[Bearer](../README.md#Bearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/problem+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **jobs_get_page**
> PageOfJob jobs_get_page(offset=offset, limit=limit, filter=filter, sort=sort)

Get Collection of Jobs

The HTTP GET request to the `/jobs` endpoint retrieves a list of all jobs created in Veeam Backup for Nutanix AHV.

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
api_instance = swagger_client.JobsApi(swagger_client.ApiClient(configuration))
offset = 0 # int | Excludes from a response the first N items of a resource collection. (optional) (default to 0)
limit = 100 # int | Specifies the maximum number of items of a resource collection to return in a response. (optional) (default to 100)
filter = swagger_client.FilterParameter() # FilterParameter | Specifies the criteria for items to be returned in a response. For more information, see the Veeam Backup for Nutanix AHV REST API Reference Overview, section [Filter Parameters](https://helpcenter.veeam.com/docs/van/rest/filter.html?ver=40). (optional)
sort = swagger_client.SortParameter() # SortParameter | Specifies the order of items in the response. For more information, see the Veeam Backup for Nutanix AHV REST API Reference Overview, section [Sort Parameters](https://helpcenter.veeam.com/docs/van/rest/sort.html?ver=40). (optional)

try:
    # Get Collection of Jobs
    api_response = api_instance.jobs_get_page(offset=offset, limit=limit, filter=filter, sort=sort)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling JobsApi->jobs_get_page: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **offset** | **int**| Excludes from a response the first N items of a resource collection. | [optional] [default to 0]
 **limit** | **int**| Specifies the maximum number of items of a resource collection to return in a response. | [optional] [default to 100]
 **filter** | [**FilterParameter**](.md)| Specifies the criteria for items to be returned in a response. For more information, see the Veeam Backup for Nutanix AHV REST API Reference Overview, section [Filter Parameters](https://helpcenter.veeam.com/docs/van/rest/filter.html?ver&#x3D;40). | [optional] 
 **sort** | [**SortParameter**](.md)| Specifies the order of items in the response. For more information, see the Veeam Backup for Nutanix AHV REST API Reference Overview, section [Sort Parameters](https://helpcenter.veeam.com/docs/van/rest/sort.html?ver&#x3D;40). | [optional] 

### Return type

[**PageOfJob**](PageOfJob.md)

### Authorization

[Bearer](../README.md#Bearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/problem+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **jobs_get_settings**
> JobSettings jobs_get_settings(id)

Get Job Setting

The HTTP POST request to the `/jobs/{id}/settings` endpoint retrieves settings of a job with the specified ID.

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
api_instance = swagger_client.JobsApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | System ID assigned to a job in Veeam Backup for Nutanix AHV.

try:
    # Get Job Setting
    api_response = api_instance.jobs_get_settings(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling JobsApi->jobs_get_settings: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| System ID assigned to a job in Veeam Backup for Nutanix AHV. | 

### Return type

[**JobSettings**](JobSettings.md)

### Authorization

[Bearer](../README.md#Bearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/problem+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **jobs_start**
> AsyncTask jobs_start(id, backup_mode=backup_mode)

Starts Job

The HTTP POST request to the `/jobs/{id}/start` endpoint launches a job with the specified ID.

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
api_instance = swagger_client.JobsApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | System ID assigned to a job in Veeam Backup for Nutanix AHV.
backup_mode = swagger_client.BackupMode() # BackupMode | Specifies the backup type (active full or incremental). If the parameter value is not defined or is set to **unknown**, an incremental backup is created. If an incremental backup cannot be created or an active full backup is scheduled on this day, an active full backup will be created even if you start an incremental run. (optional)

try:
    # Starts Job
    api_response = api_instance.jobs_start(id, backup_mode=backup_mode)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling JobsApi->jobs_start: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| System ID assigned to a job in Veeam Backup for Nutanix AHV. | 
 **backup_mode** | [**BackupMode**](.md)| Specifies the backup type (active full or incremental). If the parameter value is not defined or is set to **unknown**, an incremental backup is created. If an incremental backup cannot be created or an active full backup is scheduled on this day, an active full backup will be created even if you start an incremental run. | [optional] 

### Return type

[**AsyncTask**](AsyncTask.md)

### Authorization

[Bearer](../README.md#Bearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/problem+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **jobs_stop**
> jobs_stop(id)

Stop Job

The HTTP POST request to the `/jobs/{id}/stop` endpoint stops execution of a job with the specified ID.

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
api_instance = swagger_client.JobsApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | System ID assigned to a job in Veeam Backup for Nutanix AHV.

try:
    # Stop Job
    api_instance.jobs_stop(id)
except ApiException as e:
    print("Exception when calling JobsApi->jobs_stop: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| System ID assigned to a job in Veeam Backup for Nutanix AHV. | 

### Return type

void (empty response body)

### Authorization

[Bearer](../README.md#Bearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/problem+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **jobs_update_settings**
> jobs_update_settings(body, id)

Modify Job Settings

The HTTP PUT request to the `/jobs/{id}/settings` endpoint updates settings of a job with the specified ID.

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
api_instance = swagger_client.JobsApi(swagger_client.ApiClient(configuration))
body = swagger_client.JobSettings() # JobSettings | Specifies job settings.
id = 'id_example' # str | System ID assigned to a job in Veeam Backup for Nutanix AHV.

try:
    # Modify Job Settings
    api_instance.jobs_update_settings(body, id)
except ApiException as e:
    print("Exception when calling JobsApi->jobs_update_settings: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**JobSettings**](JobSettings.md)| Specifies job settings. | 
 **id** | **str**| System ID assigned to a job in Veeam Backup for Nutanix AHV. | 

### Return type

void (empty response body)

### Authorization

[Bearer](../README.md#Bearer)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/problem+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

