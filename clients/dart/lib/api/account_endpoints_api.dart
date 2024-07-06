//
// AUTO-GENERATED FILE, DO NOT MODIFY!
//
// @dart=2.18

// ignore_for_file: unused_element, unused_import
// ignore_for_file: always_put_required_named_parameters_first
// ignore_for_file: constant_identifier_names
// ignore_for_file: lines_longer_than_80_chars

part of openapi.api;


class AccountEndpointsApi {
  AccountEndpointsApi([ApiClient? apiClient]) : apiClient = apiClient ?? defaultApiClient;

  final ApiClient apiClient;

  /// Get User Document
  ///
  /// Retrieve the user document using a token.  This endpoint retrieves the user document for the currently authenticated user based on the provided token.
  ///
  /// Note: This method returns the HTTP [Response].
  Future<Response> getUserDocumentAccountMeGetWithHttpInfo() async {
    // ignore: prefer_const_declarations
    final path = r'/account/me';

    // ignore: prefer_final_locals
    Object? postBody;

    final queryParams = <QueryParam>[];
    final headerParams = <String, String>{};
    final formParams = <String, String>{};

    const contentTypes = <String>[];


    return apiClient.invokeAPI(
      path,
      'GET',
      queryParams,
      postBody,
      headerParams,
      formParams,
      contentTypes.isEmpty ? null : contentTypes.first,
    );
  }

  /// Get User Document
  ///
  /// Retrieve the user document using a token.  This endpoint retrieves the user document for the currently authenticated user based on the provided token.
  Future<DocumentUserDataComputedLocationAccountMeta?> getUserDocumentAccountMeGet() async {
    final response = await getUserDocumentAccountMeGetWithHttpInfo();
    if (response.statusCode >= HttpStatus.badRequest) {
      throw ApiException(response.statusCode, await _decodeBodyBytes(response));
    }
    // When a remote server returns no body with a status of 204, we shall not decode it.
    // At the time of writing this, `dart:convert` will throw an "Unexpected end of input"
    // FormatException when trying to decode an empty string.
    if (response.body.isNotEmpty && response.statusCode != HttpStatus.noContent) {
      return await apiClient.deserializeAsync(await _decodeBodyBytes(response), 'DocumentUserDataComputedLocationAccountMeta',) as DocumentUserDataComputedLocationAccountMeta;
    
    }
    return null;
  }

  /// Register User
  ///
  /// Register a new user in the database.
  ///
  /// Note: This method returns the HTTP [Response].
  ///
  /// Parameters:
  ///
  /// * [RegisterPayload] registerPayload (required):
  Future<Response> registerUserAccountPostWithHttpInfo(RegisterPayload registerPayload,) async {
    // ignore: prefer_const_declarations
    final path = r'/account';

    // ignore: prefer_final_locals
    Object? postBody = registerPayload;

    final queryParams = <QueryParam>[];
    final headerParams = <String, String>{};
    final formParams = <String, String>{};

    const contentTypes = <String>['application/json'];


    return apiClient.invokeAPI(
      path,
      'POST',
      queryParams,
      postBody,
      headerParams,
      formParams,
      contentTypes.isEmpty ? null : contentTypes.first,
    );
  }

  /// Register User
  ///
  /// Register a new user in the database.
  ///
  /// Parameters:
  ///
  /// * [RegisterPayload] registerPayload (required):
  Future<GenericResponse?> registerUserAccountPost(RegisterPayload registerPayload,) async {
    final response = await registerUserAccountPostWithHttpInfo(registerPayload,);
    if (response.statusCode >= HttpStatus.badRequest) {
      throw ApiException(response.statusCode, await _decodeBodyBytes(response));
    }
    // When a remote server returns no body with a status of 204, we shall not decode it.
    // At the time of writing this, `dart:convert` will throw an "Unexpected end of input"
    // FormatException when trying to decode an empty string.
    if (response.body.isNotEmpty && response.statusCode != HttpStatus.noContent) {
      return await apiClient.deserializeAsync(await _decodeBodyBytes(response), 'GenericResponse',) as GenericResponse;
    
    }
    return null;
  }

  /// Update User Data
  ///
  /// Update the user profile data.  This endpoint updates the user profile data for the currently authenticated user, using either an OAuth2 token or a session cookie for authentication.
  ///
  /// Note: This method returns the HTTP [Response].
  ///
  /// Parameters:
  ///
  /// * [UserData] userData (required):
  Future<Response> updateUserDataAccountProfilePutWithHttpInfo(UserData userData,) async {
    // ignore: prefer_const_declarations
    final path = r'/account/profile';

    // ignore: prefer_final_locals
    Object? postBody = userData;

    final queryParams = <QueryParam>[];
    final headerParams = <String, String>{};
    final formParams = <String, String>{};

    const contentTypes = <String>['application/json'];


    return apiClient.invokeAPI(
      path,
      'PUT',
      queryParams,
      postBody,
      headerParams,
      formParams,
      contentTypes.isEmpty ? null : contentTypes.first,
    );
  }

  /// Update User Data
  ///
  /// Update the user profile data.  This endpoint updates the user profile data for the currently authenticated user, using either an OAuth2 token or a session cookie for authentication.
  ///
  /// Parameters:
  ///
  /// * [UserData] userData (required):
  Future<GenericResponse?> updateUserDataAccountProfilePut(UserData userData,) async {
    final response = await updateUserDataAccountProfilePutWithHttpInfo(userData,);
    if (response.statusCode >= HttpStatus.badRequest) {
      throw ApiException(response.statusCode, await _decodeBodyBytes(response));
    }
    // When a remote server returns no body with a status of 204, we shall not decode it.
    // At the time of writing this, `dart:convert` will throw an "Unexpected end of input"
    // FormatException when trying to decode an empty string.
    if (response.body.isNotEmpty && response.statusCode != HttpStatus.noContent) {
      return await apiClient.deserializeAsync(await _decodeBodyBytes(response), 'GenericResponse',) as GenericResponse;
    
    }
    return null;
  }
}
