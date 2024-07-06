# openapi.api.Class1FAEndpointsApi

## Load the API package
```dart
import 'package:openapi/api.dart';
```

All URIs are relative to */api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**getAccessTokenTokenPost**](Class1FAEndpointsApi.md#getaccesstokentokenpost) | **POST** /token | Get Access Token


# **getAccessTokenTokenPost**
> GetAccessTokenResponse getAccessTokenTokenPost(username, password, grantType, scope, clientId, clientSecret)

Get Access Token

Generates an access token for a user.

### Example
```dart
import 'package:openapi/api.dart';

final api_instance = Class1FAEndpointsApi();
final username = username_example; // String | 
final password = password_example; // String | 
final grantType = grantType_example; // String | 
final scope = scope_example; // String | 
final clientId = clientId_example; // String | 
final clientSecret = clientSecret_example; // String | 

try {
    final result = api_instance.getAccessTokenTokenPost(username, password, grantType, scope, clientId, clientSecret);
    print(result);
} catch (e) {
    print('Exception when calling Class1FAEndpointsApi->getAccessTokenTokenPost: $e\n');
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **username** | **String**|  | 
 **password** | **String**|  | 
 **grantType** | **String**|  | [optional] 
 **scope** | **String**|  | [optional] [default to '']
 **clientId** | **String**|  | [optional] 
 **clientSecret** | **String**|  | [optional] 

### Return type

[**GetAccessTokenResponse**](GetAccessTokenResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/x-www-form-urlencoded
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

