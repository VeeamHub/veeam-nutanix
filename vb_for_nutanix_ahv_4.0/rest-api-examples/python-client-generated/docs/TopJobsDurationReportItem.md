# TopJobsDurationReportItem

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**job_id** | **str** | System ID assigned to a job in Veeam Backup for Nutanix AHV. | 
**job_mode** | [**JobMode**](JobMode.md) |  | [optional] 
**job_name** | **str** | Name of the job. | 
**start_time_utc** | **datetime** | Date and time of the most recent job run. | 
**duration** | **str** | Job session duration. | 
**duration_difference** | **str** | Time span between the latest job session duration and the average duration of the last 10 successful sessions of the job. | [optional] 
**percentage** | **int** | Difference between the latest job session duration and the average duration of the last 10 successful sessions of the job (in percent). | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

