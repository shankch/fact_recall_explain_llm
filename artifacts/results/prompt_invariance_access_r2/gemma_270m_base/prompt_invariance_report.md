# Prompt Invariance Report: gemma_270m_base

- Prompts analyzed: 360
- Mean answer F1: 0.1269
- Analysis-selected best family: declarative
- Analysis-selected best selectivity family: declarative

## Holdout Family Summary

| relation | prompt_family | target_rank | target_margin | full_exact_match | contains_expected | answer_f1 | answer_similarity |
| --- | --- | --- | --- | --- | --- | --- | --- |
| birth_place | chat_template | 3881.5 | -7.7344 | 0.0 | 0.0 | 0.0 | 0.2361 |
| birth_place | declarative | 306.75 | -4.875 | 0.0 | 0.25 | 0.1875 | 0.4077 |
| birth_place | qa | 582.25 | -4.9531 | 0.0 | 0.25 | 0.1667 | 0.3777 |
| birth_place | raw_question | 2467.0 | -10.0547 | 0.0 | 0.0 | 0.0 | 0.1749 |
| capital | chat_template | 45.5 | -4.1094 | 0.0 | 0.5 | 0.3333 | 0.432 |
| capital | declarative | 8.25 | -1.1562 | 0.0 | 0.25 | 0.05 | 0.1693 |
| capital | qa | 5.75 | -2.9062 | 0.0 | 0.0 | 0.0 | 0.17 |
| capital | raw_question | 36.0 | -5.6562 | 0.0 | 0.0 | 0.0 | 0.1156 |
| currency | chat_template | 28.0 | -2.25 | 0.0 | 0.5 | 0.1111 | 0.3569 |
| currency | declarative | 18.25 | -4.5469 | 0.0 | 0.75 | 0.3215 | 0.3615 |
| currency | qa | 13.25 | -1.8281 | 0.0 | 0.0 | 0.201 | 0.3441 |
| currency | raw_question | 148.5 | -5.8906 | 0.0 | 0.75 | 0.2909 | 0.4451 |
| headquarters | chat_template | 29.75 | -2.2188 | 0.0 | 0.25 | 0.125 | 0.2615 |
| headquarters | declarative | 11.5 | -2.5625 | 0.0 | 0.25 | 0.158 | 0.2348 |
| headquarters | qa | 11.25 | -0.9375 | 0.0 | 0.25 | 0.2034 | 0.2682 |
| headquarters | raw_question | 59.0 | -5.1719 | 0.0 | 0.0 | 0.101 | 0.2638 |
| official_language | chat_template | 8.5 | -0.7344 | 0.0 | 0.25 | 0.05 | 0.2799 |
| official_language | declarative | 1.75 | -0.0312 | 0.0 | 0.75 | 0.1681 | 0.2821 |
| official_language | qa | 1.25 | 0.7656 | 0.0 | 1.0 | 0.2222 | 0.2891 |
| official_language | raw_question | 20.75 | -3.6406 | 0.0 | 0.0 | 0.0 | 0.1857 |

## Control Selectivity Summary

| prompt_family | answer_f1 | target_selectivity | same_subject_control_f1 | same_relation_control_f1 | lexical_distractor_f1 | max_control_f1 |
| --- | --- | --- | --- | --- | --- | --- |
| chat_template | 0.1239 | 0.0685 | 0.0 | 0.02 | 0.0354 | 0.0554 |
| declarative | 0.177 | 0.1277 | 0.0 | 0.0091 | 0.0402 | 0.0493 |
| qa | 0.1587 | 0.0876 | 0.0 | 0.02 | 0.0511 | 0.0711 |
| raw_question | 0.0784 | 0.0582 | 0.0 | 0.0111 | 0.0091 | 0.0202 |

## Top Invariant Neurons

| layer | neuron | mean_abs_activation | activation_std | family_mean_std | sharedness | family_sensitivity | invariance_score | prompt_sensitive_score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 10 | 232 | 0.1691 | 0.0012 | 0.0002 | 142.5667 | 0.0012 | 142.3958 | 0.0 |
| 9 | 880 | 0.1684 | 0.0021 | 0.0007 | 80.6353 | 0.0042 | 80.2955 | 0.0001 |
| 5 | 1401 | 0.1678 | 0.0023 | 0.0006 | 74.0066 | 0.0037 | 73.7324 | 0.0001 |
| 0 | 1652 | 0.1676 | 0.0024 | 0.0013 | 69.9768 | 0.0076 | 69.4472 | 0.0002 |
| 9 | 1350 | 0.168 | 0.0028 | 0.0007 | 60.4221 | 0.0041 | 60.1746 | 0.0001 |
| 5 | 1457 | 0.1665 | 0.0028 | 0.0009 | 58.5515 | 0.0057 | 58.22 | 0.0002 |
| 16 | 1591 | 0.1679 | 0.003 | 0.0011 | 56.5607 | 0.0065 | 56.1948 | 0.0002 |
| 5 | 501 | 0.1663 | 0.003 | 0.0024 | 55.6423 | 0.0142 | 54.865 | 0.0004 |

