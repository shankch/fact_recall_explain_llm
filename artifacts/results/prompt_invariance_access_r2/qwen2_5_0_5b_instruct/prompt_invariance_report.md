# Prompt Invariance Report: qwen2_5_0_5b_instruct

- Prompts analyzed: 360
- Mean answer F1: 0.2544
- Analysis-selected best family: chat_template
- Analysis-selected best selectivity family: chat_template

## Holdout Family Summary

| relation | prompt_family | target_rank | target_margin | full_exact_match | contains_expected | answer_f1 | answer_similarity |
| --- | --- | --- | --- | --- | --- | --- | --- |
| birth_place | chat_template | 2651.5 | -11.0781 | 0.0 | 0.0 | 0.0 | 0.2908 |
| birth_place | declarative | 159.5 | -4.3125 | 0.0 | 0.0 | 0.0556 | 0.2665 |
| birth_place | qa | 864.5 | -5.5273 | 0.0 | 0.0 | 0.05 | 0.2745 |
| birth_place | raw_question | 3325.5 | -11.0664 | 0.0 | 0.0 | 0.0 | 0.2352 |
| capital | chat_template | 39.0 | -5.2031 | 0.75 | 0.75 | 0.75 | 0.9079 |
| capital | declarative | 58.75 | -3.1172 | 0.0 | 0.25 | 0.0714 | 0.2185 |
| capital | qa | 2.0 | 0.8125 | 0.0 | 0.75 | 0.1681 | 0.2928 |
| capital | raw_question | 36.5 | -5.8281 | 0.0 | 0.75 | 0.3083 | 0.4583 |
| currency | chat_template | 8.0 | -3.7344 | 0.0 | 0.5 | 0.4111 | 0.506 |
| currency | declarative | 16.0 | -6.3594 | 0.0 | 0.5 | 0.2364 | 0.2658 |
| currency | qa | 2.0 | -0.6719 | 0.0 | 0.25 | 0.3667 | 0.4706 |
| currency | raw_question | 96.75 | -1.2656 | 0.0 | 0.25 | 0.3 | 0.3865 |
| headquarters | chat_template | 1896.0 | -10.3477 | 0.25 | 0.25 | 0.375 | 0.6231 |
| headquarters | declarative | 45.5 | -4.2188 | 0.0 | 0.25 | 0.0714 | 0.2335 |
| headquarters | qa | 46.25 | -3.2266 | 0.0 | 0.25 | 0.15 | 0.2382 |
| headquarters | raw_question | 447.0 | -5.8516 | 0.0 | 0.25 | 0.1125 | 0.2584 |
| official_language | chat_template | 19.25 | -5.4531 | 1.0 | 1.0 | 1.0 | 1.0 |
| official_language | declarative | 4.0 | -0.6406 | 0.0 | 1.0 | 0.3429 | 0.4643 |
| official_language | qa | 1.0 | 2.2031 | 0.0 | 1.0 | 0.2181 | 0.2422 |
| official_language | raw_question | 5.5 | -0.9531 | 0.0 | 0.5 | 0.1 | 0.2274 |

## Control Selectivity Summary

| prompt_family | answer_f1 | target_selectivity | same_subject_control_f1 | same_relation_control_f1 | lexical_distractor_f1 | max_control_f1 |
| --- | --- | --- | --- | --- | --- | --- |
| chat_template | 0.5072 | 0.3511 | 0.0 | 0.025 | 0.1311 | 0.1561 |
| declarative | 0.1555 | 0.1131 | 0.0 | 0.0 | 0.0425 | 0.0425 |
| qa | 0.1906 | 0.1428 | 0.0 | 0.0 | 0.0478 | 0.0478 |
| raw_question | 0.1642 | 0.0851 | 0.0 | 0.0091 | 0.07 | 0.0791 |

## Top Invariant Neurons

| layer | neuron | mean_abs_activation | activation_std | family_mean_std | sharedness | family_sensitivity | invariance_score | prompt_sensitive_score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 8 | 4766 | 0.2778 | 0.0013 | 0.0003 | 205.6498 | 0.0011 | 205.4236 | 0.0001 |
| 12 | 4708 | 0.2764 | 0.0018 | 0.0004 | 150.9261 | 0.0015 | 150.7006 | 0.0001 |
| 9 | 2112 | 0.2769 | 0.0019 | 0.0007 | 147.382 | 0.0026 | 146.9974 | 0.0002 |
| 0 | 308 | 0.2752 | 0.0021 | 0.0016 | 129.3326 | 0.0057 | 128.6017 | 0.0004 |
| 15 | 443 | 0.2762 | 0.0024 | 0.0003 | 115.193 | 0.001 | 115.0823 | 0.0001 |
| 15 | 1024 | 0.2763 | 0.0026 | 0.0009 | 108.0895 | 0.0034 | 107.7276 | 0.0003 |
| 7 | 3747 | 0.2765 | 0.0026 | 0.0013 | 105.947 | 0.0047 | 105.4566 | 0.0004 |
| 13 | 562 | 0.2764 | 0.0028 | 0.0013 | 98.5055 | 0.0047 | 98.0467 | 0.0004 |

