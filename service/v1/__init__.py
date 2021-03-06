import os
import shutil
from typing import Optional, List
import subprocess

import json
import hashlib
import base64

from pydantic import BaseModel

from fastapi import APIRouter, Response, File, UploadFile, Depends
from fastapi import HTTPException, status
from fastapi.responses import FileResponse


router = APIRouter()


GLKERNEL_DIRECTORY=os.environ.get('GLKERNEL_DIRECTORY', '')
RESULT_DIR=os.environ.get('RESULT_DIR', '/data/results')


def results_dir():
    directory = RESULT_DIR

    if not os.path.exists(directory):
        os.mkdir(directory)
    
    return directory


def xxx_dir():
    directory = os.path.join(results_dir(), 'xxx')

    if not os.path.exists(directory):
        os.mkdir(directory)
    
    return directory


def make_hash_sha256(o):
    hasher = hashlib.sha256()
    hasher.update(repr(make_hashable(o)).encode())
    return hasher.hexdigest()


def make_hashable(o):
    if isinstance(o, (tuple, list)):
        return tuple((make_hashable(e) for e in o))

    if isinstance(o, dict):
        return tuple(sorted((k,make_hashable(v)) for k,v in o.items()))

    if isinstance(o, (set, frozenset)):
        return tuple(sorted(make_hashable(e) for e in o))

    return o


# ROOT

@router.get("/", tags=[""])
async def api_get_root():
    return {}


@router.head("/", tags=[""])
async def api_head_root(response: Response):
    response.status_code = status.HTTP_200_OK
