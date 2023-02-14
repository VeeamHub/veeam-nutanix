# ProtectionDomainSnapshot

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | System ID assigned to a restore point in Veeam Backup and Replication. | [optional] 
**type** | [**RestorePointType**](RestorePointType.md) |  | 
**creation_time_utc** | **datetime** | Date and time when the restore point was created. | [optional] 
**job_id** | **str** | System ID assigned to the job in Veeam Backup and Replication. | [optional] 
**job_name** | **str** | Name of a job that created the restore point. | [optional] 
**snapshot_id** | **str** | ID assigned to a protection domain snapshot in the Nutanix AHV environment. | [optional] 
**pd_name** | **str** | Name of the protection domain. | [optional] 
**vm_ids** | **list[str]** | IDs of VMs that are protected with the protection domain. | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

