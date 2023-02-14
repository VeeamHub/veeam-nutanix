# BackupSnapshot

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | System ID assigned to a restore point in Veeam Backup and Replication. | [optional] 
**type** | [**RestorePointType**](RestorePointType.md) |  | 
**creation_time_utc** | **datetime** | Date and time when the restore point was created. | [optional] 
**job_id** | **str** | System ID assigned to the job in Veeam Backup and Replication. | [optional] 
**job_name** | **str** | Name of a job that created the restore point. | [optional] 
**snapshot_name** | **str** | Name of a backup snapshot. | [optional] 
**snapshot_type** | [**BackupSnapshotType**](BackupSnapshotType.md) |  | [optional] 
**vm_id** | **str** | ID of the VM whose snapshot was taken. | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

