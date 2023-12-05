import hashlib
from typing import List
import uvicorn
from fastapi import FastAPI, HTTPException, UploadFile, Request
from fastapi.middleware.cors import CORSMiddleware
import glob
import json
import os
import time
import subprocess
from pathlib import Path
# pip3 install "uvicorn[standard]" for production
from starlette.responses import FileResponse, JSONResponse
import shutil
import duckdb
from starlette.staticfiles import StaticFiles
from fastapi.responses import StreamingResponse, RedirectResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

import zipfile
from io import BytesIO

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_project_path_by_uuid(uuid: str):
    project_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),"projects")
    conf_files_path = glob.glob(project_path + "/**/docs/CDM/cdmb_config.json", recursive=True)
    response = None
    for conf_file_path in conf_files_path:
        with open(conf_file_path, 'r') as config_file:
            file_contents = json.load(config_file)
            if 'uuid' in file_contents:
                if uuid == file_contents['uuid']:
                    response = conf_file_path.split('/docs')[0]
    return response


def get_hashed_files_list(ts, path,process):
    output_path = os.path.join(path, 'outputs')
    path +="/"
    files_to_has = glob.glob(path + '**', recursive=True)
    hash_file = {"files": []}
    for filename in files_to_has:
        if os.path.isfile(filename):
            if ts <= os.stat(filename).st_atime:
                md5_hash = hashlib.md5()
                with open(filename, "rb") as f:
                    # Read and update hash in chunks of 4K
                    for byte_block in iter(lambda: f.read(4096), b""):
                        md5_hash.update(byte_block)
                    hash_file['files'].append(
                        {
                            "filename": filename.replace(path, ''),
                            "hash": md5_hash.hexdigest()
                        }
                    )

    with open(os.path.join(output_path,'hashed_files_list_'+process+'_process.json'), 'w') as outfile:
        json_object = json.dumps(hash_file, indent=4)
        outfile.write(json_object)


def delete_input_directory(file_paths_):
    log = "The information from the files has been loaded into the embedded database in case of success of the check process.\n" \
          "Proceeding to delete the csv files uploaded by the user.\n"
    files_to_delete = glob.glob(file_paths_ + "/**")
    try:
        for file in files_to_delete:
            os.remove(file)
            log += f"\n {file} deleted!"
    except Exception as e:
        log += str(e)
        pass
    return log


@app.get("/api/projects")
def get_projects():
    project_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),"projects")
    conf_files_path = glob.glob(project_path + "/**/docs/CDM/cdmb_config.json", recursive=True)
    response = []
    for conf_file_path in conf_files_path:
        with open(conf_file_path, 'r') as config_file:
            file_contents = json.load(config_file)
            if 'metadata' in file_contents and 'cohort' in file_contents and 'uuid' in file_contents:
                response.append({
                    "root_path": conf_file_path.split('/docs')[0],
                    'uuid': file_contents['uuid'],
                    'data': {
                        'metadata': file_contents['metadata'],
                        'cohort': file_contents['cohort']
                    }
                })
    return {'projects': response}


@app.get("/api/projects/dbinfo/{project_id}")
def get_projects_db(project_id: str):
    path = get_project_path_by_uuid(project_id)
    conf_files_path = os.path.join(path, "docs/CDM/cdmb_config.json")
    database_path = os.path.join(path, "inputs/data.duckdb")
    query = ""
    result = []
    with open(conf_files_path, 'r') as config_file:
        file_contents = json.load(config_file)
        if 'entities' in file_contents:
            entities = file_contents['entities']
            idx = 0
            for entity in entities:
                query = query + \
                        "select '{entity_name}' as entity ,count(*) as n_registries from {table_name} " \
                            .format(entity_name=entity['name'], table_name=entity['name'])
                if idx < len(entities) - 1:
                    query = query + "\nunion all \n"
                idx += 1
            try:
                con = duckdb.connect(database_path, read_only=True)
                df_count = con.query(query).to_df()
                result = df_count.to_dict(orient="records")
            except Exception:
                result = [{"entity":"-", "n_registries":"-"}]
                return result
    return result


