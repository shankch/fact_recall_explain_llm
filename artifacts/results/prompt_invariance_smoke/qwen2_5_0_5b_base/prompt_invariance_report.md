# Prompt Invariance Report: qwen2_5_0_5b_base

- Prompts analyzed: 80
- Mean answer F1: 0.3264
- Best prompt family by answer F1: qa

## Family Summary

| relation | prompt_family | target_rank | target_margin | full_exact_match | contains_expected | answer_f1 | answer_similarity |
| --- | --- | --- | --- | --- | --- | --- | --- |
| birth_place | chat_template | 103785.25 | -18.0127 | 0.0 | 0.75 | 0.5667 | 0.6209 |
| birth_place | declarative | 19.0 | -2.0938 | 0.0 | 0.5 | 0.3095 | 0.4772 |
| birth_place | qa | 54.0 | -3.5938 | 0.25 | 0.5 | 0.45 | 0.6415 |
| birth_place | raw_question | 200.5 | -6.3672 | 0.0 | 0.5 | 0.4 | 0.5552 |
| capital | chat_template | 448.25 | -7.6875 | 0.0 | 0.5 | 0.2014 | 0.344 |
| capital | declarative | 2.0 | 0.3906 | 0.0 | 0.25 | 0.1556 | 0.3199 |
| capital | qa | 1.0 | 2.3125 | 0.5 | 0.5 | 0.6667 | 0.9727 |
| capital | raw_question | 8.0 | -2.3594 | 0.25 | 0.25 | 0.3409 | 0.4672 |
| currency | chat_template | 11224.75 | -5.9219 | 0.0 | 0.5 | 0.3056 | 0.4272 |
| currency | declarative | 112.0 | -6.8125 | 0.0 | 0.5 | 0.3333 | 0.4419 |
| currency | qa | 4.0 | -1.6094 | 0.0 | 0.5 | 0.5 | 0.6196 |
| currency | raw_question | 119.0 | -4.4062 | 0.0 | 0.0 | 0.1 | 0.3198 |
| headquarters | chat_template | 51804.25 | -15.0 | 0.0 | 0.75 | 0.4293 | 0.4923 |
| headquarters | declarative | 18.0 | -1.7656 | 0.0 | 0.5 | 0.2825 | 0.428 |
| headquarters | qa | 9.75 | -1.2656 | 0.25 | 1.0 | 0.4965 | 0.5372 |
| headquarters | raw_question | 637.0 | -8.5703 | 0.0 | 0.75 | 0.4114 | 0.491 |
| official_language | chat_template | 17392.25 | -11.4805 | 0.0 | 0.0 | 0.0 | 0.1701 |
| official_language | declarative | 8.0 | -1.4375 | 0.0 | 0.75 | 0.2667 | 0.429 |
| official_language | qa | 1.25 | 0.4375 | 0.25 | 0.5 | 0.3125 | 0.6244 |
| official_language | raw_question | 38.5 | -4.3594 | 0.0 | 0.0 | 0.0 | 0.1953 |

## Top Invariant Neurons

| layer | neuron | mean_abs_activation | activation_std | family_mean_std | sharedness | family_sensitivity | invariance_score | prompt_sensitive_score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 8 | 4766 | 0.2775 | 0.0015 | 0.0009 | 189.9477 | 0.0033 | 189.3255 | 0.0003 |
| 9 | 2519 | 0.2766 | 0.0018 | 0.0007 | 154.9587 | 0.0026 | 154.5531 | 0.0002 |
| 15 | 1024 | 0.277 | 0.0021 | 0.0006 | 133.9846 | 0.002 | 133.7169 | 0.0002 |
| 9 | 1736 | 0.2761 | 0.0021 | 0.001 | 129.6937 | 0.0036 | 129.2239 | 0.0003 |
| 0 | 308 | 0.275 | 0.0022 | 0.0017 | 124.936 | 0.006 | 124.1861 | 0.0005 |
| 1 | 2084 | 0.2764 | 0.0023 | 0.0009 | 120.6364 | 0.0034 | 120.2286 | 0.0003 |
| 9 | 568 | 0.276 | 0.0027 | 0.0006 | 102.6419 | 0.0022 | 102.4207 | 0.0002 |
| 1 | 3191 | 0.2761 | 0.0027 | 0.0021 | 103.1202 | 0.0076 | 102.3383 | 0.0006 |

## Top Prompt-Sensitive Neurons

| layer | neuron | mean_abs_activation | activation_std | family_mean_std | sharedness | family_sensitivity | invariance_score | prompt_sensitive_score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 23 | 537 | 8.1811 | 2.5732 | 2.3985 | 3.1794 | 0.2932 | 2.4586 | 19.6222 |
| 23 | 1863 | 12.7797 | 1.2952 | 1.1012 | 9.867 | 0.0862 | 9.0842 | 14.0731 |
| 23 | 2345 | 9.6688 | 1.2247 | 1.095 | 7.8948 | 0.1133 | 7.0916 | 10.5875 |
| 23 | 3935 | 14.5477 | 0.9766 | 0.6837 | 14.8963 | 0.047 | 14.2277 | 9.9457 |
| 23 | 2505 | 13.8242 | 0.9929 | 0.7136 | 13.9231 | 0.0516 | 13.2396 | 9.8654 |
| 23 | 3423 | 11.0977 | 1.015 | 0.8836 | 10.934 | 0.0796 | 10.1276 | 9.8058 |
| 23 | 2337 | 4.8985 | 2.0103 | 1.9505 | 2.4368 | 0.3982 | 1.7428 | 9.5548 |
| 23 | 4144 | 13.4266 | 0.9847 | 0.7026 | 13.6354 | 0.0523 | 12.9573 | 9.434 |

## Neuron Ablation Summary

| candidate_type | prompt_family | answer_f1_drop | contains_drop |
| --- | --- | --- | --- |
| invariant | chat_template | 0.0 | 0.0 |
| invariant | declarative | 0.0 | 0.0 |
| invariant | qa | 0.0 | -0.2 |
| invariant | raw_question | 0.0 | 0.0 |
| prompt_sensitive | chat_template | -0.0109 | 0.0 |
| prompt_sensitive | declarative | -0.1067 | -0.4 |
| prompt_sensitive | qa | 0.0 | 0.0 |
| prompt_sensitive | raw_question | 0.0 | 0.0 |