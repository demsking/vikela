//
// AUTO-GENERATED FILE, DO NOT MODIFY!
//
// @dart=2.18

// ignore_for_file: unused_element, unused_import
// ignore_for_file: always_put_required_named_parameters_first
// ignore_for_file: constant_identifier_names
// ignore_for_file: lines_longer_than_80_chars

part of openapi.api;

class DocumentUserDataComputedLocationAccountMeta {
  /// Returns a new [DocumentUserDataComputedLocationAccountMeta] instance.
  DocumentUserDataComputedLocationAccountMeta({
    required this.type,
    required this.data,
    this.id,
    this.rev,
    this.computed,
    this.meta,
  });

  String type;

  UserData data;

  ///
  /// Please note: This property should have been non-nullable! Since the specification file
  /// does not include a default value (using the "default:" property), however, the generated
  /// source code must fall back to having a nullable type.
  /// Consider adding a "default:" property in the specification file to hide this note.
  ///
  String? id;

  String? rev;

  ComputedLocation? computed;

  ///
  /// Please note: This property should have been non-nullable! Since the specification file
  /// does not include a default value (using the "default:" property), however, the generated
  /// source code must fall back to having a nullable type.
  /// Consider adding a "default:" property in the specification file to hide this note.
  ///
  AccountMeta? meta;

  @override
  bool operator ==(Object other) => identical(this, other) || other is DocumentUserDataComputedLocationAccountMeta &&
    other.type == type &&
    other.data == data &&
    other.id == id &&
    other.rev == rev &&
    other.computed == computed &&
    other.meta == meta;

  @override
  int get hashCode =>
    // ignore: unnecessary_parenthesis
    (type.hashCode) +
    (data.hashCode) +
    (id == null ? 0 : id!.hashCode) +
    (rev == null ? 0 : rev!.hashCode) +
    (computed == null ? 0 : computed!.hashCode) +
    (meta == null ? 0 : meta!.hashCode);

  @override
  String toString() => 'DocumentUserDataComputedLocationAccountMeta[type=$type, data=$data, id=$id, rev=$rev, computed=$computed, meta=$meta]';

  Map<String, dynamic> toJson() {
    final json = <String, dynamic>{};
      json[r'type'] = this.type;
      json[r'data'] = this.data;
    if (this.id != null) {
      json[r'_id'] = this.id;
    } else {
      json[r'_id'] = null;
    }
    if (this.rev != null) {
      json[r'_rev'] = this.rev;
    } else {
      json[r'_rev'] = null;
    }
    if (this.computed != null) {
      json[r'computed'] = this.computed;
    } else {
      json[r'computed'] = null;
    }
    if (this.meta != null) {
      json[r'meta'] = this.meta;
    } else {
      json[r'meta'] = null;
    }
    return json;
  }

  /// Returns a new [DocumentUserDataComputedLocationAccountMeta] instance and imports its values from
  /// [value] if it's a [Map], null otherwise.
  // ignore: prefer_constructors_over_static_methods
  static DocumentUserDataComputedLocationAccountMeta? fromJson(dynamic value) {
    if (value is Map) {
      final json = value.cast<String, dynamic>();

      // Ensure that the map contains the required keys.
      // Note 1: the values aren't checked for validity beyond being non-null.
      // Note 2: this code is stripped in release mode!
      assert(() {
        requiredKeys.forEach((key) {
          assert(json.containsKey(key), 'Required key "DocumentUserDataComputedLocationAccountMeta[$key]" is missing from JSON.');
          assert(json[key] != null, 'Required key "DocumentUserDataComputedLocationAccountMeta[$key]" has a null value in JSON.');
        });
        return true;
      }());

      return DocumentUserDataComputedLocationAccountMeta(
        type: mapValueOfType<String>(json, r'type')!,
        data: UserData.fromJson(json[r'data'])!,
        id: mapValueOfType<String>(json, r'_id'),
        rev: mapValueOfType<String>(json, r'_rev'),
        computed: ComputedLocation.fromJson(json[r'computed']),
        meta: AccountMeta.fromJson(json[r'meta']),
      );
    }
    return null;
  }

  static List<DocumentUserDataComputedLocationAccountMeta> listFromJson(dynamic json, {bool growable = false,}) {
    final result = <DocumentUserDataComputedLocationAccountMeta>[];
    if (json is List && json.isNotEmpty) {
      for (final row in json) {
        final value = DocumentUserDataComputedLocationAccountMeta.fromJson(row);
        if (value != null) {
          result.add(value);
        }
      }
    }
    return result.toList(growable: growable);
  }

  static Map<String, DocumentUserDataComputedLocationAccountMeta> mapFromJson(dynamic json) {
    final map = <String, DocumentUserDataComputedLocationAccountMeta>{};
    if (json is Map && json.isNotEmpty) {
      json = json.cast<String, dynamic>(); // ignore: parameter_assignments
      for (final entry in json.entries) {
        final value = DocumentUserDataComputedLocationAccountMeta.fromJson(entry.value);
        if (value != null) {
          map[entry.key] = value;
        }
      }
    }
    return map;
  }

  // maps a json object with a list of DocumentUserDataComputedLocationAccountMeta-objects as value to a dart map
  static Map<String, List<DocumentUserDataComputedLocationAccountMeta>> mapListFromJson(dynamic json, {bool growable = false,}) {
    final map = <String, List<DocumentUserDataComputedLocationAccountMeta>>{};
    if (json is Map && json.isNotEmpty) {
      // ignore: parameter_assignments
      json = json.cast<String, dynamic>();
      for (final entry in json.entries) {
        map[entry.key] = DocumentUserDataComputedLocationAccountMeta.listFromJson(entry.value, growable: growable,);
      }
    }
    return map;
  }

  /// The list of required keys that must be present in a JSON.
  static const requiredKeys = <String>{
    'type',
    'data',
  };
}

