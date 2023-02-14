# VirtualMachine

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | System ID assigned to a VM in the Nutanix environment. | 
**name** | **str** | Name of the VM. | 
**cluster_id** | **str** | ID of the cluster to which the VM belongs. | 
**cluster_name** | **str** | Name of the cluster to which the VM belongs. | [optional] 
**vm_size** | **int** | Size of all disks attached to the VM (in bytes). | [optional] 
**volume_group_size** | **int** | Size of all disks in the attached volume groups (in bytes). | [optional] 
**protection_domain** | **str** | Name of the protection domain that includes the VM. | [optional] 
**consistency_group** | **str** | Name of the consistency group that includes the VM. | [optional] 
**disks** | [**list[Disk]**](Disk.md) | Disks attached to the VM. | [optional] 
**volume_groups** | **list[str]** | Volume groups attached to the VM. | [optional] 
**network_adapters** | [**list[NetworkAdapter]**](NetworkAdapter.md) | Network adapters configured on the VM. | [optional] 
**guest_os_version** | **str** | Version of the operating system running in the VM. | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