## Top Prompt-Sensitive Neurons

| layer | neuron | mean_abs_activation | activation_std | family_mean_std | sharedness | family_sensitivity | invariance_score | prompt_sensitive_score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 23 | 537 | 6.9082 | 3.0477 | 2.8505 | 2.2667 | 0.4126 | 1.6046 | 19.692 |
| 23 | 1396 | 13.0469 | 1.4104 | 1.2123 | 9.2504 | 0.0929 | 8.4639 | 15.8167 |
| 23 | 1121 | 13.2549 | 1.3868 | 1.1195 | 9.5576 | 0.0845 | 8.8133 | 14.8385 |
| 23 | 3935 | 13.4469 | 1.3253 | 1.0616 | 10.1461 | 0.0789 | 9.4037 | 14.2749 |
| 23 | 1863 | 11.8857 | 1.4202 | 1.2004 | 8.369 | 0.101 | 7.6013 | 14.2675 |
| 23 | 2505 | 12.5665 | 1.3714 | 1.1316 | 9.1636 | 0.0901 | 8.4065 | 14.2207 |
| 23 | 4144 | 12.2741 | 1.4026 | 1.1373 | 8.7509 | 0.0927 | 8.0088 | 13.9593 |
| 23 | 1341 | 11.8136 | 1.2314 | 1.0176 | 9.5935 | 0.0861 | 8.8327 | 12.0212 |

## Strongest Selectivity Comparisons

| relation | metric | family_a | family_b | mean_diff | ci_low | ci_high | sign_test_pvalue | num_pairs |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| capital | target_selectivity | chat_template | declarative | -0.5947 | -0.773 | -0.4428 | 0.0002 | 18 |
| capital | target_selectivity | chat_template | qa | -0.4989 | -0.6907 | -0.323 | 0.049 | 18 |
| capital | target_selectivity | chat_template | raw_question | -0.35 | -0.5372 | -0.1748 | 0.0213 | 18 |
| capital | target_selectivity | declarative | raw_question | 0.2447 | 0.1366 | 0.3526 | 0.0001 | 18 |
| official_language | target_selectivity | chat_template | raw_question | -0.1855 | -0.3809 | -0.0086 | 0.5078 | 18 |
| official_language | target_selectivity | chat_template | qa | -0.1617 | -0.3414 | 0.0068 | 0.7539 | 18 |
| capital | target_selectivity | qa | raw_question | 0.1489 | 0.0654 | 0.2315 | 0.0074 | 18 |
| official_language | target_selectivity | declarative | raw_question | -0.1146 | -0.2021 | -0.0272 | 0.0386 | 18 |

## Neuron Ablation Summary

| candidate_type | prompt_family | answer_f1_drop | contains_drop | target_selectivity_drop | same_subject_control_f1_increase | same_relation_control_f1_increase | lexical_distractor_f1_increase | max_control_f1_increase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| invariant | chat_template | -0.025 | 0.0 | -0.0417 | 0.0 | 0.0 | -0.0167 | -0.0167 |
| invariant | declarative | 0.0033 | 0.0 | 0.0033 | 0.0 | 0.0 | 0.0 | 0.0 |
| invariant | qa | 0.02 | 0.05 | 0.0325 | 0.0 | 0.0 | 0.0125 | 0.0125 |
| invariant | raw_question | 0.0117 | 0.05 | 0.0142 | 0.0 | 0.0 | 0.0025 | 0.0025 |
| prompt_sensitive | chat_template | 0.1761 | 0.15 | 0.1678 | 0.0 | 0.0083 | -0.0167 | -0.0083 |
| prompt_sensitive | declarative | 0.0385 | 0.0 | 0.0363 | 0.0 | 0.0 | -0.0023 | -0.0023 |
| prompt_sensitive | qa | 0.0079 | 0.05 | 0.0375 | 0.0 | 0.0 | 0.0296 | 0.0296 |
| prompt_sensitive | raw_question | -0.0542 | -0.15 | -0.0231 | 0.0 | 0.0 | 0.0311 | 0.0311 |