# openapi.api.ServerEndpointsApi

## Load the API package
```dart
import 'package:openapi/api.dart';
```

All URIs are relative to */api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**getServerInfoGet**](ServerEndpointsApi.md#getserverinfoget) | **GET** / | Get Server Info


# **getServerInfoGet**
> ServerInfo getServerInfoGet()

Get Server Info

Endpoint to retrieve server information.

### Example
```dart
import 'package:openapi/api.dart';

final api_instance = ServerEndpointsApi();

try {
    final result = api_instance.getServerInfoGet();
    print(result);
} catch (e) {
    print('Exception when calling ServerEndpointsApi->getServerInfoGet: $e\n');
}
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

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

