# Prompt Invariance Report: gemma_270m_base

- Prompts analyzed: 80
- Mean answer F1: 0.1148
- Best prompt family by answer F1: declarative

## Family Summary

| relation | prompt_family | target_rank | target_margin | full_exact_match | contains_expected | answer_f1 | answer_similarity |
| --- | --- | --- | --- | --- | --- | --- | --- |
| birth_place | chat_template | 144.75 | -4.9062 | 0.0 | 0.0 | 0.0 | 0.206 |
| birth_place | declarative | 27.5 | -3.1875 | 0.0 | 0.25 | 0.1 | 0.2724 |
| birth_place | qa | 63.75 | -3.0312 | 0.0 | 0.0 | 0.0 | 0.1944 |
| birth_place | raw_question | 343.75 | -7.9375 | 0.0 | 0.0 | 0.0 | 0.0737 |
| capital | chat_template | 22.75 | -1.6406 | 0.0 | 0.25 | 0.2167 | 0.4531 |
| capital | declarative | 2.0 | -0.0938 | 0.0 | 0.5 | 0.1528 | 0.2709 |
| capital | qa | 4.25 | -1.4062 | 0.0 | 0.0 | 0.0 | 0.2112 |
| capital | raw_question | 22.5 | -4.125 | 0.0 | 0.0 | 0.1667 | 0.3612 |
| currency | chat_template | 72.5 | -2.9062 | 0.0 | 0.0 | 0.125 | 0.381 |
| currency | declarative | 15.25 | -4.6719 | 0.0 | 0.25 | 0.2339 | 0.3806 |
| currency | qa | 37.0 | -2.625 | 0.0 | 0.0 | 0.226 | 0.3627 |
| currency | raw_question | 626.5 | -6.6719 | 0.0 | 0.25 | 0.1667 | 0.4236 |
| headquarters | chat_template | 576.75 | -5.1406 | 0.25 | 0.25 | 0.25 | 0.4621 |
| headquarters | declarative | 56.25 | -1.5469 | 0.0 | 0.5 | 0.2 | 0.4141 |
| headquarters | qa | 71.0 | -2.5625 | 0.0 | 0.5 | 0.2361 | 0.4608 |
| headquarters | raw_question | 573.75 | -7.6875 | 0.0 | 0.25 | 0.0556 | 0.2233 |
| official_language | chat_template | 73.25 | -3.0 | 0.0 | 0.0 | 0.0 | 0.1764 |
| official_language | declarative | 1.75 | 0.2031 | 0.0 | 0.25 | 0.0556 | 0.2071 |
| official_language | qa | 8.75 | -1.125 | 0.0 | 0.25 | 0.0556 | 0.1663 |
| official_language | raw_question | 143.0 | -6.4219 | 0.0 | 0.25 | 0.0556 | 0.1864 |

## Top Invariant Neurons

| layer | neuron | mean_abs_activation | activation_std | family_mean_std | sharedness | family_sensitivity | invariance_score | prompt_sensitive_score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 10 | 232 | 0.1691 | 0.0012 | 0.0002 | 139.2409 | 0.0013 | 139.0627 | 0.0 |
| 9 | 880 | 0.1686 | 0.0021 | 0.0008 | 79.2991 | 0.0048 | 78.9205 | 0.0001 |
| 5 | 1401 | 0.1679 | 0.0023 | 0.0008 | 72.4853 | 0.0047 | 72.149 | 0.0001 |
| 5 | 1457 | 0.1665 | 0.0025 | 0.0009 | 67.3745 | 0.0056 | 66.9973 | 0.0002 |
| 9 | 1350 | 0.1681 | 0.0026 | 0.0007 | 64.01 | 0.0043 | 63.7338 | 0.0001 |
| 10 | 1165 | 0.1674 | 0.0027 | 0.0011 | 62.1029 | 0.0063 | 61.7124 | 0.0002 |
| 0 | 1652 | 0.1676 | 0.0028 | 0.0013 | 60.5657 | 0.008 | 60.0864 | 0.0002 |
| 7 | 1688 | 0.1674 | 0.0028 | 0.0005 | 59.232 | 0.0031 | 59.0477 | 0.0001 |

## Top Prompt-Sensitive Neurons

| layer | neuron | mean_abs_activation | activation_std | family_mean_std | sharedness | family_sensitivity | invariance_score | prompt_sensitive_score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 1765 | 1.8521 | 3.0881 | 3.0819 | 0.5997 | 1.6641 | 0.2251 | 5.7079 |
| 0 | 1165 | 2.7318 | 1.7766 | 1.7537 | 1.5377 | 0.642 | 0.9365 | 4.7909 |
| 15 | 338 | 2.395 | 1.5488 | 1.5229 | 1.5463 | 0.6359 | 0.9453 | 3.6473 |
| 1 | 283 | 1.8327 | 1.9683 | 1.9662 | 0.9311 | 1.0728 | 0.4492 | 3.6036 |
| 0 | 1392 | 4.1332 | 0.88 | 0.8714 | 4.6966 | 0.2108 | 3.8788 | 3.6015 |
| 0 | 1702 | 4.8803 | 0.6679 | 0.6569 | 7.3068 | 0.1346 | 6.4399 | 3.2061 |
| 15 | 783 | 2.1047 | 1.2955 | 1.2822 | 1.6246 | 0.6092 | 1.0096 | 2.6986 |
| 6 | 725 | 1.2685 | 2.0522 | 2.0185 | 0.6181 | 1.5912 | 0.2385 | 2.5605 |

## Neuron Ablation Summary

| candidate_type | prompt_family | answer_f1_drop | contains_drop |
| --- | --- | --- | --- |
| invariant | chat_template | 0.0 | -0.2 |
| invariant | declarative | -0.0044 | 0.0 |
| invariant | qa | 0.0 | 0.0 |
| invariant | raw_question | 0.0 | 0.0 |
| prompt_sensitive | chat_template | 0.0 | 0.0 |
| prompt_sensitive | declarative | -0.0489 | -0.2 |
| prompt_sensitive | qa | 0.0 | 0.0 |
| prompt_sensitive | raw_question | 0.0 | 0.0 |