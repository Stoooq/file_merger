from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from merge import merge_files

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/merge")
async def merge(request: Request):
    data = await request.json()
    files = data.get("files")
    logger.info(files)
    merged_file = merge_files(files)
    logger.info(merged_file)
    return {"merged_file": merged_file}