# swagger_client.BackupServersApi

All URIs are relative to *https://172.25.124.153/*

Method | HTTP request | Description
------------- | ------------- | -------------
[**backup_servers_get**](BackupServersApi.md#backup_servers_get) | **GET** /api/v4/backupServer | Get Backup Server Data
[**backup_servers_get_repositories**](BackupServersApi.md#backup_servers_get_repositories) | **GET** /api/v4/backupServer/repositories | Get Collection of Backup Repositories
[**backup_servers_get_repository_by_id**](BackupServersApi.md#backup_servers_get_repository_by_id) | **GET** /api/v4/backupServer/repositories/{id} | Get Backup Repository Data
[**backup_servers_rescan_backups**](BackupServersApi.md#backup_servers_rescan_backups) | **POST** /api/v4/backupServer/rescanBackups | Rescan Nutanix AHV Backups

# **backup_servers_get**
> BackupServer backup_servers_get()

Get Backup Server Data

The HTTP GET request to the `/backupServer` endpoint retrieves information on the Veeam Backup & Replication server that manages the backup appliance.

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
api_instance = swagger_client.BackupServersApi(swagger_client.ApiClient(configuration))

try:
    # Get Backup Server Data
    api_response = api_instance.backup_servers_get()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling BackupServersApi->backup_servers_get: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**BackupServer**](BackupServer.md)

### Authorization

[Bearer](../README.md#Bearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/problem+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **backup_servers_get_repositories**
> PageOfBackupRepository backup_servers_get_repositories(offset=offset, limit=limit, filter=filter, sort=sort)

Get Collection of Backup Repositories

The HTTP GET request to the `/repositories` endpoint retrieves a list of backup repositories to which the backup appliance has access.

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
api_instance = swagger_client.BackupServersApi(swagger_client.ApiClient(configuration))
offset = 0 # int | Excludes from a response the first N items of a resource collection. (optional) (default to 0)
limit = 100 # int | Specifies the maximum number of items of a resource collection to return in a response. (optional) (default to 100)
filter = swagger_client.FilterParameter() # FilterParameter | Specifies the criteria for items to be returned in a response. For more information, see the Veeam Backup for Nutanix AHV REST API Reference Overview, section [Filter Parameters](https://helpcenter.veeam.com/docs/van/rest/filter.html?ver=40). (optional)
sort = swagger_client.SortParameter() # SortParameter | Specifies the order of items in the response. For more information, see the Veeam Backup for Nutanix AHV REST API Reference Overview, section [Sort Parameter](https://helpcenter.veeam.com/docs/van/rest/sort.html?ver=40). (optional)

try:
    # Get Collection of Backup Repositories
    api_response = api_instance.backup_servers_get_repositories(offset=offset, limit=limit, filter=filter, sort=sort)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling BackupServersApi->backup_servers_get_repositories: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **offset** | **int**| Excludes from a response the first N items of a resource collection. | [optional] [default to 0]
 **limit** | **int**| Specifies the maximum number of items of a resource collection to return in a response. | [optional] [default to 100]
 **filter** | [**FilterParameter**](.md)| Specifies the criteria for items to be returned in a response. For more information, see the Veeam Backup for Nutanix AHV REST API Reference Overview, section [Filter Parameters](https://helpcenter.veeam.com/docs/van/rest/filter.html?ver&#x3D;40). | [optional] 
 **sort** | [**SortParameter**](.md)| Specifies the order of items in the response. For more information, see the Veeam Backup for Nutanix AHV REST API Reference Overview, section [Sort Parameter](https://helpcenter.veeam.com/docs/van/rest/sort.html?ver&#x3D;40). | [optional] 

### Return type

[**PageOfBackupRepository**](PageOfBackupRepository.md)

### Authorization

[Bearer](../README.md#Bearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/problem+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **backup_servers_get_repository_by_id**
> BackupRepository backup_servers_get_repository_by_id(id)

Get Backup Repository Data

The HTTP GET request to the `/repositories/{id}` endpoint retrieves information on a backup repository with the specified ID.

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
api_instance = swagger_client.BackupServersApi(swagger_client.ApiClient(configuration))
id = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | Specifies the ID assigned to a backup repository in Veeam Backup for Nutanix AHV.

try:
    # Get Backup Repository Data
    api_response = api_instance.backup_servers_get_repository_by_id(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling BackupServersApi->backup_servers_get_repository_by_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | [**str**](.md)| Specifies the ID assigned to a backup repository in Veeam Backup for Nutanix AHV. | 

### Return type

[**BackupRepository**](BackupRepository.md)

### Authorization

[Bearer](../README.md#Bearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/problem+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **backup_servers_rescan_backups**
> AsyncTask backup_servers_rescan_backups()

Rescan Nutanix AHV Backups

The HTTP POST request to the `/backupServer/rescanBackups` endpoint allows you to scan Veeam Backup & Replication repositories and to update information on available Nutanix AHV backups in the backup appliance configuration database.

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
api_instance = swagger_client.BackupServersApi(swagger_client.ApiClient(configuration))

try:
    # Rescan Nutanix AHV Backups
    api_response = api_instance.backup_servers_rescan_backups()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling BackupServersApi->backup_servers_rescan_backups: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**AsyncTask**](AsyncTask.md)

### Authorization

[Bearer](../README.md#Bearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/problem+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

