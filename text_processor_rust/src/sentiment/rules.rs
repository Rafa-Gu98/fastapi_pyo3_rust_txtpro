use crate::sentiment::{dictionary::SentimentDictionary, tokenizer::Language};

pub struct RuleProcessor {
    dictionary: SentimentDictionary,
}

impl RuleProcessor {
    pub fn new() -> Self {
        Self {
            dictionary: SentimentDictionary::new(),
        }
    }
    
    pub fn process_context(&self, words: &[String], index: usize, language: &Language) -> f64 {
        let current_word = &words[index];
        let mut sentiment = self.dictionary.get_word_sentiment(current_word).unwrap_or(0.0);
        
        // 根据语言选择不同的处理窗口大小
        let negation_window = match language {
            Language::Chinese => 2,  // 中文否定词通常更靠近被修饰词
            Language::English => 3,  // 英文可能有更复杂的语法结构
            Language::Mixed => 3,
        };
        
        let start = if index >= negation_window { index - negation_window } else { 0 };
        
        let mut negation_count = 0;
        let mut intensifier_multiplier = 1.0;
        
        // 向前扫描否定词和程度副词
        for i in start..index {
            let word = &words[i];
            
            // 检查否定词
            if self.dictionary.is_negator(word) {
                negation_count += 1;
            }
            
            // 检查程度副词
            if let Some(multiplier) = self.dictionary.get_intensifier(word) {
                intensifier_multiplier *= multiplier;
            }
        }
        
        // 中文特殊处理：检查相邻词汇的组合
        if matches!(language, Language::Chinese | Language::Mixed) {
            sentiment = self.handle_chinese_patterns(words, index, sentiment);
        }
        
        // 应用程度副词
        sentiment *= intensifier_multiplier;
        
        // 应用否定规则
        if negation_count % 2 == 1 {
            // 中文否定通常更直接
            let negation_factor = match language {
                Language::Chinese => -0.9,
                _ => -0.8,
            };
            sentiment *= negation_factor;
        }
        
        sentiment
    }
    
    fn handle_chinese_patterns(&self, words: &[String], index: usize, mut sentiment: f64) -> f64 {
        // 处理中文特殊语法模式
        if index > 0 {
            let prev_word = &words[index - 1];
            let current_word = &words[index];
            
            // 处理常见的中文情感模式
            match (prev_word.as_str(), current_word.as_str()) {
                ("不", "好") => sentiment = -0.5,      // "不好"
                ("不", "错") => sentiment = 0.4,       // "不错" (实际是积极的)
                ("没", "用") => sentiment = -0.6,      // "没用"
                ("很", word) if self.dictionary.get_word_sentiment(word).is_some() => {
                    // "很"字修饰情感词
                    sentiment *= 1.3;
                }
                _ => {}
            }
        }
        
        sentiment
    }
}