@app.get("/api/results")
def get_results():
    project_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),"projects")
    outputs_files = list(filter(os.path.isfile, glob.glob(project_path + "/**/outputs/**", recursive=True)))
    outputs_files.sort(key=os.path.getctime, reverse=True)
    response_files = []
    response_projects = []
    project_name_l = []
    project_uuid_l = []
    for output_file in outputs_files:
        root_path = output_file.split("/outputs/")[0]
        if '/logs/' in output_file:
            filename = output_file.split("/logs/")[1]
        else:
            filename = output_file.split("/outputs/")[1]
        config_file_path = os.path.join(root_path, "docs", "CDM", "cdmb_config.json")
        project_name = None
        use_case_name = None
        uuid = None
        with open(config_file_path, 'r') as config_file:
            file_contents = json.load(config_file)
            if 'metadata' in file_contents and 'cohort' in file_contents and 'uuid' in file_contents:
                uuid = file_contents['uuid']
                if "project" in file_contents['metadata']:
                    project_name = file_contents['metadata']['project']
                if "use_case" in file_contents['metadata']:
                    use_case_name = file_contents['metadata']['use_case']
        complete_name = project_name + ' - ' + use_case_name
        if complete_name not in project_name_l and uuid not in project_uuid_l:
            # distinct project
            project_name_l.append(complete_name)
            project_uuid_l.append(uuid)
        response_files.append({
            "complete_name": complete_name,
            "uuid": uuid,
            "filename": filename,
            "created_at": time.ctime(os.path.getctime(output_file))
        })
    for (name_, uuid_) in zip(project_name_l, project_uuid_l):
        response_projects.append({"project": name_, "uuid": uuid_})
    return {"projects": response_projects, "files": response_files}


