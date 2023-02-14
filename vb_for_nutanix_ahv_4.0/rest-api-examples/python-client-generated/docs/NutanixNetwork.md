# NutanixNetwork

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | ID assigned to the network in the Nutanix AHV environment. | [optional] 
**name** | **str** | Name of the network in the Nutanix AHV environment. | [optional] 
**network_address** | **str** | Network IP prefix. | [optional] 
**ip_management_on** | **bool** | Defines whether the IP Address Management feature is enabled on the network. For more information, see [Nutanix documentation](https://portal.nutanix.com/page/documents/details?targetId&#x3D;AHV-Admin-Guide-v6_5:ahv-acr-host-ipam-r.html). | [optional] 
**prefix_length** | **int** | Length of the routing prefix to identify the subnet mask to be used by devices requesting an IP address from the DHCP service. | [optional] 
**ip_pool** | **list[str]** | Ranges of the IP addresses that can be assigned to devices requesting an IP address from the DHCP service. | [optional] 
**gateway_ip** | **str** | IP address of the default gateway to be used by devices requesting an IP address from the DHCP service. | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

