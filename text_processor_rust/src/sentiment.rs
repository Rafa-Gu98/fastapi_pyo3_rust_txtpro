pub mod dictionary;
pub mod analyzer;
pub mod rules;
pub mod tokenizer;  // 新增：多语言分词器

pub use analyzer::SentimentAnalyzer;

#[derive(Debug, Clone)]
pub struct SentimentResult {
    pub score: f64,           // -1.0 到 1.0 的情感分数
    pub label: String,        // "positive", "negative", "neutral"
    pub confidence: f64,      // 0.0 到 1.0 的置信度
    pub word_count: usize,    // 处理的词汇数
    pub positive_words: Vec<String>,  // 识别的积极词汇
    pub negative_words: Vec<String>,  // 识别的消极词汇
    pub language: String,     // 新增：检测到的主要语言 "en", "zh", "mixed"
}