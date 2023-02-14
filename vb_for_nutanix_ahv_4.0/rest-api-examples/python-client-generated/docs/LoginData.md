# LoginData

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**grant_type** | [**GrantType**](GrantType.md) |  | 
**user_name** | **str** | \\[Required if the &#x60;grant_type&#x60; parameter value is *Password*\\] User name. | [optional] 
**password** | **str** | \\[Required if the &#x60;grant_type&#x60; parameter value is *Password*\\] Password of the user. | [optional] 
**refresh_token** | **str** | \\[Required if the &#x60;grant_type&#x60; parameter value is *RefreshToken*\\] Refresh token. | [optional] 
**updater_token** | **str** | \\[Required if the &#x60;grant_type&#x60; parameter value is *UpdaterToken*\\] Updater token. | [optional] 
**long_lived_refresh_token** | **bool** | Defines whether the expiration time of the refresh token is increased to 14 days. | [optional] [default to False]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