# Launch DQA
@app.get("/api/dqa/{project_id}")
def launch_dqa(project_id: str):
    path = get_project_path_by_uuid(project_id)
    dqa_path = os.path.join(path, 'src', 'dqa-scripts', 'dqa.py')
    isExisting = os.path.exists(dqa_path)
    if not isExisting:
        raise HTTPException(status_code=400, detail='Cannot find dqa.py in your project')
    output_path = os.path.join(path, 'outputs', 'logs')
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    get_installed_libraries(output_path, os.path.join(path, 'docs', 'CDM', 'cdmb_config.json'))
    ts_script = time.time()
    process = subprocess.Popen(["python3", dqa_path],
                               stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
    output, error = process.communicate()
    process.wait()
    output = output.replace("\x1b[39m", "")
    output = output.replace("\x1b[31m", "")
    output = output.replace("\x1b[1m", "")
    output = output.replace("\x1b[22m", "")

    log_path = os.path.join(output_path, 'data_quality_assesment.log')
    isExisting = os.path.exists(log_path)
    if isExisting:
        os.remove(log_path)
    with open(log_path, 'w') as f:
        f.write(output)

    get_hashed_files_list(ts_script, path,'dqa')
    if process.returncode != 0:
            raise HTTPException(status_code=400, detail=output)
    return {"status_code": process.returncode, "output": output}


@app.get("/api/checking/{project_id}")
def launch_checking(project_id: str):
    path = get_project_path_by_uuid(project_id)
    checking_path = os.path.join(path, 'src', 'check_load-scripts', 'check_load.py')
    isExisting = os.path.exists(checking_path)
    if not isExisting:
        raise HTTPException(status_code=400, detail='Cannot find check_load.py in your project')
    output_path = os.path.join(path, 'outputs', 'logs')
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    get_installed_libraries(output_path, os.path.join(path, 'docs', 'CDM', 'cdmb_config.json'))
    ts_script = time.time()
    process = subprocess.Popen(["python3", checking_path],
                               stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
    output, error = process.communicate()
    process.wait()
    output = output.replace("\x1b[39m", "")
    output = output.replace("\x1b[31m", "")
    output = output.replace("\x1b[1m", "")
    output = output.replace("\x1b[22m", "")

    ## Remove files
    input_directory = os.path.join(path, 'src', 'check_load-scripts', 'inputs')
    log_files_deletion = delete_input_directory(input_directory)
    output += log_files_deletion
    log_path = os.path.join(output_path, 'checking_data_syntax.log')
    isExisting = os.path.exists(log_path)
    if isExisting:
        os.remove(log_path)
    with open(log_path, 'w') as f:
        f.write(output)
    get_hashed_files_list(ts_script, path,'check_load')
    if process.returncode != 0:
            raise HTTPException(status_code=400, detail=output)
    return {"status_code": process.returncode, "output": output}


# Launch validation
@app.get("/api/validator/{project_id}")
def launch_validator(project_id: str):
    path = get_project_path_by_uuid(project_id)
    validator_path = os.path.join(path, 'src', 'validation-scripts', 'validator.py')
    isExisting = os.path.exists(validator_path)
    if not isExisting:
        raise HTTPException(status_code=400, detail='Cannot find validator.py in your project')
    output_path = os.path.join(path, 'outputs', 'logs')
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    get_installed_libraries(output_path, os.path.join(path, 'docs', 'CDM', 'cdmb_config.json'))
    ts_script = time.time()
    process = subprocess.Popen(["python3", validator_path],
                               stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
    output, error = process.communicate()
    process.wait()
    output = output.replace("\x1b[39m", "")
    output = output.replace("\x1b[31m", "")
    output = output.replace("\x1b[1m", "")
    output = output.replace("\x1b[22m", "")
    log_path = os.path.join(output_path, 'checking_data_compliance.log')
    isExisting = os.path.exists(log_path)
    if isExisting:
        os.remove(log_path)
    with open(log_path, 'w') as f:
        f.write(output)
    if process.returncode == 0:
        validator_report_path = os.path.join(path, 'src', 'validation-scripts', 'validator_report.qmd')
        isExisting = os.path.exists(validator_report_path)
        if not isExisting:
            raise HTTPException(status_code=400, detail='Cannot find validator_report.qmd in your project')
        process_report = subprocess.Popen(["quarto", "render", validator_report_path, "--output-dir", "../../outputs"],
                                        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
        output_report, error = process_report.communicate()
        process_report.wait()
        output_report = output_report.replace("\x1b[39m", "")
        output_report = output_report.replace("\x1b[31m", "")
        output_report = output_report.replace("\x1b[1m", "")
        output_report = output_report.replace("\x1b[22m", "")
        log_path = os.path.join(output_path, 'report_validation_report.log')
        isExisting = os.path.exists(log_path)
        if isExisting:
            os.remove(log_path)
        with open(log_path, 'w') as f:
            f.write(output_report)
        output += "\n Launching report: \n\n"
        output += output_report
    get_hashed_files_list(ts_script, path,'validator')
    if process.returncode != 0:
        raise HTTPException(status_code=400, detail=output)
    return {"status_code": process.returncode, "output": output}


def get_installed_libraries(output_path:str, cdmb_config_path:str):

    script_version= f"""
    #!/bin/bash
    cdmb_version=$(cat {cdmb_config_path} | grep -E 'cdmb_version' | tr -d ' ",' | cut -d ':' -f 2)
    echo "CDMB version: $cdmb_version" > "{output_path}/sys_info.log"
    echo "ASPIRE version: $ASPIRE_VERSION" >> "{output_path}/sys_info.log"
    echo "Pipeline version: $PIPELINE_VERSION \n" >> "{output_path}/sys_info.log"
    """
    process = subprocess.Popen(script_version,shell=True,
                                   stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
    output, error = process.communicate()
    process.wait()

    script_memory= f"""
    #!/bin/bash
    output=$(cat /proc/meminfo | grep -E 'MemTotal|MemFree|MemAvailable')
    echo "$output \n" >> "{output_path}/sys_info.log"
    """
    process = subprocess.Popen(script_memory,shell=True,
                                   stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
    output, error = process.communicate()
    process.wait()
    script_libraries = f"""
    #!/bin/bash
    output=$(micromamba -n aspire list)
    echo "$output" >> "{output_path}/sys_info.log"
    """
    process = subprocess.Popen(script_libraries,shell=True,
                                   stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
    output, error = process.communicate()
    process.wait()

# Launch analysis
@app.get("/api/analysis/{project_id}/{script_name}")
def launch_analysis(project_id: str, script_name: str):
    path = get_project_path_by_uuid(project_id)
    script_path = os.path.join(path, 'src', 'analysis-scripts', script_name)
    output_path = os.path.join(path, 'outputs', 'logs')
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    isExisting = os.path.exists(script_path)
    if not isExisting:
        raise HTTPException(status_code=400, detail='Cannot find ' + script_name + ' in your project')

    get_installed_libraries(output_path, os.path.join(path, 'docs', 'CDM', 'cdmb_config.json'))
    file_name, file_extension = os.path.splitext(script_path)
    file_extension = file_extension.upper()
    if file_extension == ".R":
        ts_script = time.time()
        process = subprocess.Popen(["Rscript", script_path],
                                   stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
        output, error = process.communicate()
        process.wait()
        output = output.replace("\x1b[39m", "")
        output = output.replace("\x1b[31m", "")
        output = output.replace("\x1b[1m", "")
        output = output.replace("\x1b[22m", "")
        log_path = os.path.join(output_path, 'analysis_execution.log')
        isExisting = os.path.exists(log_path)
        if isExisting:
            os.remove(log_path)
        with open(log_path, 'w') as f:
            f.write(output)
        get_hashed_files_list(ts_script, path,'analysis')
        if process.returncode != 0:
            raise HTTPException(status_code=400, detail=output)
        return {"status_code": process.returncode, "output": output}
    elif file_extension == ".PY":
        ts_script = time.time()
        process = subprocess.Popen(["python3", script_path],
                                   stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
        output, error = process.communicate()
        process.wait()
        output = output.replace("\x1b[39m", "")
        output = output.replace("\x1b[31m", "")
        output = output.replace("\x1b[1m", "")
        output = output.replace("\x1b[22m", "")
        log_path = os.path.join(output_path, 'analysis_execution.log')
        isExisting = os.path.exists(log_path)
        if isExisting:
            os.remove(log_path)
        with open(log_path, 'w') as f:
            f.write(output)
        get_hashed_files_list(ts_script, path,'analysis')
        if process.returncode != 0:
            raise HTTPException(status_code=400, detail=output)
        return {"status_code": process.returncode, "output": output}
    elif file_extension == ".QMD":
        ts_script = time.time()
        # if _quarto.yml does not exist
        quarto_path = os.path.join(path, 'src', 'analysis-scripts', "_quarto.yml")
        isExisting = os.path.exists(quarto_path)
        if not isExisting:
            with open(quarto_path, 'w') as f:
                f.write('project:\n\toutput-dir: ../../outputs\nformat:\n\thtml:\n\t\tembed-resources: true')
        process = subprocess.Popen(["quarto", "render", script_path, "--output-dir", "../../outputs"],
                                   stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
        output, error = process.communicate()
        process.wait()
        # remove colors
        output = output.replace("\x1b[39m", "")
        output = output.replace("\x1b[31m", "")
        output = output.replace("\x1b[1m", "")
        output = output.replace("\x1b[22m", "")
        log_path = os.path.join(output_path, 'analysis_execution.log')
        isExisting = os.path.exists(log_path)
        if isExisting:
            os.remove(log_path)
        with open(log_path, 'w') as f:
            f.write(output)
        get_hashed_files_list(ts_script, path,'analysis')
        if process.returncode != 0:
            raise HTTPException(status_code=400, detail=output)
        return {"status_code": process.returncode, "output": output}
    else:
        raise HTTPException(status_code=400, detail="Script with invalid extension. Only .py, .R , .qmd (Python or R) are supported.")


# Launch analysis
@app.get("/api/analysis")
def get_analysis_scripts():
    projects = get_projects()
    response = {"scripts": []}
    for project in projects['projects']:
        root_path = project['root_path']
        text_files = glob.glob(root_path + "/src/analysis-scripts/**.*", recursive=False)
        uuid = project['uuid']
        text_files = [file.rsplit('/', 1)[1] for file in text_files]
        text_files = [file for file in text_files if str(file.split('.')[1]).lower() in ["py", "r", "qmd"]]
        response["scripts"].append({"uuid": uuid, "files": text_files})
    return response

# Download all files
@app.get("/api/download/{project_id}")
def download_all(project_id: str):
    try:
        path_ = get_project_path_by_uuid(project_id)
        outputs_files = list(filter(os.path.isfile,glob.glob(os.path.join(path_ + "/outputs/**"), recursive=True)))
        return zipfiles(outputs_files)
    except:
        raise HTTPException(status_code=400, detail=f'Something went wrong trying to download all the files.')

# Download file
@app.get("/api/download/{project_id}/{filename}")
def download_file(project_id: str, filename: str):
    path_ = get_project_path_by_uuid(project_id)
    if '.log' in filename:
        file_path = os.path.join(path_, "outputs", "logs", filename)
        if os.path.exists(file_path):
            return FileResponse(path=file_path, filename=filename)
    file_path = os.path.join(path_, "outputs", filename)
    if os.path.exists(file_path):
        return FileResponse(path=file_path, filename=filename)
    raise HTTPException(status_code=400, detail=f'Cannot find {filename} file in your project')


# Download datamodel documentation
@app.get("/api/datamodel/{project_id}")
async def download_documentation(project_id: str):
    path_ = get_project_path_by_uuid(project_id)
    file_list = glob.glob(path_ + "/docs/**", recursive=True)
    return zipfiles(file_list)


def zipfiles(file_list):
    io = BytesIO()
    with zipfile.ZipFile(io, mode='w', compression=zipfile.ZIP_DEFLATED) as zip:
        for fpath in file_list:
            zip.write(fpath,arcname=str(fpath).split('projects/')[1])
        zip.close()
    return StreamingResponse(
        iter([io.getvalue()]),
        media_type="application/x-zip-compressed",
        headers={"Content-Disposition": f"attachment;"}
    )


# Subir ficheros
@app.post("/api/uploadfiles/{project_id}")
async def create_upload_file(files: List[UploadFile], project_id: str):
    path_ = get_project_path_by_uuid(project_id)
    output_path = os.path.join(path_, 'outputs', 'logs')
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    status = 0
    output = ""
    for upload_file in files:
        try:
            destination_path = Path(os.path.join(path_, "src", "check_load-scripts", "inputs", upload_file.filename))
            with destination_path.open("wb") as buffer:
                shutil.copyfileobj(upload_file.file, buffer)
            upload_file.file.close()
            output += f"\n {upload_file.filename} - size {os.stat(destination_path).st_size} bytes --> OK \n"
        except Exception as e:
            status = 1
            output += "\n"
            output += f"{upload_file.filename} - {str(e)}"
            output += "\n"
            raise HTTPException(status_code=400, detail=output)
        finally:
            upload_file.file.close()
    log_path = os.path.join(output_path, 'mapping_input_files.log')
    isExisting = os.path.exists(log_path)
    if isExisting:
        os.remove(log_path)
    with open(log_path, 'w') as f:
        f.write(output)
    return {"status_code": status, "output": output}


@app.delete("/api/delete/{project_id}")
async def delete_outputs_files(project_id: str):
    path_ = get_project_path_by_uuid(project_id)
    outputs_files = list(filter(os.path.isfile, glob.glob(path_ + "/outputs/**", recursive=True)))
    status = 0
    output = ""
    for file in outputs_files:
        try:
            os.remove(file)
            output += f"\n {file} --> DELETED \n"
        except Exception as e:
            status = 1
            output += "\n"
            output += f"{file} - {str(e)}"
            output += "\n"
            raise HTTPException(status_code=400, detail=output)
    return {"status_code": status, "output": output}


app.mount("/", StaticFiles(directory=os.path.join(os.path.dirname(os.path.realpath(__file__)),"front"), html=True), name="front")


@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request, exc):
    if request.url.path in ["/", "/mapdata", "/analysis", "/results", "/documentation", "/about"]:
        return RedirectResponse("/")
    else:
        return JSONResponse({"detail": str(exc.detail)}, status_code=exc.status_code)

if __name__ == "__main__":
    port = os.getenv('APP_PORT') if os.getenv('APP_PORT') else 3000
    host = os.getenv('APP_HOST') if os.getenv('APP_HOST') else "0.0.0.0"
    uvicorn.run(app, host=host, port=int(port))
