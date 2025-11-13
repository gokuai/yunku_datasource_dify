from typing import Any, Mapping
from GoKuai.file import File


from dify_plugin.errors.tool import ToolProviderCredentialValidationError
from dify_plugin.interfaces.datasource import DatasourceProvider


class YunkuDatasourceProvider(DatasourceProvider):
    def _validate_credentials(self, credentials: Mapping[str, Any]) -> None:
        try:
            if not credentials.get("client_id"):
                raise ToolProviderCredentialValidationError(
                    "client_id is required."
                )
            if not credentials or not credentials.get("client_secret"):
                raise ToolProviderCredentialValidationError(
                    "client_secret is required."
                )

            sdk = File(
                credentials.get("client_id"),
                credentials.get("client_secret"),
                credentials.get("base_url"),
            )
            data = sdk.callApi("POST", "/1/file/ls",{}, {"fullpath":""})
            if data is False:
                raise ToolProviderCredentialValidationError(
                    "client_id or client_secret is invalid."
                )
            
           
        except Exception as e:
            raise ToolProviderCredentialValidationError(str(e))