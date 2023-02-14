# swagger_client.ClustersApi

All URIs are relative to *https://172.25.124.153/*

Method | HTTP request | Description
------------- | ------------- | -------------
[**clusters_get**](ClustersApi.md#clusters_get) | **GET** /api/v4/clusters | Get Collection of Nutanix AHV Clusters
[**clusters_get_auto_protection**](ClustersApi.md#clusters_get_auto_protection) | **GET** /api/v4/clusters/{id}/autoProtection | Get Cluster Auto-Protection Settings
[**clusters_get_by_id**](ClustersApi.md#clusters_get_by_id) | **GET** /api/v4/clusters/{id} | Get Nutanix AHV Cluster Data
[**clusters_get_networks**](ClustersApi.md#clusters_get_networks) | **GET** /api/v4/clusters/{id}/networks | Get Collection of Networks
[**clusters_get_pds**](ClustersApi.md#clusters_get_pds) | **GET** /api/v4/clusters/{id}/protectionDomains | Get Collection of Protection Domains
[**clusters_get_storage_containers**](ClustersApi.md#clusters_get_storage_containers) | **GET** /api/v4/clusters/{id}/storageContainers | Get Collection of Storage Containers
[**clusters_get_vm_by_id**](ClustersApi.md#clusters_get_vm_by_id) | **GET** /api/v4/clusters/{id}/vms/{vmId} | Get Virtual Machine Data
[**clusters_get_vms**](ClustersApi.md#clusters_get_vms) | **GET** /api/v4/clusters/{id}/vms | Get Collection of Virtual Machines
[**clusters_get_volume_group_by_id**](ClustersApi.md#clusters_get_volume_group_by_id) | **GET** /api/v4/clusters/{id}/volumeGroups/{volumeGroupId} | Get Volume Group Data
[**clusters_get_volume_groups**](ClustersApi.md#clusters_get_volume_groups) | **GET** /api/v4/clusters/{id}/volumeGroups | Get Collection of Volume Groups in Cluster
[**clusters_refresh_pds_async**](ClustersApi.md#clusters_refresh_pds_async) | **POST** /api/v4/clusters/{id}/protectionDomains/refresh | Infrastructure Rescan for Protection Domains
[**clusters_refresh_vms_async**](ClustersApi.md#clusters_refresh_vms_async) | **POST** /api/v4/clusters/{id}/vms/refreshAsync | Infrastructure Rescan for Virtual Machines
[**clusters_refresh_volume_groups**](ClustersApi.md#clusters_refresh_volume_groups) | **POST** /api/v4/clusters/{id}/volumeGroups/refresh | Infrastructure Rescan for Volume Groups
[**clusters_rescan_snapshots**](ClustersApi.md#clusters_rescan_snapshots) | **POST** /api/v4/clusters/{id}/rescanSnapshots | Cluster Rescan for Snapshots
[**clusters_update_auto_protection_settings**](ClustersApi.md#clusters_update_auto_protection_settings) | **PUT** /api/v4/clusters/{id}/autoProtection | Modify Cluster Auto-Protection Settings

# **clusters_get**
> list[Cluster] clusters_get()

Get Collection of Nutanix AHV Clusters

The HTTP GET request to the `/clusters` endpoint retrieves information on Nutanix AHV clusters to which the backup appliance has access.

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
api_instance = swagger_client.ClustersApi(swagger_client.ApiClient(configuration))

try:
    # Get Collection of Nutanix AHV Clusters
    api_response = api_instance.clusters_get()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ClustersApi->clusters_get: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**list[Cluster]**](Cluster.md)

### Authorization

[Bearer](../README.md#Bearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/problem+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **clusters_get_auto_protection**
> AutoProtectionSettings clusters_get_auto_protection(id)

Get Cluster Auto-Protection Settings

The HTTP GET request to the `/clusters/{id}/autoProtection` endpoint retrieves auto-protection settings configured for the specified cluster.

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
api_instance = swagger_client.ClustersApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | Specifies the ID assigned to a cluster in the Nutanix AHV environment. To learn the ID, [get a collection of Nutanix AHV clusters](#tag/Clusters/operation/Clusters_Get) to which the backup appliance has access.

try:
    # Get Cluster Auto-Protection Settings
    api_response = api_instance.clusters_get_auto_protection(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ClustersApi->clusters_get_auto_protection: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Specifies the ID assigned to a cluster in the Nutanix AHV environment. To learn the ID, [get a collection of Nutanix AHV clusters](#tag/Clusters/operation/Clusters_Get) to which the backup appliance has access. | 

### Return type

[**AutoProtectionSettings**](AutoProtectionSettings.md)

### Authorization

[Bearer](../README.md#Bearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/problem+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **clusters_get_by_id**
> Cluster clusters_get_by_id(id)

Get Nutanix AHV Cluster Data

The HTTP GET request to the `/clusters/{id}` endpoint retrieves information on a Nutanix AHV cluster with the specified ID.

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
api_instance = swagger_client.ClustersApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | Specifies the ID assigned to a cluster in the Nutanix AHV environment. To learn the ID, [get a collection of Nutanix AHV clusters](#tag/Clusters/operation/Clusters_Get) to which the backup appliance has access.

try:
    # Get Nutanix AHV Cluster Data
    api_response = api_instance.clusters_get_by_id(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ClustersApi->clusters_get_by_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Specifies the ID assigned to a cluster in the Nutanix AHV environment. To learn the ID, [get a collection of Nutanix AHV clusters](#tag/Clusters/operation/Clusters_Get) to which the backup appliance has access. | 

### Return type

[**Cluster**](Cluster.md)

### Authorization

[Bearer](../README.md#Bearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/problem+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **clusters_get_networks**
> list[NutanixNetwork] clusters_get_networks(id)

Get Collection of Networks

The HTTP GET request to the `/clusters/{id}/networks` endpoint retrieves a list of all networks configured in the specified Nutanix AHV cluster.

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
api_instance = swagger_client.ClustersApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | Specifies the ID assigned to a cluster in the Nutanix AHV environment. To learn the ID, [get a collection of Nutanix AHV clusters](#tag/Clusters/operation/Clusters_Get) to which the backup appliance has access.

try:
    # Get Collection of Networks
    api_response = api_instance.clusters_get_networks(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ClustersApi->clusters_get_networks: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Specifies the ID assigned to a cluster in the Nutanix AHV environment. To learn the ID, [get a collection of Nutanix AHV clusters](#tag/Clusters/operation/Clusters_Get) to which the backup appliance has access. | 

### Return type

[**list[NutanixNetwork]**](NutanixNetwork.md)

### Authorization

[Bearer](../README.md#Bearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/problem+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **clusters_get_pds**
> PageOfProtectionDomain clusters_get_pds(id, offset=offset, limit=limit, filter=filter, sort=sort)

Get Collection of Protection Domains

The HTTP GET request to the `/clusters/{id}/protectionDomains` endpoint retrieves a list of all protection domains configured in the specified Nutanix AHV Cluster.

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
api_instance = swagger_client.ClustersApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | Specifies the ID assigned to a cluster in the Nutanix AHV environment. To learn the ID, [get a collection of Nutanix AHV clusters](#tag/Clusters/operation/Clusters_Get) to which the backup appliance has access.
offset = 0 # int | Excludes from a response the first N items of a resource collection. (optional) (default to 0)
limit = 100 # int | Specifies the maximum number of items of a resource collection to return in a response. (optional) (default to 100)
filter = swagger_client.FilterParameter() # FilterParameter | Specifies the criteria for items to be returned in a response. For more information, see the Veeam Backup for Nutanix AHV REST API Reference Overview, section [Filter Parameters](https://helpcenter.veeam.com/docs/van/rest/filter.html?ver=40). (optional)
sort = swagger_client.SortParameter() # SortParameter | Specifies the order of items in the response. For more information, see the Veeam Backup for Nutanix AHV REST API Reference Overview, section [Sort Parameters](https://helpcenter.veeam.com/docs/van/rest/sort.html?ver=40). (optional)

try:
    # Get Collection of Protection Domains
    api_response = api_instance.clusters_get_pds(id, offset=offset, limit=limit, filter=filter, sort=sort)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ClustersApi->clusters_get_pds: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Specifies the ID assigned to a cluster in the Nutanix AHV environment. To learn the ID, [get a collection of Nutanix AHV clusters](#tag/Clusters/operation/Clusters_Get) to which the backup appliance has access. | 
 **offset** | **int**| Excludes from a response the first N items of a resource collection. | [optional] [default to 0]
 **limit** | **int**| Specifies the maximum number of items of a resource collection to return in a response. | [optional] [default to 100]
 **filter** | [**FilterParameter**](.md)| Specifies the criteria for items to be returned in a response. For more information, see the Veeam Backup for Nutanix AHV REST API Reference Overview, section [Filter Parameters](https://helpcenter.veeam.com/docs/van/rest/filter.html?ver&#x3D;40). | [optional] 
 **sort** | [**SortParameter**](.md)| Specifies the order of items in the response. For more information, see the Veeam Backup for Nutanix AHV REST API Reference Overview, section [Sort Parameters](https://helpcenter.veeam.com/docs/van/rest/sort.html?ver&#x3D;40). | [optional] 

### Return type

[**PageOfProtectionDomain**](PageOfProtectionDomain.md)

### Authorization

[Bearer](../README.md#Bearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/problem+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **clusters_get_storage_containers**
> PageOfStorageContainer clusters_get_storage_containers(id, offset=offset, limit=limit, filter=filter, sort=sort)

Get Collection of Storage Containers

The HTTP GET request to the `/clusters/{id}/storageContainers` endpoint retrieves a list of all storage containers configured in the specified Nutanix AHV cluster.

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
api_instance = swagger_client.ClustersApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | Specifies the ID assigned to a cluster in the Nutanix AHV environment. To learn the ID, [get a collection of Nutanix AHV clusters](#tag/Clusters/operation/Clusters_Get) to which the backup appliance has access.
offset = 0 # int | Excludes from a response the first N items of a resource collection. (optional) (default to 0)
limit = 100 # int | Specifies the maximum number of items of a resource collection to return in a response. (optional) (default to 100)
filter = swagger_client.FilterParameter() # FilterParameter | Specifies the criteria for items to be returned in a response. For more information, see the Veeam Backup for Nutanix AHV REST API Reference Overview, section [Filter Parameters](https://helpcenter.veeam.com/docs/van/rest/filter.html?ver=40). (optional)
sort = swagger_client.SortParameter() # SortParameter | Specifies the order of items in the response. For more information, see the Veeam Backup for Nutanix AHV REST API Reference Overview, section [Sort Parameters](https://helpcenter.veeam.com/docs/van/rest/sort.html?ver=40). (optional)

try:
    # Get Collection of Storage Containers
    api_response = api_instance.clusters_get_storage_containers(id, offset=offset, limit=limit, filter=filter, sort=sort)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ClustersApi->clusters_get_storage_containers: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Specifies the ID assigned to a cluster in the Nutanix AHV environment. To learn the ID, [get a collection of Nutanix AHV clusters](#tag/Clusters/operation/Clusters_Get) to which the backup appliance has access. | 
 **offset** | **int**| Excludes from a response the first N items of a resource collection. | [optional] [default to 0]
 **limit** | **int**| Specifies the maximum number of items of a resource collection to return in a response. | [optional] [default to 100]
 **filter** | [**FilterParameter**](.md)| Specifies the criteria for items to be returned in a response. For more information, see the Veeam Backup for Nutanix AHV REST API Reference Overview, section [Filter Parameters](https://helpcenter.veeam.com/docs/van/rest/filter.html?ver&#x3D;40). | [optional] 
 **sort** | [**SortParameter**](.md)| Specifies the order of items in the response. For more information, see the Veeam Backup for Nutanix AHV REST API Reference Overview, section [Sort Parameters](https://helpcenter.veeam.com/docs/van/rest/sort.html?ver&#x3D;40). | [optional] 

### Return type

[**PageOfStorageContainer**](PageOfStorageContainer.md)

### Authorization

[Bearer](../README.md#Bearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/problem+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **clusters_get_vm_by_id**
> VirtualMachine clusters_get_vm_by_id(id, vm_id)

Get Virtual Machine Data

The HTTP GET request to the `/clusters/{id}/vms/{vmId}` endpoint retrieves information on a VM with the specified ID.

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
api_instance = swagger_client.ClustersApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | Specifies the ID assigned to a cluster in the Nutanix AHV environment. To learn the ID, [get a collection of Nutanix AHV clusters](#tag/Clusters/operation/Clusters_Get) to which the backup appliance has access.
vm_id = 'vm_id_example' # str | Specifies the ID assigned to a VM that belongs to the specified cluster.

try:
    # Get Virtual Machine Data
    api_response = api_instance.clusters_get_vm_by_id(id, vm_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ClustersApi->clusters_get_vm_by_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Specifies the ID assigned to a cluster in the Nutanix AHV environment. To learn the ID, [get a collection of Nutanix AHV clusters](#tag/Clusters/operation/Clusters_Get) to which the backup appliance has access. | 
 **vm_id** | **str**| Specifies the ID assigned to a VM that belongs to the specified cluster. | 

### Return type

[**VirtualMachine**](VirtualMachine.md)

### Authorization

[Bearer](../README.md#Bearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/problem+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **clusters_get_vms**
> PageOfVirtualMachine clusters_get_vms(id, offset=offset, limit=limit, filter=filter, sort=sort)

Get Collection of Virtual Machines

The HTTP GET request to the `/virtualMachines` endpoint retrieves a list of all virtual machines residing on a specified cluster.

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
api_instance = swagger_client.ClustersApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | Specifies the ID assigned to a cluster in the Nutanix AHV environment. To learn the ID, [get a collection of Nutanix AHV clusters](#tag/Clusters/operation/Clusters_Get) to which the backup appliance has access.
offset = 0 # int | Excludes from a response the first N items of a resource collection. (optional) (default to 0)
limit = 100 # int | Specifies the maximum number of items of a resource collection to return in a response. (optional) (default to 100)
filter = swagger_client.FilterParameter() # FilterParameter | Specifies the criteria for items to be returned in a response. For more information, see the Veeam Backup for Nutanix AHV REST API Reference Overview, section [Filter Parameters](https://helpcenter.veeam.com/docs/van/rest/filter.html?ver=40). (optional)
sort = swagger_client.SortParameter() # SortParameter | Specifies the order of items in the response. For more information, see the Veeam Backup for Nutanix AHV REST API Reference Overview, section [Sort Parameter](https://helpcenter.veeam.com/docs/van/rest/sort.html?ver=40). (optional)

try:
    # Get Collection of Virtual Machines
    api_response = api_instance.clusters_get_vms(id, offset=offset, limit=limit, filter=filter, sort=sort)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ClustersApi->clusters_get_vms: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Specifies the ID assigned to a cluster in the Nutanix AHV environment. To learn the ID, [get a collection of Nutanix AHV clusters](#tag/Clusters/operation/Clusters_Get) to which the backup appliance has access. | 
 **offset** | **int**| Excludes from a response the first N items of a resource collection. | [optional] [default to 0]
 **limit** | **int**| Specifies the maximum number of items of a resource collection to return in a response. | [optional] [default to 100]
 **filter** | [**FilterParameter**](.md)| Specifies the criteria for items to be returned in a response. For more information, see the Veeam Backup for Nutanix AHV REST API Reference Overview, section [Filter Parameters](https://helpcenter.veeam.com/docs/van/rest/filter.html?ver&#x3D;40). | [optional] 
 **sort** | [**SortParameter**](.md)| Specifies the order of items in the response. For more information, see the Veeam Backup for Nutanix AHV REST API Reference Overview, section [Sort Parameter](https://helpcenter.veeam.com/docs/van/rest/sort.html?ver&#x3D;40). | [optional] 

### Return type

[**PageOfVirtualMachine**](PageOfVirtualMachine.md)

### Authorization

[Bearer](../README.md#Bearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/problem+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **clusters_get_volume_group_by_id**
> VolumeGroup clusters_get_volume_group_by_id(id, volume_group_id)

Get Volume Group Data

The HTTP GET request to the `/clusters/{id}/volumeGroups/{volumeGroupId}` endpoint retrieves information on a volume group in the specified cluster.

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
api_instance = swagger_client.ClustersApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | Specifies the ID assigned to a cluster in the Nutanix AHV environment. To learn the ID, [get a collection of Nutanix AHV clusters](#tag/Clusters/operation/Clusters_Get) to which the backup appliance has access.
volume_group_id = 'volume_group_id_example' # str | Specifies the ID assigned to a volume group in the Nutanix AHV environment.

try:
    # Get Volume Group Data
    api_response = api_instance.clusters_get_volume_group_by_id(id, volume_group_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ClustersApi->clusters_get_volume_group_by_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Specifies the ID assigned to a cluster in the Nutanix AHV environment. To learn the ID, [get a collection of Nutanix AHV clusters](#tag/Clusters/operation/Clusters_Get) to which the backup appliance has access. | 
 **volume_group_id** | **str**| Specifies the ID assigned to a volume group in the Nutanix AHV environment. | 

### Return type

[**VolumeGroup**](VolumeGroup.md)

### Authorization

[Bearer](../README.md#Bearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/problem+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **clusters_get_volume_groups**
> list[VolumeGroup] clusters_get_volume_groups(id)

Get Collection of Volume Groups in Cluster

The HTTP GET request to the `/clusters/{id}/volumeGroups` endpoint retrieves a list of all volume groups configured in the specified Nutanix AHV cluster.

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
api_instance = swagger_client.ClustersApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | Specifies the ID assigned to a cluster in the Nutanix AHV environment. To learn the ID, [get a collection of Nutanix AHV clusters](#tag/Clusters/operation/Clusters_Get) to which the backup appliance has access.

try:
    # Get Collection of Volume Groups in Cluster
    api_response = api_instance.clusters_get_volume_groups(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ClustersApi->clusters_get_volume_groups: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Specifies the ID assigned to a cluster in the Nutanix AHV environment. To learn the ID, [get a collection of Nutanix AHV clusters](#tag/Clusters/operation/Clusters_Get) to which the backup appliance has access. | 

### Return type

[**list[VolumeGroup]**](VolumeGroup.md)

### Authorization

[Bearer](../README.md#Bearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/problem+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **clusters_refresh_pds_async**
> clusters_refresh_pds_async(id)

Infrastructure Rescan for Protection Domains

The HTTP POST request to the `/clusters/{id}/protectionDomains/refresh` endpoint runs the infrastructure rescanning operation for protection domains.

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
api_instance = swagger_client.ClustersApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | Specifies the ID assigned to a cluster in the Nutanix AHV environment. To learn the ID, [get a collection of Nutanix AHV clusters](#tag/Clusters/operation/Clusters_Get) to which the backup appliance has access.

try:
    # Infrastructure Rescan for Protection Domains
    api_instance.clusters_refresh_pds_async(id)
except ApiException as e:
    print("Exception when calling ClustersApi->clusters_refresh_pds_async: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Specifies the ID assigned to a cluster in the Nutanix AHV environment. To learn the ID, [get a collection of Nutanix AHV clusters](#tag/Clusters/operation/Clusters_Get) to which the backup appliance has access. | 

### Return type

void (empty response body)

### Authorization

[Bearer](../README.md#Bearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/problem+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **clusters_refresh_vms_async**
> AsyncTask clusters_refresh_vms_async(id)

Infrastructure Rescan for Virtual Machines

The HTTP POST request to the `/clusters/{id}/vms/refreshAsync` endpoint runs the infrastructure rescanning operation for virtual machines.

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
api_instance = swagger_client.ClustersApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | Specifies the ID assigned to a cluster in the Nutanix AHV environment. To learn the ID, [get a collection of Nutanix AHV clusters](#tag/Clusters/operation/Clusters_Get) to which the backup appliance has access.

try:
    # Infrastructure Rescan for Virtual Machines
    api_response = api_instance.clusters_refresh_vms_async(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ClustersApi->clusters_refresh_vms_async: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Specifies the ID assigned to a cluster in the Nutanix AHV environment. To learn the ID, [get a collection of Nutanix AHV clusters](#tag/Clusters/operation/Clusters_Get) to which the backup appliance has access. | 

### Return type

[**AsyncTask**](AsyncTask.md)

### Authorization

[Bearer](../README.md#Bearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/problem+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **clusters_refresh_volume_groups**
> clusters_refresh_volume_groups(id)

Infrastructure Rescan for Volume Groups

The HTTP POST request to the `/clusters/{id}/volumeGroups/refresh` endpoint runs the infrastructure rescanning operation for volume groups.

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
api_instance = swagger_client.ClustersApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | Specifies the ID assigned to a cluster in the Nutanix AHV environment. To learn the ID, [get a collection of Nutanix AHV clusters](#tag/Clusters/operation/Clusters_Get) to which the backup appliance has access.

try:
    # Infrastructure Rescan for Volume Groups
    api_instance.clusters_refresh_volume_groups(id)
except ApiException as e:
    print("Exception when calling ClustersApi->clusters_refresh_volume_groups: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Specifies the ID assigned to a cluster in the Nutanix AHV environment. To learn the ID, [get a collection of Nutanix AHV clusters](#tag/Clusters/operation/Clusters_Get) to which the backup appliance has access. | 

### Return type

void (empty response body)

### Authorization

[Bearer](../README.md#Bearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/problem+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **clusters_rescan_snapshots**
> AsyncTask clusters_rescan_snapshots(id)

Cluster Rescan for Snapshots

The HTTP POST request to the `/clusters/{id}/rescanSnapshots` endpoint runs the cluster rescanning operation for snapshots. Compatible snapshots are automatically imported.

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
api_instance = swagger_client.ClustersApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | Specifies the ID assigned to a cluster in the Nutanix AHV environment. To learn the ID, [get a collection of Nutanix AHV clusters](#tag/Clusters/operation/Clusters_Get) to which the backup appliance has access.

try:
    # Cluster Rescan for Snapshots
    api_response = api_instance.clusters_rescan_snapshots(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ClustersApi->clusters_rescan_snapshots: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Specifies the ID assigned to a cluster in the Nutanix AHV environment. To learn the ID, [get a collection of Nutanix AHV clusters](#tag/Clusters/operation/Clusters_Get) to which the backup appliance has access. | 

### Return type

[**AsyncTask**](AsyncTask.md)

### Authorization

[Bearer](../README.md#Bearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/problem+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **clusters_update_auto_protection_settings**
> clusters_update_auto_protection_settings(body, id)

Modify Cluster Auto-Protection Settings

The HTTP PUT request to the `/clusters/{id}/autoProtection` endpoint configures auto-protection settings for the specified cluster.

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
api_instance = swagger_client.ClustersApi(swagger_client.ApiClient(configuration))
body = swagger_client.AutoProtectionSettings() # AutoProtectionSettings | Specifies auto-protection settings.
id = 'id_example' # str | Specifies the ID assigned to a cluster in the Nutanix AHV environment. To learn the ID, [get a collection of Nutanix AHV clusters](#tag/Clusters/operation/Clusters_Get) to which the backup appliance has access.

try:
    # Modify Cluster Auto-Protection Settings
    api_instance.clusters_update_auto_protection_settings(body, id)
except ApiException as e:
    print("Exception when calling ClustersApi->clusters_update_auto_protection_settings: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**AutoProtectionSettings**](AutoProtectionSettings.md)| Specifies auto-protection settings. | 
 **id** | **str**| Specifies the ID assigned to a cluster in the Nutanix AHV environment. To learn the ID, [get a collection of Nutanix AHV clusters](#tag/Clusters/operation/Clusters_Get) to which the backup appliance has access. | 

### Return type

void (empty response body)

### Authorization

[Bearer](../README.md#Bearer)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/problem+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

