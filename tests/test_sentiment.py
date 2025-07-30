import pytest
from app.services import SentimentService

class TestSentimentAnalysis:
    
    def test_english_positive_sentiment(self):
        """测试英文积极情感"""
        text = "Extremely fantastic! I very love it!"
        result = SentimentService.analyze_sentiment(text)
        
        assert result['score'] > 0.3
        assert result['label'] == 'positive'
        assert result['confidence'] > 0.5
        assert result['language'] == 'en'
        assert 'fantastic' in result['positive_words']
        assert 'love' in result['positive_words']
    
    def test_chinese_positive_sentiment(self):
        """测试中文积极情感"""
        text = "很好！超级完美！"
        result = SentimentService.analyze_sentiment(text)
        
        assert result['score'] > 0.3
        assert result['label'] == 'positive'
        assert result['language'] == 'zh'
        assert '很好' in result['positive_words'] or '完美' in result['positive_words']
    
    def test_english_negative_sentiment(self):
        """测试英文消极情感"""
        text = "This is terrible. I hate this awful product completely."
        result = SentimentService.analyze_sentiment(text)
        
        assert result['score'] < -0.3
        assert result['label'] == 'negative'
        assert result['language'] == 'en'
        assert 'terrible' in result['negative_words']
        assert 'hate' in result['negative_words']
    
    def test_chinese_negative_sentiment(self):
        """测试中文消极情感"""
        text = "垃圾!太糟糕了!"
        result = SentimentService.analyze_sentiment(text)
        
        assert result['score'] < -0.3
        assert result['label'] == 'negative'
        assert result['language'] == 'zh'
        assert '糟糕' in result['negative_words'] or '失望' in result['negative_words']
    
    def test_mixed_language_sentiment(self):
        """测试中英混合情感"""
        text = "卓越! Perfect!"
        result = SentimentService.analyze_sentiment(text)
        
        assert result['score'] > 0.2
        assert result['label'] == 'positive'
        assert result['language'] == 'mixed'
    
    def test_neutral_sentiment(self):
        """测试中性情感"""
        text = "This is a product. It has some features."
        result = SentimentService.analyze_sentiment(text)
        
        assert -0.1 <= result['score'] <= 0.1
        assert result['label'] == 'neutral'
    
    def test_english_negation_handling(self):
        """测试英文否定词处理"""
        positive_text = "This is good."
        negative_text = "This is not good."
        
        pos_result = SentimentService.analyze_sentiment(positive_text)
        neg_result = SentimentService.analyze_sentiment(negative_text)
        
        assert pos_result['score'] > neg_result['score']
    
    def test_chinese_negation_handling(self):
        """测试中文否定词处理"""
        positive_text = "这个很好。"
        negative_text = "这个不好。"
        
        pos_result = SentimentService.analyze_sentiment(positive_text)
        neg_result = SentimentService.analyze_sentiment(negative_text)
        
        assert pos_result['score'] > neg_result['score']
    
    def test_chinese_special_patterns(self):
        """测试中文特殊语法模式"""
        # "不错" 实际是积极的
        text = "这个产品不错，质量还可以。"
        result = SentimentService.analyze_sentiment(text)
        
        assert result['score'] > 0.0
        assert result['label'] in ['positive', 'neutral']
    
    def test_intensifier_handling(self):
        """测试程度副词处理"""
        # 英文
        normal_text = "This is good."
        intense_text = "This is very good."
        
        normal_result = SentimentService.analyze_sentiment(normal_text)
        intense_result = SentimentService.analyze_sentiment(intense_text)
        
        assert intense_result['score'] > normal_result['score']
        
        # 中文
        normal_zh = "这个好。"
        intense_zh = "这个非常好。"
        
        normal_zh_result = SentimentService.analyze_sentiment(normal_zh)
        intense_zh_result = SentimentService.analyze_sentiment(intense_zh)
        
        assert intense_zh_result['score'] > normal_zh_result['score']
    
    def test_empty_text(self):
        """测试空文本"""
        result = SentimentService.analyze_sentiment("")
        assert result['score'] == 0.0
        assert result['label'] == 'neutral'
        assert result['word_count'] == 0
    
    def test_language_detection(self):
        """测试语言检测"""
        en_text = "This is a great English sentence with many words."
        zh_text = "这是一个很长的中文句子，包含了很多中文字符和词汇。"
        mixed_text = "Hello 你好 world 世界!"
        
        en_result = SentimentService.analyze_sentiment(en_text)
        zh_result = SentimentService.analyze_sentiment(zh_text)
        mixed_result = SentimentService.analyze_sentiment(mixed_text)
        
        assert en_result['language'] == 'en'
        assert zh_result['language'] == 'zh'
        assert mixed_result['language'] == 'mixed'