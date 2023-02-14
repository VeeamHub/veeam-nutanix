# RestoreSettings

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**source_vm_id** | **str** | ID of a source VM to restore from. | 
**target_vm_name** | **str** | New name of the restored VM. | [optional] 
**preserve_original_vm_id** | **bool** | Defines whether the ID of the source VM will be kept. | [optional] 
**restore_point_id** | **str** | System ID assigned to the restore point in Veeam Backup and Replication. | 
**storage_container_id** | **str** | ID assigned to a storage container assigned in the Nutanix AHV environment. | [optional] 
**network_adapters** | [**list[NetworkAdapterRemap]**](NetworkAdapterRemap.md) | Network adapter configuration for restore. | [optional] 
**reason** | **str** | Reason for restore. | [optional] 
**power_on_vm_after_restore** | **bool** | Defines whether the VM will be powered on after restore. | [optional] 
**disconnect_networks_after_restore** | **bool** | Defines whether all network adapters will be disconnected from their networks after restore. | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

