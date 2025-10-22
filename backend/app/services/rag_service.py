from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Qdrant
from qdrant_client import QdrantClient
from app.config import settings
from app.models import TaxCalculationRequest, TaxCalculationResult

class RAGService:
    """
    จัดการ RAG Pipeline
    - เชื่อมต่อกับ Qdrant Vector Database
    - ค้นหาข้อมูลที่เกี่ยวข้อง (Retrieval)
    - ส่งข้อมูลไปให้ AI Service (Augmented Generation)
    """
    
    def __init__(self):
        # Initialize Qdrant Client
        self.qdrant_client = QdrantClient(
            url=settings.qdrant_url,
            timeout=30
        )
        
        # Initialize Embeddings
        self.embeddings = OpenAIEmbeddings(
            openai_api_key=settings.openai_api_key
        )
        
        # Initialize Vector Store
        try:
            self.vector_store = Qdrant(
                client=self.qdrant_client,
                collection_name=settings.qdrant_collection_name,
                embeddings=self.embeddings
            )
        except Exception as e:
            print(f"Warning: Could not connect to Qdrant: {e}")
            self.vector_store = None
    
    def _build_search_query(
        self,
        request: TaxCalculationRequest,
        tax_result: TaxCalculationResult
    ) -> str:
        """
        สร้าง Query สำหรับค้นหาใน Vector DB
        
        Args:
            request: ข้อมูลผู้ใช้
            tax_result: ผลการคำนวณภาษี
            
        Returns:
            Query string
        """
        # สร้าง query ที่เฉพาะเจาะจง
        query_parts = [
            f"วิธีลดภาษีสำหรับคนที่มีรายได้ {tax_result.gross_income:,.0f} บาท",
            f"ต้องเสียภาษี {tax_result.tax_amount:,.0f} บาท"
        ]
        
        # เพิ่มข้อมูลความเสี่ยง
        if request.risk_tolerance == "low":
            query_parts.append("ต้องการความเสี่ยงต่ำ ปลอดภัย")
        elif request.risk_tolerance == "high":
            query_parts.append("รับความเสี่ยงสูงได้ ผลตอบแทนสูง")
        else:
            query_parts.append("ความเสี่ยงปานกลาง สมดุล")
        
        # เพิ่มข้อมูลว่ามีการลงทุนอะไรบ้างแล้ว
        existing_investments = []
        if request.rmf > 0:
            existing_investments.append("RMF")
        if request.ssf > 0:
            existing_investments.append("SSF")
        if request.life_insurance > 0:
            existing_investments.append("ประกันชีวิต")
        if request.pension_insurance > 0:
            existing_investments.append("ประกันบำนาญ")
        
        if existing_investments:
            query_parts.append(f"มีการลงทุนใน {', '.join(existing_investments)} แล้ว")
        
        return " ".join(query_parts)
    
    async def retrieve_relevant_documents(
        self,
        request: TaxCalculationRequest,
        tax_result: TaxCalculationResult
    ) -> str:
        """
        ค้นหาเอกสารที่เกี่ยวข้องจาก Vector DB
        
        Args:
            request: ข้อมูลผู้ใช้
            tax_result: ผลการคำนวณภาษี
            
        Returns:
            ข้อความที่รวมเอกสารที่เกี่ยวข้อง
        """
        if not self.vector_store:
            print("Warning: Vector store not available, using fallback context")
            return self._get_fallback_context()
        
        try:
            # สร้าง query
            query = self._build_search_query(request, tax_result)
            
            print(f"RAG Query: {query}")
            
            # ค้นหาเอกสาร
            docs = await self.vector_store.asimilarity_search(
                query,
                k=settings.rag_top_k
            )
            
            if not docs:
                print("No documents found, using fallback")
                return self._get_fallback_context()
            
            # รวมเอกสารเป็นข้อความเดียว
            context_parts = []
            for i, doc in enumerate(docs, 1):
                context_parts.append(f"[เอกสารที่ {i}]\n{doc.page_content}\n")
            
            return "\n".join(context_parts)
            
        except Exception as e:
            print(f"Error retrieving documents: {e}")
            return self._get_fallback_context()
    
    def _get_fallback_context(self) -> str:
        """
        ข้อมูลสำรองกรณีที่ Vector DB ไม่พร้อม
        """
        return """
        [ข้อมูลพื้นฐานเกี่ยวกับการลดภาษี]
        
        1. กองทุน RMF (Retirement Mutual Fund):
           - ลดหย่อนได้สูงสุด 30% ของรายได้ ไม่เกิน 500,000 บาท
           - ต้องถือจนอายุ 55 ปี และถือครบ 5 ปี
           - ผลตอบแทนประมาณ 5-8% ต่อปี (ขึ้นกับตลาด)
           - เหมาะกับคนที่ต้องการเก็บเงินระยะยาว
        
        2. กองทุน SSF (Super Savings Fund):
           - ลดหย่อนได้สูงสุด 30% ของรายได้ ไม่เกิน 200,000 บาท
           - ต้องถือครบ 10 ปี
           - ผลตอบแทนประมาณ 4-7% ต่อปี
           - มีความยืดหยุ่นมากกว่า RMF
        
        3. ประกันบำนาญ:
           - ลดหย่อนได้สูงสุด 15% ของรายได้ ไม่เกิน 200,000 บาท
           - รับประกันผลตอบแทน ความเสี่ยงต่ำ
           - ผลตอบแทนประมาณ 3-4% ต่อปี
           - เหมาะกับคนที่ไม่ชอบเสี่ยง
        
        4. กองทุนสำรองเลี้ยงชีพ (Provident Fund):
           - ลดหย่อนได้สูงสุด 15% ของเงินเดือน ไม่เกิน 500,000 บาท
           - บริษัทจ่ายเพิ่มให้ (Matching)
           - ผลตอบแทนประมาณ 4-6% ต่อปี
        
        5. เงินบริจาค:
           - ลดหย่อนได้สูงสุด 10% ของรายได้หลังหักค่าใช้จ่าย
           - บริจาคให้การศึกษา/กีฬา ลดหย่อน 2 เท่า
           - ไม่มีผลตอบแทนทางการเงิน แต่ได้บุญ
        """
    
    def check_collection_exists(self) -> bool:
        """
        ตรวจสอบว่า Collection ใน Qdrant มีอยู่หรือไม่
        """
        try:
            collections = self.qdrant_client.get_collections()
            collection_names = [c.name for c in collections.collections]
            return settings.qdrant_collection_name in collection_names
        except Exception as e:
            print(f"Error checking collection: {e}")
            return False