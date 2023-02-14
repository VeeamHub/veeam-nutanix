# Job

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | System ID assigned to a job in the Veeam Backup for Nutanix AHV. | 
**name** | **str** | Name of the job. | 
**description** | **str** | Description of the job. | [optional] 
**mode** | [**JobMode**](JobMode.md) |  | 
**settings** | [**JobSettings**](JobSettings.md) |  | 
**status** | [**JobStatus**](JobStatus.md) |  | [optional] 
**objects** | **int** | Total number of objects added to the job. | [optional] 
**next_run_info** | **str** | Job run type (manual or automatic). | [optional] 
**next_run_utc** | **datetime** | Date and time of the next planned job run. | [optional] 
**last_run_utc** | **datetime** | Date and time of the latest job run. | [optional] 
**last_session_id** | **str** | System ID assigned to the latest job session. | [optional] 
**enabled** | **bool** | Defines whether the job is enabled. | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

