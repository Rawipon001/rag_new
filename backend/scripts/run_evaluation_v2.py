"""
Script สำหรับรัน Evaluation
ใช้ AIServiceForEvaluation แยกจากระบบหลัก

วิธีใช้งาน:
    python backend/scripts/run_evaluation.py --mode quick
    python backend/scripts/run_evaluation.py --mode full
    python backend/scripts/run_evaluation.py --mode full --no-save
"""

import sys
import os
import asyncio
import json
import argparse
from pathlib import Path
from datetime import datetime

# เพิ่ม path
sys.path.append(str(Path(__file__).parent.parent))

# ระบบ Evaluation (ใหม่)
from app.services.evaluation_service import EvaluationService
from app.services.evaluation_test_data import EvaluationTestData
from app.services.ai_service_for_evaluation import AIServiceForEvaluation  # ← ใช้ตัวใหม่!

# ระบบหลัก (เดิม)
from app.services.rag_service import RAGService
from app.services.tax_service import TaxService, TaxCalculationRequest  # ← import จาก tax_service


async def evaluate_ai_recommendations(verbose: bool = True, save_logs: bool = True):
    """
    ประเมินคำแนะนำจาก AI ทั้งหมด
    
    Args:
        verbose: แสดงข้อความ debug
        save_logs: บันทึก logs ลงไฟล์
    """
    print("\n" + "="*80)
    print("🚀 STARTING AI TAX ADVISOR EVALUATION")
    print("="*80)
    print(f"⚙️  Verbose: {verbose}")
    print(f"💾 Save logs: {save_logs}")
    print("="*80 + "\n")
    
    # สร้าง services
    evaluator = EvaluationService()
    ai_service = AIServiceForEvaluation(verbose=verbose, save_to_file=save_logs)  # ← ใช้ตัวใหม่!
    rag_service = RAGService()
    tax_service = TaxService()
    
    # แสดงตำแหน่ง log directory
    if save_logs:
        print(f"📂 Logs will be saved to: {ai_service.log_dir}\n")
    
    # ดึง test cases
    test_cases = EvaluationTestData.get_all_test_cases()
    
    all_results = []
    
    for idx, test_case in enumerate(test_cases, 1):
        print(f"\n{'='*80}")
        print(f"📋 TEST CASE {idx} / {len(test_cases)}")
        print(f"{'='*80}")
        
        # สร้าง request
        request = TaxCalculationRequest(**test_case['input'])
        print(f"\n💰 รายได้: {request.gross_income:,} บาท")
        print(f"🎯 ระดับความเสี่ยง: {request.risk_tolerance}")
        
        # คำนวณภาษี
        tax_result = tax_service.calculate_tax(request)
        print(f"💸 ภาษีที่ต้องจ่าย: {tax_result.tax_amount:,} บาท")
        
        # ดึงข้อมูลจาก RAG
        query = f"""รายได้ {request.gross_income} บาท ระดับความเสี่ยง {request.risk_tolerance} ต้องการลดภาษี"""
        
        try:
            # ลองเรียกแบบปกติก่อน
            retrieved_docs = await rag_service.retrieve_relevant_documents(query)
        except TypeError:
            # ถ้า error แสดงว่า rag_service ต้องการ parameter เพิ่ม
            # ลองส่ง tax_result ด้วย
            try:
                retrieved_docs = await rag_service.retrieve_relevant_documents(query, tax_result)
            except:
                # ถ้ายัง error ใช้ mock data
                print("⚠️  RAG service error, using mock data")
                retrieved_docs = [type('obj', (object,), {'page_content': 'RMF ลดหย่อนภาษีได้ 30% ของรายได้'})()]
        
        
        # ดึง content จาก documents (รองรับหลายรูปแบบ)
        context_parts = []
        for doc in retrieved_docs:
            if hasattr(doc, 'page_content'):
                context_parts.append(doc.page_content)
            elif hasattr(doc, 'content'):
                context_parts.append(doc.content)
            elif isinstance(doc, str):
                context_parts.append(doc)
            elif isinstance(doc, dict):
                context_parts.append(doc.get('content', '') or doc.get('page_content', ''))
        
        context = "\n\n".join(context_parts) if context_parts else "ไม่มีข้อมูลจาก RAG"
        
        # เรียก AI (ตัวใหม่ที่แสดง raw response)
        print(f"\n🤖 กำลังสร้างคำแนะนำจาก AI...\n")
        ai_recommendations, raw_response = await ai_service.generate_recommendations(
            request, tax_result, context, test_case_id=idx
        )
        
        print(f"✅ AI สร้างคำแนะนำ {len(ai_recommendations)} รายการ")
        
        # ประเมินแต่ละคำแนะนำ
        expected_recommendations = test_case['expected_recommendations']
        
        case_results = {
            'test_case': idx,
            'input': test_case['input'],
            'raw_response': raw_response,  # ← เก็บ raw response ด้วย
            'ai_recommendations_count': len(ai_recommendations),
            'expected_recommendations_count': len(expected_recommendations),
            'evaluations': []
        }
        
        # ประเมินคำแนะนำทีละตัว
        for ai_rec_idx, ai_rec in enumerate(ai_recommendations[:3], 1):
            if ai_rec_idx <= len(expected_recommendations):
                expected_rec = expected_recommendations[ai_rec_idx - 1]
                
                print(f"\n{'─'*80}")
                print(f"📊 ประเมินคำแนะนำที่ {ai_rec_idx}")
                print(f"{'─'*80}")
                
                print(f"\n✅ Expected: {expected_rec['strategy']}")
                print(f"🤖 AI:       {ai_rec.get('strategy', 'N/A')}")
                
                # ประเมิน
                eval_result = evaluator.evaluate_recommendation(
                    expected_rec, ai_rec
                )
                
                evaluator.print_evaluation_report(eval_result)
                
                case_results['evaluations'].append({
                    'recommendation_index': ai_rec_idx,
                    'expected': expected_rec,
                    'ai': ai_rec,
                    'scores': eval_result
                })
        
        all_results.append(case_results)
    
    # สรุปผลรวม
    print(f"\n{'='*80}")
    print("📈 OVERALL SUMMARY")
    print(f"{'='*80}")
    
    # คำนวณค่าเฉลี่ย
    all_rouge1 = []
    all_rouge2 = []
    all_rougeL = []
    all_bleu4 = []
    all_investment_accuracy = []
    all_tax_saving_accuracy = []
    
    for case in all_results:
        for eval_item in case['evaluations']:
            scores = eval_item['scores']
            all_rouge1.append(scores.get('rouge1_f1', 0))
            all_rouge2.append(scores.get('rouge2_f1', 0))
            all_rougeL.append(scores.get('rougeL_f1', 0))
            all_bleu4.append(scores.get('bleu4', 0))
            all_investment_accuracy.append(scores.get('investment_amount_accuracy', 0))
            all_tax_saving_accuracy.append(scores.get('tax_saving_accuracy', 0))
    
    import numpy as np
    
    print(f"\n🔴 ROUGE Scores (Average):")
    print(f"  ROUGE-1 F1: {np.mean(all_rouge1):.4f}")
    print(f"  ROUGE-2 F1: {np.mean(all_rouge2):.4f}")
    print(f"  ROUGE-L F1: {np.mean(all_rougeL):.4f}")
    
    print(f"\n🔵 BLEU Score (Average):")
    print(f"  BLEU-4: {np.mean(all_bleu4):.4f}")
    
    print(f"\n💰 Numeric Accuracy (Average):")
    print(f"  Investment Amount: {np.mean(all_investment_accuracy):.2f}%")
    print(f"  Tax Saving: {np.mean(all_tax_saving_accuracy):.2f}%")
    
    # บันทึกผลลงไฟล์
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # สร้างโฟลเดอร์ถ้ายังไม่มี
    output_dir = Path("evaluation_results")
    output_dir.mkdir(exist_ok=True)
    
    output_file = output_dir / f"evaluation_results_{timestamp}.json"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_results, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 บันทึกผลลงไฟล์: {output_file}")
    
    if save_logs:
        print(f"📂 Raw responses และ logs อยู่ที่: {ai_service.log_dir}")
    
    print(f"\n{'='*80}")
    print("✨ EVALUATION COMPLETED!")
    print(f"{'='*80}\n")


