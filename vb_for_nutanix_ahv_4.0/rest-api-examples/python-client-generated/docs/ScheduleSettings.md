# ScheduleSettings

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**enabled** | **bool** | Defines whether a schedule is configured for the job. | [optional] 
**type** | [**ScheduleType**](ScheduleType.md) |  | [optional] 
**weekly** | [**WeeklySchedule**](WeeklySchedule.md) |  | [optional] 
**monthly** | [**MonthlySchedule**](MonthlySchedule.md) |  | [optional] 
**periodic** | [**PeriodicSchedule**](PeriodicSchedule.md) |  | [optional] 
**automatic_retry** | **bool** | Defines whether Veeam Backup for Nutanix AHV retires backing up a VM in case of a failure. | [optional] 
**retry_count** | **int** | Maximum number of retry attempts specified for the job. | [optional] 
**retry_time_delay** | **int** | Time delay before retry (in minutes). | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

