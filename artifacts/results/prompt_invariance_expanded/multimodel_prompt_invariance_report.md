# Multi-Model Prompt Invariance Study

- Models evaluated: 6
- Total prompts per model: 160

## Best prompt family per model

| model_name | model_family | model_variant | prompt_family | answer_f1 |
| --- | --- | --- | --- | --- |
| qwen2_5_0_5b_base | qwen | base | qa | 0.4753 |
| qwen2_5_0_5b_instruct | qwen | instruct | chat_template | 0.3860 |
| smollm2_360m_base | smollm2 | base | qa | 0.3494 |
| smollm2_360m_instruct | smollm2 | instruct | chat_template | 0.3077 |
| gemma_270m_it | gemma | instruct | raw_question | 0.2881 |
| gemma_270m_base | gemma | base | declarative | 0.1334 |

## Strongest family comparisons by answer F1 difference

| model_name | relation | family_a | family_b | mean_diff | ci_low | ci_high | pvalue |
| --- | --- | --- | --- | --- | --- | --- | --- |
| smollm2_360m_instruct | capital | chat_template | qa | -0.6333 | -0.8750 | -0.3500 | 0.0312 |
| smollm2_360m_instruct | capital | chat_template | raw_question | -0.6333 | -0.8750 | -0.3500 | 0.0312 |
| qwen2_5_0_5b_base | capital | declarative | qa | 0.6198 | 0.3875 | 0.8243 | 0.0156 |
| qwen2_5_0_5b_base | capital | chat_template | qa | 0.5833 | 0.2932 | 0.7951 | 0.0703 |
| smollm2_360m_instruct | headquarters | declarative | qa | -0.5271 | -0.7265 | -0.3080 | 0.0312 |
| smollm2_360m_instruct | headquarters | declarative | raw_question | -0.5271 | -0.7265 | -0.3080 | 0.0312 |
| qwen2_5_0_5b_instruct | capital | chat_template | declarative | -0.5066 | -0.8026 | -0.1771 | 0.0625 |
| qwen2_5_0_5b_base | official_language | chat_template | qa | 0.5062 | 0.1702 | 0.8694 | 0.2188 |
| qwen2_5_0_5b_base | official_language | qa | raw_question | -0.5035 | -0.8194 | -0.2188 | 0.0625 |
| qwen2_5_0_5b_base | capital | qa | raw_question | -0.4754 | -0.7500 | -0.1629 | 0.0625 |
| qwen2_5_0_5b_instruct | headquarters | chat_template | declarative | -0.3944 | -0.7885 | -0.1149 | 0.2188 |
| qwen2_5_0_5b_instruct | capital | chat_template | qa | -0.3847 | -0.6908 | -0.0518 | 0.4531 |