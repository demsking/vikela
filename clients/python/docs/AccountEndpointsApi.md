# vikela_client.AccountEndpointsApi

All URIs are relative to */api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_user_document_account_me_get**](AccountEndpointsApi.md#get_user_document_account_me_get) | **GET** /account/me | Get User Document
[**register_user_account_post**](AccountEndpointsApi.md#register_user_account_post) | **POST** /account | Register User
[**update_user_data_account_profile_put**](AccountEndpointsApi.md#update_user_data_account_profile_put) | **PUT** /account/profile | Update User Data


# **get_user_document_account_me_get**
> DocumentUserDataComputedLocationAccountMeta get_user_document_account_me_get()

Get User Document

Retrieve the user document using a token.  This endpoint retrieves the user document for the currently authenticated user based on the provided token.

### Example

* OAuth Authentication (OAuth2PasswordBearer):

```python
import vikela_client
from vikela_client.models.document_user_data_computed_location_account_meta import DocumentUserDataComputedLocationAccountMeta
from vikela_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to /api
# See configuration.py for a list of all supported configuration parameters.
configuration = vikela_client.Configuration(
    host = "/api"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

configuration.access_token = os.environ["ACCESS_TOKEN"]

# Enter a context with an instance of the API client
with vikela_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = vikela_client.AccountEndpointsApi(api_client)

    try:
        # Get User Document
        api_response = api_instance.get_user_document_account_me_get()
        print("The response of AccountEndpointsApi->get_user_document_account_me_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AccountEndpointsApi->get_user_document_account_me_get: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**DocumentUserDataComputedLocationAccountMeta**](DocumentUserDataComputedLocationAccountMeta.md)

### Authorization

[OAuth2PasswordBearer](../README.md#OAuth2PasswordBearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**401** | Unauthorized |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **register_user_account_post**
> GenericResponse register_user_account_post(register_payload)

Register User

Register a new user in the database.

### Example


```python
import vikela_client
from vikela_client.models.generic_response import GenericResponse
from vikela_client.models.register_payload import RegisterPayload
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
    api_instance = vikela_client.AccountEndpointsApi(api_client)
    register_payload = vikela_client.RegisterPayload() # RegisterPayload | 

    try:
        # Register User
        api_response = api_instance.register_user_account_post(register_payload)
        print("The response of AccountEndpointsApi->register_user_account_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AccountEndpointsApi->register_user_account_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **register_payload** | [**RegisterPayload**](RegisterPayload.md)|  | 

### Return type

[**GenericResponse**](GenericResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Successful Response |  -  |
**400** | Bad Request |  -  |
**401** | Unauthorized |  -  |
**409** | Conflict |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_user_data_account_profile_put**
> GenericResponse update_user_data_account_profile_put(user_data)

Update User Data

Update the user profile data.  This endpoint updates the user profile data for the currently authenticated user, using either an OAuth2 token or a session cookie for authentication.

### Example

* OAuth Authentication (OAuth2PasswordBearer):

```python
import vikela_client
from vikela_client.models.generic_response import GenericResponse
from vikela_client.models.user_data import UserData
from vikela_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to /api
# See configuration.py for a list of all supported configuration parameters.
configuration = vikela_client.Configuration(
    host = "/api"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

configuration.access_token = os.environ["ACCESS_TOKEN"]

# Enter a context with an instance of the API client
with vikela_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = vikela_client.AccountEndpointsApi(api_client)
    user_data = vikela_client.UserData() # UserData | 

    try:
        # Update User Data
        api_response = api_instance.update_user_data_account_profile_put(user_data)
        print("The response of AccountEndpointsApi->update_user_data_account_profile_put:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AccountEndpointsApi->update_user_data_account_profile_put: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_data** | [**UserData**](UserData.md)|  | 

### Return type

[**GenericResponse**](GenericResponse.md)

### Authorization

[OAuth2PasswordBearer](../README.md#OAuth2PasswordBearer)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**401** | Unauthorized |  -  |
**404** | Not Found |  -  |
**409** | Conflict |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

