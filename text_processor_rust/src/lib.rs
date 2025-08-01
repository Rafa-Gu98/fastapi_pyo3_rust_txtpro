use pyo3::prelude::*;
use regex::Regex;
use rayon::prelude::*;
use std::collections::HashMap;
use pyo3::types::PyDict;
mod sentiment;
use sentiment::SentimentAnalyzer;

/// Count word frequencies in text (computationally intensive)
#[pyfunction]
fn count_words(text: String) -> PyResult<HashMap<String, usize>> {
    let re = Regex::new(r"[\w']+").unwrap();
    let mut word_count: HashMap<String, usize> = HashMap::new();
    for mat in re.find_iter(&text) {
        let word = mat.as_str().to_lowercase();
        *word_count.entry(word).or_insert(0) += 1;
    }
    Ok(word_count)
}

/// Extract email addresses from text
#[pyfunction]
fn extract_emails(text: &str) -> PyResult<Vec<String>> {
    let email_regex = Regex::new(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b").unwrap();
    let emails: Vec<String> = email_regex
        .find_iter(text)
        .map(|mat| mat.as_str().to_string())
        .collect();
    
    Ok(emails)
}

/// Clean and normalize text (parallel processing)
#[pyfunction]
fn clean_text(text: &str) -> PyResult<String> {
    let lines: Vec<&str> = text.lines().collect();
    let cleaned_lines: Vec<String> = lines
        .par_iter()
        .map(|line| {
            line.trim()
                .chars()
                .filter(|c| c.is_alphanumeric() || c.is_whitespace() || ".,!?".contains(*c))
                .collect()
        })
        .collect();
    
    Ok(cleaned_lines.join("\n"))
}

#[pyfunction]
fn analyze_sentiment(text: &str) -> PyResult<PyObject> {
    let analyzer = SentimentAnalyzer::new();
    let result = analyzer.analyze(text);
    
    Python::with_gil(|py| {
        let dict = PyDict::new(py);
        dict.set_item("score", result.score)?;
        dict.set_item("label", result.label)?;
        dict.set_item("confidence", result.confidence)?;
        dict.set_item("word_count", result.word_count)?;
        dict.set_item("positive_words", result.positive_words)?;
        dict.set_item("negative_words", result.negative_words)?;
        dict.set_item("language", result.language)?;
        Ok(dict.into())
    })
}

/// A Python module implemented in Rust
#[pymodule]
fn text_processor_rust(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(count_words, m)?)?;
    m.add_function(wrap_pyfunction!(extract_emails, m)?)?;
    m.add_function(wrap_pyfunction!(clean_text, m)?)?;
    // 新增情感分析函数
    m.add_function(wrap_pyfunction!(analyze_sentiment, m)?)?;

    Ok(())
}
