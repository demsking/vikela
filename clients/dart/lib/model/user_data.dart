//
// AUTO-GENERATED FILE, DO NOT MODIFY!
//
// @dart=2.18

// ignore_for_file: unused_element, unused_import
// ignore_for_file: always_put_required_named_parameters_first
// ignore_for_file: constant_identifier_names
// ignore_for_file: lines_longer_than_80_chars

part of openapi.api;

class UserData {
  /// Returns a new [UserData] instance.
  UserData({
    required this.email,
    required this.firstName,
    required this.lastName,
    required this.dateOfBirth,
    this.gender,
    this.address,
    this.phoneNumber,
    this.interests = const [],
    this.bio,
    this.profilePictureUrl,
    this.socialLinks,
  });

  String email;

  String firstName;

  String lastName;

  String dateOfBirth;

  UserDataGenderEnum? gender;

  String? address;

  String? phoneNumber;

  List<String>? interests;

  String? bio;

  String? profilePictureUrl;

  Object? socialLinks;

  @override
  bool operator ==(Object other) => identical(this, other) || other is UserData &&
    other.email == email &&
    other.firstName == firstName &&
    other.lastName == lastName &&
    other.dateOfBirth == dateOfBirth &&
    other.gender == gender &&
    other.address == address &&
    other.phoneNumber == phoneNumber &&
    _deepEquality.equals(other.interests, interests) &&
    other.bio == bio &&
    other.profilePictureUrl == profilePictureUrl &&
    other.socialLinks == socialLinks;

  @override
  int get hashCode =>
    // ignore: unnecessary_parenthesis
    (email.hashCode) +
    (firstName.hashCode) +
    (lastName.hashCode) +
    (dateOfBirth.hashCode) +
    (gender == null ? 0 : gender!.hashCode) +
    (address == null ? 0 : address!.hashCode) +
    (phoneNumber == null ? 0 : phoneNumber!.hashCode) +
    (interests == null ? 0 : interests!.hashCode) +
    (bio == null ? 0 : bio!.hashCode) +
    (profilePictureUrl == null ? 0 : profilePictureUrl!.hashCode) +
    (socialLinks == null ? 0 : socialLinks!.hashCode);

  @override
  String toString() => 'UserData[email=$email, firstName=$firstName, lastName=$lastName, dateOfBirth=$dateOfBirth, gender=$gender, address=$address, phoneNumber=$phoneNumber, interests=$interests, bio=$bio, profilePictureUrl=$profilePictureUrl, socialLinks=$socialLinks]';

  Map<String, dynamic> toJson() {
    final json = <String, dynamic>{};
      json[r'email'] = this.email;
      json[r'first_name'] = this.firstName;
      json[r'last_name'] = this.lastName;
      json[r'date_of_birth'] = this.dateOfBirth;
    if (this.gender != null) {
      json[r'gender'] = this.gender;
    } else {
      json[r'gender'] = null;
    }
    if (this.address != null) {
      json[r'address'] = this.address;
    } else {
      json[r'address'] = null;
    }
    if (this.phoneNumber != null) {
      json[r'phone_number'] = this.phoneNumber;
    } else {
      json[r'phone_number'] = null;
    }
    if (this.interests != null) {
      json[r'interests'] = this.interests;
    } else {
      json[r'interests'] = null;
    }
    if (this.bio != null) {
      json[r'bio'] = this.bio;
    } else {
      json[r'bio'] = null;
    }
    if (this.profilePictureUrl != null) {
      json[r'profile_picture_url'] = this.profilePictureUrl;
    } else {
      json[r'profile_picture_url'] = null;
    }
    if (this.socialLinks != null) {
      json[r'social_links'] = this.socialLinks;
    } else {
      json[r'social_links'] = null;
    }
    return json;
  }

  /// Returns a new [UserData] instance and imports its values from
  /// [value] if it's a [Map], null otherwise.
  // ignore: prefer_constructors_over_static_methods
  static UserData? fromJson(dynamic value) {
    if (value is Map) {
      final json = value.cast<String, dynamic>();

      // Ensure that the map contains the required keys.
      // Note 1: the values aren't checked for validity beyond being non-null.
      // Note 2: this code is stripped in release mode!
      assert(() {
        requiredKeys.forEach((key) {
          assert(json.containsKey(key), 'Required key "UserData[$key]" is missing from JSON.');
          assert(json[key] != null, 'Required key "UserData[$key]" has a null value in JSON.');
        });
        return true;
      }());

      return UserData(
        email: mapValueOfType<String>(json, r'email')!,
        firstName: mapValueOfType<String>(json, r'first_name')!,
        lastName: mapValueOfType<String>(json, r'last_name')!,
        dateOfBirth: mapValueOfType<String>(json, r'date_of_birth')!,
        gender: UserDataGenderEnum.fromJson(json[r'gender']),
        address: mapValueOfType<String>(json, r'address'),
        phoneNumber: mapValueOfType<String>(json, r'phone_number'),
        interests: json[r'interests'] is Iterable
            ? (json[r'interests'] as Iterable).cast<String>().toList(growable: false)
            : const [],
        bio: mapValueOfType<String>(json, r'bio'),
        profilePictureUrl: mapValueOfType<String>(json, r'profile_picture_url'),
        socialLinks: mapValueOfType<Object>(json, r'social_links'),
      );
    }
    return null;
  }

