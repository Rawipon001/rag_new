"""
FastAPI Main Application
Version: Qdrant Support
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.models import TaxCalculationRequest, TaxCalculationResponse
from app.services.tax_calculator import tax_calculator_service
from app.services.rag_service import RAGService
from app.services.ai_service import AIService
from app.config import settings

app = FastAPI(
    title="AI Tax Advisor API",
    description="ระบบแนะนำการวางแผนภาษีด้วย AI + Qdrant RAG",
    version="3.2-qdrant"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
print("=" * 50)
print("🚀 Initializing AI Tax Advisor API")
print("=" * 50)

rag_service = RAGService()
ai_service = AIService()

print("=" * 50)
print("✅ Initialization complete")
print("=" * 50)


@app.get("/")
async def root():
    return {
        "message": "AI Tax Advisor API",
        "version": "3.2-qdrant",
        "status": "running",
        "qdrant": {
            "url": settings.qdrant_url,
            "collection": settings.qdrant_collection_name,
            "available": rag_service.is_available()
        }
    }


@app.get("/health")
async def health_check():
    """Health check with Qdrant status"""
    qdrant_info = rag_service.get_collection_info()
    
    return {
        "status": "healthy",
        "qdrant": qdrant_info,
        "rag_available": rag_service.is_available()
    }


@app.post("/api/calculate-tax", response_model=TaxCalculationResponse)
async def calculate_tax_with_multiple_plans(
    request: TaxCalculationRequest
) -> TaxCalculationResponse:
    """
    คำนวณภาษีและรับแผนการลงทุนหลายแผน
    """
    try:
        # 1. คำนวณภาษี
        tax_result = tax_calculator_service.calculate_tax(request)
        
        # 2. ดึงข้อมูลจาก Qdrant RAG
        context = "ไม่มีข้อมูลจาก RAG"
        
        if rag_service.is_available():
            query = f"""
            รายได้ {request.gross_income} บาท 
            ระดับความเสี่ยง {request.risk_tolerance}
            ต้องการวางแผนภาษีและลงทุน
            มีครอบครัว บุตร บิดามารดา
            """
            
            try:
                retrieved_docs = await rag_service.retrieve_relevant_documents(
                    query, 
                    k=settings.rag_top_k
                )
                
                if retrieved_docs:
                    context_parts = []
                    for doc in retrieved_docs:
                        if hasattr(doc, 'page_content'):
                            context_parts.append(doc.page_content)
                        elif hasattr(doc, 'content'):
                            context_parts.append(doc.content)
                        elif isinstance(doc, str):
                            context_parts.append(doc)
                    
                    if context_parts:
                        context = "\n\n".join(context_parts)
                        print(f"✅ RAG Context: {len(context)} characters")
                else:
                    print("⚠️ RAG: No documents retrieved")
                    
            except Exception as e:
                print(f"⚠️ RAG Error: {e}")
                import traceback
                traceback.print_exc()
        else:
            print("⚠️ RAG not available - using AI without context")
        
        # 3. เรียก AI เพื่อสร้างหลายแผน
        investment_plans = await ai_service.generate_recommendations(
            request, tax_result, context
        )
        
        # 4. Return response
        return TaxCalculationResponse(
            tax_result=tax_result,
            investment_plans=investment_plans
        )
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )