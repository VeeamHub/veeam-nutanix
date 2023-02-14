# ProtectedVirtualMachine

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | System ID assigned to a VM in the Nutanix AHV environment. | [optional] 
**name** | **str** | Name of the VM. | [optional] 
**snapshots** | **int** | Number of all snapshots created for the VM. | [optional] 
**backups** | **int** | Number of VM backups created with Veeam Backup for Nutanix AHV. | [optional] 
**cluster_id** | **str** | ID of the cluster to which the VM belongs. | [optional] 
**cluster_name** | **str** | Name of the cluster to which the VM belongs. | [optional] 
**last_protection_date_utc** | **datetime** | Date and time when the latest restore point was created. | [optional] 
**last_restore_point_id** | **str** | System ID assigned to the recent restore point in Veeam Backup and Replication. | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

