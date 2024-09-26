from typing import List

from huggingface_hub import InferenceClient
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pymilvus import MilvusClient
from sentence_transformers import SentenceTransformer
from tqdm import tqdm


class Embeddings:
    def __init__(self) -> None:
        self._embedding_model = None

    def get_chunks(self, file_path: str) -> List:
        loader = PyPDFLoader(file_path)
        docs = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=200
        )
        chunks = text_splitter.split_documents(docs)
        text_lines = [chunk.page_content for chunk in chunks]
        return text_lines

    def create_embeddings_model(self):
        embedding_model = SentenceTransformer("BAAI/bge-small-en-v1.5")
        self._embedding_model = embedding_model
        return self._embedding_model

    def emb_text(self, text: str) -> List:
        return self._embedding_model.encode([text], normalize_embeddings=True).tolist()[
            0
        ]


class Milvus:
    def __init__(self) -> None:
        self._milvus_client = MilvusClient(uri="./hf_milvus_demo.db")
        self._collection_name = "rag_collection"

    def load_data_in_milvus(self, text_lines: List, embedding: Embeddings) -> None:
        if self._milvus_client.has_collection(self._collection_name):
            self._milvus_client.drop_collection(self._collection_name)
        self._milvus_client.create_collection(
            collection_name=self._collection_name,
            dimension=384,
            metric_type="IP",  # Inner product distance
            consistency_level="Strong",  # Strong consistency level
        )
        data = []
        for i, line in enumerate(tqdm(text_lines, desc="Creating embeddings")):
            data.append({"id": i, "vector": embedding.emb_text(line), "text": line})

        self._milvus_client.insert(collection_name=self._collection_name, data=data)

    def retrieve_data_from_milvus(self, question: str, embedding: Embeddings) -> str:
        search_res = self._milvus_client.search(
            collection_name=self._collection_name,
            data=[
                embedding.emb_text(question)
            ],  # Use the `emb_text` function to convert the question to an embedding vector
            limit=3,  # Return top 3 results
            search_params={"metric_type": "IP", "params": {}},  # Inner product distance
            output_fields=["text"],  # Return the text field
        )
        retrieved_lines_with_distances = [
            (res["entity"]["text"], res["distance"]) for res in search_res[0]
        ]
        context = "\n".join(
            [
                line_with_distance[0]
                for line_with_distance in retrieved_lines_with_distances
            ]
        )
        return context


class LLMInference:
    def __init__(self, hf_model_name: str) -> None:
        self._prompt = """
        Using the information provided within the <context> tags, answer the question enclosed in the <question> tags. If you are unsure or lack sufficient information, respond with only "I don't know." Return the answer as a string.

        <context>
        {context}
        </context>

        <question>
        {question}
        </question>
        
        """
        self._model_name = hf_model_name

    def get_llm_response(self, context: str, question: str) -> str:
        llm_client = InferenceClient(model=self._model_name, timeout=120)
        prompt = self._prompt.format(context=context, question=question)
        answer = llm_client.text_generation(
            prompt,
            max_new_tokens=1000,
        ).strip()
        return answer
