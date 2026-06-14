# Multi-Model Prompt Invariance Study

- Models evaluated: 6
- Total prompts per model: 360

## Held-out family selection summary

| model_name | model_family | model_variant | analysis_best_answer_family | analysis_best_selectivity_family | holdout_best_answer_f1 | holdout_answer_f1_diff | holdout_target_selectivity_diff |
| --- | --- | --- | --- | --- | --- | --- | --- |
| gemma_270m_base | gemma | base | declarative | declarative | 0.1770 | 0.0183 | 0.0402 |
| gemma_270m_it | gemma | instruct | raw_question | raw_question | 0.2704 | 0.1074 | 0.0460 |
| qwen2_5_0_5b_base | qwen | base | qa | qa | 0.5033 | 0.3925 | 0.3454 |
| qwen2_5_0_5b_instruct | qwen | instruct | chat_template | chat_template | 0.5072 | 0.3517 | 0.2381 |
| smollm2_360m_base | smollm2 | base | qa | qa | 0.3235 | -0.0078 | -0.0156 |
| smollm2_360m_instruct | smollm2 | instruct | chat_template | chat_template | 0.2908 | 0.2908 | 0.2390 |

## Strongest family comparisons by answer F1 difference

| model_name | relation | family_a | family_b | mean_diff | ci_low | ci_high | pvalue |
| --- | --- | --- | --- | --- | --- | --- | --- |
| qwen2_5_0_5b_base | capital | declarative | qa | 0.6798 | 0.5220 | 0.8208 | 0.0000 |
| qwen2_5_0_5b_base | official_language | chat_template | qa | 0.6694 | 0.4249 | 0.8889 | 0.0018 |
| qwen2_5_0_5b_base | official_language | qa | raw_question | -0.6435 | -0.8410 | -0.4336 | 0.0002 |
| smollm2_360m_instruct | capital | chat_template | qa | -0.6037 | -0.7926 | -0.4147 | 0.0002 |
| smollm2_360m_instruct | capital | chat_template | raw_question | -0.6037 | -0.7926 | -0.4147 | 0.0002 |
| qwen2_5_0_5b_instruct | capital | chat_template | declarative | -0.5947 | -0.7730 | -0.4428 | 0.0002 |
| qwen2_5_0_5b_base | capital | chat_template | qa | 0.5889 | 0.4227 | 0.7299 | 0.0003 |
| qwen2_5_0_5b_base | capital | qa | raw_question | -0.5863 | -0.7917 | -0.3669 | 0.0005 |
| qwen2_5_0_5b_instruct | capital | chat_template | qa | -0.4989 | -0.6907 | -0.3230 | 0.0490 |
| smollm2_360m_instruct | headquarters | declarative | qa | -0.4665 | -0.5826 | -0.3099 | 0.0001 |
| smollm2_360m_instruct | headquarters | declarative | raw_question | -0.4665 | -0.5826 | -0.3099 | 0.0001 |
| qwen2_5_0_5b_base | official_language | declarative | qa | 0.4287 | 0.1804 | 0.6444 | 0.1435 |

## Strongest family comparisons by target selectivity

| model_name | relation | family_a | family_b | mean_diff | ci_low | ci_high | pvalue |
| --- | --- | --- | --- | --- | --- | --- | --- |
| qwen2_5_0_5b_base | capital | declarative | qa | 0.6798 | 0.5220 | 0.8208 | 0.0000 |
| smollm2_360m_instruct | capital | chat_template | qa | -0.6037 | -0.7926 | -0.4147 | 0.0002 |
| smollm2_360m_instruct | capital | chat_template | raw_question | -0.6037 | -0.7926 | -0.4147 | 0.0002 |
| qwen2_5_0_5b_instruct | capital | chat_template | declarative | -0.5947 | -0.7730 | -0.4428 | 0.0002 |
| qwen2_5_0_5b_base | capital | chat_template | qa | 0.5889 | 0.4227 | 0.7299 | 0.0003 |
| qwen2_5_0_5b_base | capital | qa | raw_question | -0.5863 | -0.7917 | -0.3669 | 0.0005 |
| qwen2_5_0_5b_instruct | capital | chat_template | qa | -0.4989 | -0.6907 | -0.3230 | 0.0490 |
| qwen2_5_0_5b_base | official_language | chat_template | qa | 0.4573 | 0.2351 | 0.6887 | 0.0215 |
| qwen2_5_0_5b_base | official_language | qa | raw_question | -0.4460 | -0.6561 | -0.2361 | 0.0039 |
| qwen2_5_0_5b_base | currency | qa | raw_question | -0.3615 | -0.5504 | -0.1934 | 0.0063 |
| qwen2_5_0_5b_instruct | capital | chat_template | raw_question | -0.3500 | -0.5372 | -0.1748 | 0.0213 |
| smollm2_360m_instruct | capital | chat_template | declarative | -0.3218 | -0.5100 | -0.1182 | 0.0490 |