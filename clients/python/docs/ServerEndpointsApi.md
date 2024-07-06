# vikela_client.ServerEndpointsApi

All URIs are relative to */api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_server_info_get**](ServerEndpointsApi.md#get_server_info_get) | **GET** / | Get Server Info


# **get_server_info_get**
> ServerInfo get_server_info_get()

Get Server Info

Endpoint to retrieve server information.

### Example


```python
import vikela_client
from vikela_client.models.server_info import ServerInfo
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
    api_instance = vikela_client.ServerEndpointsApi(api_client)

    try:
        # Get Server Info
        api_response = api_instance.get_server_info_get()
        print("The response of ServerEndpointsApi->get_server_info_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ServerEndpointsApi->get_server_info_get: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**ServerInfo**](ServerInfo.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

