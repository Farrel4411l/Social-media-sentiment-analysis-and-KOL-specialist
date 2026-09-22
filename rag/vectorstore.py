# Author: Muhammad Farrel Haidar
# Project: AI PR & KOL Specialist DSS
# Date: 2026-09-22

import os
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document

class VectorDBInitializer:
    """
    Inisialisasi Vector Database untuk menyimpan literatur psikologi marketing
    dan framework copywriting (AIDA, PAS, dll).
    """
    def __init__(self, persist_directory: str = "data/chroma_db"):
        self.persist_directory = persist_directory
        # Menggunakan HuggingFace embedding yang ringan dan cepat untuk SLM
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    def initialize_mock_data(self) -> Chroma:
        """
        Menyuntikkan mock data literatur marketing sebagai knowledge base RAG.
        """
        docs = [
            Document(
                page_content="Framework AIDA (Attention, Interest, Desire, Action): Digunakan untuk menarik perhatian audiens, mempertahankan minat, membangun keinginan, dan memancing tindakan (call to action). Sangat cocok untuk campaign brand awareness dan peluncuran produk baru.",
                metadata={"framework": "AIDA", "type": "copywriting"}
            ),
            Document(
                page_content="Framework PAS (Problem, Agitate, Solution): Mulai dengan menyebutkan masalah (pain point) audiens, perburuk masalah tersebut agar terasa emosional dan mendesak, lalu tawarkan produk sebagai solusi. Efektif untuk audiens dengan pain point yang spesifik dan butuh solusi instan.",
                metadata={"framework": "PAS", "type": "copywriting"}
            ),
            Document(
                page_content="Cialdini's Social Proof Principle: Manusia cenderung mengikuti tindakan banyak orang. Penggunaan KOL, influencer, atau testimonial massal sangat ampuh untuk meyakinkan audiens yang ragu-ragu dan belum percaya (trust issue).",
                metadata={"framework": "Cialdini", "type": "psychology"}
            ),
            Document(
                page_content="Scarcity Marketing: Memberikan batasan waktu atau kuantitas untuk memicu Fear of Missing Out (FOMO). Cocok untuk promo flash sale atau produk eksklusif agar audiens segera bertindak.",
                metadata={"framework": "Scarcity", "type": "psychology"}
            )
        ]
        
        # Membuat dan menyimpan vector database
        vector_db = Chroma.from_documents(
            documents=docs,
            embedding=self.embeddings,
            persist_directory=self.persist_directory
        )
        # Langchain versi terbaru biasanya akan otomatis persist,
        # tapi memanggil persist() aman jika menggunakan Chroma versi lawas.
        try:
            vector_db.persist()
        except AttributeError:
            pass
            
        return vector_db

    def get_vector_db(self) -> Chroma:
        """
        Mengambil instance Vector DB yang sudah terinisialisasi.
        """
        # Jika folder belum ada, kita init dengan mock data
        if not os.path.exists(self.persist_directory):
            return self.initialize_mock_data()
            
        return Chroma(
            persist_directory=self.persist_directory, 
            embedding_function=self.embeddings
        )

if __name__ == "__main__":
    initializer = VectorDBInitializer()
    db = initializer.initialize_mock_data()
    print("Vector DB initialized successfully with Marketing Frameworks.")
