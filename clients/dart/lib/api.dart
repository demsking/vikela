//
// AUTO-GENERATED FILE, DO NOT MODIFY!
//
// @dart=2.18

// ignore_for_file: unused_element, unused_import
// ignore_for_file: always_put_required_named_parameters_first
// ignore_for_file: constant_identifier_names
// ignore_for_file: lines_longer_than_80_chars

library openapi.api;

import 'dart:async';
import 'dart:convert';
import 'dart:io';

import 'package:collection/collection.dart';
import 'package:http/http.dart';
import 'package:intl/intl.dart';
import 'package:meta/meta.dart';

part 'api_client.dart';
part 'api_helper.dart';
part 'api_exception.dart';
part 'auth/authentication.dart';
part 'auth/api_key_auth.dart';
part 'auth/oauth.dart';
part 'auth/http_basic_auth.dart';
part 'auth/http_bearer_auth.dart';

part 'api/account_endpoints_api.dart';
part 'api/class1_fa_endpoints_api.dart';
part 'api/class2_fa_endpoints_api.dart';
part 'api/server_endpoints_api.dart';

part 'model/account_meta.dart';
part 'model/address.dart';
part 'model/computed_location.dart';
part 'model/document_user_data_computed_location_account_meta.dart';
part 'model/error_response.dart';
part 'model/generic_response.dart';
part 'model/get_access_token_response.dart';
part 'model/http_validation_error.dart';
part 'model/location.dart';
part 'model/postcode.dart';
part 'model/register_payload.dart';
part 'model/server_info.dart';
part 'model/user_data.dart';
part 'model/validation_error.dart';
part 'model/validation_error_loc_inner.dart';


/// An [ApiClient] instance that uses the default values obtained from
/// the OpenAPI specification file.
var defaultApiClient = ApiClient();

const _delimiters = {'csv': ',', 'ssv': ' ', 'tsv': '\t', 'pipes': '|'};
const _dateEpochMarker = 'epoch';
const _deepEquality = DeepCollectionEquality();
final _dateFormatter = DateFormat('yyyy-MM-dd');
final _regList = RegExp(r'^List<(.*)>$');
final _regSet = RegExp(r'^Set<(.*)>$');
final _regMap = RegExp(r'^Map<String,(.*)>$');

bool _isEpochMarker(String? pattern) => pattern == _dateEpochMarker || pattern == '/$_dateEpochMarker/';
