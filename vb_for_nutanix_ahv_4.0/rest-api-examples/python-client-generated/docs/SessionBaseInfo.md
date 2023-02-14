# SessionBaseInfo

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | System ID assigned to a session in the Veeam Backup for Nutanix AHV. | [optional] 
**name** | **str** | Name of the session. | [optional] 
**session_type** | [**SessionType**](SessionType.md) |  | [optional] 
**state** | [**SessionState**](SessionState.md) |  | [optional] 
**result** | [**SessionResult**](SessionResult.md) |  | [optional] 
**job_name** | **str** | Name of the job related to the session. | [optional] 
**objects_count** | **int** | Number of objects processed in the session. | [optional] 
**start_time_utc** | **datetime** | Date and time when the session started. | [optional] 
**finish_time_utc** | **datetime** | Date and time when the session finished or stopped. | [optional] 
**reason** | **str** | Reason for the restore operation. | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

