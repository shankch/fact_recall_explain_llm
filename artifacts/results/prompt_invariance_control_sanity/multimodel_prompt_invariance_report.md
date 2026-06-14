# Multi-Model Prompt Invariance Study

- Models evaluated: 1
- Total prompts per model: 16

## Best prompt family per model

| model_name | model_family | model_variant | prompt_family | answer_f1 |
| --- | --- | --- | --- | --- |
| gemma_270m_base | gemma | base | chat_template | 0.2500 |

## Strongest family comparisons by answer F1 difference

| model_name | relation | family_a | family_b | mean_diff | ci_low | ci_high | pvalue |
| --- | --- | --- | --- | --- | --- | --- | --- |
| gemma_270m_base | capital | chat_template | qa | -0.5000 | -1.0000 | 0.0000 | 1.0000 |
| gemma_270m_base | capital | chat_template | raw_question | -0.5000 | -1.0000 | 0.0000 | 1.0000 |
| gemma_270m_base | capital | declarative | qa | -0.2857 | -0.2857 | -0.2857 | 0.5000 |
| gemma_270m_base | capital | declarative | raw_question | -0.2857 | -0.2857 | -0.2857 | 0.5000 |
| gemma_270m_base | capital | chat_template | declarative | -0.2143 | -0.7143 | 0.2857 | 1.0000 |
| gemma_270m_base | official_language | chat_template | declarative | 0.1250 | 0.0000 | 0.2500 | 1.0000 |
| gemma_270m_base | official_language | chat_template | qa | 0.1250 | 0.0000 | 0.2500 | 1.0000 |
| gemma_270m_base | official_language | qa | raw_question | -0.1250 | -0.2500 | 0.0000 | 1.0000 |
| gemma_270m_base | official_language | declarative | raw_question | -0.1250 | -0.2500 | 0.0000 | 1.0000 |
| gemma_270m_base | capital | qa | raw_question | 0.0000 | 0.0000 | 0.0000 | 1.0000 |
| gemma_270m_base | official_language | declarative | qa | 0.0000 | -0.2500 | 0.2500 | 1.0000 |
| gemma_270m_base | official_language | chat_template | raw_question | 0.0000 | 0.0000 | 0.0000 | 1.0000 |

## Strongest family comparisons by target selectivity

| model_name | relation | family_a | family_b | mean_diff | ci_low | ci_high | pvalue |
| --- | --- | --- | --- | --- | --- | --- | --- |
| gemma_270m_base | capital | chat_template | qa | -0.5000 | -1.0000 | 0.0000 | 1.0000 |
| gemma_270m_base | capital | chat_template | raw_question | -0.5000 | -1.0000 | 0.0000 | 1.0000 |
| gemma_270m_base | capital | declarative | qa | -0.2857 | -0.2857 | -0.2857 | 0.5000 |
| gemma_270m_base | capital | declarative | raw_question | -0.2857 | -0.2857 | -0.2857 | 0.5000 |
| gemma_270m_base | capital | chat_template | declarative | -0.2143 | -0.7143 | 0.2857 | 1.0000 |
| gemma_270m_base | official_language | chat_template | declarative | 0.1250 | 0.0000 | 0.2500 | 1.0000 |
| gemma_270m_base | official_language | chat_template | qa | 0.1250 | 0.0000 | 0.2500 | 1.0000 |
| gemma_270m_base | official_language | qa | raw_question | -0.1250 | -0.2500 | 0.0000 | 1.0000 |
| gemma_270m_base | official_language | declarative | raw_question | -0.1250 | -0.2500 | 0.0000 | 1.0000 |
| gemma_270m_base | capital | qa | raw_question | 0.0000 | 0.0000 | 0.0000 | 1.0000 |
| gemma_270m_base | official_language | declarative | qa | 0.0000 | -0.2500 | 0.2500 | 1.0000 |
| gemma_270m_base | official_language | chat_template | raw_question | 0.0000 | 0.0000 | 0.0000 | 1.0000 |