async def quick_test(verbose: bool = True, save_logs: bool = True):
    """
    ทดสอบแบบง่ายๆ
    """
    print("\n🧪 Quick Test - Evaluation Service with Raw Response\n")
    
    evaluator = EvaluationService()
    
    # ตัวอย่างคำตอบ
    reference = "ลงทุน RMF 200,000 บาท สามารถลดหย่อนภาษีได้ 50,000 บาท และได้ผลตอบแทนประมาณ 8% ต่อปี"
    hypothesis = "แนะนำลงทุน RMF จำนวน 200,000 บาท เพื่อลดภาษีได้ 50,000 บาท คาดว่าจะได้ผลตอบแทน 8% ต่อปี"
    
    scores = evaluator.evaluate_single(reference, hypothesis, use_bertscore=False)
    evaluator.print_evaluation_report(scores)
    
    print("\n" + "="*80)
    print("ℹ️  หมายเหตุ:")
    print("="*80)
    print("Quick test ไม่ได้เรียก OpenAI")
    print("ถ้าต้องการดู raw response จาก OpenAI ให้รัน:")
    print("  python backend/scripts/run_evaluation.py --mode full")
    print("="*80 + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Evaluate AI Tax Advisor')
    parser.add_argument(
        '--mode',
        choices=['full', 'quick'],
        default='quick',
        help='Evaluation mode: full (ประเมินทั้งหมด) or quick (ทดสอบเร็ว)'
    )
    parser.add_argument(
        '--no-verbose',
        action='store_true',
        help='ปิดการแสดงข้อความ debug'
    )
    parser.add_argument(
        '--no-save',
        action='store_true',
        help='ไม่บันทึก logs ลงไฟล์'
    )
    
    args = parser.parse_args()
    
    verbose = not args.no_verbose
    save_logs = not args.no_save
    
    if args.mode == 'full':
        print("🚀 Running FULL evaluation...")
        print(f"   - Verbose: {verbose}")
        print(f"   - Save logs: {save_logs}")
        asyncio.run(evaluate_ai_recommendations(verbose=verbose, save_logs=save_logs))
    else:
        print("⚡ Running QUICK test...")
        asyncio.run(quick_test(verbose=verbose, save_logs=save_logs))