# vikela_client.2FAEndpointsApi

All URIs are relative to */api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**call_2_fa_setup2fa_setup_post**](2FAEndpointsApi.md#call_2_fa_setup2fa_setup_post) | **POST** /2fa/setup | 2Fa Setup
[**call_2_fa_verification2fa_verify_post**](2FAEndpointsApi.md#call_2_fa_verification2fa_verify_post) | **POST** /2fa/verify | 2Fa Verification


# **call_2_fa_setup2fa_setup_post**
> object call_2_fa_setup2fa_setup_post(username, password)

2Fa Setup

Endpoint to set up Two-Factor Authentication (2FA) for a user.

### Example


```python
import vikela_client
from vikela_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to /api
# See configuration.py for a list of all supported configuration parameters.
configuration = vikela_client.Configuration(
    host = "/api"
)


# Enter a context with an instance of the API client
with vikela_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = vikela_client.2FAEndpointsApi(api_client)
    username = 'username_example' # str | 
    password = 'password_example' # str | 

    try:
        # 2Fa Setup
        api_response = api_instance.call_2_fa_setup2fa_setup_post(username, password)
        print("The response of 2FAEndpointsApi->call_2_fa_setup2fa_setup_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling 2FAEndpointsApi->call_2_fa_setup2fa_setup_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **username** | **str**|  | 
 **password** | **str**|  | 

### Return type

**object**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **call_2_fa_verification2fa_verify_post**
> object call_2_fa_verification2fa_verify_post(username, token)

2Fa Verification

Endpoint to verify the Two-Factor Authentication (2FA) token for a user.

### Example


```python
import vikela_client
from vikela_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to /api
# See configuration.py for a list of all supported configuration parameters.
configuration = vikela_client.Configuration(
    host = "/api"
)


# Enter a context with an instance of the API client
with vikela_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = vikela_client.2FAEndpointsApi(api_client)
    username = 'username_example' # str | 
    token = 'token_example' # str | 

    try:
        # 2Fa Verification
        api_response = api_instance.call_2_fa_verification2fa_verify_post(username, token)
        print("The response of 2FAEndpointsApi->call_2_fa_verification2fa_verify_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling 2FAEndpointsApi->call_2_fa_verification2fa_verify_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **username** | **str**|  | 
 **token** | **str**|  | 

### Return type

**object**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

