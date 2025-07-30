use crate::sentiment::{
    SentimentResult, 
    rules::RuleProcessor, 
    tokenizer::{MultiLanguageTokenizer, Language}
};
use rayon::prelude::*;

pub struct SentimentAnalyzer {
    rule_processor: RuleProcessor,
    tokenizer: MultiLanguageTokenizer,  // 修复：添加缺少的tokenizer字段
}

impl SentimentAnalyzer {
    pub fn new() -> Self {
        Self {
            rule_processor: RuleProcessor::new(),
            tokenizer: MultiLanguageTokenizer::new(),  // 修复：初始化tokenizer
        }
    }
    
    pub fn analyze(&self, text: &str) -> SentimentResult {
        let _start_time = std::time::Instant::now();
        
        // 多语言分词（使用tokenizer）
        let tokenized = self.tokenizer.tokenize(text);
        let words = tokenized.words;
        let language = tokenized.language;
        let word_count = words.len();
        
        if word_count == 0 {
            return SentimentResult {
                score: 0.0,
                label: "neutral".to_string(),
                confidence: 0.0,
                word_count: 0,
                positive_words: vec![],
                negative_words: vec![],
                language: self.language_to_string(&language),
            };
        }
        
        // 并行处理每个词的情感分数
        let word_sentiments: Vec<(String, f64)> = words
            .par_iter()
            .enumerate()
            .map(|(i, word)| {
                // 修复：添加缺少的language参数
                let sentiment = self.rule_processor.process_context(&words, i, &language);
                (word.clone(), sentiment)
            })
            .collect();
        
        // 计算总体情感分数
        let total_score: f64 = word_sentiments.iter().map(|(_, score)| score).sum();
        
        // 根据语言调整归一化策略
        let normalized_score = match language {
            Language::Chinese => {
                // 中文通常情感表达更含蓄，调整权重
                (total_score / word_count as f64 * 1.2).max(-1.0).min(1.0)
            }
            Language::English => {
                // 英文标准归一化
                (total_score / word_count as f64).max(-1.0).min(1.0)
            }
            Language::Mixed => {
                // 混合语言取平均
                (total_score / word_count as f64 * 1.1).max(-1.0).min(1.0)
            }
        };
        
        // 分类和置信度（需要language参数）
        let (label, confidence) = self.classify_sentiment(normalized_score, &language);
        
        // 提取积极和消极词汇
        let positive_words: Vec<String> = word_sentiments
            .iter()
            .filter(|(_, score)| *score > 0.1)
            .map(|(word, _)| word.clone())
            .collect();
            
        let negative_words: Vec<String> = word_sentiments
            .iter()
            .filter(|(_, score)| *score < -0.1)
            .map(|(word, _)| word.clone())
            .collect();
        
        SentimentResult {
            score: normalized_score,
            label,
            confidence,
            word_count,
            positive_words,
            negative_words,
            language: self.language_to_string(&language),
        }
    }
    
    fn classify_sentiment(&self, score: f64, language: &Language) -> (String, f64) {
        let abs_score = score.abs();
        
        // 根据语言调整分类阈值
        let (pos_threshold, neg_threshold) = match language {
            Language::Chinese => (0.08, -0.08),  // 中文阈值稍微低一些
            Language::English => (0.1, -0.1),    // 英文标准阈值
            Language::Mixed => (0.09, -0.09),    // 混合语言中间值
        };
        
        let confidence = abs_score;
        
        let label = if score > pos_threshold {
            "positive"
        } else if score < neg_threshold {
            "negative"
        } else {
            "neutral"
        }.to_string();
        
        (label, confidence)
    }
    
    fn language_to_string(&self, language: &Language) -> String {
        match language {
            Language::English => "en".to_string(),
            Language::Chinese => "zh".to_string(),
            Language::Mixed => "mixed".to_string(),
        }
    }
}