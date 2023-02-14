# Session

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | System ID assigned to a session in the Veeam Backup for Nutanix AHV. | [optional] 
**name** | **str** | Name of the session. | [optional] 
**session_type** | [**SessionType**](SessionType.md) |  | [optional] 
**parent_session_id** | **str** | System ID of a session that initiated the current session. | [optional] 
**state** | [**SessionState**](SessionState.md) |  | [optional] 
**result** | [**SessionResult**](SessionResult.md) |  | [optional] 
**start_time_utc** | **datetime** | Date and time when the session started. | [optional] 
**finish_time_utc** | **datetime** | Date and time when the session finished or stopped. | [optional] 
**duration** | **str** | Time taken to complete the latest job session (in ms). | [optional] 
**context** | [**SessionContext**](SessionContext.md) |  | [optional] 
**progress_state** | [**SessionProgressState**](SessionProgressState.md) |  | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

