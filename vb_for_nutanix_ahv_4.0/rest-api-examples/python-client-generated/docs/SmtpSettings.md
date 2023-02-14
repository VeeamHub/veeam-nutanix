# SmtpSettings

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**host** | **str** | DNS name or an IP address of an SMTP server. | 
**port** | **int** | Port number used by the SMTP server. Default value is *25*. | [optional] [default to 25]
**use_ssl** | **bool** | Defines whether to use the secure connection for email operations. Default value is *false*. | [optional] 
**certificate_thumbprint** | **str** | Hexadecimal string that uniquely identifies a certificate used on the SMTP server. | [optional] 
**authentication_required** | **bool** | Defines whether to use a specific account to connect to the SMTP server. Default value is *false*. | [optional] 
**username** | **str** | Specifies user name used to access the account on the SMTP server. | [optional] 
**password** | **str** | Password used to access the account on the SMTP server. | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

