# openapi.api.Class2FAEndpointsApi

## Load the API package
```dart
import 'package:openapi/api.dart';
```

All URIs are relative to */api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**call2fASetup2faSetupPost**](Class2FAEndpointsApi.md#call2fasetup2fasetuppost) | **POST** /2fa/setup | 2Fa Setup
[**call2fAVerification2faVerifyPost**](Class2FAEndpointsApi.md#call2faverification2faverifypost) | **POST** /2fa/verify | 2Fa Verification


# **call2fASetup2faSetupPost**
> Object call2fASetup2faSetupPost(username, password)

2Fa Setup

Endpoint to set up Two-Factor Authentication (2FA) for a user.

### Example
```dart
import 'package:openapi/api.dart';

final api_instance = Class2FAEndpointsApi();
final username = username_example; // String | 
final password = password_example; // String | 

try {
    final result = api_instance.call2fASetup2faSetupPost(username, password);
    print(result);
} catch (e) {
    print('Exception when calling Class2FAEndpointsApi->call2fASetup2faSetupPost: $e\n');
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **username** | **String**|  | 
 **password** | **String**|  | 

### Return type

[**Object**](Object.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **call2fAVerification2faVerifyPost**
> Object call2fAVerification2faVerifyPost(username, token)

2Fa Verification

Endpoint to verify the Two-Factor Authentication (2FA) token for a user.

### Example
```dart
import 'package:openapi/api.dart';

final api_instance = Class2FAEndpointsApi();
final username = username_example; // String | 
final token = token_example; // String | 

try {
    final result = api_instance.call2fAVerification2faVerifyPost(username, token);
    print(result);
} catch (e) {
    print('Exception when calling Class2FAEndpointsApi->call2fAVerification2faVerifyPost: $e\n');
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **username** | **String**|  | 
 **token** | **String**|  | 

### Return type

[**Object**](Object.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

