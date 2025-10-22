from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.models import (
    TaxCalculationRequest, 
    TaxOptimizationResponse,
    Recommendation
)
from app.services.tax_calculator import TaxCalculator
from app.services.rag_service import RAGService
from app.services.ai_service import AIService

# Initialize FastAPI
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="AI-powered tax advisor for Thai personal income tax"
)

# CORS Middleware - แก้ไขให้รองรับ localhost ทุก port
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Services
rag_service = RAGService()
ai_service = AIService()

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "app": settings.app_name,
        "version": settings.app_version,
        "status": "running"
    }

@app.get("/health")
async def health_check():
    """
    ตรวจสอบสถานะของระบบทั้งหมด
    """
    qdrant_status = rag_service.check_collection_exists()
    
    return {
        "status": "healthy",
        "qdrant_connected": qdrant_status,
        "collection_exists": qdrant_status,
        "collection_name": settings.qdrant_collection_name
    }

@app.post("/api/calculate", response_model=TaxOptimizationResponse)
async def calculate_tax(request: TaxCalculationRequest):
    """
    คำนวณภาษีและแนะนำวิธีลดภาษี
    
    Flow:
    1. คำนวณภาษีปัจจุบัน
    2. ถ้าไม่เสียภาษี → ส่งผลลัพธ์กลับไป
    3. ถ้าเสียภาษี → ใช้ RAG หาวิธีลดภาษี
    """
    try:
        print(f"📥 Received request: {request}")
        
        # Step 1: คำนวณภาษี
        tax_result = TaxCalculator.calculate(request)
        print(f"💰 Tax calculated: {tax_result.tax_amount:,.0f} บาท")
        
        # Step 2: Triage - ต้องการการลดภาษีหรือไม่?
        if not tax_result.requires_optimization:
            # ไม่เสียภาษี หรือ เสียภาษีน้อยมาก
            return TaxOptimizationResponse(
                current_tax=tax_result,
                recommendations=[],
                summary=f"""
                ยินดีด้วยครับ! คุณไม่ต้องเสียภาษีเงินได้ หรือเสียภาษีน้อยมาก 
                ({tax_result.tax_amount:,.0f} บาท)
                
                รายได้รวม: {tax_result.gross_income:,.0f} บาท
                ค่าลดหย่อนทั้งหมด: {tax_result.total_deductions:,.0f} บาท
                เงินได้สุทธิ: {tax_result.net_income:,.0f} บาท
                """,
                disclaimer="ข้อมูลนี้เป็นการคำนวณเบื้องต้นเท่านั้น"
            )
        
        # Step 3: ใช้ RAG Pipeline เพื่อหาวิธีลดภาษี
        print(f"🔍 Starting RAG Pipeline for tax optimization...")
        
        # 3.1 Retrieve - ค้นหาข้อมูลที่เกี่ยวข้องจาก Vector DB
        retrieved_context = await rag_service.retrieve_relevant_documents(
            request, tax_result
        )
        print(f"📚 Retrieved context length: {len(retrieved_context)}")
        
        # 3.2 Augmented Generation - ให้ AI สร้างคำแนะนำ
        recommendations_raw = await ai_service.generate_recommendations(
            request, tax_result, retrieved_context
        )
        print(f"🤖 AI generated {len(recommendations_raw)} recommendations")
        
        # 3.3 แปลงเป็น Pydantic Models
        recommendations = [
            Recommendation(**rec) for rec in recommendations_raw
        ]
        
        # Step 4: สร้าง Summary
        total_potential_savings = sum(rec.tax_saving for rec in recommendations)
        summary = f"""
        คุณเสียภาษีปัจจุบัน {tax_result.tax_amount:,.0f} บาท 
        (อัตราภาษีเฉลี่ย {tax_result.effective_tax_rate}%)
        
        เราพบ {len(recommendations)} วิธีที่สามารถช่วยลดภาษีได้
        
        ⭐ แนะนำ: {recommendations[0].strategy}
        💰 สามารถลดภาษีได้มากสุดถึง {total_potential_savings:,.0f} บาท
        
        เลือกวิธีที่เหมาะกับคุณด้านล่าง
        """
        
        response = TaxOptimizationResponse(
            current_tax=tax_result,
            recommendations=recommendations,
            summary=summary,
            disclaimer="⚠️ ข้อมูลนี้เป็นเพียงคำแนะนำเบื้องต้น กรุณาปรึกษาที่ปรึกษาทางการเงินมืออาชีพก่อนตัดสินใจลงทุน"
        )
        
        print(f"✅ Response ready with {len(recommendations)} recommendations")
        return response
        
    except Exception as e:
        print(f"❌ Error in calculate_tax: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"เกิดข้อผิดพลาดในการคำนวณ: {str(e)}"
        )

@app.post("/api/calculate-simple")
async def calculate_tax_simple(request: TaxCalculationRequest):
    """
    คำนวณภาษีเท่านั้น (ไม่ใช้ RAG)
    ใช้สำหรับทดสอบ
    """
    try:
        tax_result = TaxCalculator.calculate(request)
        return tax_result
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error calculating tax: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )