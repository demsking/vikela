# UserData


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**email** | **str** |  | 
**first_name** | **str** |  | 
**last_name** | **str** |  | 
**date_of_birth** | **str** |  | 
**gender** | **str** |  | [optional] 
**address** | **str** |  | [optional] 
**phone_number** | **str** |  | [optional] 
**interests** | **List[str]** |  | [optional] 
**bio** | **str** |  | [optional] 
**profile_picture_url** | **str** |  | [optional] 
**social_links** | **object** |  | [optional] 

## Example

```python
from vikela_client.models.user_data import UserData

# TODO update the JSON string below
json = "{}"
# create an instance of UserData from a JSON string
user_data_instance = UserData.from_json(json)
# print the JSON string representation of the object
print(UserData.to_json())

# convert the object into a dict
user_data_dict = user_data_instance.to_dict()
# create an instance of UserData from a dict
user_data_from_dict = UserData.from_dict(user_data_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


