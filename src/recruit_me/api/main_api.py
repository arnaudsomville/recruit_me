"""Define the api endpoints."""

import shutil
from fastapi import FastAPI, File, UploadFile
import uvicorn

from recruit_me.backend.recruit_me_core import RecruitMe

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

if __name__ == '__main__': #pragma: no cover
    uvicorn.run("main_api:app", host="0.0.0.0", port=8100, reload=True)

