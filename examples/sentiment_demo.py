"""
多语言情感分析功能演示
"""

import sys
import json
from pathlib import Path

# 添加项目路径
sys.path.append(str(Path(__file__).parent.parent))

from app.services import SentimentService

def demo_multilingual_sentiment():
    """多语言情感分析演示"""
    print("=== 多语言情感分析演示 ===")
    
    test_texts = [
        # 英文测试
        ("en", "I absolutely love this amazing product! It's fantastic!"),
        ("en", "This is the worst thing I've ever bought. Terrible quality."),
        ("en", "The weather is okay today, nothing special."),
        ("en", "Not bad, but could be much better."),
        
        # 中文测试
        ("zh", "我非常喜欢这个产品！质量很棒，服务也很好！"),
        ("zh", "这个东西太糟糕了，我很失望，质量很差。"),
        ("zh", "还可以吧，没什么特别的。"),
        ("zh", "不错，但还有改进的空间。"),
        
        # 混合语言测试
        ("mixed", "This product 很好，quality is excellent 质量很棒！"),
        ("mixed", "Very disappointed 很失望，not worth the money 不值这个价。"),
    ]
    
    for expected_lang, text in test_texts:
        result = SentimentService.analyze_sentiment(text)
        print(f"\n文本: {text}")
        print(f"检测语言: {result['language']} (预期: {expected_lang})")
        print(f"情感分数: {result['score']:.3f}")
        print(f"分类: {result['label']}")
        print(f"置信度: {result['confidence']:.3f}")
        print(f"积极词汇: {result['positive_words']}")
        print(f"消极词汇: {result['negative_words']}")
        print(f"处理时间: {result['processing_time_ms']}ms")

def demo_chinese_special_cases():
    """中文特殊情况演示"""
    print("\n=== 中文特殊语法演示 ===")
    
    special_cases = [
        "这个产品不错，质量还行。",  # "不错"是积极的
        "这个不好，我不喜欢。",     # 否定词处理
        "很好很好，非常满意！",     # 程度副词叠加
        "还可以，没什么特别。",     # 中性表达
        "一点都不好，太差了。",     # 强否定
    ]
    
    for text in special_cases:
        result = SentimentService.analyze_sentiment(text)
        print(f"\n文本: {text}")
        print(f"情感分数: {result['score']:.3f} | 分类: {result['label']}")
        print(f"积极词: {result['positive_words']}")
        print(f"消极词: {result['negative_words']}")

def demo_performance_comparison():
    """性能对比演示"""
    print("\n=== 性能对比演示 ===")
    
    # 英文大文本
    en_large = "This is an incredible product with outstanding quality and excellent customer service. " * 50
    
    # 中文大文本  
    zh_large = "这是一个非常棒的产品，质量很好，服务也很棒，我很满意。" * 50
    
    # 混合大文本
    mixed_large = "This product 很好，quality is excellent 质量很棒，service 服务 is great！" * 50
    
    test_cases = [
        ("英文", en_large),
        ("中文", zh_large),
        ("混合", mixed_large)
    ]
    
    for lang_name, text in test_cases:
        result = SentimentService.analyze_sentiment(text)
        print(f"\n{lang_name}文本:")
        print(f"  词汇数: {result['word_count']}")
        print(f"  处理时间: {result['processing_time_ms']}ms")
        print(f"  检测语言: {result['language']}")
        print(f"  情感分数: {result['score']:.3f}")

def demo_batch_processing():
    """批量处理演示"""
    print("\n=== 批量处理演示 ===")
    
    batch_texts = [
        "Great product, highly recommended!",
        "这个产品很棒，强烈推荐！",
        "Terrible quality, waste of money.",
        "质量太差，浪费钱。",
        "It's okay, nothing special.",
        "还行吧，没什么特别的。"
    ]
    
    import time
    start_time = time.time()
    
    results = SentimentService.batch_analyze_sentiment(batch_texts)
    
    end_time = time.time()
    total_time = (end_time - start_time) * 1000
    
    print(f"批量处理 {len(batch_texts)} 条文本，总耗时: {total_time:.1f}ms")
    print(f"平均每条: {total_time/len(batch_texts):.1f}ms")
    
    for i, (text, result) in enumerate(zip(batch_texts, results)):
        print(f"\n文本{i+1}: {text}")
        print(f"  语言: {result['language']} | 情感: {result['label']} ({result['score']:.2f})")

if __name__ == "__main__":
    demo_multilingual_sentiment()
    demo_chinese_special_cases()
    demo_performance_comparison()
    demo_batch_processing()