from fastapi import APIRouter, BackgroundTasks, UploadFile

from application.handlers.file_manager_handler import FileManagerHandler


class UploadFileHttp:
    name = "file-manager"
    router = APIRouter(tags=[name])

    @staticmethod
    @router.post(
        path=f"/{name}/upload-file", description="Supported formats: .parquet and .csv"
    )
    async def upload_file(
        file: UploadFile, background_task: BackgroundTasks, overwrite: bool = False
    ):
        file_content = await file.read()
        await file.close()
        background_task.add_task(
            FileManagerHandler.store_metadata,
            file_content=file_content,
            file_name=file.filename,
            overwrite=overwrite,
        )
        return {"response": True}
