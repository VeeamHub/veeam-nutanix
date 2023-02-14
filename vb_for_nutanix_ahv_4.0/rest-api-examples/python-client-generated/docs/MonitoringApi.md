# swagger_client.MonitoringApi

All URIs are relative to *https://172.25.124.153/*

Method | HTTP request | Description
------------- | ------------- | -------------
[**monitoring_download_cpu_usage_csv**](MonitoringApi.md#monitoring_download_cpu_usage_csv) | **GET** /api/v4/monitoring/downloadCpuUsageCsv | Get CPU Utilization Statistics
[**monitoring_download_memory_usage_csv**](MonitoringApi.md#monitoring_download_memory_usage_csv) | **GET** /api/v4/monitoring/downloadMemoryUsageCsv | Get RAM Consumption Statistics
[**monitoring_download_storage_usage_csv**](MonitoringApi.md#monitoring_download_storage_usage_csv) | **GET** /api/v4/monitoring/downloadStorageUsageCsv | Get Storage Usage Statistics

# **monitoring_download_cpu_usage_csv**
> str monitoring_download_cpu_usage_csv()

Get CPU Utilization Statistics

The HTTP GET request to the `/monitoring/downloadCpuUsageCsv` endpoint retrieves statistics on backup appliance CPU utilization and allows you download it in a CSV file.

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
api_instance = swagger_client.MonitoringApi(swagger_client.ApiClient(configuration))

try:
    # Get CPU Utilization Statistics
    api_response = api_instance.monitoring_download_cpu_usage_csv()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling MonitoringApi->monitoring_download_cpu_usage_csv: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

**str**

### Authorization

[Bearer](../README.md#Bearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/octet-stream, application/problem+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **monitoring_download_memory_usage_csv**
> str monitoring_download_memory_usage_csv()

Get RAM Consumption Statistics

The HTTP GET request to the `/monitoring/downloadMemoryUsageCsv` endpoint retrieves statistics on backup appliance RAM consumption and allows you download it in a CSV file.

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
api_instance = swagger_client.MonitoringApi(swagger_client.ApiClient(configuration))

try:
    # Get RAM Consumption Statistics
    api_response = api_instance.monitoring_download_memory_usage_csv()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling MonitoringApi->monitoring_download_memory_usage_csv: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

**str**

### Authorization

[Bearer](../README.md#Bearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/octet-stream, application/problem+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **monitoring_download_storage_usage_csv**
> str monitoring_download_storage_usage_csv()

Get Storage Usage Statistics

The HTTP GET request to the `/monitoring/downloadMemoryUsageCsv` endpoint retrieves statistics on backup appliance storage usage and allows you download it in a CSV file.

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
api_instance = swagger_client.MonitoringApi(swagger_client.ApiClient(configuration))

try:
    # Get Storage Usage Statistics
    api_response = api_instance.monitoring_download_storage_usage_csv()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling MonitoringApi->monitoring_download_storage_usage_csv: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

**str**

### Authorization

[Bearer](../README.md#Bearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/octet-stream, application/problem+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

