import os
import shutil
from typing import Optional, List
import subprocess
import tempfile

import json

from pydantic import BaseModel

from fastapi import APIRouter, Response, File, UploadFile, Form
from fastapi import HTTPException, status, BackgroundTasks
from fastapi.responses import FileResponse


router = APIRouter()


GLKERNEL_DIRECTORY = os.environ.get('GLKERNEL_DIRECTORY', '')
RESULT_DIR = os.environ.get('RESULT_DIR', '/data/results')
WORKING_DIRECTORY = '/opt/dependencies/glkernel/'


def remove_temporary_files(file_ids, file_names):
    for f, f_name in zip(file_ids, file_names):
        print("Remove", f_name, flush=True)
        try:
            os.close(f)
            os.remove(f_name)
        except:
            pass


# ROOT

@router.get("/", tags=[""])
async def get_root():
    return {}


@router.head("/", tags=[""])
async def head_root(response: Response):
    response.status_code = status.HTTP_200_OK


# IMAGES

@router.post("/image_from_script", tags=["image"])
async def get_image_from_script(background_tasks: BackgroundTasks, script: str = Form(...)):
    script_f, script_f_name = tempfile.mkstemp(suffix=".js", text=True)
    with open(script_f, 'w+t') as f:
        f.write(script)

    image_f, image_f_name = tempfile.mkstemp(suffix=".png", text=False)

    glkernel_binary = os.path.join(GLKERNEL_DIRECTORY, 'glkernel-cli')
    arguments = [ glkernel_binary, "run", "--force", "--output", image_f_name, "--format", ".png", script_f_name ]

    try:
        print(' '.join(arguments), flush=True)
        p = subprocess.run(arguments, capture_output=True, check=True, cwd=WORKING_DIRECTORY)
    except:
        print(p.stdout.decode("utf-8"), flush=True)
        print(p.stderr.decode("utf-8"), flush=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=p.stderr.decode("utf-8"),
        )
    
    background_tasks.add_task(remove_temporary_files, [script_f, image_f], [script_f_name, image_f_name])

    return FileResponse(image_f_name, filename="kernel.png", media_type='image/png')


@router.post("/image_from_script_file", tags=["image"])
async def get_image_from_script_file(background_tasks: BackgroundTasks, script_file: UploadFile = File(...)):
    script_f, script_f_name = tempfile.mkstemp(suffix=".js", text=True)
    with open(script_f, 'w+b') as f:
        shutil.copyfileobj(script_file.file, f)

    image_f, image_f_name = tempfile.mkstemp(suffix=".png", text=False)

    glkernel_binary = os.path.join(GLKERNEL_DIRECTORY, 'glkernel-cli')
    arguments = [ glkernel_binary, "run", "--force", "--output", image_f_name, "--format", ".png", script_f_name ]

    try:
        print(' '.join(arguments), flush=True)
        p = subprocess.run(arguments, capture_output=True, check=True, cwd=WORKING_DIRECTORY)
    except:
        print(p.stdout.decode("utf-8"), flush=True)
        print(p.stderr.decode("utf-8"), flush=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=p.stderr.decode("utf-8"),
        )

    background_tasks.add_task(remove_temporary_files, [script_f, image_f], [script_f_name, image_f_name])

    return FileResponse(image_f_name, filename="kernel.png", media_type='image/png')


@router.post("/image_from_declaration", tags=["image"])
async def get_image_from_declaration(background_tasks: BackgroundTasks, declaration: str = Form(...)):
    declaration_f, declaration_f_name = tempfile.mkstemp(suffix=".json", text=True)
    with open(declaration_f, 'w+t') as f:
        f.write(declaration)

    array_f, array_f_name = tempfile.mkstemp(suffix=".json", text=True)

    glkernel_binary = os.path.join(GLKERNEL_DIRECTORY, 'glkernel-cmd')
    arguments = [ glkernel_binary, "--i", declaration_f_name, "--o", array_f_name ]

    try:
        print(' '.join(arguments), flush=True)
        p = subprocess.run(arguments, capture_output=True, check=True, cwd=WORKING_DIRECTORY)
    except:
        print(p.stdout.decode("utf-8"), flush=True)
        print(p.stderr.decode("utf-8"), flush=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=p.stderr.decode("utf-8"),
        )

    image_f, image_f_name = tempfile.mkstemp(suffix=".png", text=False)

    glkernel_binary = os.path.join(GLKERNEL_DIRECTORY, 'glkernel-cli')
    arguments = [ glkernel_binary, "run", "--force", "--output", image_f_name, "--format", ".png", array_f_name ]

    try:
        print(' '.join(arguments), flush=True)
        p = subprocess.run(arguments, capture_output=True, check=True, cwd=WORKING_DIRECTORY)
    except:
        print(p.stdout.decode("utf-8"), flush=True)
        print(p.stderr.decode("utf-8"), flush=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=p.stderr.decode("utf-8"),
        )

    background_tasks.add_task(remove_temporary_files, [declaration_f, array_f, image_f], [declaration_f_name, array_f_name, image_f_names])

    return FileResponse(image_f_name, filename="kernel.png", media_type='image/png')


