import text_processor_rust
from typing import Dict, List, Any
import time

class TextProcessorService:
    @staticmethod
    def count_words(text: str) -> Dict[str, Any]:
        start_time = time.time()
        
        # Call Rust extension
        word_count = text_processor_rust.count_words(text)
        
        processing_time = time.time() - start_time
        
        return {
            "word_count": word_count,
            "total_words": sum(word_count.values()),
            "unique_words": len(word_count),
            "processing_time_ms": round(processing_time * 1000, 2)
        }
    
    @staticmethod
    def extract_emails(text: str) -> Dict[str, Any]:
        start_time = time.time()
        
        emails = text_processor_rust.extract_emails(text)
        
        processing_time = time.time() - start_time
        
        return {
            "emails": emails,
            "email_count": len(emails),
            "processing_time_ms": round(processing_time * 1000, 2)
        }
    
    @staticmethod
    def clean_text(text: str) -> Dict[str, Any]:
        start_time = time.time()
        
        cleaned = text_processor_rust.clean_text(text)
        
        processing_time = time.time() - start_time
        
        return {
            "cleaned_text": cleaned,
            "original_length": len(text),
            "cleaned_length": len(cleaned),
            "processing_time_ms": round(processing_time * 1000, 2)
        }
    
class SentimentService:
    @staticmethod
    def analyze_sentiment(text: str) -> Dict[str, Any]:
        """分析文本情感"""
        start_time = time.time()
        
        try:
            # 调用Rust扩展
            result = text_processor_rust.analyze_sentiment(text)
            
            # 添加处理时间
            processing_time_ms = int((time.time() - start_time) * 1000)
            result['processing_time_ms'] = processing_time_ms
            
            return result
            
        except Exception as e:
            raise ValueError(f"Sentiment analysis failed: {str(e)}")
    
    @staticmethod
    def batch_analyze_sentiment(texts: List[str]) -> List[Dict[str, Any]]:
        """批量情感分析"""
        return [SentimentService.analyze_sentiment(text) for text in texts]