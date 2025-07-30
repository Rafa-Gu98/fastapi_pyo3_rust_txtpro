use jieba_rs::Jieba;
use once_cell::sync::Lazy;
use regex::Regex;
use unicode_segmentation::UnicodeSegmentation;

// 全局初始化分词器
static JIEBA: Lazy<Jieba> = Lazy::new(|| Jieba::new());

#[derive(Debug, Clone)]
pub enum Language {
    English,
    Chinese,
    Mixed,
}

#[derive(Debug, Clone)]
pub struct TokenizedText {
    pub words: Vec<String>,
    pub language: Language,
}

pub struct MultiLanguageTokenizer {
    chinese_regex: Regex,
    english_regex: Regex,
}

impl MultiLanguageTokenizer {
    pub fn new() -> Self {
        Self {
            chinese_regex: Regex::new(r"[\u4e00-\u9fff]+").unwrap(),
            english_regex: Regex::new(r"[a-zA-Z]+").unwrap(),
        }
    }
    
    pub fn tokenize(&self, text: &str) -> TokenizedText {
        let language = self.detect_language(text);
        let words = match language {
            Language::Chinese => self.tokenize_chinese(text),
            Language::English => self.tokenize_english(text),
            Language::Mixed => self.tokenize_mixed(text),
        };
        
        TokenizedText { words, language }
    }
    
    fn detect_language(&self, text: &str) -> Language {
        let chinese_chars = self.chinese_regex.find_iter(text).count();
        let english_words = self.english_regex.find_iter(text).count();
        
        if chinese_chars > english_words * 2 {
            Language::Chinese
        } else if english_words > chinese_chars * 2 {
            Language::English
        } else {
            Language::Mixed
        }
    }
    
    fn tokenize_chinese(&self, text: &str) -> Vec<String> {
        JIEBA.cut(text, false)
            .into_iter()
            .map(|s| s.trim().to_lowercase())
            .filter(|s| !s.is_empty() && s.len() > 1)
            .collect()
    }
    
    fn tokenize_english(&self, text: &str) -> Vec<String> {
        text.unicode_words()
            .map(|word| word.to_lowercase())
            .filter(|word| word.len() > 1)
            .collect()
    }
    
    fn tokenize_mixed(&self, text: &str) -> Vec<String> {
        let mut words = Vec::new();
        
        // 分别处理中英文片段
        let parts: Vec<&str> = text.split_whitespace().collect();
        for part in parts {
            if self.chinese_regex.is_match(part) {
                words.extend(self.tokenize_chinese(part));
            } else {
                words.extend(self.tokenize_english(part));
            }
        }
        
        words
    }
}