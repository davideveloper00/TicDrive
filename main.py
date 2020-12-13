import models
import os
import shutil
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Callable
from typing import List
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import HTMLResponse
from models import database_files
from models import FilesInDB
from datetime import date

app = FastAPI()
today = date.today()
consecutivo = 0



@app.get("/listfiles")
async def files():
    #return {"message": database_files.get("Contabilidad")}
    return {"message": database_files}


@app.post("/uploadfiles/")
async def create_upload_files(archivo: UploadFile = File(...)):
    global consecutivo
    consecutivo += 1
    database_files[archivo.filename] = FilesInDB(**{"nombredocument" : archivo.filename,
                                                    "iddocument" : consecutivo,
                                                    "tipo": archivo.content_type,
                                                    "fechacarga": today.strftime("%d/%m/%Y"),
                                                    "fechavencimiento": today.strftime("%d/%m/%Y"),
                                                    "idusuario": 3,
                                                    "urlfile": "/usr/Desktop"})
           
    return {"Nombre": archivo.filename , "Tipo": archivo.content_type}




@app.get("/")
async def main():
    content = """
<form action="/uploadfiles/" enctype="multipart/form-data" method="post">
<input name="archivo" type="file" multiple>
<input type="submit">
<!--input name = "fechaven" type="text"-->
</form>
</body>
    """
    return HTMLResponse(content=content)