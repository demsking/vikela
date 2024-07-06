//
// AUTO-GENERATED FILE, DO NOT MODIFY!
//
// @dart=2.18

// ignore_for_file: unused_element, unused_import
// ignore_for_file: always_put_required_named_parameters_first
// ignore_for_file: constant_identifier_names
// ignore_for_file: lines_longer_than_80_chars

part of openapi.api;

class Address {
  /// Returns a new [Address] instance.
  Address({
    required this.country,
    required this.countryCode,
    this.region,
    this.postcode,
    this.road,
    this.town,
    this.municipality,
    this.county,
    this.state,
    this.city,
  });

  String country;

  String countryCode;

  String? region;

  Postcode? postcode;

  String? road;

  String? town;

  String? municipality;

  String? county;

  String? state;

  String? city;

  @override
  bool operator ==(Object other) => identical(this, other) || other is Address &&
    other.country == country &&
    other.countryCode == countryCode &&
    other.region == region &&
    other.postcode == postcode &&
    other.road == road &&
    other.town == town &&
    other.municipality == municipality &&
    other.county == county &&
    other.state == state &&
    other.city == city;

  @override
  int get hashCode =>
    // ignore: unnecessary_parenthesis
    (country.hashCode) +
    (countryCode.hashCode) +
    (region == null ? 0 : region!.hashCode) +
    (postcode == null ? 0 : postcode!.hashCode) +
    (road == null ? 0 : road!.hashCode) +
    (town == null ? 0 : town!.hashCode) +
    (municipality == null ? 0 : municipality!.hashCode) +
    (county == null ? 0 : county!.hashCode) +
    (state == null ? 0 : state!.hashCode) +
    (city == null ? 0 : city!.hashCode);

  @override
  String toString() => 'Address[country=$country, countryCode=$countryCode, region=$region, postcode=$postcode, road=$road, town=$town, municipality=$municipality, county=$county, state=$state, city=$city]';

  Map<String, dynamic> toJson() {
    final json = <String, dynamic>{};
      json[r'country'] = this.country;
      json[r'country_code'] = this.countryCode;
    if (this.region != null) {
      json[r'region'] = this.region;
    } else {
      json[r'region'] = null;
    }
    if (this.postcode != null) {
      json[r'postcode'] = this.postcode;
    } else {
      json[r'postcode'] = null;
    }
    if (this.road != null) {
      json[r'road'] = this.road;
    } else {
      json[r'road'] = null;
    }
    if (this.town != null) {
      json[r'town'] = this.town;
    } else {
      json[r'town'] = null;
    }
    if (this.municipality != null) {
      json[r'municipality'] = this.municipality;
    } else {
      json[r'municipality'] = null;
    }
    if (this.county != null) {
      json[r'county'] = this.county;
    } else {
      json[r'county'] = null;
    }
    if (this.state != null) {
      json[r'state'] = this.state;
    } else {
      json[r'state'] = null;
    }
    if (this.city != null) {
      json[r'city'] = this.city;
    } else {
      json[r'city'] = null;
    }
    return json;
  }

  /// Returns a new [Address] instance and imports its values from
  /// [value] if it's a [Map], null otherwise.
  // ignore: prefer_constructors_over_static_methods
  static Address? fromJson(dynamic value) {
    if (value is Map) {
      final json = value.cast<String, dynamic>();

      // Ensure that the map contains the required keys.
      // Note 1: the values aren't checked for validity beyond being non-null.
      // Note 2: this code is stripped in release mode!
      assert(() {
        requiredKeys.forEach((key) {
          assert(json.containsKey(key), 'Required key "Address[$key]" is missing from JSON.');
          assert(json[key] != null, 'Required key "Address[$key]" has a null value in JSON.');
        });
        return true;
      }());

      return Address(
        country: mapValueOfType<String>(json, r'country')!,
        countryCode: mapValueOfType<String>(json, r'country_code')!,
        region: mapValueOfType<String>(json, r'region'),
        postcode: Postcode.fromJson(json[r'postcode']),
        road: mapValueOfType<String>(json, r'road'),
        town: mapValueOfType<String>(json, r'town'),
        municipality: mapValueOfType<String>(json, r'municipality'),
        county: mapValueOfType<String>(json, r'county'),
        state: mapValueOfType<String>(json, r'state'),
        city: mapValueOfType<String>(json, r'city'),
      );
    }
    return null;
  }

  static List<Address> listFromJson(dynamic json, {bool growable = false,}) {
    final result = <Address>[];
    if (json is List && json.isNotEmpty) {
      for (final row in json) {
        final value = Address.fromJson(row);
        if (value != null) {
          result.add(value);
        }
      }
    }
    return result.toList(growable: growable);
  }

  static Map<String, Address> mapFromJson(dynamic json) {
    final map = <String, Address>{};
    if (json is Map && json.isNotEmpty) {
      json = json.cast<String, dynamic>(); // ignore: parameter_assignments
      for (final entry in json.entries) {
        final value = Address.fromJson(entry.value);
        if (value != null) {
          map[entry.key] = value;
        }
      }
    }
    return map;
  }

  // maps a json object with a list of Address-objects as value to a dart map
  static Map<String, List<Address>> mapListFromJson(dynamic json, {bool growable = false,}) {
    final map = <String, List<Address>>{};
    if (json is Map && json.isNotEmpty) {
      // ignore: parameter_assignments
      json = json.cast<String, dynamic>();
      for (final entry in json.entries) {
        map[entry.key] = Address.listFromJson(entry.value, growable: growable,);
      }
    }
    return map;
  }

  /// The list of required keys that must be present in a JSON.
  static const requiredKeys = <String>{
    'country',
    'country_code',
  };
}

