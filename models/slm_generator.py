# Author: Muhammad Farrel Haidar
# Project: AI PR & KOL Specialist DSS
# Date: 2026-09-22

import json
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

class StrategistSLMGenerator:
    """
    Modul SLM (Small Language Model) yang bertindak sebagai PR Strategist.
    Menerima context dari RAG dan hasil sentimen, lalu men-generate KOL Brief
    dalam format JSON terstruktur berkat prompt engineering yang presisi.
    """
    def __init__(self, model_name_or_path: str = "Qwen/Qwen2.5-7B-Instruct"):
        self.model_name = model_name_or_path
        self.llm = self._initialize_mock_llm()
        self.parser = JsonOutputParser()
        self.prompt_template = self._build_prompt_template()

    def _initialize_mock_llm(self):
        """
        Inisialisasi LLM/SLM. Karena ini tahap scaffolding/DSS boilerplate, 
        kita menggunakan Mock Class agar eksekusi sistem tidak terblokir oleh download model besar.
        Di tahap production, ini diganti dengan model asli via HuggingFacePipeline.
        """
        # --- PROD CODE SNIPPET ---
        # from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
        # from langchain_community.llms.huggingface_pipeline import HuggingFacePipeline
        # tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        # model = AutoModelForCausalLM.from_pretrained(self.model_name)
        # pipe = pipeline("text-generation", model=model, tokenizer=tokenizer, max_new_tokens=512)
        # return HuggingFacePipeline(pipeline=pipe)
        
        class MockLLM:
            def invoke(self, prompt_text: str):
                # Model pura-pura mengembalikan struktur JSON yang diminta
                mock_response = {
                    "Campaign Objective": "Memulihkan kepercayaan audiens dan membuktikan kualitas serta keaslian produk",
                    "Psychological Angle": "Menggunakan Cialdini's Social Proof dipadukan dengan PAS (Problem, Agitate, Solution) untuk menjawab keraguan konsumen",
                    "Persona": "Otoritatif namun berempati (Authority & Empathetic), jujur, dan edukatif",
                    "Storyline": "KOL memulai dengan menceritakan pengalaman buruk (pain point) saat membeli produk palsu, kemudian menunjukkan produk asli brand ini, melakukan demonstrasi nyata, dan mengajak audiens untuk hanya membeli dari official store."
                }
                return json.dumps(mock_response)
                
        return MockLLM()

    def _build_prompt_template(self) -> ChatPromptTemplate:
        """
        Merancang System Prompt dan User Prompt secara ketat untuk 
        memastikan keluaran (output) adalah valid JSON dengan keys spesifik.
        """
        system_instructions = (
            "You are an elite PR & KOL Strategist AI. Your goal is to design highly persuasive KOL (Key Opinion Leader) "
            "marketing briefs based on public sentiment and specific marketing psychology frameworks.\n\n"
            "You MUST output the result EXCLUSIVELY as a valid JSON object. Do not add markdown blocks (like ```json), "
            "do not add conversational text. The JSON must exactly have the following 4 keys:\n"
            "- \"Campaign Objective\": (string) The main marketing goal of this KOL campaign.\n"
            "- \"Psychological Angle\": (string) How the provided framework is applied to the audience's pain points.\n"
            "- \"Persona\": (string) The ideal characteristics or vibe of the KOL (e.g., Empathetic, Authority, Energetic).\n"
            "- \"Storyline\": (string) A brief, step-by-step storyline of what the KOL should say or act out in the content.\n"
        )
        
        user_message = (
            "Based on the following input data, generate the KOL Brief.\n\n"
            "--- AUDIENCE SENTIMENT & PAIN POINTS ---\n"
            "{sentiment_analysis}\n\n"
            "--- PSYCHOLOGICAL MARKETING FRAMEWORKS (RAG CONTEXT) ---\n"
            "{rag_context}\n"
        )
        
        return ChatPromptTemplate.from_messages([
            ("system", system_instructions),
            ("user", user_message)
        ])

    def generate_brief(self, sentiment_data: dict, rag_context: list) -> dict:
        """
        Menjalankan prompt engineering ke SLM dan mem-parsing output JSON.
        """
        # Format input data
        sentiment_str = json.dumps(sentiment_data, indent=2)
        context_str = "\n".join([f"- {ctx}" for ctx in rag_context])
        
        # Menghasilkan prompt utuh
        messages = self.prompt_template.format_messages(
            sentiment_analysis=sentiment_str,
            rag_context=context_str
        )
        
        full_prompt = "\n".join([m.content for m in messages])
        
        # Eksekusi inference LLM
        raw_output = self.llm.invoke(full_prompt)
        
        # Parsing string menjadi JSON / Python Dictionary
        try:
            structured_brief = self.parser.parse(raw_output)
            return structured_brief
        except Exception as e:
            return {
                "error": "Failed to parse SLM output as JSON",
                "raw_output": raw_output
            }
