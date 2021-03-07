import os
import shutil
from typing import Optional, List
import subprocess
import tempfile

import json

from pydantic import BaseModel

from fastapi import APIRouter, Response, File, UploadFile, Body
from fastapi import HTTPException, status
from fastapi.responses import FileResponse


router = APIRouter()


GLKERNEL_DIRECTORY = os.environ.get('GLKERNEL_DIRECTORY', '')
RESULT_DIR = os.environ.get('RESULT_DIR', '/data/results')
WORKING_DIRECTORY = '/opt/dependencies/glkernel/'


# ROOT

@router.get("/", tags=[""])
async def get_root():
    return {}


@router.head("/", tags=[""])
async def head_root(response: Response):
    response.status_code = status.HTTP_200_OK


# IMAGES
#
#@router.post("/image_from_script", tags=["image"])
#async def get_image_from_script(script: str = Body(...)):
#    script_f, script_f_name = tempfile.mkstemp(suffix=".js", text=True)
#    script_f.write(script)
#    script_f.close()
#
#    image_f, image_f_name = tempfile.mkstemp(suffix=".png", text=False)
#
#    glkernel_binary = os.path.join(GLKERNEL_DIRECTORY, 'glkernel-cli')
#    arguments = [ glkernel_binary, "run", "--force", "--output", image_f_name, "--format", ".png", script_f_name ]
#
#    print(' '.join(arguments), flush=True)
#
#    p = subprocess.run(arguments, capture_output=True, cwd=WORKING_DIRECTORY)
#    print(p.stdout.decode("utf-8"), flush=True)
#    print(p.stderr.decode("utf-8"), flush=True)
#
#    return FileResponse(image_f_name, filename="kernel.png", media_type='image/png')
#

@router.post("/image_from_script_file", tags=["image"])
async def get_image_from_script_file(script_file: UploadFile = File(...)):
    script_f, script_f_name = tempfile.mkstemp(suffix=".js", text=True)
    with open(script_f, 'w+b') as f:
        shutil.copyfileobj(script_file.file, f)

    image_f, image_f_name = tempfile.mkstemp(suffix=".png", text=False)

    glkernel_binary = os.path.join(GLKERNEL_DIRECTORY, 'glkernel-cli')
    arguments = [ glkernel_binary, "run", "--force", "--output", image_f_name, "--format", ".png", script_f_name ]

    print(' '.join(arguments), flush=True)

    p = subprocess.run(arguments, capture_output=True, cwd=WORKING_DIRECTORY)
    print(p.stdout.decode("utf-8"), flush=True)
    print(p.stderr.decode("utf-8"), flush=True)

    return FileResponse(image_f_name, filename="kernel.png", media_type='image/png')

#
#@router.post("/image_from_declaration", tags=["image"])
#async def get_image_from_declaration(declaration: str = Body(...)):
#    declaration_f, declaration_f_name = tempfile.mkstemp(suffix=".json", text=True)
#    declaration_f.write(declaration)
#    declaration_f.close()
#
#    array_f, array_f_name = tempfile.mkstemp(suffix=".json", text=True)
#
#    glkernel_binary = os.path.join(GLKERNEL_DIRECTORY, 'glkernel-cmd')
#    arguments = [ glkernel_binary, "--i", declaration_f_name, "--o", array_f_name ]
#
#    print(' '.join(arguments), flush=True)
#
#    p = subprocess.run(arguments, capture_output=True, cwd=WORKING_DIRECTORY)
#    print(p.stdout.decode("utf-8"), flush=True)
#    print(p.stderr.decode("utf-8"), flush=True)
#
#    image_f, image_f_name = tempfile.mkstemp(suffix=".png", text=False)
#
#    glkernel_binary = os.path.join(GLKERNEL_DIRECTORY, 'glkernel-cli')
#    arguments = [ glkernel_binary, "run", "--force", "--output", image_f_name, "--format", ".png", array_f_name ]
#
#    print(' '.join(arguments), flush=True)
#
#    p = subprocess.run(arguments, capture_output=True, cwd=WORKING_DIRECTORY)
#    print(p.stdout.decode("utf-8"), flush=True)
#    print(p.stderr.decode("utf-8"), flush=True)
#
#    return FileResponse(image_f_name, filename="kernel.png", media_type='image/png')
#

