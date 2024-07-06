# DocumentUserDataComputedLocationAccountMeta


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | **str** |  | 
**data** | [**UserData**](UserData.md) |  | 
**id** | **str** |  | [optional] 
**rev** | **str** |  | [optional] 
**computed** | [**ComputedLocation**](ComputedLocation.md) |  | [optional] 
**meta** | [**AccountMeta**](AccountMeta.md) |  | [optional] 

## Example

```python
from vikela_client.models.document_user_data_computed_location_account_meta import DocumentUserDataComputedLocationAccountMeta

# TODO update the JSON string below
json = "{}"
# create an instance of DocumentUserDataComputedLocationAccountMeta from a JSON string
document_user_data_computed_location_account_meta_instance = DocumentUserDataComputedLocationAccountMeta.from_json(json)
# print the JSON string representation of the object
print(DocumentUserDataComputedLocationAccountMeta.to_json())

# convert the object into a dict
document_user_data_computed_location_account_meta_dict = document_user_data_computed_location_account_meta_instance.to_dict()
# create an instance of DocumentUserDataComputedLocationAccountMeta from a dict
document_user_data_computed_location_account_meta_from_dict = DocumentUserDataComputedLocationAccountMeta.from_dict(document_user_data_computed_location_account_meta_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


