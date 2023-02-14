# VirtualMachineMetadata

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | ID assigned to a virtual machine in the Nutanix AHV environment. | [optional] 
**name** | **str** | Name of the virtual machine. | [optional] 
**protection_domain** | **str** | Name of the protection domain that contains the virtual machine. | [optional] 
**consistency_group** | **str** | Name of the consistency group that contains the virtual machine. | [optional] 
**cluster_id** | **str** | ID assigned to a cluster the virtual machine belongs to. | [optional] 
**cluster_name** | **str** | Name of a cluster the virtual machine belongs to. | [optional] 
**size** | **int** | Size of all disk attached to the virtual machine (in bytes). | [optional] 
**disks** | [**list[Disk]**](Disk.md) | List of disks attached to the virtual machine. | [optional] 
**network_adapters** | [**list[NetworkAdapter]**](NetworkAdapter.md) | List of network adapters configured on the virtual machine. | [optional] 
**networks** | [**list[NutanixNetwork]**](NutanixNetwork.md) | List of networks the virtual machine is connected to. | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

