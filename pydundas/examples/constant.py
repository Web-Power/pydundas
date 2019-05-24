from pydundas import Api, Session

# If we are only looking at constants, there is no need to be actually logged in.
api = Api(None)
capi = api.constant()

print("Get direct value of STANDARD_EXCEL_EXPORT_PROVIDER_ID:")
print(capi.STANDARD_EXCEL_EXPORT_PROVIDER_ID)

print("One ID could be bound to multiple names, eg. 885dcdcb-7975-4f86-870d-77eb50d81b72:")
print(capi.getNamesById("885dcdcb-7975-4f86-870d-77eb50d81b72"))

print("Value of STANDARD_EXCEL_EXPORT_PROVIDER_ID using a getter:")
print(capi.getIdByName('STANDARD_EXCEL_EXPORT_PROVIDER_ID'))
