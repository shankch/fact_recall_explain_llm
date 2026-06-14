# Multi-Model Prompt Invariance Study

- Models evaluated: 5
- Total prompts per model: 80

## Best prompt family per model

| model_name | model_family | model_variant | prompt_family | answer_f1 |
| --- | --- | --- | --- | --- |
| qwen2_5_0_5b_base | qwen | base | qa | 0.4851 |
| qwen2_5_0_5b_instruct | qwen | instruct | chat_template | 0.3867 |
| smollm2_360m_instruct | smollm2 | instruct | chat_template | 0.3437 |
| gemma_270m_it | gemma | instruct | raw_question | 0.2661 |
| gemma_270m_base | gemma | base | declarative | 0.1485 |

## Strongest family comparisons by answer F1 difference

| model_name | relation | family_a | family_b | mean_diff | ci_low | ci_high | pvalue |
| --- | --- | --- | --- | --- | --- | --- | --- |
| smollm2_360m_instruct | headquarters | declarative | qa | -0.6732 | -0.7750 | -0.5714 | 0.1250 |
| smollm2_360m_instruct | headquarters | declarative | raw_question | -0.6732 | -0.7750 | -0.5714 | 0.1250 |
| smollm2_360m_instruct | birth_place | chat_template | raw_question | -0.6667 | -1.0000 | -0.2063 | 0.2500 |
| smollm2_360m_instruct | birth_place | chat_template | qa | -0.6667 | -1.0000 | -0.2063 | 0.2500 |
| smollm2_360m_instruct | birth_place | chat_template | declarative | -0.6167 | -0.9500 | -0.1825 | 0.2500 |
| qwen2_5_0_5b_base | capital | declarative | qa | 0.5111 | 0.1333 | 0.8167 | 0.2500 |
| qwen2_5_0_5b_base | capital | chat_template | qa | 0.4653 | 0.0069 | 0.8069 | 0.6250 |
| qwen2_5_0_5b_instruct | headquarters | chat_template | declarative | -0.4556 | -1.0000 | 0.1706 | 0.6250 |
| smollm2_360m_instruct | capital | chat_template | qa | -0.4167 | -0.8333 | 0.0000 | 0.5000 |
| smollm2_360m_instruct | capital | chat_template | raw_question | -0.4167 | -0.8333 | 0.0000 | 0.5000 |
| qwen2_5_0_5b_base | currency | qa | raw_question | -0.4000 | -0.8000 | 0.0000 | 0.5000 |
| qwen2_5_0_5b_instruct | currency | chat_template | declarative | -0.3879 | -0.8247 | -0.0361 | 0.6250 |