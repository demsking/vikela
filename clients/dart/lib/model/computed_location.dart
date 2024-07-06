//
// AUTO-GENERATED FILE, DO NOT MODIFY!
//
// @dart=2.18

// ignore_for_file: unused_element, unused_import
// ignore_for_file: always_put_required_named_parameters_first
// ignore_for_file: constant_identifier_names
// ignore_for_file: lines_longer_than_80_chars

part of openapi.api;

class ComputedLocation {
  /// Returns a new [ComputedLocation] instance.
  ComputedLocation({
    required this.location,
  });

  Location location;

  @override
  bool operator ==(Object other) => identical(this, other) || other is ComputedLocation &&
    other.location == location;

  @override
  int get hashCode =>
    // ignore: unnecessary_parenthesis
    (location.hashCode);

  @override
  String toString() => 'ComputedLocation[location=$location]';

  Map<String, dynamic> toJson() {
    final json = <String, dynamic>{};
      json[r'location'] = this.location;
    return json;
  }

  /// Returns a new [ComputedLocation] instance and imports its values from
  /// [value] if it's a [Map], null otherwise.
  // ignore: prefer_constructors_over_static_methods
  static ComputedLocation? fromJson(dynamic value) {
    if (value is Map) {
      final json = value.cast<String, dynamic>();

      // Ensure that the map contains the required keys.
      // Note 1: the values aren't checked for validity beyond being non-null.
      // Note 2: this code is stripped in release mode!
      assert(() {
        requiredKeys.forEach((key) {
          assert(json.containsKey(key), 'Required key "ComputedLocation[$key]" is missing from JSON.');
          assert(json[key] != null, 'Required key "ComputedLocation[$key]" has a null value in JSON.');
        });
        return true;
      }());

      return ComputedLocation(
        location: Location.fromJson(json[r'location'])!,
      );
    }
    return null;
  }

  static List<ComputedLocation> listFromJson(dynamic json, {bool growable = false,}) {
    final result = <ComputedLocation>[];
    if (json is List && json.isNotEmpty) {
      for (final row in json) {
        final value = ComputedLocation.fromJson(row);
        if (value != null) {
          result.add(value);
        }
      }
    }
    return result.toList(growable: growable);
  }

  static Map<String, ComputedLocation> mapFromJson(dynamic json) {
    final map = <String, ComputedLocation>{};
    if (json is Map && json.isNotEmpty) {
      json = json.cast<String, dynamic>(); // ignore: parameter_assignments
      for (final entry in json.entries) {
        final value = ComputedLocation.fromJson(entry.value);
        if (value != null) {
          map[entry.key] = value;
        }
      }
    }
    return map;
  }

  // maps a json object with a list of ComputedLocation-objects as value to a dart map
  static Map<String, List<ComputedLocation>> mapListFromJson(dynamic json, {bool growable = false,}) {
    final map = <String, List<ComputedLocation>>{};
    if (json is Map && json.isNotEmpty) {
      // ignore: parameter_assignments
      json = json.cast<String, dynamic>();
      for (final entry in json.entries) {
        map[entry.key] = ComputedLocation.listFromJson(entry.value, growable: growable,);
      }
    }
    return map;
  }

  /// The list of required keys that must be present in a JSON.
  static const requiredKeys = <String>{
    'location',
  };
}

