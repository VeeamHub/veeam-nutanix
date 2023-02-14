# swagger_client.DashboardApi

All URIs are relative to *https://172.25.124.153/*

Method | HTTP request | Description
------------- | ------------- | -------------
[**dashboard_get_backup_repositories_report**](DashboardApi.md#dashboard_get_backup_repositories_report) | **GET** /api/v4/dashboard/backupRepositories | Get Collection of Available Backup Repositories
[**dashboard_get_protected_vms**](DashboardApi.md#dashboard_get_protected_vms) | **GET** /api/v4/dashboard/protectedVms | Get Number of Protected VMs
[**dashboard_get_protected_vms_in_cluster**](DashboardApi.md#dashboard_get_protected_vms_in_cluster) | **GET** /api/v4/dashboard/protectedVmsInCluster | Get Collection of Protected VMs
[**dashboard_get_session_ratio_report**](DashboardApi.md#dashboard_get_session_ratio_report) | **GET** /api/v4/dashboard/sessionRatio | Get Job Type Statistics
[**dashboard_get_sessions_summary_report**](DashboardApi.md#dashboard_get_sessions_summary_report) | **GET** /api/v4/dashboard/sessionsSummary | Get Session Status Statistics for Last 24 Hours
[**dashboard_get_system_monitoring_info**](DashboardApi.md#dashboard_get_system_monitoring_info) | **GET** /api/v4/dashboard/systemMonitoringInfo | Get Resource Usage Statistics
[**dashboard_get_top_jobs_duration_report**](DashboardApi.md#dashboard_get_top_jobs_duration_report) | **GET** /api/v4/dashboard/topJobsDuration | Get Collection of Recent Job Sessions Duration
[**dashboard_get_unprotected_vms_in_cluster**](DashboardApi.md#dashboard_get_unprotected_vms_in_cluster) | **GET** /api/v4/dashboard/unprotectedVmsInCluster | Get Collection of Unprotected VMs

# **dashboard_get_backup_repositories_report**
> PageOfBackupRepositoryReportItem dashboard_get_backup_repositories_report(offset=offset, limit=limit, filter=filter, sort=sort)

Get Collection of Available Backup Repositories

The HTTP GET request to the `dashboard/backupRepositories` endpoint retrieves a list of available backup repositories.

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
api_instance = swagger_client.DashboardApi(swagger_client.ApiClient(configuration))
offset = 0 # int | Excludes from a response the first N items of a resource collection. (optional) (default to 0)
limit = 100 # int | Specifies the maximum number of items of a resource collection to return in a response. (optional) (default to 100)
filter = swagger_client.FilterParameter() # FilterParameter | Specifies the criteria for items to be returned in a response. For more information, see the Veeam Backup for Nutanix AHV REST API Reference Overview, section [Filter Parameters](https://helpcenter.veeam.com/docs/van/rest/filter.html?ver=40). (optional)
sort = swagger_client.SortParameter() # SortParameter | Specifies the order of items in the response. For more information, see the Veeam Backup for Nutanix AHV REST API Reference Overview, section [Sort Parameters](https://helpcenter.veeam.com/docs/van/rest/sort.html?ver=40). (optional)

try:
    # Get Collection of Available Backup Repositories
    api_response = api_instance.dashboard_get_backup_repositories_report(offset=offset, limit=limit, filter=filter, sort=sort)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DashboardApi->dashboard_get_backup_repositories_report: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **offset** | **int**| Excludes from a response the first N items of a resource collection. | [optional] [default to 0]
 **limit** | **int**| Specifies the maximum number of items of a resource collection to return in a response. | [optional] [default to 100]
 **filter** | [**FilterParameter**](.md)| Specifies the criteria for items to be returned in a response. For more information, see the Veeam Backup for Nutanix AHV REST API Reference Overview, section [Filter Parameters](https://helpcenter.veeam.com/docs/van/rest/filter.html?ver&#x3D;40). | [optional] 
 **sort** | [**SortParameter**](.md)| Specifies the order of items in the response. For more information, see the Veeam Backup for Nutanix AHV REST API Reference Overview, section [Sort Parameters](https://helpcenter.veeam.com/docs/van/rest/sort.html?ver&#x3D;40). | [optional] 

### Return type

[**PageOfBackupRepositoryReportItem**](PageOfBackupRepositoryReportItem.md)

### Authorization

[Bearer](../README.md#Bearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/problem+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **dashboard_get_protected_vms**
> ProtectedVmsReport dashboard_get_protected_vms()

Get Number of Protected VMs

The HTTP GET request to the `/dashboard/protectedVms` endpoint retrieves a number of VM protected with snapshots, a number of VM protected with backups and a number of unprotected VMs.

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
api_instance = swagger_client.DashboardApi(swagger_client.ApiClient(configuration))

try:
    # Get Number of Protected VMs
    api_response = api_instance.dashboard_get_protected_vms()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DashboardApi->dashboard_get_protected_vms: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**ProtectedVmsReport**](ProtectedVmsReport.md)

### Authorization

[Bearer](../README.md#Bearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/problem+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **dashboard_get_protected_vms_in_cluster**
> PageOfProtectedVirtualMachine dashboard_get_protected_vms_in_cluster(offset=offset, limit=limit, filter=filter, sort=sort)

Get Collection of Protected VMs

The HTTP GET request to the `/dashboard/protectedVmsInCluster` endpoint retrieves a list of protected VMs.

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
api_instance = swagger_client.DashboardApi(swagger_client.ApiClient(configuration))
offset = 0 # int | Excludes from a response the first N items of a resource collection. (optional) (default to 0)
limit = 100 # int | Specifies the maximum number of items of a resource collection to return in a response. (optional) (default to 100)
filter = swagger_client.FilterParameter() # FilterParameter | Specifies the criteria for items to be returned in a response. For more information, see the Veeam Backup for Nutanix AHV REST API Reference Overview, section [Filter Parameters](https://helpcenter.veeam.com/docs/van/rest/filter.html?ver=40). (optional)
sort = swagger_client.SortParameter() # SortParameter | Specifies the order of items in the response. For more information, see the Veeam Backup for Nutanix AHV REST API Reference Overview, section [Sort Parameters](https://helpcenter.veeam.com/docs/van/rest/sort.html?ver=40). (optional)

try:
    # Get Collection of Protected VMs
    api_response = api_instance.dashboard_get_protected_vms_in_cluster(offset=offset, limit=limit, filter=filter, sort=sort)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DashboardApi->dashboard_get_protected_vms_in_cluster: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **offset** | **int**| Excludes from a response the first N items of a resource collection. | [optional] [default to 0]
 **limit** | **int**| Specifies the maximum number of items of a resource collection to return in a response. | [optional] [default to 100]
 **filter** | [**FilterParameter**](.md)| Specifies the criteria for items to be returned in a response. For more information, see the Veeam Backup for Nutanix AHV REST API Reference Overview, section [Filter Parameters](https://helpcenter.veeam.com/docs/van/rest/filter.html?ver&#x3D;40). | [optional] 
 **sort** | [**SortParameter**](.md)| Specifies the order of items in the response. For more information, see the Veeam Backup for Nutanix AHV REST API Reference Overview, section [Sort Parameters](https://helpcenter.veeam.com/docs/van/rest/sort.html?ver&#x3D;40). | [optional] 

### Return type

[**PageOfProtectedVirtualMachine**](PageOfProtectedVirtualMachine.md)

### Authorization

[Bearer](../README.md#Bearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/problem+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **dashboard_get_session_ratio_report**
> SessionRatioReport dashboard_get_session_ratio_report(period)

Get Job Type Statistics

The HTTP GET request to the `/dashboard/sessionRatio` endpoint retrieves a total number of job sessions and a number of successfully completed sessions during the specified period. The statistics is provided for each type of job: backup, snapshot and PD snapshot.

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
api_instance = swagger_client.DashboardApi(swagger_client.ApiClient(configuration))
period = swagger_client.ReportPeriod() # ReportPeriod | Specifies the period to collect the statistics.

try:
    # Get Job Type Statistics
    api_response = api_instance.dashboard_get_session_ratio_report(period)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DashboardApi->dashboard_get_session_ratio_report: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **period** | [**ReportPeriod**](.md)| Specifies the period to collect the statistics. | 

### Return type

[**SessionRatioReport**](SessionRatioReport.md)

### Authorization

[Bearer](../README.md#Bearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/problem+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **dashboard_get_sessions_summary_report**
> SessionsSummaryReport dashboard_get_sessions_summary_report()

Get Session Status Statistics for Last 24 Hours

The HTTP GET request to the `/dashboard/sessionsSummary` endpoint retrieves a number of sessions started for data protection or disaster recovery operations during the past 24 hours that completed successfully, a number of sessions that completed with warnings, a number of sessions that completed with errors, and a number of sessions that are currently running.

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
api_instance = swagger_client.DashboardApi(swagger_client.ApiClient(configuration))

try:
    # Get Session Status Statistics for Last 24 Hours
    api_response = api_instance.dashboard_get_sessions_summary_report()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DashboardApi->dashboard_get_sessions_summary_report: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**SessionsSummaryReport**](SessionsSummaryReport.md)

### Authorization

[Bearer](../README.md#Bearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/problem+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **dashboard_get_system_monitoring_info**
> SystemMonitoringInfo dashboard_get_system_monitoring_info(metric_type, _from=_from, to=to, report_interval=report_interval)

Get Resource Usage Statistics

The HTTP GET request to the `/dashboard/systemMonitoringInfo` endpoint retrieves CPU utilization, RAM consumption and storage usage on the backup appliance.

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
api_instance = swagger_client.DashboardApi(swagger_client.ApiClient(configuration))
metric_type = [swagger_client.SystemMetricType()] # list[SystemMetricType] | Returns only data on resources of the specified types.
_from = '2013-10-20T19:20:30+01:00' # datetime | Returns only data after the specified date and time. (optional)
to = '2013-10-20T19:20:30+01:00' # datetime | Returns only data before the specified date and time. (optional)
report_interval = 'report_interval_example' # str | Returns data for periods defined by the specified time interval. By default, the interval equals 30 minutes. (optional)

try:
    # Get Resource Usage Statistics
    api_response = api_instance.dashboard_get_system_monitoring_info(metric_type, _from=_from, to=to, report_interval=report_interval)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DashboardApi->dashboard_get_system_monitoring_info: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **metric_type** | [**list[SystemMetricType]**](SystemMetricType.md)| Returns only data on resources of the specified types. | 
 **_from** | **datetime**| Returns only data after the specified date and time. | [optional] 
 **to** | **datetime**| Returns only data before the specified date and time. | [optional] 
 **report_interval** | **str**| Returns data for periods defined by the specified time interval. By default, the interval equals 30 minutes. | [optional] 

### Return type

[**SystemMonitoringInfo**](SystemMonitoringInfo.md)

### Authorization

[Bearer](../README.md#Bearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/problem+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **dashboard_get_top_jobs_duration_report**
> PageOfTopJobsDurationReportItem dashboard_get_top_jobs_duration_report(job_mode, offset=offset, limit=limit, filter=filter, sort=sort)

Get Collection of Recent Job Sessions Duration

The HTTP GET request to the `/dashboard/topJobsDuration` endpoint retrieves duration statistics for recent sessions of the specified job type.

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
api_instance = swagger_client.DashboardApi(swagger_client.ApiClient(configuration))
job_mode = swagger_client.JobMode() # JobMode | Specifies the job type.
offset = 0 # int | Excludes from a response the first N items of a resource collection. (optional) (default to 0)
limit = 100 # int | Specifies the maximum number of items of a resource collection to return in a response. (optional) (default to 100)
filter = swagger_client.FilterParameter() # FilterParameter | Specifies the criteria for items to be returned in a response. For more information, see the Veeam Backup for Nutanix AHV REST API Reference Overview, section [Filter Parameters](https://helpcenter.veeam.com/docs/van/rest/filter.html?ver=40). (optional)
sort = swagger_client.SortParameter() # SortParameter | Specifies the order of items in the response. For more information, see the Veeam Backup for Nutanix AHV REST API Reference Overview, section [Sort Parameters](https://helpcenter.veeam.com/docs/van/rest/sort.html?ver=40). (optional)

try:
    # Get Collection of Recent Job Sessions Duration
    api_response = api_instance.dashboard_get_top_jobs_duration_report(job_mode, offset=offset, limit=limit, filter=filter, sort=sort)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DashboardApi->dashboard_get_top_jobs_duration_report: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **job_mode** | [**JobMode**](.md)| Specifies the job type. | 
 **offset** | **int**| Excludes from a response the first N items of a resource collection. | [optional] [default to 0]
 **limit** | **int**| Specifies the maximum number of items of a resource collection to return in a response. | [optional] [default to 100]
 **filter** | [**FilterParameter**](.md)| Specifies the criteria for items to be returned in a response. For more information, see the Veeam Backup for Nutanix AHV REST API Reference Overview, section [Filter Parameters](https://helpcenter.veeam.com/docs/van/rest/filter.html?ver&#x3D;40). | [optional] 
 **sort** | [**SortParameter**](.md)| Specifies the order of items in the response. For more information, see the Veeam Backup for Nutanix AHV REST API Reference Overview, section [Sort Parameters](https://helpcenter.veeam.com/docs/van/rest/sort.html?ver&#x3D;40). | [optional] 

### Return type

[**PageOfTopJobsDurationReportItem**](PageOfTopJobsDurationReportItem.md)

### Authorization

[Bearer](../README.md#Bearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/problem+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **dashboard_get_unprotected_vms_in_cluster**
> PageOfUnprotectedVirtualMachine dashboard_get_unprotected_vms_in_cluster(offset=offset, limit=limit, filter=filter, sort=sort)

Get Collection of Unprotected VMs

The HTTP GET request to the `/dashboard/unprotectedVmsInCluster` endpoint retrieves a list of unprotected VMs.

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
api_instance = swagger_client.DashboardApi(swagger_client.ApiClient(configuration))
offset = 0 # int | Excludes from a response the first N items of a resource collection. (optional) (default to 0)
limit = 100 # int | Specifies the maximum number of items of a resource collection to return in a response. (optional) (default to 100)
filter = swagger_client.FilterParameter() # FilterParameter | Specifies the criteria for items to be returned in a response. For more information, see the Veeam Backup for Nutanix AHV REST API Reference Overview, section [Filter Parameters](https://helpcenter.veeam.com/docs/van/rest/filter.html?ver=40). (optional)
sort = swagger_client.SortParameter() # SortParameter | Specifies the order of items in the response. For more information, see the Veeam Backup for Nutanix AHV REST API Reference Overview, section [Sort Parameters](https://helpcenter.veeam.com/docs/van/rest/sort.html?ver=40). (optional)

try:
    # Get Collection of Unprotected VMs
    api_response = api_instance.dashboard_get_unprotected_vms_in_cluster(offset=offset, limit=limit, filter=filter, sort=sort)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DashboardApi->dashboard_get_unprotected_vms_in_cluster: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **offset** | **int**| Excludes from a response the first N items of a resource collection. | [optional] [default to 0]
 **limit** | **int**| Specifies the maximum number of items of a resource collection to return in a response. | [optional] [default to 100]
 **filter** | [**FilterParameter**](.md)| Specifies the criteria for items to be returned in a response. For more information, see the Veeam Backup for Nutanix AHV REST API Reference Overview, section [Filter Parameters](https://helpcenter.veeam.com/docs/van/rest/filter.html?ver&#x3D;40). | [optional] 
 **sort** | [**SortParameter**](.md)| Specifies the order of items in the response. For more information, see the Veeam Backup for Nutanix AHV REST API Reference Overview, section [Sort Parameters](https://helpcenter.veeam.com/docs/van/rest/sort.html?ver&#x3D;40). | [optional] 

### Return type

[**PageOfUnprotectedVirtualMachine**](PageOfUnprotectedVirtualMachine.md)

### Authorization

[Bearer](../README.md#Bearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/problem+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

