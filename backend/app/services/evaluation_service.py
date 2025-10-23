"""
Evaluation Service สำหรับประเมินคุณภาพคำตอบของ AI
ใช้ ROUGE, BLEU, และ BERTScore
"""

from typing import Dict, List, Any
import numpy as np

# ROUGE
from rouge_score import rouge_scorer

# BLEU
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction

# BERTScore
from bert_score import score as bert_score

# Thai tokenizer
from pythainlp.tokenize import word_tokenize


class EvaluationService:
    """
    Service สำหรับประเมินคุณภาพคำตอบ
    """
    
    def __init__(self):
        # สร้าง ROUGE scorer
        self.rouge_scorer = rouge_scorer.RougeScorer(
            ['rouge1', 'rouge2', 'rougeL'], 
            use_stemmer=False
        )
        
        # BLEU smoothing function
        self.smoothing = SmoothingFunction().method1
    
    def tokenize_thai(self, text: str) -> List[str]:
        """
        Tokenize ภาษาไทย
        
        Args:
            text: ข้อความภาษาไทย
            
        Returns:
            List of tokens
        """
        return word_tokenize(text, engine='newmm')
    
    def calculate_rouge(
        self, 
        reference: str, 
        hypothesis: str
    ) -> Dict[str, float]:
        """
        คำนวณ ROUGE scores
        
        ROUGE-1: Unigram overlap
        ROUGE-2: Bigram overlap
        ROUGE-L: Longest common subsequence
        
        Args:
            reference: คำตอบที่ถูกต้อง (ground truth)
            hypothesis: คำตอบจาก AI
            
        Returns:
            Dict ของ ROUGE scores
        """
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
    
    def calculate_bleu(
        self, 
        reference: str, 
        hypothesis: str
    ) -> Dict[str, float]:
        """
        คำนวณ BLEU score
        
        BLEU วัดความคล้ายของ n-grams ระหว่างคำตอบ
        
        Args:
            reference: คำตอบที่ถูกต้อง
            hypothesis: คำตอบจาก AI
            
        Returns:
            Dict ของ BLEU scores
        """
        # Tokenize
        ref_tokens = self.tokenize_thai(reference)
        hyp_tokens = self.tokenize_thai(hypothesis)
        
        # คำนวณ BLEU-1, BLEU-2, BLEU-3, BLEU-4
        bleu1 = sentence_bleu(
            [ref_tokens], hyp_tokens, 
            weights=(1, 0, 0, 0),
            smoothing_function=self.smoothing
        )
        bleu2 = sentence_bleu(
            [ref_tokens], hyp_tokens, 
            weights=(0.5, 0.5, 0, 0),
            smoothing_function=self.smoothing
        )
        bleu3 = sentence_bleu(
            [ref_tokens], hyp_tokens, 
            weights=(0.33, 0.33, 0.33, 0),
            smoothing_function=self.smoothing
        )
        bleu4 = sentence_bleu(
            [ref_tokens], hyp_tokens, 
            weights=(0.25, 0.25, 0.25, 0.25),
            smoothing_function=self.smoothing
        )
        
        return {
            'bleu1': bleu1,
            'bleu2': bleu2,
            'bleu3': bleu3,
            'bleu4': bleu4,
        }
    
    def calculate_bertscore(
        self, 
        references: List[str], 
        hypotheses: List[str],
        lang: str = 'th'
    ) -> Dict[str, float]:
        """
        คำนวณ BERTScore
        
        BERTScore ใช้ BERT embeddings เพื่อวัดความคล้ายทางความหมาย
        
        Args:
            references: List ของคำตอบที่ถูกต้อง
            hypotheses: List ของคำตอบจาก AI
            lang: ภาษา (th=ไทย, en=อังกฤษ)
            
        Returns:
            Dict ของ BERTScore (Precision, Recall, F1)
        """
        # คำนวณ BERTScore
        P, R, F1 = bert_score(
            hypotheses, 
            references, 
            lang=lang,
            verbose=False,
            model_type='xlm-roberta-base'  # รองรับหลายภาษารวมไทย
        )
        
        return {
            'bertscore_precision': P.mean().item(),
            'bertscore_recall': R.mean().item(),
            'bertscore_f1': F1.mean().item(),
        }
    
    def evaluate_single(
        self, 
        reference: str, 
        hypothesis: str,
        use_bertscore: bool = True
    ) -> Dict[str, Any]:
        """
        ประเมินคำตอบเดียว
        
        Args:
            reference: คำตอบที่ถูกต้อง
            hypothesis: คำตอบจาก AI
            use_bertscore: ใช้ BERTScore หรือไม่ (ใช้เวลานาน)
            
        Returns:
            Dict ของ metrics ทั้งหมด
        """
        results = {}
        
        # ROUGE
        rouge_scores = self.calculate_rouge(reference, hypothesis)
        results.update(rouge_scores)
        
        # BLEU
        bleu_scores = self.calculate_bleu(reference, hypothesis)
        results.update(bleu_scores)
        
        # BERTScore (optional - ใช้เวลานาน)
        if use_bertscore:
            bert_scores = self.calculate_bertscore([reference], [hypothesis])
            results.update(bert_scores)
        
        return results
    
    def evaluate_batch(
        self, 
        references: List[str], 
        hypotheses: List[str],
        use_bertscore: bool = True
    ) -> Dict[str, Any]:
        """
        ประเมินหลายคำตอบพร้อมกัน
        
        Args:
            references: List ของคำตอบที่ถูกต้อง
            hypotheses: List ของคำตอบจาก AI
            use_bertscore: ใช้ BERTScore หรือไม่
            
        Returns:
            Dict ของ metrics เฉลี่ย
        """
        all_rouge1_f1 = []
        all_rouge2_f1 = []
        all_rougeL_f1 = []
        all_bleu4 = []
        
        # คำนวณทีละคู่
        for ref, hyp in zip(references, hypotheses):
            # ROUGE
            rouge_scores = self.calculate_rouge(ref, hyp)
            all_rouge1_f1.append(rouge_scores['rouge1_f1'])
            all_rouge2_f1.append(rouge_scores['rouge2_f1'])
            all_rougeL_f1.append(rouge_scores['rougeL_f1'])
            
            # BLEU
            bleu_scores = self.calculate_bleu(ref, hyp)
            all_bleu4.append(bleu_scores['bleu4'])
        
        results = {
            'rouge1_f1_avg': np.mean(all_rouge1_f1),
            'rouge2_f1_avg': np.mean(all_rouge2_f1),
            'rougeL_f1_avg': np.mean(all_rougeL_f1),
            'bleu4_avg': np.mean(all_bleu4),
        }
        
        # BERTScore (คำนวณทีเดียวทั้ง batch - เร็วกว่า)
        if use_bertscore:
            bert_scores = self.calculate_bertscore(references, hypotheses)
            results.update(bert_scores)
        
        return results
    
    def evaluate_recommendation(
        self,
        reference_recommendation: Dict[str, Any],
        ai_recommendation: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        ประเมินคำแนะนำภาษี (เฉพาะ project นี้)
        
        Args:
            reference_recommendation: คำแนะนำที่ถูกต้อง
            ai_recommendation: คำแนะนำจาก AI
            
        Returns:
            Dict ของ metrics + accuracy ของตัวเลข
        """
        # ประเมินข้อความ
        ref_text = f"{reference_recommendation.get('strategy', '')} {reference_recommendation.get('description', '')}"
        hyp_text = f"{ai_recommendation.get('strategy', '')} {ai_recommendation.get('description', '')}"
        
        text_scores = self.evaluate_single(ref_text, hyp_text, use_bertscore=False)
        
        # ประเมินความแม่นยำของตัวเลข
        numeric_accuracy = {}
        
        numeric_fields = [
            'investment_amount',
            'tax_saving',
            'expected_return_1y',
            'expected_return_3y',
            'expected_return_5y'
        ]
        
        for field in numeric_fields:
            ref_val = reference_recommendation.get(field, 0)
            ai_val = ai_recommendation.get(field, 0)
            
            if ref_val > 0:
                # คำนวณ percentage error
                error = abs(ref_val - ai_val) / ref_val * 100
                accuracy = max(0, 100 - error)
                numeric_accuracy[f'{field}_accuracy'] = accuracy
        
        # รวม scores
        results = {**text_scores, **numeric_accuracy}
        
        return results
    
    def print_evaluation_report(self, results: Dict[str, Any]):
        """
        แสดงผลรายงานการประเมิน
        
        Args:
            results: ผลการประเมิน
        """
        print("\n" + "="*60)
        print("📊 EVALUATION REPORT")
        print("="*60)
        
        # ROUGE
        if 'rouge1_f1' in results:
            print("\n🔴 ROUGE Scores:")
            print(f"  ROUGE-1 F1: {results.get('rouge1_f1', 0):.4f}")
            print(f"  ROUGE-2 F1: {results.get('rouge2_f1', 0):.4f}")
            print(f"  ROUGE-L F1: {results.get('rougeL_f1', 0):.4f}")
        
        # BLEU
        if 'bleu4' in results:
            print("\n🔵 BLEU Scores:")
            print(f"  BLEU-1: {results.get('bleu1', 0):.4f}")
            print(f"  BLEU-2: {results.get('bleu2', 0):.4f}")
            print(f"  BLEU-3: {results.get('bleu3', 0):.4f}")
            print(f"  BLEU-4: {results.get('bleu4', 0):.4f}")
        
        # BERTScore
        if 'bertscore_f1' in results:
            print("\n🟢 BERTScore:")
            print(f"  Precision: {results.get('bertscore_precision', 0):.4f}")
            print(f"  Recall: {results.get('bertscore_recall', 0):.4f}")
            print(f"  F1: {results.get('bertscore_f1', 0):.4f}")
        
        # Numeric Accuracy
        accuracy_keys = [k for k in results.keys() if k.endswith('_accuracy')]
        if accuracy_keys:
            print("\n💰 Numeric Accuracy:")
            for key in accuracy_keys:
                field = key.replace('_accuracy', '')
                print(f"  {field}: {results[key]:.2f}%")
        
        print("\n" + "="*60)


# ==========================================
# ตัวอย่างการใช้งาน
# ==========================================

if __name__ == "__main__":
    evaluator = EvaluationService()
    
    # ตัวอย่างที่ 1: ประเมินคำตอบเดียว
    print("\n📝 Example 1: Single Evaluation")
    
    reference = "ลงทุน RMF 200,000 บาท สามารถลดหย่อนภาษีได้ 50,000 บาท"
    hypothesis = "แนะนำลงทุน RMF จำนวน 200,000 บาท เพื่อลดภาษีได้ 50,000 บาท"
    
    scores = evaluator.evaluate_single(reference, hypothesis, use_bertscore=False)
    evaluator.print_evaluation_report(scores)
    
    # ตัวอย่างที่ 2: ประเมินคำแนะนำ
    print("\n📝 Example 2: Recommendation Evaluation")
    
    reference_rec = {
        "strategy": "ลงทุน RMF 200,000 บาท",
        "description": "ลงทุนในกองทุน RMF ประเภทผสม",
        "investment_amount": 200000,
        "tax_saving": 50000,
        "expected_return_1y": 5.5,
        "expected_return_3y": 6.8,
        "expected_return_5y": 8.0,
    }
    
    ai_rec = {
        "strategy": "ลงทุน RMF 200,000 บาท",
        "description": "ลงทุนในกองทุน RMF กองทุนผสม",
        "investment_amount": 200000,
        "tax_saving": 48000,  # ผิดนิดหน่อย
        "expected_return_1y": 5.8,  # ผิดนิดหน่อย
        "expected_return_3y": 6.5,
        "expected_return_5y": 8.2,
    }
    
    rec_scores = evaluator.evaluate_recommendation(reference_rec, ai_rec)
    evaluator.print_evaluation_report(rec_scores)