  static List<UserData> listFromJson(dynamic json, {bool growable = false,}) {
    final result = <UserData>[];
    if (json is List && json.isNotEmpty) {
      for (final row in json) {
        final value = UserData.fromJson(row);
        if (value != null) {
          result.add(value);
        }
      }
    }
    return result.toList(growable: growable);
  }

  static Map<String, UserData> mapFromJson(dynamic json) {
    final map = <String, UserData>{};
    if (json is Map && json.isNotEmpty) {
      json = json.cast<String, dynamic>(); // ignore: parameter_assignments
      for (final entry in json.entries) {
        final value = UserData.fromJson(entry.value);
        if (value != null) {
          map[entry.key] = value;
        }
      }
    }
    return map;
  }

  // maps a json object with a list of UserData-objects as value to a dart map
  static Map<String, List<UserData>> mapListFromJson(dynamic json, {bool growable = false,}) {
    final map = <String, List<UserData>>{};
    if (json is Map && json.isNotEmpty) {
      // ignore: parameter_assignments
      json = json.cast<String, dynamic>();
      for (final entry in json.entries) {
        map[entry.key] = UserData.listFromJson(entry.value, growable: growable,);
      }
    }
    return map;
  }

  /// The list of required keys that must be present in a JSON.
  static const requiredKeys = <String>{
    'email',
    'first_name',
    'last_name',
    'date_of_birth',
  };
}


class UserDataGenderEnum {
  /// Instantiate a new enum with the provided [value].
  const UserDataGenderEnum._(this.value);

  /// The underlying value of this enum member.
  final String value;

  @override
  String toString() => value;

  String toJson() => value;

  static const male = UserDataGenderEnum._(r'male');
  static const female = UserDataGenderEnum._(r'female');

  /// List of all possible values in this [enum][UserDataGenderEnum].
  static const values = <UserDataGenderEnum>[
    male,
    female,
  ];

  static UserDataGenderEnum? fromJson(dynamic value) => UserDataGenderEnumTypeTransformer().decode(value);

  static List<UserDataGenderEnum> listFromJson(dynamic json, {bool growable = false,}) {
    final result = <UserDataGenderEnum>[];
    if (json is List && json.isNotEmpty) {
      for (final row in json) {
        final value = UserDataGenderEnum.fromJson(row);
        if (value != null) {
          result.add(value);
        }
      }
    }
    return result.toList(growable: growable);
  }
}

/// Transformation class that can [encode] an instance of [UserDataGenderEnum] to String,
/// and [decode] dynamic data back to [UserDataGenderEnum].
class UserDataGenderEnumTypeTransformer {
  factory UserDataGenderEnumTypeTransformer() => _instance ??= const UserDataGenderEnumTypeTransformer._();

  const UserDataGenderEnumTypeTransformer._();

  String encode(UserDataGenderEnum data) => data.value;

  /// Decodes a [dynamic value][data] to a UserDataGenderEnum.
  ///
  /// If [allowNull] is true and the [dynamic value][data] cannot be decoded successfully,
  /// then null is returned. However, if [allowNull] is false and the [dynamic value][data]
  /// cannot be decoded successfully, then an [UnimplementedError] is thrown.
  ///
  /// The [allowNull] is very handy when an API changes and a new enum value is added or removed,
  /// and users are still using an old app with the old code.
  UserDataGenderEnum? decode(dynamic data, {bool allowNull = true}) {
    if (data != null) {
      switch (data) {
        case r'male': return UserDataGenderEnum.male;
        case r'female': return UserDataGenderEnum.female;
        default:
          if (!allowNull) {
            throw ArgumentError('Unknown enum value to decode: $data');
          }
      }
    }
    return null;
  }

  /// Singleton [UserDataGenderEnumTypeTransformer] instance.
  static UserDataGenderEnumTypeTransformer? _instance;
}


