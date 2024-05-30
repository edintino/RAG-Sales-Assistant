import sys,os
sys.path.append(os.getcwd())

import pandas as pd
import settings as s
from data_processing import generate_text_from_data

from llama_index.core import VectorStoreIndex, Settings
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.llms.ollama import Ollama
from llama_index.core.schema import TextNode

class EmbeddingSystem:
    """
    A system for embedding textual data using the Ollama embedding and LLM models.
    
    Attributes:
        data_path (str): The file path to the CSV data file.
        data (pd.DataFrame): The data loaded from the CSV file.
        texts (list of str): The textual data generated from the DataFrame.
        nodes (list of TextNode): The list of TextNodes created from the texts.
        index (VectorStoreIndex): The indexing system used for creating and managing text embeddings.
    """
    
    def __init__(self, data_path):
        """
        Initializes the EmbeddingSystem with data loaded from a specified path.
        
        Args:
            data_path (str): The path to the data file in CSV format.
        """
        self.data = pd.read_csv(data_path)
        self.texts = generate_text_from_data(self.data)
        self.configure_settings()
        self.nodes = self.create_text_nodes()
        self.index = VectorStoreIndex(self.nodes)
    
    def configure_settings(self):
        """
        Configures settings for the embedding model and LLM based on predefined specifications.
        """
        Settings.embed_model = OllamaEmbedding(model_name=s.embedding_model)
        Settings.llm = Ollama(model=s.llm_model,
                              request_timeout=360.0,
                              temperature=0,
                              system_prompt=s.sales_assistant_prompt
                             )
    
    def create_text_nodes(self):
        """
        Creates text nodes for each piece of text data.
        
        Returns:
            list of TextNode: A list of TextNode objects created from the text data.
        """
        return [TextNode(text=text, id_=i) for i, text in enumerate(self.texts)]
    
    def get_chat_engine(self):
        """
        Retrieves the chat engine from the index.

        Returns:
            ChatEngine: The chat engine capable of handling text queries.
        """
        return self.index.as_chat_engine('condense_plus_context')
