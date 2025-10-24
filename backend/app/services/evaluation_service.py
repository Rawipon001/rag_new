"""
Evaluation Service - Enhanced Version
ปรับปรุงให้แสดงผลสวยงาม อ่านง่าย และจัดโฟลเดอร์เป็นระเบียบ
"""

from typing import Dict, List, Any, Tuple
import numpy as np
import json
from pathlib import Path
from datetime import datetime

# ROUGE
from rouge_score import rouge_scorer

# BLEU
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction

# BERTScore (Optional)
try:
    from bert_score import score as bert_score
    BERTSCORE_AVAILABLE = True
except:
    BERTSCORE_AVAILABLE = False

# Thai tokenizer (Optional)
try:
    from pythainlp.tokenize import word_tokenize
    THAI_TOKENIZER_AVAILABLE = True
except:
    THAI_TOKENIZER_AVAILABLE = False


class Colors:
    """ANSI Color codes สำหรับ terminal"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class EvaluationService:
    """
    Service สำหรับประเมินคุณภาพคำตอบ AI Tax Advisor
    Enhanced Version - แสดงผลสวยงามและอ่านง่าย
    """
    
    def __init__(self):
        # ROUGE scorer
        self.rouge_scorer = rouge_scorer.RougeScorer(
            ['rouge1', 'rouge2', 'rougeL'], 
            use_stemmer=False
        )
        
        # BLEU smoothing
        self.smoothing = SmoothingFunction().method1
        
        print(f"{Colors.GREEN}✅ Evaluation Service initialized{Colors.END}")
    
    def tokenize_thai(self, text: str) -> List[str]:
        """Tokenize ภาษาไทย"""
        if THAI_TOKENIZER_AVAILABLE:
            return word_tokenize(text, engine='newmm')
        else:
            return text.split()
    
    def calculate_rouge(self, reference: str, hypothesis: str) -> Dict[str, float]:
        """คำนวณ ROUGE scores"""
        scores = self.rouge_scorer.score(reference, hypothesis)
        
        return {
            'rouge1_precision': scores['rouge1'].precision,
            'rouge1_recall': scores['rouge1'].recall,
            'rouge1_f1': scores['rouge1'].fmeasure,
            'rouge2_precision': scores['rouge2'].precision,
            'rouge2_recall': scores['rouge2'].recall,
            'rouge2_f1': scores['rouge2'].fmeasure,
            'rougeL_precision': scores['rougeL'].precision,
            'rougeL_recall': scores['rougeL'].recall,
            'rougeL_f1': scores['rougeL'].fmeasure,
        }
    
    def calculate_bleu(self, reference: str, hypothesis: str) -> Dict[str, float]:
        """คำนวณ BLEU score"""
        ref_tokens = self.tokenize_thai(reference)
        hyp_tokens = self.tokenize_thai(hypothesis)
        
        bleu1 = sentence_bleu([ref_tokens], hyp_tokens, weights=(1, 0, 0, 0), smoothing_function=self.smoothing)
        bleu2 = sentence_bleu([ref_tokens], hyp_tokens, weights=(0.5, 0.5, 0, 0), smoothing_function=self.smoothing)
        bleu3 = sentence_bleu([ref_tokens], hyp_tokens, weights=(0.33, 0.33, 0.33, 0), smoothing_function=self.smoothing)
        bleu4 = sentence_bleu([ref_tokens], hyp_tokens, weights=(0.25, 0.25, 0.25, 0.25), smoothing_function=self.smoothing)
        
        return {
            'bleu1': bleu1,
            'bleu2': bleu2,
            'bleu3': bleu3,
            'bleu4': bleu4,
        }
    
    def calculate_numeric_accuracy(self, expected_value: float, actual_value: float, tolerance: float = 0.1) -> Tuple[float, bool]:
        """คำนวณความแม่นยำของตัวเลข"""
        if expected_value == 0:
            return (100.0, actual_value == 0)
        
        error_percentage = abs(expected_value - actual_value) / expected_value
        accuracy = max(0, (1 - error_percentage) * 100)
        is_within_tolerance = error_percentage <= tolerance
        
        return (accuracy, is_within_tolerance)
    
    def get_score_color(self, score: float, metric_type: str = 'general') -> str:
        """เลือกสีตามคะแนน"""
        if metric_type == 'accuracy':
            if score >= 90:
                return Colors.GREEN
            elif score >= 75:
                return Colors.YELLOW
            else:
                return Colors.RED
        else:  # text metrics
            if score >= 0.4:
                return Colors.GREEN
            elif score >= 0.25:
                return Colors.YELLOW
            else:
                return Colors.RED
    
    def get_score_emoji(self, score: float, metric_type: str = 'general') -> str:
        """เลือก emoji ตามคะแนน"""
        if metric_type == 'accuracy':
            if score >= 90:
                return "🎯"
            elif score >= 75:
                return "✅"
            else:
                return "⚠️"
        else:  # text metrics
            if score >= 0.4:
                return "🎯"
            elif score >= 0.25:
                return "✅"
            else:
                return "⚠️"
    
    def print_progress_bar(self, value: float, max_value: float = 100, width: int = 30):
        """แสดง progress bar"""
        percentage = (value / max_value) * 100
        filled = int((value / max_value) * width)
        bar = '█' * filled + '░' * (width - filled)
        
        color = self.get_score_color(percentage, 'accuracy')
        emoji = self.get_score_emoji(percentage, 'accuracy')
        
        return f"{emoji} {color}{bar}{Colors.END} {percentage:.1f}%"
    
    def evaluate_plan(self, expected_plan: Dict[str, Any], ai_plan: Dict[str, Any], use_bertscore: bool = False) -> Dict[str, Any]:
        """ประเมิน 1 แผนการลงทุน"""
        results = {
            'text_metrics': {},
            'numeric_metrics': {},
            'structural_metrics': {}
        }
        
        # 1. ประเมินข้อความ
        expected_text = f"{expected_plan.get('description', '')} {expected_plan.get('plan_name', '')}"
        ai_text = f"{ai_plan.get('description', '')} {ai_plan.get('plan_name', '')}"
        
        if expected_text.strip() and ai_text.strip():
            rouge_scores = self.calculate_rouge(expected_text, ai_text)
            bleu_scores = self.calculate_bleu(expected_text, ai_text)
            results['text_metrics'] = {**rouge_scores, **bleu_scores}
        
        # 2. ประเมินตัวเลข
        numeric_fields = ['total_investment', 'total_tax_saving']
        for field in numeric_fields:
            expected_val = expected_plan.get(field, 0)
            ai_val = ai_plan.get(field, 0)
            
            if expected_val > 0:
                accuracy, within_tolerance = self.calculate_numeric_accuracy(expected_val, ai_val, tolerance=0.15)
                
                results['numeric_metrics'][field] = {
                    'expected': expected_val,
                    'actual': ai_val,
                    'accuracy': accuracy,
                    'within_tolerance': within_tolerance,
                    'error_percentage': abs(expected_val - ai_val) / expected_val * 100 if expected_val > 0 else 0
                }
        
        # 3. ประเมินโครงสร้าง
        expected_allocations = expected_plan.get('allocations', [])
        ai_allocations = ai_plan.get('allocations', [])
        
        results['structural_metrics'] = {
            'expected_allocation_count': len(expected_allocations),
            'actual_allocation_count': len(ai_allocations),
            'has_correct_structure': 'allocations' in ai_plan and len(ai_allocations) > 0
        }
        
        # 4. ประเมิน allocations
        allocation_scores = []
        for i, (exp_alloc, ai_alloc) in enumerate(zip(expected_allocations, ai_allocations[:len(expected_allocations)])):
            alloc_score = self.evaluate_allocation(exp_alloc, ai_alloc)
            allocation_scores.append(alloc_score)
        
        if allocation_scores:
            results['allocation_metrics'] = {
                'individual_scores': allocation_scores,
                'average_investment_accuracy': np.mean([s.get('investment_accuracy', 0) for s in allocation_scores]),
                'average_tax_saving_accuracy': np.mean([s.get('tax_saving_accuracy', 0) for s in allocation_scores])
            }
        
        return results
    
    def evaluate_allocation(self, expected_alloc: Dict[str, Any], ai_alloc: Dict[str, Any]) -> Dict[str, float]:
        """ประเมิน 1 allocation item"""
        results = {}
        
        exp_inv = expected_alloc.get('investment_amount', 0)
        ai_inv = ai_alloc.get('investment_amount', 0)
        if exp_inv > 0:
            inv_accuracy, _ = self.calculate_numeric_accuracy(exp_inv, ai_inv, tolerance=0.2)
            results['investment_accuracy'] = inv_accuracy
        
        exp_tax = expected_alloc.get('tax_saving', 0)
        ai_tax = ai_alloc.get('tax_saving', 0)
        if exp_tax > 0:
            tax_accuracy, _ = self.calculate_numeric_accuracy(exp_tax, ai_tax, tolerance=0.2)
            results['tax_saving_accuracy'] = tax_accuracy
        
        results['category_match'] = expected_alloc.get('category', '').lower() in ai_alloc.get('category', '').lower()
        
        return results
    
    def evaluate_complete_response(self, expected_plans: Dict[str, Dict], ai_response: Dict[str, Any], use_bertscore: bool = False) -> Dict[str, Any]:
        """ประเมินคำตอบทั้งหมด (3 แผน)"""
        results = {
            'overall_metrics': {},
            'plan_metrics': {}
        }
        
        ai_plans = ai_response.get('plans', [])
        
        results['overall_metrics']['expected_plan_count'] = 3
        results['overall_metrics']['actual_plan_count'] = len(ai_plans)
        results['overall_metrics']['has_all_plans'] = len(ai_plans) >= 3
        
        plan_keys = ['plan_1', 'plan_2', 'plan_3']
        all_text_scores = []
        all_numeric_scores = []
        
        for i, (plan_key, ai_plan) in enumerate(zip(plan_keys, ai_plans[:3])):
            expected_plan = expected_plans.get(plan_key, {})
            
            if expected_plan:
                plan_results = self.evaluate_plan(expected_plan, ai_plan, use_bertscore)
                results['plan_metrics'][f'plan_{i+1}'] = plan_results
                
                if 'text_metrics' in plan_results:
                    all_text_scores.append(plan_results['text_metrics'])
                if 'numeric_metrics' in plan_results:
                    all_numeric_scores.append(plan_results['numeric_metrics'])
        
        # คำนวณค่าเฉลี่ย
        if all_text_scores:
            avg_text_metrics = {}
            for key in all_text_scores[0].keys():
                values = [s[key] for s in all_text_scores if key in s]
                if values:
                    avg_text_metrics[f'avg_{key}'] = np.mean(values)
            results['overall_metrics']['text_metrics'] = avg_text_metrics
        
        if all_numeric_scores:
            all_accuracies = []
            for plan_numerics in all_numeric_scores:
                for field, data in plan_numerics.items():
                    if isinstance(data, dict) and 'accuracy' in data:
                        all_accuracies.append(data['accuracy'])
            
            if all_accuracies:
                results['overall_metrics']['avg_numeric_accuracy'] = np.mean(all_accuracies)
        
        return results
    
    def print_evaluation_report(self, results: Dict[str, Any], test_case_name: str = "", save_to_file: bool = False, output_dir: Path = None):
        """แสดงรายงานที่สวยงามและอ่านง่าย"""
        
        print("\n" + "="*80)
        print(f"{Colors.BOLD}{Colors.CYAN}📊 EVALUATION REPORT{Colors.END}")
        if test_case_name:
            print(f"{Colors.YELLOW}Test Case: {test_case_name}{Colors.END}")
        print("="*80 + "\n")
        
        # Overall Summary
        if 'overall_metrics' in results:
            overall = results['overall_metrics']
            
            print(f"{Colors.BOLD}🎯 OVERALL SUMMARY{Colors.END}")
            print("─" * 80)
            
            # Plans count
            plan_count = overall.get('actual_plan_count', 0)
            expected_count = overall.get('expected_plan_count', 3)
            has_all = overall.get('has_all_plans', False)
            
            status_emoji = "✅" if has_all else "❌"
            status_color = Colors.GREEN if has_all else Colors.RED
            
            print(f"  Plans Generated: {status_color}{plan_count}/{expected_count} {status_emoji}{Colors.END}")
            
            # Numeric Accuracy
            if 'avg_numeric_accuracy' in overall:
                acc = overall['avg_numeric_accuracy']
                print(f"\n  💰 Numeric Accuracy:")
                print(f"     {self.print_progress_bar(acc, 100, 40)}")
                print(f"     Value: {acc:.2f}%")
            
            # Text Similarity
            if 'text_metrics' in overall:
                text_m = overall['text_metrics']
                print(f"\n  📝 Text Similarity:")
                
                if 'avg_rouge1_f1' in text_m:
                    score = text_m['avg_rouge1_f1']
                    color = self.get_score_color(score, 'general')
                    emoji = self.get_score_emoji(score, 'general')
                    print(f"     {emoji} ROUGE-1: {color}{score:.4f}{Colors.END}")
                
                if 'avg_rouge2_f1' in text_m:
                    score = text_m['avg_rouge2_f1']
                    color = self.get_score_color(score, 'general')
                    emoji = self.get_score_emoji(score, 'general')
                    print(f"     {emoji} ROUGE-2: {color}{score:.4f}{Colors.END}")
                
                if 'avg_bleu4' in text_m:
                    score = text_m['avg_bleu4']
                    color = self.get_score_color(score, 'general')
                    emoji = self.get_score_emoji(score, 'general')
                    print(f"     {emoji} BLEU-4:  {color}{score:.4f}{Colors.END}")
            
            print()
        
        # Plan by Plan
        if 'plan_metrics' in results:
            print(f"\n{Colors.BOLD}📋 DETAILED RESULTS BY PLAN{Colors.END}")
            print("="*80 + "\n")
            
            for plan_key, plan_results in results['plan_metrics'].items():
                plan_num = plan_key.split('_')[1]
                print(f"{Colors.BOLD}{Colors.BLUE}▶ Plan {plan_num}{Colors.END}")
                print("─" * 80)
                
                # Numeric metrics
                if 'numeric_metrics' in plan_results:
                    num_m = plan_results['numeric_metrics']
                    
                    for field, data in num_m.items():
                        if isinstance(data, dict):
                            acc = data['accuracy']
                            expected = data['expected']
                            actual = data['actual']
                            within = data['within_tolerance']
                            
                            status = "✅" if within else "⚠️"
                            color = Colors.GREEN if within else Colors.YELLOW
                            
                            field_display = field.replace('_', ' ').title()
                            
                            print(f"\n  {Colors.BOLD}{field_display}:{Colors.END} {status}")
                            print(f"    Expected: {expected:>12,.0f} บาท")
                            print(f"    Actual:   {actual:>12,.0f} บาท")
                            print(f"    Accuracy: {color}{acc:.1f}%{Colors.END}")
                
                # Allocation metrics
                if 'allocation_metrics' in plan_results:
                    alloc_m = plan_results['allocation_metrics']
                    print(f"\n  {Colors.BOLD}Allocation Accuracy:{Colors.END}")
                    
                    inv_acc = alloc_m['average_investment_accuracy']
                    tax_acc = alloc_m['average_tax_saving_accuracy']
                    
                    print(f"    Investment: {self.print_progress_bar(inv_acc, 100, 30)}")
                    print(f"    Tax Saving: {self.print_progress_bar(tax_acc, 100, 30)}")
                
                print()
        
        print("="*80 + "\n")
        
        # Save to file
        if save_to_file and output_dir:
            output_dir.mkdir(parents=True, exist_ok=True)
            report_file = output_dir / f"report_{test_case_name.replace(' ', '_')}.json"
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            print(f"{Colors.GREEN}💾 Report saved to: {report_file}{Colors.END}\n")
    
    def generate_summary_statistics(self, all_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """สร้างสถิติสรุป"""
        summary = {
            'total_test_cases': len(all_results),
            'text_metrics': {},
            'numeric_metrics': {}
        }
        
        all_rouge1 = []
        all_rouge2 = []
        all_bleu4 = []
        all_numeric_acc = []
        
        for result in all_results:
            if 'overall_metrics' in result:
                overall = result['overall_metrics']
                
                if 'text_metrics' in overall:
                    text_m = overall['text_metrics']
                    if 'avg_rouge1_f1' in text_m:
                        all_rouge1.append(text_m['avg_rouge1_f1'])
                    if 'avg_rouge2_f1' in text_m:
                        all_rouge2.append(text_m['avg_rouge2_f1'])
                    if 'avg_bleu4' in text_m:
                        all_bleu4.append(text_m['avg_bleu4'])
                
                if 'avg_numeric_accuracy' in overall:
                    all_numeric_acc.append(overall['avg_numeric_accuracy'])
        
        if all_rouge1:
            summary['text_metrics']['avg_rouge1_f1'] = np.mean(all_rouge1)
        if all_rouge2:
            summary['text_metrics']['avg_rouge2_f1'] = np.mean(all_rouge2)
        if all_bleu4:
            summary['text_metrics']['avg_bleu4'] = np.mean(all_bleu4)
        if all_numeric_acc:
            summary['numeric_metrics']['avg_accuracy'] = np.mean(all_numeric_acc)
            summary['numeric_metrics']['min_accuracy'] = np.min(all_numeric_acc)
            summary['numeric_metrics']['max_accuracy'] = np.max(all_numeric_acc)
        
        return summary
    
    def print_summary_report(self, summary: Dict[str, Any]):
        """แสดงรายงานสรุปแบบสวยงาม"""
        
        print("\n" + "="*80)
        print(f"{Colors.BOLD}{Colors.HEADER}📈 FINAL SUMMARY STATISTICS{Colors.END}")
        print("="*80 + "\n")
        
        total = summary.get('total_test_cases', 0)
        print(f"{Colors.BOLD}Total Test Cases:{Colors.END} {Colors.CYAN}{total}{Colors.END}\n")
        
        # Text Metrics
        if 'text_metrics' in summary and summary['text_metrics']:
            print(f"{Colors.BOLD}📝 Text Similarity (Average Across All Tests):{Colors.END}")
            print("─" * 80)
            
            for key, value in summary['text_metrics'].items():
                metric_name = key.replace('avg_', '').replace('_', '-').upper()
                color = self.get_score_color(value, 'general')
                emoji = self.get_score_emoji(value, 'general')
                print(f"  {emoji} {metric_name:12} : {color}{value:.4f}{Colors.END}")
            print()
        
        # Numeric Metrics
        if 'numeric_metrics' in summary and summary['numeric_metrics']:
            print(f"{Colors.BOLD}💰 Numeric Accuracy:{Colors.END}")
            print("─" * 80)
            
            for key, value in summary['numeric_metrics'].items():
                metric_name = key.replace('_', ' ').title()
                color = self.get_score_color(value, 'accuracy')
                emoji = self.get_score_emoji(value, 'accuracy')
                print(f"  {emoji} {metric_name:15} : {color}{value:.2f}%{Colors.END}")
            print()
        
        print("="*80 + "\n")