## Top Prompt-Sensitive Neurons

| layer | neuron | mean_abs_activation | activation_std | family_mean_std | sharedness | family_sensitivity | invariance_score | prompt_sensitive_score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 1765 | 1.8382 | 3.0629 | 3.0578 | 0.6001 | 1.6635 | 0.2253 | 5.6208 |
| 0 | 1165 | 2.7236 | 1.7752 | 1.7534 | 1.5343 | 0.6438 | 0.9334 | 4.7757 |
| 15 | 338 | 2.3892 | 1.546 | 1.5221 | 1.5454 | 0.6371 | 0.944 | 3.6367 |
| 1 | 283 | 1.8375 | 1.9712 | 1.9685 | 0.9322 | 1.0713 | 0.4501 | 3.6171 |
| 0 | 1392 | 4.1227 | 0.8743 | 0.8652 | 4.7156 | 0.2099 | 3.8976 | 3.567 |
| 0 | 1702 | 4.8642 | 0.6702 | 0.6594 | 7.2576 | 0.1356 | 6.3912 | 3.2076 |
| 15 | 783 | 2.0908 | 1.2877 | 1.2741 | 1.6236 | 0.6094 | 1.0088 | 2.6638 |
| 6 | 725 | 1.2725 | 2.0589 | 2.0257 | 0.618 | 1.592 | 0.2384 | 2.5776 |

## Strongest Selectivity Comparisons

| relation | metric | family_a | family_b | mean_diff | ci_low | ci_high | sign_test_pvalue | num_pairs |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| capital | target_selectivity | chat_template | qa | -0.2951 | -0.4296 | -0.1469 | 0.0039 | 18 |
| capital | target_selectivity | chat_template | raw_question | -0.221 | -0.358 | -0.0689 | 0.0703 | 18 |
| capital | target_selectivity | chat_template | declarative | -0.173 | -0.2828 | -0.0543 | 0.0654 | 18 |
| capital | target_selectivity | declarative | qa | -0.1221 | -0.1774 | -0.0673 | 0.002 | 18 |
| currency | target_selectivity | chat_template | raw_question | 0.1142 | -0.107 | 0.3575 | 1.0 | 18 |
| headquarters | target_selectivity | chat_template | qa | 0.1035 | -0.0275 | 0.2378 | 0.146 | 18 |
| currency | target_selectivity | qa | raw_question | 0.1022 | -0.0457 | 0.2642 | 0.7539 | 18 |
| headquarters | target_selectivity | chat_template | declarative | 0.0932 | -0.0103 | 0.1913 | 0.146 | 18 |

## Neuron Ablation Summary

| candidate_type | prompt_family | answer_f1_drop | contains_drop | target_selectivity_drop | same_subject_control_f1_increase | same_relation_control_f1_increase | lexical_distractor_f1_increase | max_control_f1_increase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| invariant | chat_template | 0.1039 | 0.25 | 0.0596 | 0.0 | -0.0089 | -0.0354 | -0.0443 |
| invariant | declarative | 0.0031 | 0.0 | 0.0046 | 0.0 | 0.0 | 0.0016 | 0.0016 |
| invariant | qa | 0.0204 | 0.0 | -0.0196 | 0.0 | 0.0 | -0.04 | -0.04 |
| invariant | raw_question | -0.0727 | -0.05 | -0.0729 | 0.0 | -0.0111 | 0.0109 | -0.0002 |
| prompt_sensitive | chat_template | -0.0136 | 0.0 | 0.0365 | 0.0 | 0.005 | 0.0452 | 0.0502 |
| prompt_sensitive | declarative | 0.017 | 0.05 | 0.005 | 0.0 | 0.0 | -0.012 | -0.012 |
| prompt_sensitive | qa | -0.0716 | -0.15 | -0.0594 | 0.0 | 0.0 | 0.0122 | 0.0122 |
| prompt_sensitive | raw_question | -0.2191 | -0.3 | -0.1535 | 0.0 | -0.0111 | 0.0767 | 0.0656 |