@router.post("/image_from_declaration_file", tags=["image"])
async def get_image_from_declaration_file(background_tasks: BackgroundTasks, declaration_file: UploadFile = File(...)):
    declaration_f, declaration_f_name = tempfile.mkstemp(suffix=".json", text=True)
    with open(declaration_f, 'w+b') as f:
        shutil.copyfileobj(declaration_file.file, f)

    array_f, array_f_name = tempfile.mkstemp(suffix=".json", text=True)

    glkernel_binary = os.path.join(GLKERNEL_DIRECTORY, 'glkernel-cmd')
    arguments = [ glkernel_binary, "--i", declaration_f_name, "--o", array_f_name ]

    try:
        print(' '.join(arguments), flush=True)
        p = subprocess.run(arguments, capture_output=True, check=True, cwd=WORKING_DIRECTORY)
    except:
        print(p.stdout.decode("utf-8"), flush=True)
        print(p.stderr.decode("utf-8"), flush=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=p.stderr.decode("utf-8"),
        )

    image_f, image_f_name = tempfile.mkstemp(suffix=".png", text=False)

    glkernel_binary = os.path.join(GLKERNEL_DIRECTORY, 'glkernel-cli')
    arguments = [ glkernel_binary, "run", "--force", "--output", image_f_name, "--format", ".png", array_f_name ]

    try:
        print(' '.join(arguments), flush=True)
        p = subprocess.run(arguments, capture_output=True, check=True, cwd=WORKING_DIRECTORY)
    except:
        print(p.stdout.decode("utf-8"), flush=True)
        print(p.stderr.decode("utf-8"), flush=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=p.stderr.decode("utf-8"),
        )

    background_tasks.add_task(remove_temporary_files, [declaration_f, array_f, image_f], [declaration_f_name, array_f_name, image_f_name])

    return FileResponse(image_f_name, filename="kernel.png", media_type='image/png')


@router.post("/image_from_array", tags=["image"])
async def get_image_from_array(background_tasks: BackgroundTasks, array: str = Form(...)):
    array_f, array_f_name = tempfile.mkstemp(suffix=".json", text=True)
    with open(array_f, 'w+t') as f:
        f.write(array)

    image_f, image_f_name = tempfile.mkstemp(suffix=".png", text=False)

    glkernel_binary = os.path.join(GLKERNEL_DIRECTORY, 'glkernel-cli')
    arguments = [ glkernel_binary, "run", "--force", "--output", image_f_name, "--format", ".png", array_f_name ]

    try:
        print(' '.join(arguments), flush=True)
        p = subprocess.run(arguments, capture_output=True, check=True, cwd=WORKING_DIRECTORY)
    except:
        print(p.stdout.decode("utf-8"), flush=True)
        print(p.stderr.decode("utf-8"), flush=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=p.stderr.decode("utf-8"),
        )

    background_tasks.add_task(remove_temporary_files, [array_f, image_f], [array_f_name, image_f_name])

    return FileResponse(image_f_name, filename="kernel.png", media_type='image/png')


@router.post("/image_from_array_file", tags=["image"])
async def get_image_from_array_file(background_tasks: BackgroundTasks, array_file: UploadFile = File(...)):
    array_f, array_f_name = tempfile.mkstemp(suffix=".json", text=True)
    with open(array_f, 'w+b') as f:
        shutil.copyfileobj(array_file.file, f)

    image_f, image_f_name = tempfile.mkstemp(suffix=".png", text=False)

    glkernel_binary = os.path.join(GLKERNEL_DIRECTORY, 'glkernel-cli')
    arguments = [ glkernel_binary, "run", "--force", "--output", image_f_name, "--format", ".png", array_f_name ]

    try:
        print(' '.join(arguments), flush=True)
        p = subprocess.run(arguments, capture_output=True, check=True, cwd=WORKING_DIRECTORY)
    except:
        print(p.stdout.decode("utf-8"), flush=True)
        print(p.stderr.decode("utf-8"), flush=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=p.stderr.decode("utf-8"),
        )

    background_tasks.add_task(remove_temporary_files, [array_f, image_f], [array_f_name, image_f_name])

    return FileResponse(image_f_name, filename="kernel.png", media_type='image/png')


# ARRAY