@router.post("/image_from_declaration_file", tags=["image"])
async def get_image_from_declaration_file(declaration_file: UploadFile = File(...)):
    declaration_f, declaration_f_name = tempfile.mkstemp(suffix=".json", text=True)
    with open(declaration_f, 'w+b') as f:
        shutil.copyfileobj(declaration_file.file, f)

    array_f, array_f_name = tempfile.mkstemp(suffix=".json", text=True)

    glkernel_binary = os.path.join(GLKERNEL_DIRECTORY, 'glkernel-cmd')
    arguments = [ glkernel_binary, "--i", declaration_f_name, "--o", array_f_name ]

    print(' '.join(arguments), flush=True)

    p = subprocess.run(arguments, capture_output=True, cwd=WORKING_DIRECTORY)
    print(p.stdout.decode("utf-8"), flush=True)
    print(p.stderr.decode("utf-8"), flush=True)

    image_f, image_f_name = tempfile.mkstemp(suffix=".png", text=False)

    glkernel_binary = os.path.join(GLKERNEL_DIRECTORY, 'glkernel-cli')
    arguments = [ glkernel_binary, "run", "--force", "--output", image_f_name, "--format", ".png", array_f_name ]

    print(' '.join(arguments), flush=True)

    p = subprocess.run(arguments, capture_output=True, cwd=WORKING_DIRECTORY)
    print(p.stdout.decode("utf-8"), flush=True)
    print(p.stderr.decode("utf-8"), flush=True)

    return FileResponse(image_f_name, filename="kernel.png", media_type='image/png')

#
#@router.post("/image_from_array", tags=["image"])
#async def get_image_from_array(array: str = Body(...)):
#    array_f, array_f_name = tempfile.mkstemp(suffix=".json", text=True)
#    array_f.write(array)
#    array_f.close()
#
#    image_f, image_f_name = tempfile.mkstemp(suffix=".png", text=False)
#
#    glkernel_binary = os.path.join(GLKERNEL_DIRECTORY, 'glkernel-cli')
#    arguments = [ glkernel_binary, "run", "--force", "--output", image_f_name, "--format", ".png", array_f_name ]
#
#    print(' '.join(arguments), flush=True)
#
#    p = subprocess.run(arguments, capture_output=True, cwd=WORKING_DIRECTORY)
#    print(p.stdout.decode("utf-8"), flush=True)
#    print(p.stderr.decode("utf-8"), flush=True)
#
#    return FileResponse(image_f_name, filename="kernel.png", media_type='image/png')
#

@router.post("/image_from_array_file", tags=["image"])
async def get_image_from_array_file(array_file: UploadFile = File(...)):
    array_f, array_f_name = tempfile.mkstemp(suffix=".json", text=True)
    with open(array_f, 'w+b') as f:
        shutil.copyfileobj(array_file.file, f)

    image_f, image_f_name = tempfile.mkstemp(suffix=".png", text=False)

    glkernel_binary = os.path.join(GLKERNEL_DIRECTORY, 'glkernel-cli')
    arguments = [ glkernel_binary, "run", "--force", "--output", image_f_name, "--format", ".png", array_f_name ]

    print(' '.join(arguments), flush=True)

    p = subprocess.run(arguments, capture_output=True, cwd=WORKING_DIRECTORY)
    print(p.stdout.decode("utf-8"), flush=True)
    print(p.stderr.decode("utf-8"), flush=True)

    return FileResponse(image_f_name, filename="kernel.png", media_type='image/png')


