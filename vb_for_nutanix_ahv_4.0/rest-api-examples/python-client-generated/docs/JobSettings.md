# JobSettings

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | System ID assigned to a job in the Veeam Backup for Nutanix AHV. | [optional] 
**name** | **str** | Name of the job. | 
**description** | **str** | Description opf the job. | [optional] 
**mode** | [**JobMode**](JobMode.md) |  | 
**cluster_id** | **str** | ID of a cluster whose resources the job protects. | 
**repository_id** | **str** | ID of a repository where backups created by the job are stored. | [optional] 
**vm_ids** | **list[str]** | IDs of virtual machines processed by the job. | [optional] 
**protection_domains** | **list[str]** | Names of protection domains processed by the job. | [optional] 
**schedule_settings** | [**ScheduleSettings**](ScheduleSettings.md) |  | 
**active_full_settings** | [**ActiveFullSettings**](ActiveFullSettings.md) |  | [optional] 
**deleted_vm_retention** | [**DeletedVmRetentionSettings**](DeletedVmRetentionSettings.md) |  | [optional] 
**gfs_settings** | [**GfsSettings**](GfsSettings.md) |  | [optional] 
**health_check_settings** | [**HealthCheckSettings**](HealthCheckSettings.md) |  | [optional] 
**synthetic_full_settings** | [**SyntheticFullSettings**](SyntheticFullSettings.md) |  | [optional] 
**retention_settings** | [**RetentionSettings**](RetentionSettings.md) |  | 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