@router.post("/array_from_script", tags=["array"])
async def get_array_from_script(background_tasks: BackgroundTasks, script: str = Form(...)):
    script_f, script_f_name = tempfile.mkstemp(suffix=".js", text=True)
    with open(script_f, 'w+t') as f:
        f.write(script)

    array_f, array_f_name = tempfile.mkstemp(suffix=".json", text=False)

    glkernel_binary = os.path.join(GLKERNEL_DIRECTORY, 'glkernel-cli')
    arguments = [ glkernel_binary, "run", "--force", "--output", array_f_name, "--format", ".json", script_f_name ]

    try:
        print(' '.join(arguments), flush=True)
        p = subprocess.run(arguments, capture_output=True, check=True, cwd=WORKING_DIRECTORY)
    except:
        print(p.stdout.decode("utf-8"), flush=True)
        print(p.stderr.decode("utf-8"), flush=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=p.stderr.decode("utf-8"),
        )

    background_tasks.add_task(remove_temporary_files, [script_f, array_f], [script_f_name, array_f_name])

    return FileResponse(array_f_name, filename="kernel.json", media_type='application/json')


@router.post("/array_from_script_file", tags=["array"])
async def get_array_from_script_file(background_tasks: BackgroundTasks, script_file: UploadFile = File(...)):
    script_f, script_f_name = tempfile.mkstemp(suffix=".js", text=True)
    with open(script_f, 'w+b') as f:
        shutil.copyfileobj(script_file.file, f)

    array_f, array_f_name = tempfile.mkstemp(suffix=".json", text=False)

    glkernel_binary = os.path.join(GLKERNEL_DIRECTORY, 'glkernel-cli')
    arguments = [ glkernel_binary, "run", "--force", "--output", array_f_name, "--format", ".json", script_f_name ]

    try:
        print(' '.join(arguments), flush=True)
        p = subprocess.run(arguments, capture_output=True, check=True, cwd=WORKING_DIRECTORY)
    except:
        print(p.stdout.decode("utf-8"), flush=True)
        print(p.stderr.decode("utf-8"), flush=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=p.stderr.decode("utf-8"),
        )

    background_tasks.add_task(remove_temporary_files, [script_f, array_f], [script_f_name, array_f_name])

    return FileResponse(array_f_name, filename="kernel.json", media_type='application/json')


@router.post("/array_from_declaration", tags=["array"])
async def get_array_from_declaration(background_tasks: BackgroundTasks, declaration: str = Form(...)):
    declaration_f, declaration_f_name = tempfile.mkstemp(suffix=".json", text=True)
    with open(declaration_f, 'w+t') as f:
        f.write(declaration)

    array_f, array_f_name = tempfile.mkstemp(suffix=".json", text=True)

    glkernel_binary = os.path.join(GLKERNEL_DIRECTORY, 'glkernel-cmd')
    arguments = [ glkernel_binary, "--i", declaration_f_name, "--o", array_f_name ]

    try:
        print(' '.join(arguments), flush=True)
        p = subprocess.run(arguments, capture_output=True, check=True, cwd=WORKING_DIRECTORY)
    except:
        print(p.stdout.decode("utf-8"), flush=True)
        print(p.stderr.decode("utf-8"), flush=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=p.stderr.decode("utf-8"),
        )

    background_tasks.add_task(remove_temporary_files, [declaration_f, array_f], [declaration_f_name, array_f_name])

    return FileResponse(array_f_name, filename="kernel.json", media_type='application/json')


@router.post("/array_from_declaration_file", tags=["array"])
async def get_array_from_declaration_file(background_tasks: BackgroundTasks, declaration_file: UploadFile = File(...)):
    declaration_f, declaration_f_name = tempfile.mkstemp(suffix=".json", text=True)
    with open(declaration_f, 'w+b') as f:
        shutil.copyfileobj(declaration_file.file, f)

    array_f, array_f_name = tempfile.mkstemp(suffix=".json", text=True)

    glkernel_binary = os.path.join(GLKERNEL_DIRECTORY, 'glkernel-cmd')
    arguments = [ glkernel_binary, "--i", declaration_f_name, "--o", array_f_name ]

    try:
        print(' '.join(arguments), flush=True)
        p = subprocess.run(arguments, capture_output=True, check=True, cwd=WORKING_DIRECTORY)
    except:
        print(p.stdout.decode("utf-8"), flush=True)
        print(p.stderr.decode("utf-8"), flush=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=p.stderr.decode("utf-8"),
        )

    background_tasks.add_task(remove_temporary_files, [declaration_f, array_f], [declaration_f_name, array_f_name])

    return FileResponse(array_f_name, filename="kernel.json", media_type='application/json')
