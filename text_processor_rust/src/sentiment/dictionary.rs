use std::collections::HashMap;
use once_cell::sync::Lazy;

// 英文情感词典
static EN_POSITIVE_WORDS: Lazy<HashMap<&'static str, f64>> = Lazy::new(|| {
    let mut map = HashMap::new();
    // 基础积极词汇
    map.insert("good", 0.5);
    map.insert("great", 0.8);
    map.insert("excellent", 1.0);
    map.insert("amazing", 0.9);
    map.insert("wonderful", 0.8);
    map.insert("fantastic", 0.9);
    map.insert("love", 0.7);
    map.insert("like", 0.3);
    map.insert("happy", 0.6);
    map.insert("satisfied", 0.5);
    map.insert("awesome", 0.8);
    map.insert("perfect", 0.9);
    map.insert("outstanding", 0.9);
    map.insert("brilliant", 0.8);
    map.insert("superb", 0.8);
    map
});

static EN_NEGATIVE_WORDS: Lazy<HashMap<&'static str, f64>> = Lazy::new(|| {
    let mut map = HashMap::new();
    map.insert("bad", -0.5);
    map.insert("terrible", -1.0);
    map.insert("awful", -0.9);
    map.insert("hate", -0.8);
    map.insert("dislike", -0.4);
    map.insert("sad", -0.6);
    map.insert("angry", -0.7);
    map.insert("disappointed", -0.6);
    map.insert("horrible", -0.9);
    map.insert("disgusting", -0.8);
    map.insert("annoying", -0.5);
    map.insert("boring", -0.4);
    map
});

// 中文情感词典
static ZH_POSITIVE_WORDS: Lazy<HashMap<&'static str, f64>> = Lazy::new(|| {
    let mut map = HashMap::new();
    // 中文积极词汇
    map.insert("好", 0.5);
    map.insert("很好", 0.7);
    map.insert("棒", 0.6);
    map.insert("不错", 0.5);
    map.insert("喜欢", 0.6);
    map.insert("爱", 0.8);
    map.insert("满意", 0.6);
    map.insert("开心", 0.7);
    map.insert("高兴", 0.7);
    map.insert("优秀", 0.8);
    map.insert("完美", 0.9);
    map.insert("赞", 0.6);
    map.insert("给力", 0.7);
    map.insert("超棒", 0.8);
    map.insert("惊喜", 0.7);
    map.insert("优质", 0.7);
    map.insert("精彩", 0.8);
    map.insert("杰出", 0.8);
    map.insert("卓越", 0.9);
    map.insert("出色", 0.8);
    map
});

static ZH_NEGATIVE_WORDS: Lazy<HashMap<&'static str, f64>> = Lazy::new(|| {
    let mut map = HashMap::new();
    map.insert("坏", -0.5);
    map.insert("差", -0.5);
    map.insert("糟糕", -0.8);
    map.insert("讨厌", -0.7);
    map.insert("恨", -0.8);
    map.insert("失望", -0.6);
    map.insert("难过", -0.6);
    map.insert("生气", -0.7);
    map.insert("愤怒", -0.8);
    map.insert("垃圾", -0.9);
    map.insert("烂", -0.8);
    map.insert("无聊", -0.4);
    map.insert("恶心", -0.8);
    map.insert("可怕", -0.7);
    map.insert("糟", -0.6);
    map.insert("臭", -0.6);
    map.insert("破", -0.5);
    map.insert("烦", -0.5);
    map.insert("恼火", -0.6);
    map.insert("郁闷", -0.5);
    map
});

// 程度副词
static EN_INTENSIFIERS: Lazy<HashMap<&'static str, f64>> = Lazy::new(|| {
    let mut map = HashMap::new();
    map.insert("very", 1.5);
    map.insert("extremely", 2.0);
    map.insert("really", 1.3);
    map.insert("quite", 1.2);
    map.insert("somewhat", 0.8);
    map.insert("slightly", 0.7);
    map.insert("absolutely", 1.8);
    map.insert("totally", 1.6);
    map.insert("incredibly", 1.7);
    map.insert("super", 1.4);
    map
});

static ZH_INTENSIFIERS: Lazy<HashMap<&'static str, f64>> = Lazy::new(|| {
    let mut map = HashMap::new();
    map.insert("很", 1.3);
    map.insert("非常", 1.6);
    map.insert("极其", 1.8);
    map.insert("超级", 1.5);
    map.insert("特别", 1.4);
    map.insert("相当", 1.2);
    map.insert("比较", 0.8);
    map.insert("有点", 0.7);
    map.insert("稍微", 0.6);
    map.insert("十分", 1.5);
    map.insert("格外", 1.4);
    map.insert("异常", 1.6);
    map.insert("超", 1.4);
    map.insert("巨", 1.5);
    map.insert("贼", 1.3);
    map
});

// 否定词
static EN_NEGATORS: Lazy<Vec<&'static str>> = Lazy::new(|| {
    vec![
        "not", "no", "never", "none", "nobody", "nothing", 
        "neither", "nowhere", "isn't", "wasn't", "shouldn't",
        "wouldn't", "couldn't", "won't", "can't", "don't",
        "doesn't", "didn't", "haven't", "hasn't", "hadn't"
    ]
});

static ZH_NEGATORS: Lazy<Vec<&'static str>> = Lazy::new(|| {
    vec![
        "不", "没", "没有", "不是", "非", "无", "未", "勿",
        "别", "莫", "毋", "不用", "不要", "不能", "不会",
        "不可", "不得", "不必", "不该", "不应", "不许"
    ]
});

pub struct SentimentDictionary;

impl SentimentDictionary {
    pub fn new() -> Self {
        Self
    }
    
    pub fn get_word_sentiment(&self, word: &str) -> Option<f64> {
        // 先检查中文词典
        if let Some(score) = ZH_POSITIVE_WORDS.get(word).or_else(|| ZH_NEGATIVE_WORDS.get(word)) {
            return Some(*score);
        }
        
        // 再检查英文词典
        let word_lower = word.to_lowercase();
        EN_POSITIVE_WORDS.get(word_lower.as_str()).copied()
            .or_else(|| EN_NEGATIVE_WORDS.get(word_lower.as_str()).copied())
    }
    
    pub fn get_intensifier(&self, word: &str) -> Option<f64> {
        // 检查中文程度副词
        if let Some(multiplier) = ZH_INTENSIFIERS.get(word) {
            return Some(*multiplier);
        }
        
        // 检查英文程度副词
        EN_INTENSIFIERS.get(word.to_lowercase().as_str()).copied()
    }
    
    pub fn is_negator(&self, word: &str) -> bool {
        // 检查中文否定词
        if ZH_NEGATORS.contains(&word) {
            return true;
        }
        
        // 检查英文否定词
        EN_NEGATORS.contains(&word.to_lowercase().as_str())
    }
}