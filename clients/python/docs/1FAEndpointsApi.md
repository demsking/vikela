# vikela_client.1FAEndpointsApi

All URIs are relative to */api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_access_token_token_post**](1FAEndpointsApi.md#get_access_token_token_post) | **POST** /token | Get Access Token


# **get_access_token_token_post**
> GetAccessTokenResponse get_access_token_token_post(username, password, grant_type=grant_type, scope=scope, client_id=client_id, client_secret=client_secret)

Get Access Token

Generates an access token for a user.

### Example


```python
import vikela_client
from vikela_client.models.get_access_token_response import GetAccessTokenResponse
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
    api_instance = vikela_client.1FAEndpointsApi(api_client)
    username = 'username_example' # str | 
    password = 'password_example' # str | 
    grant_type = 'grant_type_example' # str |  (optional)
    scope = '' # str |  (optional) (default to '')
    client_id = 'client_id_example' # str |  (optional)
    client_secret = 'client_secret_example' # str |  (optional)

    try:
        # Get Access Token
        api_response = api_instance.get_access_token_token_post(username, password, grant_type=grant_type, scope=scope, client_id=client_id, client_secret=client_secret)
        print("The response of 1FAEndpointsApi->get_access_token_token_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling 1FAEndpointsApi->get_access_token_token_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **username** | **str**|  | 
 **password** | **str**|  | 
 **grant_type** | **str**|  | [optional] 
 **scope** | **str**|  | [optional] [default to &#39;&#39;]
 **client_id** | **str**|  | [optional] 
 **client_secret** | **str**|  | [optional] 

### Return type

[**GetAccessTokenResponse**](GetAccessTokenResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/x-www-form-urlencoded
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**401** | Unauthorized |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

