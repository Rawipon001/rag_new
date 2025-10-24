"""
Evaluation Runner - Enhanced Version
- แสดงผลสวยงาม อ่านง่าย
- แยกโฟลเดอร์ logs กับ results
- Progress indicator
"""

import sys
import os
import asyncio
import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any

# เพิ่ม path
sys.path.append(str(Path(__file__).parent.parent))

# Import evaluation modules
from app.services.evaluation_service import EvaluationService
from app.services.evaluation_test_data import EvaluationTestData
from app.services.ai_service_for_evaluation import AIServiceForEvaluation

# Import ระบบหลัก
from app.services.rag_service import RAGService
from app.services.tax_calculator import tax_calculator_service
from app.models import TaxCalculationRequest


# ANSI Colors
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'


class EvaluationRunner:
    """
    Runner สำหรับ Evaluation - Enhanced Version
    """
    
    def __init__(
        self, 
        verbose: bool = True, 
        save_logs: bool = True,
        use_bertscore: bool = False
    ):
        self.verbose = verbose
        self.save_logs = save_logs
        self.use_bertscore = use_bertscore
        
        # สร้าง services
        self.evaluator = EvaluationService()
        self.ai_service = AIServiceForEvaluation(verbose=verbose, save_to_file=save_logs)
        self.rag_service = RAGService()
        
        # 📁 แยกโฟลเดอร์ให้ชัดเจน
        self.base_dir = Path("evaluation_output")
        self.logs_dir = self.base_dir / "logs"
        self.results_dir = self.base_dir / "results"
        
        # สร้างโฟลเดอร์
        self.base_dir.mkdir(exist_ok=True)
        self.logs_dir.mkdir(exist_ok=True)
        self.results_dir.mkdir(exist_ok=True)
        
        # อัพเดท ai_service ให้ใช้โฟลเดอร์ logs
        if hasattr(self.ai_service, 'log_dir'):
            self.ai_service.log_dir = self.logs_dir
        
        self.print_header()
    
    def print_header(self):
        """แสดง Header สวยงาม"""
        print("\n" + "="*80)
        print(f"{Colors.BOLD}{Colors.CYAN}🚀 AI TAX ADVISOR - EVALUATION SYSTEM{Colors.END}")
        print("="*80)
        print(f"  📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"  🔧 Mode: {'Verbose' if self.verbose else 'Silent'}")
        print(f"  💾 Save logs: {'Yes' if self.save_logs else 'No'}")
        print(f"  🤖 BERTScore: {'Enabled' if self.use_bertscore else 'Disabled'}")
        print(f"\n  📁 Output directories:")
        print(f"     Logs:    {self.logs_dir}")
        print(f"     Results: {self.results_dir}")
        print("="*80 + "\n")
    
    def print_progress(self, current: int, total: int, message: str = ""):
        """แสดง Progress"""
        percentage = (current / total) * 100
        filled = int((current / total) * 40)
        bar = '█' * filled + '░' * (40 - filled)
        
        print(f"\r  Progress: {bar} {percentage:.0f}% - {message}", end='', flush=True)
        
        if current == total:
            print()  # New line when complete
    
    async def run_single_test_case(
        self,
        test_case: Dict[str, Any],
        test_case_id: int
    ) -> Dict[str, Any]:
        """รัน 1 test case"""
        
        test_name = test_case.get('name', f'Test Case {test_case_id}')
        
        print("\n" + "="*80)
        print(f"{Colors.BOLD}{Colors.BLUE}📋 TEST CASE {test_case_id}: {test_name}{Colors.END}")
        print("="*80)
        print(f"  {Colors.CYAN}{test_case.get('description', 'N/A')}{Colors.END}")
        
        # สร้าง request
        request_data = test_case['input']
        request = TaxCalculationRequest(**request_data)
        
        print(f"\n  💰 รายได้: {Colors.YELLOW}{request.gross_income:,}{Colors.END} บาท")
        print(f"  🎯 ความเสี่ยง: {Colors.YELLOW}{request.risk_tolerance}{Colors.END}")
        
        # Step 1: คำนวณภาษี
        print(f"\n  {Colors.CYAN}[1/4]{Colors.END} คำนวณภาษี...", end='')
        tax_result = tax_calculator_service.calculate_tax(request)
        print(f" {Colors.GREEN}✓{Colors.END}")
        
        print(f"     └─ เงินได้สุทธิ: {tax_result.taxable_income:,} บาท")
        print(f"     └─ ภาษี: {tax_result.tax_amount:,} บาท ({tax_result.effective_tax_rate:.2f}%)")
        
        # Step 2: ดึงข้อมูลจาก RAG
        print(f"  {Colors.CYAN}[2/4]{Colors.END} ดึงข้อมูลจาก RAG...", end='')
        query = f"รายได้ {request.gross_income} บาท ระดับความเสี่ยง {request.risk_tolerance}"
        
        try:
            retrieved_docs = await self.rag_service.retrieve_relevant_documents(query, k=5)
            context_parts = []
            for doc in retrieved_docs:
                if hasattr(doc, 'page_content'):
                    context_parts.append(doc.page_content)
                elif hasattr(doc, 'content'):
                    context_parts.append(doc.content)
                elif isinstance(doc, str):
                    context_parts.append(doc)
            
            context = "\n\n".join(context_parts) if context_parts else "ไม่มีข้อมูลจาก RAG"
            print(f" {Colors.GREEN}✓{Colors.END} ({len(context)} chars)")
        except Exception as e:
            print(f" {Colors.YELLOW}⚠{Colors.END}")
            context = "ไม่มีข้อมูลจาก RAG"
        
        # Step 3: เรียก AI
        print(f"  {Colors.CYAN}[3/4]{Colors.END} เรียก OpenAI...", end='')
        ai_response, raw_response = await self.ai_service.generate_recommendations(
            request, tax_result, context, test_case_id=test_case_id
        )
        print(f" {Colors.GREEN}✓{Colors.END} ({len(ai_response.get('plans', []))} plans)")
        
        # Step 4: ประเมินผล
        print(f"  {Colors.CYAN}[4/4]{Colors.END} ประเมินผล...", end='')
        expected_plans = test_case.get('expected_plans', {})
        
        evaluation_results = self.evaluator.evaluate_complete_response(
            expected_plans,
            ai_response,
            use_bertscore=self.use_bertscore
        )
        print(f" {Colors.GREEN}✓{Colors.END}")
        
        # แสดงรายงาน
        self.evaluator.print_evaluation_report(
            evaluation_results,
            test_case_name=test_name,
            save_to_file=self.save_logs,
            output_dir=self.results_dir
        )
        
        # บันทึกผลลัพธ์
        result = {
            'test_case_id': test_case_id,
            'test_case_name': test_name,
            'input': request_data,
            'tax_result': {
                'gross_income': tax_result.gross_income,
                'taxable_income': tax_result.taxable_income,
                'tax_amount': tax_result.tax_amount,
                'effective_tax_rate': tax_result.effective_tax_rate
            },
            'ai_response': ai_response,
            'expected_plans': expected_plans,
            'evaluation_results': evaluation_results,
            'raw_response_preview': raw_response[:300]
        }
        
        return result
    
    async def run_all_test_cases(self) -> List[Dict[str, Any]]:
        """รันทุก test cases"""
        
        test_cases = EvaluationTestData.get_all_test_cases()
        all_results = []
        
        print(f"\n{Colors.BOLD}🧪 RUNNING {len(test_cases)} TEST CASES{Colors.END}")
        print("="*80 + "\n")
        
        for i, test_case in enumerate(test_cases, 1):
            try:
                result = await self.run_single_test_case(test_case, i)
                all_results.append(result)
                
                # แสดง progress
                self.print_progress(i, len(test_cases), f"Completed {i}/{len(test_cases)}")
                
            except Exception as e:
                print(f"\n{Colors.RED}❌ Error in test case {i}: {e}{Colors.END}")
                import traceback
                traceback.print_exc()
        
        return all_results
    
    def save_final_results(
        self,
        all_results: List[Dict[str, Any]],
        summary: Dict[str, Any]
    ):
        """บันทึกผลลัพธ์สุดท้าย"""
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        print(f"\n{Colors.BOLD}💾 SAVING RESULTS{Colors.END}")
        print("─"*80)
        
        # 1. Detailed Results
        detailed_file = self.results_dir / f"detailed_results_{timestamp}.json"
        with open(detailed_file, 'w', encoding='utf-8') as f:
            json.dump(all_results, f, indent=2, ensure_ascii=False)
        print(f"  {Colors.GREEN}✓{Colors.END} Detailed results: {detailed_file.name}")
        
        # 2. Summary
        summary_file = self.results_dir / f"summary_{timestamp}.json"
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        print(f"  {Colors.GREEN}✓{Colors.END} Summary: {summary_file.name}")
        
        # 3. Human-readable Report
        report_file = self.results_dir / f"report_{timestamp}.txt"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("="*80 + "\n")
            f.write("AI TAX ADVISOR - EVALUATION REPORT\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("="*80 + "\n\n")
            
            f.write(f"Total Test Cases: {summary.get('total_test_cases', 0)}\n\n")
            
            # Text metrics
            if 'text_metrics' in summary and summary['text_metrics']:
                f.write("TEXT SIMILARITY METRICS:\n")
                f.write("-"*40 + "\n")
                for key, value in summary['text_metrics'].items():
                    metric_name = key.replace('avg_', '').upper()
                    f.write(f"  {metric_name:12} : {value:.4f}\n")
                f.write("\n")
            
            # Numeric metrics
            if 'numeric_metrics' in summary and summary['numeric_metrics']:
                f.write("NUMERIC ACCURACY:\n")
                f.write("-"*40 + "\n")
                for key, value in summary['numeric_metrics'].items():
                    metric_name = key.replace('_', ' ').title()
                    f.write(f"  {metric_name:15} : {value:.2f}%\n")
                f.write("\n")
            
            # Test case details
            f.write("\n" + "="*80 + "\n")
            f.write("DETAILED RESULTS BY TEST CASE\n")
            f.write("="*80 + "\n\n")
            
            for result in all_results:
                f.write(f"Test Case {result['test_case_id']}: {result['test_case_name']}\n")
                f.write("-"*80 + "\n")
                
                eval_res = result.get('evaluation_results', {})
                if 'overall_metrics' in eval_res:
                    overall = eval_res['overall_metrics']
                    f.write(f"  Plans: {overall.get('actual_plan_count', 0)}/{overall.get('expected_plan_count', 3)}\n")
                    
                    if 'avg_numeric_accuracy' in overall:
                        f.write(f"  Numeric Accuracy: {overall['avg_numeric_accuracy']:.2f}%\n")
                    
                    if 'text_metrics' in overall:
                        text_m = overall['text_metrics']
                        if 'avg_rouge1_f1' in text_m:
                            f.write(f"  ROUGE-1 F1: {text_m['avg_rouge1_f1']:.4f}\n")
                        if 'avg_bleu4' in text_m:
                            f.write(f"  BLEU-4: {text_m['avg_bleu4']:.4f}\n")
                
                f.write("\n")
        
        print(f"  {Colors.GREEN}✓{Colors.END} Report: {report_file.name}")
        
        # 4. สร้าง README ในโฟลเดอร์ results
        readme_file = self.results_dir / "README.txt"
        with open(readme_file, 'w', encoding='utf-8') as f:
            f.write("="*80 + "\n")
            f.write("EVALUATION RESULTS\n")
            f.write("="*80 + "\n\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("FILES:\n")
            f.write(f"  - detailed_results_{timestamp}.json : Full results with all data\n")
            f.write(f"  - summary_{timestamp}.json          : Summary statistics\n")
            f.write(f"  - report_{timestamp}.txt            : Human-readable report\n")
            f.write(f"  - report_*.json                     : Individual test case reports\n\n")
            f.write("LOGS:\n")
            f.write(f"  See ../logs/ directory for:\n")
            f.write(f"    - prompt_test_case_*.txt         : Prompts sent to OpenAI\n")
            f.write(f"    - raw_response_test_case_*.txt   : Raw responses from OpenAI\n")
            f.write(f"    - parsed_result_test_case_*.json : Parsed results\n")
        
        print(f"  {Colors.GREEN}✓{Colors.END} README: {readme_file.name}")
        print()


async def quick_test():
    """ทดสอบแบบง่ายๆ"""
    
    print(f"\n{Colors.CYAN}🧪 Quick Test - Evaluation Service{Colors.END}\n")
    
    evaluator = EvaluationService()
    
    expected_plan = {
        "plan_id": "1",
        "plan_name": "ทางเลือกที่ 1 - เน้นประกัน",
        "description": "เน้นความคุ้มครองและความปลอดภัย",
        "total_investment": 150000,
        "total_tax_saving": 15000,
        "allocations": [
            {
                "category": "ประกันชีวิต",
                "investment_amount": 50000,
                "percentage": 33.33,
                "tax_saving": 5000,
                "risk_level": "low"
            }
        ]
    }
    
    ai_plan = {
        "plan_id": "1",
        "plan_name": "ทางเลือกที่ 1 - เน้นความปลอดภัย",
        "description": "เน้นความคุ้มครองและสร้างรากฐาน",
        "total_investment": 145000,
        "total_tax_saving": 14500,
        "allocations": [
            {
                "category": "ประกันชีวิต",
                "investment_amount": 48000,
                "percentage": 33.10,
                "tax_saving": 4800,
                "risk_level": "low"
            }
        ]
    }
    
    print("Evaluating sample plan...")
    results = evaluator.evaluate_plan(expected_plan, ai_plan, use_bertscore=False)
    
    # แสดงผลสวยงาม
    evaluator.print_evaluation_report(
        {'plan_metrics': {'plan_1': results}},
        test_case_name="Quick Test Sample"
    )


async def main():
    """Main function"""
    
    parser = argparse.ArgumentParser(
        description='AI Tax Advisor - Enhanced Evaluation',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run_evaluation_complete.py --mode quick
  python run_evaluation_complete.py --mode full
  python run_evaluation_complete.py --mode full --test-case 1
  python run_evaluation_complete.py --mode full --bertscore
        """
    )
    
    parser.add_argument('--mode', choices=['quick', 'full'], default='quick',
                       help='Evaluation mode')
    parser.add_argument('--test-case', type=int, choices=[1, 2, 3],
                       help='Run specific test case')
    parser.add_argument('--bertscore', action='store_true',
                       help='Use BERTScore (slower)')
    parser.add_argument('--no-verbose', action='store_true',
                       help='Disable verbose logging')
    parser.add_argument('--no-save', action='store_true',
                       help='Disable saving logs')
    
    args = parser.parse_args()
    
    if args.mode == 'quick':
        await quick_test()
        return
    
    # Full evaluation
    runner = EvaluationRunner(
        verbose=not args.no_verbose,
        save_logs=not args.no_save,
        use_bertscore=args.bertscore
    )
    
    # รัน specific test case หรือทั้งหมด
    if args.test_case:
        test_case = EvaluationTestData.get_test_case_by_id(args.test_case)
        result = await runner.run_single_test_case(test_case, args.test_case)
        all_results = [result]
    else:
        all_results = await runner.run_all_test_cases()
    
    # สร้าง summary
    print(f"\n{Colors.BOLD}{Colors.HEADER}📈 GENERATING SUMMARY{Colors.END}")
    print("="*80 + "\n")
    
    evaluation_results = [r['evaluation_results'] for r in all_results if 'evaluation_results' in r]
    summary = runner.evaluator.generate_summary_statistics(evaluation_results)
    
    runner.evaluator.print_summary_report(summary)
    
    # บันทึกผลลัพธ์
    runner.save_final_results(all_results, summary)
    
    # Final summary
    print(f"\n{Colors.BOLD}{Colors.GREEN}✅ EVALUATION COMPLETED!{Colors.END}")
    print("="*80)
    print(f"  Test cases: {len(all_results)}")
    print(f"  Results: {runner.results_dir}")
    print(f"  Logs: {runner.logs_dir}")
    
    if 'numeric_metrics' in summary and 'avg_accuracy' in summary['numeric_metrics']:
        acc = summary['numeric_metrics']['avg_accuracy']
        print(f"  Average accuracy: {Colors.CYAN}{acc:.2f}%{Colors.END}")
    
    print("="*80 + "\n")


if __name__ == "__main__":
    asyncio.run(main())