# ARRAY
#
#@router.post("/array_from_script", tags=["array"])
#async def get_array_from_script(script: str = Body(...)):
#    script_f, script_f_name = tempfile.mkstemp(suffix=".js", text=True)
#    script_f.write(script)
#    script_f.close()
#
#    array_f, array_f_name = tempfile.mkstemp(suffix=".json", text=False)
#
#    glkernel_binary = os.path.join(GLKERNEL_DIRECTORY, 'glkernel-cli')
#    arguments = [ glkernel_binary, "run", "--force", "--output", array_f_name, "--format", ".json", script_f_name ]
#
#    print(' '.join(arguments), flush=True)
#
#    p = subprocess.run(arguments, capture_output=True, cwd=WORKING_DIRECTORY)
#    print(p.stdout.decode("utf-8"), flush=True)
#    print(p.stderr.decode("utf-8"), flush=True)
#
#    return FileResponse(array_f_name, filename="kernel.json", media_type='application/json')
#

@router.post("/array_from_script_file", tags=["array"])
async def get_array_from_script_file(script_file: UploadFile = File(...)):
    script_f, script_f_name = tempfile.mkstemp(suffix=".js", text=True)
    with open(script_f, 'w+b') as f:
        shutil.copyfileobj(script_file.file, f)

    array_f, array_f_name = tempfile.mkstemp(suffix=".json", text=False)

    glkernel_binary = os.path.join(GLKERNEL_DIRECTORY, 'glkernel-cli')
    arguments = [ glkernel_binary, "run", "--force", "--output", array_f_name, "--format", ".json", script_f_name ]

    print(' '.join(arguments), flush=True)

    p = subprocess.run(arguments, capture_output=True, cwd=WORKING_DIRECTORY)
    print(p.stdout.decode("utf-8"), flush=True)
    print(p.stderr.decode("utf-8"), flush=True)

    return FileResponse(array_f_name, filename="kernel.json", media_type='application/json')

#
#@router.post("/array_from_declaration", tags=["array"])
#async def get_array_from_declaration(declaration: str = Body(...)):
#    declaration_f, declaration_f_name = tempfile.mkstemp(suffix=".json", text=True)
#    declaration_f.write(declaration)
#    declaration_f.close()
#
#    array_f, array_f_name = tempfile.mkstemp(suffix=".json", text=True)
#
#    glkernel_binary = os.path.join(GLKERNEL_DIRECTORY, 'glkernel-cmd')
#    arguments = [ glkernel_binary, "--i", declaration_f_name, "--o", array_f_name ]
#
#    print(' '.join(arguments), flush=True)
#
#    p = subprocess.run(arguments, capture_output=True, cwd=WORKING_DIRECTORY)
#    print(p.stdout.decode("utf-8"), flush=True)
#    print(p.stderr.decode("utf-8"), flush=True)
#
#    return FileResponse(array_f_name, filename="kernel.json", media_type='application/json')
#

@router.post("/array_from_declaration_file", tags=["array"])
async def get_array_from_declaration_file(declaration_file: UploadFile = File(...)):
    declaration_f, declaration_f_name = tempfile.mkstemp(suffix=".json", text=True)
    with open(declaration_f, 'w+b') as f:
        shutil.copyfileobj(declaration_file.file, f)

    array_f, array_f_name = tempfile.mkstemp(suffix=".json", text=True)

    glkernel_binary = os.path.join(GLKERNEL_DIRECTORY, 'glkernel-cmd')
    arguments = [ glkernel_binary, "--i", declaration_f_name, "--o", array_f_name ]

    print(' '.join(arguments), flush=True)

    p = subprocess.run(arguments, capture_output=True, cwd=WORKING_DIRECTORY)
    print(p.stdout.decode("utf-8"), flush=True)
    print(p.stderr.decode("utf-8"), flush=True)

    return FileResponse(array_f_name, filename="kernel.json", media_type='application/json')
