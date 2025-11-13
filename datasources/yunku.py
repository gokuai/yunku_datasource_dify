from collections.abc import Generator
from dify_plugin.entities.datasource import (
    DatasourceMessage,
    OnlineDriveBrowseFilesRequest,
    OnlineDriveBrowseFilesResponse,
    OnlineDriveDownloadFileRequest,
    OnlineDriveFile,
    OnlineDriveFileBucket,
)
from dify_plugin.interfaces.datasource.online_drive import OnlineDriveDatasource
from GoKuai.file import File
import requests
import mimetypes
import os


class YunkuDataSource(OnlineDriveDatasource):
    def _browse_files(
        self, request: OnlineDriveBrowseFilesRequest
    ) -> OnlineDriveBrowseFilesResponse:
        credentials = self.runtime.credentials
        # bucket_name = request.bucket
        prefix = request.prefix or ""
        max_keys = request.max_keys or 100
        next_page_parameters = request.next_page_parameters or {}


        if not credentials:
            raise ValueError("Credentials not found")

        sdk = File(
            credentials.get("client_id"),
            credentials.get("client_secret"),
                            credentials.get("base_url"),

        )

        start = next_page_parameters.get("start", 0)

        post = {
            "fullpath": prefix,
            "size": max_keys,
            "start": next_page_parameters.get("start", 0),
        }

        isOk = sdk.callApi("POST", "/1/file/ls", {}, post)
        if isOk is False:
            raise ValueError("Error")
        response = sdk.getHttpResponse(True)

        next_page_parameters["start"] = start + max_keys
        is_truncated = response.get("count") > next_page_parameters.get("start", 0)

        files = []
        for file in response.get("list", []):
            if file.get("dir") == 0:
                file_type = "file"
            else:
                file_type = "folder"
            files.append(
                OnlineDriveFile(
                    id=prefix + "/" + file.get("filename"),
                    name=file.get("filename"),
                    size=file.get("filesize"),
                    type=file_type,
                )  # or "file"
            )

        return OnlineDriveBrowseFilesResponse(
            result=[
                OnlineDriveFileBucket(
                    bucket="",
                    files=files,
                    is_truncated=is_truncated,
                    next_page_parameters=next_page_parameters,
                )
            ]
        )

    def _download_file(
        self, request: OnlineDriveDownloadFileRequest
    ) -> Generator[DatasourceMessage, None, None]:

        credentials = self.runtime.credentials
        fullpath = request.id
        if not credentials:
            raise ValueError("Credentials not found")

        post = {
            "fullpath": fullpath,
        }

        sdk = File(
            credentials.get("client_id"),
            credentials.get("client_secret"),
            credentials.get("base_url"),
        )

        isOk = sdk.callApi("POST", "/1/file/download_url", {}, post)
        if isOk is False:
            raise ValueError("download_url request failed")
        response = sdk.getHttpResponse(True)

        file_name = self._get_filename_from_url(fullpath)
        mime_type = self._get_mime_type_from_filename(file_name)

        url = response.get("urls", [])
        
        if len(url) > 0:
            file_content = requests.get(url[0]).content
        else:
            raise ValueError("url not found")
        
        yield self.create_blob_message(
            file_content, meta={"file_name": file_name, "mime_type": mime_type}
        )


    def _get_mime_type_from_filename(self, filename: str) -> str:
        mime_type, _ = mimetypes.guess_type(filename)
        return mime_type or "application/octet-stream"

    def _get_filename_from_url(self, url: str) -> str:
        filename = os.path.basename(url)
        return filename
