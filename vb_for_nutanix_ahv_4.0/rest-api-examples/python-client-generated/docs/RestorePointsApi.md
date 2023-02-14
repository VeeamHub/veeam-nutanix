# swagger_client.RestorePointsApi

All URIs are relative to *https://172.25.124.153/*

Method | HTTP request | Description
------------- | ------------- | -------------
[**restore_points_delete_by_id**](RestorePointsApi.md#restore_points_delete_by_id) | **DELETE** /api/v4/restorePoints/{id}/delete | Delete Restore Point
[**restore_points_disk_restore**](RestorePointsApi.md#restore_points_disk_restore) | **POST** /api/v4/restorePoints/diskRestore | Perform Disk Restore
[**restore_points_get**](RestorePointsApi.md#restore_points_get) | **GET** /api/v4/restorePoints | Get VM Restore Points
[**restore_points_get_backup_by_id**](RestorePointsApi.md#restore_points_get_backup_by_id) | **GET** /api/v4/restorePoints/backups/{id} | Get Backup Data
[**restore_points_get_backup_snapshot_by_id**](RestorePointsApi.md#restore_points_get_backup_snapshot_by_id) | **GET** /api/v4/restorePoints/backupSnapshots/{id} | Get Backup Snapshot Data
[**restore_points_get_disks_from_restore_point**](RestorePointsApi.md#restore_points_get_disks_from_restore_point) | **GET** /api/v4/restorePoints/{id}/disks | Get Collection of Disks From Restore Point
[**restore_points_get_network_adapters_from_restore_point**](RestorePointsApi.md#restore_points_get_network_adapters_from_restore_point) | **GET** /api/v4/restorePoints/{id}/networkAdapters | Get Collection of Network Adapters From Restore Point
[**restore_points_get_protection_domain_snapshot_by_id**](RestorePointsApi.md#restore_points_get_protection_domain_snapshot_by_id) | **GET** /api/v4/restorePoints/protectionDomainSnapshots/{id} | Get Protection Domain Snapshot Data
[**restore_points_get_restore_point_by_id**](RestorePointsApi.md#restore_points_get_restore_point_by_id) | **GET** /api/v4/restorePoints/{id} | Get Restore Point Data
[**restore_points_get_user_snapshot_by_id**](RestorePointsApi.md#restore_points_get_user_snapshot_by_id) | **GET** /api/v4/restorePoints/userSnapshots/{id} | Get User Snapshot Data
[**restore_points_restore**](RestorePointsApi.md#restore_points_restore) | **POST** /api/v4/restorePoints/restore | Perform VM Restore

# **restore_points_delete_by_id**
> restore_points_delete_by_id(id, delete_from_server=delete_from_server)

Delete Restore Point

The HTTP DELETE request to the `/restorePoints/{id}/delete` endpoint deletes a restore point with the specified ID.

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
api_instance = swagger_client.RestorePointsApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | System ID assigned to a restore point in Veeam Backup and Replication.
delete_from_server = false # bool | Defines whether backup files will be deleted from backup repositories. (optional) (default to false)

try:
    # Delete Restore Point
    api_instance.restore_points_delete_by_id(id, delete_from_server=delete_from_server)
except ApiException as e:
    print("Exception when calling RestorePointsApi->restore_points_delete_by_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| System ID assigned to a restore point in Veeam Backup and Replication. | 
 **delete_from_server** | **bool**| Defines whether backup files will be deleted from backup repositories. | [optional] [default to false]

### Return type

void (empty response body)

### Authorization

[Bearer](../README.md#Bearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/problem+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **restore_points_disk_restore**
> AsyncTask restore_points_disk_restore(body)

Perform Disk Restore

The HTTP POST request to the /restorePoints/diskRestore endpoint performs restore of disks using the specified restore settings.

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
api_instance = swagger_client.RestorePointsApi(swagger_client.ApiClient(configuration))
body = swagger_client.DiskRestoreSettings() # DiskRestoreSettings | 

try:
    # Perform Disk Restore
    api_response = api_instance.restore_points_disk_restore(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling RestorePointsApi->restore_points_disk_restore: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**DiskRestoreSettings**](DiskRestoreSettings.md)|  | 

### Return type

[**AsyncTask**](AsyncTask.md)

### Authorization

[Bearer](../README.md#Bearer)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json, application/problem+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **restore_points_get**
> PageOfRestorePointBase restore_points_get(vm_id=vm_id, offset=offset, limit=limit, filter=filter, sort=sort)

Get VM Restore Points

The HTTP GET request to the `/restorePoints` endpoint retrieves a list of all restore points of a VM in Veeam Backup for Nutanix AHV.

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
api_instance = swagger_client.RestorePointsApi(swagger_client.ApiClient(configuration))
vm_id = 'vm_id_example' # str | ID of a protected VM assigned in the Nutanix environment. (optional)
offset = 0 # int | Excludes from a response the first N items of a resource collection. (optional) (default to 0)
limit = 100 # int | Specifies the maximum number of items of a resource collection to return in a response. (optional) (default to 100)
filter = swagger_client.FilterParameter() # FilterParameter | Specifies the criteria for items to be returned in a response. For more information, see the Veeam Backup for Nutanix AHV REST API Reference Overview, section [Filter Parameters](https://helpcenter.veeam.com/docs/van/rest/filter.html?ver=40). (optional)
sort = swagger_client.SortParameter() # SortParameter | Specifies the order of items in the response. For more information, see the Veeam Backup for Nutanix AHV REST API Reference Overview, section [Sort Parameters](https://helpcenter.veeam.com/docs/van/rest/sort.html?ver=40). (optional)

try:
    # Get VM Restore Points
    api_response = api_instance.restore_points_get(vm_id=vm_id, offset=offset, limit=limit, filter=filter, sort=sort)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling RestorePointsApi->restore_points_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **vm_id** | **str**| ID of a protected VM assigned in the Nutanix environment. | [optional] 
 **offset** | **int**| Excludes from a response the first N items of a resource collection. | [optional] [default to 0]
 **limit** | **int**| Specifies the maximum number of items of a resource collection to return in a response. | [optional] [default to 100]
 **filter** | [**FilterParameter**](.md)| Specifies the criteria for items to be returned in a response. For more information, see the Veeam Backup for Nutanix AHV REST API Reference Overview, section [Filter Parameters](https://helpcenter.veeam.com/docs/van/rest/filter.html?ver&#x3D;40). | [optional] 
 **sort** | [**SortParameter**](.md)| Specifies the order of items in the response. For more information, see the Veeam Backup for Nutanix AHV REST API Reference Overview, section [Sort Parameters](https://helpcenter.veeam.com/docs/van/rest/sort.html?ver&#x3D;40). | [optional] 

### Return type

[**PageOfRestorePointBase**](PageOfRestorePointBase.md)

### Authorization

[Bearer](../README.md#Bearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/problem+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **restore_points_get_backup_by_id**
> BackupRestorePoint restore_points_get_backup_by_id(id)

Get Backup Data

The HTTP GET request to the `/restorePoints/backups/{id}` endpoint retrieves information on a backup with the specified ID.

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
api_instance = swagger_client.RestorePointsApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | System ID assigned to a restore point in Veeam Backup and Replication.

try:
    # Get Backup Data
    api_response = api_instance.restore_points_get_backup_by_id(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling RestorePointsApi->restore_points_get_backup_by_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| System ID assigned to a restore point in Veeam Backup and Replication. | 

### Return type

[**BackupRestorePoint**](BackupRestorePoint.md)

### Authorization

[Bearer](../README.md#Bearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/problem+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **restore_points_get_backup_snapshot_by_id**
> BackupSnapshot restore_points_get_backup_snapshot_by_id(id)

Get Backup Snapshot Data

The HTTP GET request to the `/restorePoints/backupSnapshots/{id}` endpoint retrieves information on a backup snapshot with the specified ID.

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
api_instance = swagger_client.RestorePointsApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | System ID assigned to a backup snapshot in Veeam Backup and Replication.

try:
    # Get Backup Snapshot Data
    api_response = api_instance.restore_points_get_backup_snapshot_by_id(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling RestorePointsApi->restore_points_get_backup_snapshot_by_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| System ID assigned to a backup snapshot in Veeam Backup and Replication. | 

### Return type

[**BackupSnapshot**](BackupSnapshot.md)

### Authorization

[Bearer](../README.md#Bearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/problem+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **restore_points_get_disks_from_restore_point**
> list[Disk] restore_points_get_disks_from_restore_point(id)

Get Collection of Disks From Restore Point

The HTTP GET request to the `/restorePoints/{id}/disks` endpoint retrieves a list of disks from the specified VM restore point.

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
api_instance = swagger_client.RestorePointsApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | System ID assigned to a restore point in Veeam Backup and Replication.

try:
    # Get Collection of Disks From Restore Point
    api_response = api_instance.restore_points_get_disks_from_restore_point(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling RestorePointsApi->restore_points_get_disks_from_restore_point: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| System ID assigned to a restore point in Veeam Backup and Replication. | 

### Return type

[**list[Disk]**](Disk.md)

### Authorization

[Bearer](../README.md#Bearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/problem+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **restore_points_get_network_adapters_from_restore_point**
> list[NetworkAdapter] restore_points_get_network_adapters_from_restore_point(id)

Get Collection of Network Adapters From Restore Point

The HTTP GET request to the `/restorePoints/{id}/networkAdapters` endpoint retrieves a list of network adapters from metadata of a restore point with the specified ID. The information can be provided for backups and backup snapshot only.

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
api_instance = swagger_client.RestorePointsApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | System ID assigned to a restore point in Veeam Backup and Replication.

try:
    # Get Collection of Network Adapters From Restore Point
    api_response = api_instance.restore_points_get_network_adapters_from_restore_point(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling RestorePointsApi->restore_points_get_network_adapters_from_restore_point: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| System ID assigned to a restore point in Veeam Backup and Replication. | 

### Return type

[**list[NetworkAdapter]**](NetworkAdapter.md)

### Authorization

[Bearer](../README.md#Bearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/problem+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **restore_points_get_protection_domain_snapshot_by_id**
> ProtectionDomainSnapshot restore_points_get_protection_domain_snapshot_by_id(id)

Get Protection Domain Snapshot Data

The HTTP GET request to the `/restorePoints/protectionDomainSnapshots/{id}` endpoint retrieves information on a protection domain snapshot with the specified ID.

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
api_instance = swagger_client.RestorePointsApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | System ID assigned to a protection domain snapshot in Nutanix AHV environment.

try:
    # Get Protection Domain Snapshot Data
    api_response = api_instance.restore_points_get_protection_domain_snapshot_by_id(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling RestorePointsApi->restore_points_get_protection_domain_snapshot_by_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| System ID assigned to a protection domain snapshot in Nutanix AHV environment. | 

### Return type

[**ProtectionDomainSnapshot**](ProtectionDomainSnapshot.md)

### Authorization

[Bearer](../README.md#Bearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/problem+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **restore_points_get_restore_point_by_id**
> RestorePointBase restore_points_get_restore_point_by_id(id)

Get Restore Point Data

The HTTP GET request to the `/restorePoints/{id}` endpoint retrieves information on a restore point with the specified ID.

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
api_instance = swagger_client.RestorePointsApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | System ID assigned to a restore point in Veeam Backup and Replication.

try:
    # Get Restore Point Data
    api_response = api_instance.restore_points_get_restore_point_by_id(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling RestorePointsApi->restore_points_get_restore_point_by_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| System ID assigned to a restore point in Veeam Backup and Replication. | 

### Return type

[**RestorePointBase**](RestorePointBase.md)

### Authorization

[Bearer](../README.md#Bearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/problem+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **restore_points_get_user_snapshot_by_id**
> UserSnapshot restore_points_get_user_snapshot_by_id(id)

Get User Snapshot Data

The HTTP GET request to the `/restorePoints/userSnapshots/{id}` endpoint retrieves information on a user snapshot with the specified ID.

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
api_instance = swagger_client.RestorePointsApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | System ID assigned to a user snapshot in Nutanix AHV environment.

try:
    # Get User Snapshot Data
    api_response = api_instance.restore_points_get_user_snapshot_by_id(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling RestorePointsApi->restore_points_get_user_snapshot_by_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| System ID assigned to a user snapshot in Nutanix AHV environment. | 

### Return type

[**UserSnapshot**](UserSnapshot.md)

### Authorization

[Bearer](../README.md#Bearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/problem+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **restore_points_restore**
> AsyncTask restore_points_restore(body)

Perform VM Restore

The HTTP POST request to the `/restorePoints/restore` endpoint performs restore of an entire VM from a restore point.

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
api_instance = swagger_client.RestorePointsApi(swagger_client.ApiClient(configuration))
body = swagger_client.RestoreSettings() # RestoreSettings | 

try:
    # Perform VM Restore
    api_response = api_instance.restore_points_restore(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling RestorePointsApi->restore_points_restore: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**RestoreSettings**](RestoreSettings.md)|  | 

### Return type

[**AsyncTask**](AsyncTask.md)

### Authorization

[Bearer](../README.md#Bearer)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json, application/problem+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

