import shutil
from typing import Dict
from pydantic import BaseModel
from typing import Optional
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Callable
from datetime import date
from fastapi import UploadFile


today = date.today()
class FilesInDB(BaseModel): 
    #Atributos de la clase
    #La clase BaseModel ya tiene un constructor
    nombredocument: Optional [str]
    iddocument :    Optional [int]
    tipo: Optional [str]
    fechacarga: Optional[str]
    fechavencimiento: Optional[str]# Pendiente construir fecha vencimiento
    idusuario : Optional [int]
    urlfile : Optional [str]
database_files = Dict[str, FilesInDB]
database_files = {
    "Contabilidad": FilesInDB(**{"nombredocument":"Contabilidad",
                            "iddocument": 1,
                            "tipo":"XLSX",
                            "fechacarga": today.strftime("%d/%m/%Y"),
                            "fechavencimiento": today.strftime("%d/%m/%Y"),
                            "idusuario": 3,
                            "urlfile" : "Contabilidad.XLSX"}),
    "Empleados": FilesInDB(**{"nombredocument":"Empleados",
                            "iddocument": 2,
                            "tipo":"PDF",
                            "fechacarga": today.strftime("%d/%m/%Y"),
                            "fechavencimiento": today.strftime("%d/%m/%Y"),
                            "idusuario": 1,
                            "urlfile" : "Empleados.pdf"}),
}



def save_upload_file(upload_file: UploadFile, destination: Path) -> None:
    try:
        with destination.open("wb") as buffer:
            shutil.copyfileobj(upload_file.file, buffer)
    finally:
        upload_file.file.close()


def save_upload_file_tmp(upload_file: UploadFile) -> Path:
    try:
        suffix = Path(upload_file.filename).suffix
        with NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            shutil.copyfileobj(upload_file.file, tmp)
            tmp_path = Path(tmp.name)
    finally:
        upload_file.file.close()
    return tmp_path


def handle_upload_file(
    upload_file: UploadFile, handler: Callable[[Path], None]
) -> None:
    tmp_path = save_upload_file_tmp(upload_file)
    try:
        handler(tmp_path)  # Do something with the saved temp file
    finally:
        tmp_path.unlink()  # Delete the temp file