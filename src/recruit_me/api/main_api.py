"""Define the api endpoints."""

from pathlib import Path
import shutil
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
import uvicorn

from recruit_me.backend.recruit_me_core import RecruitMe
from recruit_me.models.endpoint_models import EmailSendingEndpointModel, UpdateAnswerEndpointModel
from recruit_me.utils.configuration import MainConfig

app = FastAPI(
    title="Recruit_me",
    description="Program that automates the process of sending CVs and tracking the status of submitted applications.",
    summary="Life is to short to have to spend energy on sending CVs.",
    version="0.0.1"
)

STATUS_SUCCESS = 200
STATUS_FILE_ALREADY_EXISTS = 409
STATUS_INTERNAL_ERROR = 500
STATUS_BAD_REQUEST = 400

@app.get('/health')
def get_health()->dict:
    """Health endpoint.

    Returns:
        int: Status 200 if everything is fine.
    """
    return {"status_code" : STATUS_SUCCESS}

@app.post('/upload_template')
def upload_template(file: UploadFile | None = None)->dict:
    """Permit to upload a template to the available resources.

    Args:
        file (UploadFile): Template to upload.

    Returns:
        int: Status of the task.
    """
    if file is None:
        file = File(...)
    
    template_location = RecruitMe().get_template_folder()
    authorized_template_formats = ['.txt', '.html']

    if not file.filename.endswith(tuple(authorized_template_formats)):
        return { 
            'status_code': STATUS_BAD_REQUEST,
            'description': f'Unauthorized file format. The ones accepted are {" ,".join(map(str, authorized_template_formats))}'
            }


    if template_location.joinpath(file.filename).exists():
        return { 
            'status_code': STATUS_FILE_ALREADY_EXISTS,
            'description': 'The template already exists.'
            }
    try:
        with template_location.joinpath(file.filename).open('wb') as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        return { 
            'status_code': STATUS_INTERNAL_ERROR,
            'description': f'Internal error while saving : {e}'
        }
    return {
        'status_code': STATUS_SUCCESS,
        'description': f'Template saved as {file.filename}.'
    }
    
@app.post('/upload_cv')
def upload_cv(file: UploadFile | None = None)->dict:
    """Permit to upload a cv to the available resources.

    Args:
        file (UploadFile): CV to upload.

    Returns:
        int: Status of the task.
    """
    if file is None:
        file = File(...)
    
    template_location = RecruitMe().get_cv_folder()
    authorized_template_formats = ['.pdf']

    if not file.filename.endswith(tuple(authorized_template_formats)):
        return { 
            'status_code': STATUS_BAD_REQUEST,
            'description': f'Unauthorized file format. The ones accepted are {" ,".join(map(str, authorized_template_formats))}'
            }


    if template_location.joinpath(file.filename).exists():
        return { 
            'status_code': STATUS_FILE_ALREADY_EXISTS,
            'description': 'The cv already exists.'
            }
    try:
        with template_location.joinpath(file.filename).open('wb') as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        return { 
            'status_code': STATUS_INTERNAL_ERROR,
            'description': f'Internal error while saving : {e}'
        }
    return {
        'status_code': STATUS_SUCCESS,
        'description': f'Template saved as {file.filename}.'
    }

@app.get('/get_cv_list')
def get_cv_list()->dict:
    """Retrieve the list of uploaded cvs.

    Returns:
        dict: List of cvs uploaded.
    """
    try:
        cv_list = RecruitMe().get_cv_list()
    except Exception as e:
        return {
            'status_code': STATUS_INTERNAL_ERROR,
            'description': f'Internal error : {e}'
        }
    return {
        'status_code': STATUS_SUCCESS,
        'description': ' '.join(map(str, cv_list))
    }

@app.get('/get_template_list')
def get_template_list()->dict:
    """Retrieve the list of uploaded templates.

    Returns:
        dict: List of templates uploaded.
    """
    try:
        cv_list = RecruitMe().get_template_list()
    except Exception as e:
        return {
            'status_code': STATUS_INTERNAL_ERROR,
            'description': f'Internal error : {e}'
        }
    return {
        'status_code': STATUS_SUCCESS,
        'description': ' '.join(map(str, cv_list))
    }

@app.post('/send_email')
def send_email(email_data: EmailSendingEndpointModel)->dict:
    """Endpoint used to send emails.

    Args:
        email_data (EmailSendingEndpointModel): _description_

    Returns:
        dict: _description_
    """
    RecruitMe().send_email(
        email_recipient=email_data.email_recipient,
        email_object= email_data.email_object,
        cv_filename=email_data.cv_filename,
        cover_letter_template_filename=email_data.cover_letter_template_filename,
        email_template_filename=email_data.email_template_filename
    )
    return {
        'status_code': STATUS_SUCCESS,
        'description': f'Email successfully sent to {email_data.email_recipient.email}'
    }

@app.get("/download_summary", response_class=FileResponse, response_model=None)
def download_summary() -> FileResponse:
    """Endpoint to download the summary file.

    Returns:
        FileResponse: The requested file if it exists.
    """
    file_path = Path.home().joinpath(f'{MainConfig().home_folder}/{MainConfig().csv_file}')

    if not file_path.exists():
        return {
            'status_code': STATUS_SUCCESS,
            'description': 'The CSV is empty, send emails first.'
        }

    return FileResponse(
        path=file_path,
        media_type="application/octet-stream",
        filename=MainConfig().csv_file
    )

@app.post('/update_answer')
def update_answer(data: UpdateAnswerEndpointModel)->dict:
    try:
        RecruitMe().update_response_status(
            data.email,
            data.new_answer
        )
    except Exception as e:
        return {
            'status_code': STATUS_INTERNAL_ERROR,
            'description': f'Internal error : {e}'
        }
    return {
        'status_code': STATUS_SUCCESS,
        'description': 'Data updated'
    }

if __name__ == '__main__': #pragma: no cover
    uvicorn.run("main_api:app", host="0.0.0.0", port=8100, reload=True)

