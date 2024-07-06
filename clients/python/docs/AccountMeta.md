# AccountMeta


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**username** | **str** |  | 
**roles** | **List[str]** |  | 
**created_at** | **str** |  | [optional] 
**updated_at** | **str** |  | [optional] 

## Example

```python
from vikela_client.models.account_meta import AccountMeta

# TODO update the JSON string below
json = "{}"
# create an instance of AccountMeta from a JSON string
account_meta_instance = AccountMeta.from_json(json)
# print the JSON string representation of the object
print(AccountMeta.to_json())

# convert the object into a dict
account_meta_dict = account_meta_instance.to_dict()
# create an instance of AccountMeta from a dict
account_meta_from_dict = AccountMeta.from_dict(account_meta_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


