import os
import shutil

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, File, Request, UploadFile
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

load_dotenv()
os.environ["HF_TOKEN"] = os.getenv("HF_TOKEN")

app = FastAPI()

from utility import Embeddings, LLMInference, Milvus

HF_MODEL_NAME = "mistralai/Mixtral-8x7B-Instruct-v0.1"
llm = LLMInference(HF_MODEL_NAME)
embedding = Embeddings()
embedding_model = embedding.create_embeddings_model()
milvus = Milvus()


# Specify the directory where the HTML files are located
templates = Jinja2Templates(directory="templates")

UPLOAD_DIR = "uploaded_files"

if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)


# Route to serve the index.html page
@app.get("/", response_class=HTMLResponse)
def render_homepage(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/upload_document")
def process_file(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    text_chunks = embedding.get_chunks(file_path)
    milvus.load_data_in_milvus(text_chunks, embedding)
    return {
        "filename": file.filename,
        "message": "File uploaded and processed successfully!",
    }


@app.post("/ask_question")
def answer_question(request: dict):
    question = request["query"]
    context = milvus.retrieve_data_from_milvus(question, embedding)
    answer = llm.get_llm_response(context, question)
    response = JSONResponse(content={"answer": answer})
    return response


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
