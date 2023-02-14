# DiskRestoreSettings

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**source_vm_id** | **str** | ID of a source VM to restore from. | 
**target_vm_id** | **str** | ID of a target VM to restore to. | 
**restore_point_id** | **str** | System ID assigned to the restore point in Veeam Backup and Replication. | 
**disk_settings** | [**list[DiskSettingsForRestore]**](DiskSettingsForRestore.md) | List of disk settings to restore (used only for disk restore) | 
**reason** | **str** | Reason for restore. | [optional] 
**power_on_vm_after_restore** | **bool** | Defines whether the VM will be powered on after restore. | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

