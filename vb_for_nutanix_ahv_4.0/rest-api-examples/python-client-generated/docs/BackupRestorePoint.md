# BackupRestorePoint

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | System ID assigned to a restore point in Veeam Backup and Replication. | [optional] 
**type** | [**RestorePointType**](RestorePointType.md) |  | 
**creation_time_utc** | **datetime** | Date and time when the restore point was created. | [optional] 
**job_id** | **str** | System ID assigned to the job in Veeam Backup and Replication. | [optional] 
**job_name** | **str** | Name of a job that created the restore point. | [optional] 
**is_corrupted** | **bool** | Defines whether the backup is corrupted. | [optional] 
**backup_type** | **str** | Type of the backup. | [optional] 
**backup_snapshot_id** | **str** | System ID assigned to the backup snapshot in Veeam Backup for Nutanix AHV. | [optional] 
**vm_id** | **str** | ID of a VM that was backed up. | [optional] 
**backup_id** | **str** | System ID assigned to the backup in Veeam Backup for Nutanix AHV. | [optional] 
**backup_size_bytes** | **int** | Size of the backup (in bytes). | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

