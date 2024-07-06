# openapi.api.AccountEndpointsApi

## Load the API package
```dart
import 'package:openapi/api.dart';
```

All URIs are relative to */api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**getUserDocumentAccountMeGet**](AccountEndpointsApi.md#getuserdocumentaccountmeget) | **GET** /account/me | Get User Document
[**registerUserAccountPost**](AccountEndpointsApi.md#registeruseraccountpost) | **POST** /account | Register User
[**updateUserDataAccountProfilePut**](AccountEndpointsApi.md#updateuserdataaccountprofileput) | **PUT** /account/profile | Update User Data


# **getUserDocumentAccountMeGet**
> DocumentUserDataComputedLocationAccountMeta getUserDocumentAccountMeGet()

Get User Document

Retrieve the user document using a token.  This endpoint retrieves the user document for the currently authenticated user based on the provided token.

### Example
```dart
import 'package:openapi/api.dart';
// TODO Configure OAuth2 access token for authorization: OAuth2PasswordBearer
//defaultApiClient.getAuthentication<OAuth>('OAuth2PasswordBearer').accessToken = 'YOUR_ACCESS_TOKEN';

final api_instance = AccountEndpointsApi();

try {
    final result = api_instance.getUserDocumentAccountMeGet();
    print(result);
} catch (e) {
    print('Exception when calling AccountEndpointsApi->getUserDocumentAccountMeGet: $e\n');
}
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

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **registerUserAccountPost**
> GenericResponse registerUserAccountPost(registerPayload)

Register User

Register a new user in the database.

### Example
```dart
import 'package:openapi/api.dart';

final api_instance = AccountEndpointsApi();
final registerPayload = RegisterPayload(); // RegisterPayload | 

try {
    final result = api_instance.registerUserAccountPost(registerPayload);
    print(result);
} catch (e) {
    print('Exception when calling AccountEndpointsApi->registerUserAccountPost: $e\n');
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **registerPayload** | [**RegisterPayload**](RegisterPayload.md)|  | 

### Return type

[**GenericResponse**](GenericResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **updateUserDataAccountProfilePut**
> GenericResponse updateUserDataAccountProfilePut(userData)

Update User Data

Update the user profile data.  This endpoint updates the user profile data for the currently authenticated user, using either an OAuth2 token or a session cookie for authentication.

### Example
```dart
import 'package:openapi/api.dart';
// TODO Configure OAuth2 access token for authorization: OAuth2PasswordBearer
//defaultApiClient.getAuthentication<OAuth>('OAuth2PasswordBearer').accessToken = 'YOUR_ACCESS_TOKEN';

final api_instance = AccountEndpointsApi();
final userData = UserData(); // UserData | 

try {
    final result = api_instance.updateUserDataAccountProfilePut(userData);
    print(result);
} catch (e) {
    print('Exception when calling AccountEndpointsApi->updateUserDataAccountProfilePut: $e\n');
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **userData** | [**UserData**](UserData.md)|  | 

### Return type

[**GenericResponse**](GenericResponse.md)

### Authorization

[OAuth2PasswordBearer](../README.md#OAuth2PasswordBearer)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

