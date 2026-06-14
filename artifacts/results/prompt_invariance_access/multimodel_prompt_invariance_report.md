# Multi-Model Prompt Invariance Study

- Models evaluated: 6
- Total prompts per model: 240

## Best prompt family per model

| model_name | model_family | model_variant | prompt_family | answer_f1 |
| --- | --- | --- | --- | --- |
| qwen2_5_0_5b_base | qwen | base | qa | 0.4772 |
| qwen2_5_0_5b_instruct | qwen | instruct | chat_template | 0.4047 |
| smollm2_360m_base | smollm2 | base | qa | 0.3333 |
| smollm2_360m_instruct | smollm2 | instruct | chat_template | 0.3072 |
| gemma_270m_it | gemma | instruct | raw_question | 0.2766 |
| gemma_270m_base | gemma | base | declarative | 0.1555 |

## Strongest family comparisons by answer F1 difference

| model_name | relation | family_a | family_b | mean_diff | ci_low | ci_high | pvalue |
| --- | --- | --- | --- | --- | --- | --- | --- |
| qwen2_5_0_5b_base | capital | declarative | qa | 0.6725 | 0.5055 | 0.8370 | 0.0010 |
| smollm2_360m_instruct | capital | chat_template | qa | -0.6222 | -0.8389 | -0.3831 | 0.0039 |
| smollm2_360m_instruct | capital | chat_template | raw_question | -0.6222 | -0.8389 | -0.3831 | 0.0039 |
| qwen2_5_0_5b_base | capital | chat_template | qa | 0.6056 | 0.4155 | 0.7709 | 0.0063 |
| qwen2_5_0_5b_instruct | capital | chat_template | declarative | -0.6010 | -0.8001 | -0.3781 | 0.0039 |
| qwen2_5_0_5b_base | official_language | chat_template | qa | 0.5875 | 0.3158 | 0.8542 | 0.0391 |
| qwen2_5_0_5b_base | official_language | qa | raw_question | -0.5486 | -0.7986 | -0.2986 | 0.0078 |
| qwen2_5_0_5b_base | capital | qa | raw_question | -0.5461 | -0.7708 | -0.2961 | 0.0078 |
| qwen2_5_0_5b_instruct | capital | chat_template | qa | -0.5081 | -0.6965 | -0.2700 | 0.0654 |
| smollm2_360m_instruct | headquarters | declarative | qa | -0.4428 | -0.6075 | -0.2794 | 0.0039 |
| smollm2_360m_instruct | headquarters | declarative | raw_question | -0.4428 | -0.6075 | -0.2794 | 0.0039 |
| qwen2_5_0_5b_instruct | capital | chat_template | raw_question | -0.3569 | -0.5071 | -0.1527 | 0.0215 |

## Strongest family comparisons by target selectivity

| model_name | relation | family_a | family_b | mean_diff | ci_low | ci_high | pvalue |
| --- | --- | --- | --- | --- | --- | --- | --- |
| qwen2_5_0_5b_base | capital | declarative | qa | 0.6725 | 0.5055 | 0.8370 | 0.0010 |
| smollm2_360m_instruct | capital | chat_template | qa | -0.6222 | -0.8389 | -0.3831 | 0.0039 |
| smollm2_360m_instruct | capital | chat_template | raw_question | -0.6222 | -0.8389 | -0.3831 | 0.0039 |
| qwen2_5_0_5b_base | capital | chat_template | qa | 0.6056 | 0.4155 | 0.7709 | 0.0063 |
| qwen2_5_0_5b_instruct | capital | chat_template | declarative | -0.6010 | -0.8001 | -0.3781 | 0.0039 |
| qwen2_5_0_5b_base | capital | qa | raw_question | -0.5461 | -0.7708 | -0.2961 | 0.0078 |
| qwen2_5_0_5b_instruct | capital | chat_template | qa | -0.5081 | -0.6965 | -0.2700 | 0.0654 |
| smollm2_360m_instruct | headquarters | declarative | qa | -0.4150 | -0.5770 | -0.2520 | 0.0039 |
| smollm2_360m_instruct | headquarters | declarative | raw_question | -0.4150 | -0.5770 | -0.2520 | 0.0039 |
| qwen2_5_0_5b_instruct | capital | chat_template | raw_question | -0.3569 | -0.5071 | -0.1527 | 0.0215 |
| qwen2_5_0_5b_base | official_language | chat_template | qa | 0.3527 | 0.0916 | 0.6330 | 0.2188 |
| smollm2_360m_instruct | capital | chat_template | declarative | -0.3486 | -0.5621 | -0.1231 | 0.0654 |