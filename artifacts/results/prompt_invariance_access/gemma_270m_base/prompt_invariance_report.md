# Prompt Invariance Report: gemma_270m_base

- Prompts analyzed: 240
- Mean answer F1: 0.1240
- Best prompt family by answer F1: declarative

## Family Summary

| relation | prompt_family | target_rank | target_margin | full_exact_match | contains_expected | answer_f1 | answer_similarity |
| --- | --- | --- | --- | --- | --- | --- | --- |
| birth_place | chat_template | 1781.5 | -6.5469 | 0.0 | 0.0 | 0.0 | 0.1895 |
| birth_place | declarative | 176.1667 | -3.7708 | 0.0 | 0.1667 | 0.0958 | 0.2865 |
| birth_place | qa | 351.0 | -4.0625 | 0.0 | 0.1667 | 0.0764 | 0.2655 |
| birth_place | raw_question | 1487.5 | -9.1484 | 0.0 | 0.1667 | 0.0972 | 0.2011 |
| capital | chat_template | 27.3333 | -2.0885 | 0.0 | 0.4167 | 0.2759 | 0.4248 |
| capital | declarative | 20.6667 | -0.1875 | 0.0 | 0.5833 | 0.1497 | 0.2485 |
| capital | qa | 7.3333 | -1.9531 | 0.0 | 0.0 | 0.0 | 0.17 |
| capital | raw_question | 36.3333 | -4.9792 | 0.0 | 0.0833 | 0.1111 | 0.2517 |
| currency | chat_template | 100.75 | -2.7865 | 0.0 | 0.0833 | 0.1222 | 0.3632 |
| currency | declarative | 137.75 | -5.1615 | 0.0 | 0.4167 | 0.2514 | 0.3962 |
| currency | qa | 55.5 | -2.5885 | 0.0 | 0.1667 | 0.1587 | 0.3499 |
| currency | raw_question | 406.8333 | -6.8229 | 0.0 | 0.3333 | 0.2431 | 0.4605 |
| headquarters | chat_template | 418.1667 | -4.375 | 0.0833 | 0.25 | 0.1806 | 0.3457 |
| headquarters | declarative | 95.75 | -1.7708 | 0.0 | 0.4167 | 0.156 | 0.3206 |
| headquarters | qa | 94.5833 | -1.7656 | 0.0 | 0.3333 | 0.1775 | 0.3388 |
| headquarters | raw_question | 453.3333 | -7.1354 | 0.0 | 0.1667 | 0.0522 | 0.2153 |
| official_language | chat_template | 31.5833 | -2.0 | 0.0 | 0.1667 | 0.0394 | 0.1996 |
| official_language | declarative | 1.75 | -0.0208 | 0.0 | 0.5833 | 0.1245 | 0.2293 |
| official_language | qa | 3.75 | -0.0417 | 0.0 | 0.5833 | 0.1296 | 0.247 |
| official_language | raw_question | 68.0833 | -5.5521 | 0.0 | 0.1667 | 0.0394 | 0.1959 |

## Control Selectivity Summary

| prompt_family | answer_f1 | target_selectivity | same_subject_control_f1 | same_relation_control_f1 | lexical_distractor_f1 | max_control_f1 |
| --- | --- | --- | --- | --- | --- | --- |
| chat_template | 0.1236 | 0.1161 | 0.0028 | 0.0 | 0.0048 | 0.0075 |
| declarative | 0.1555 | 0.1243 | 0.0058 | 0.01 | 0.0187 | 0.0312 |
| qa | 0.1084 | 0.0884 | 0.0 | 0.0089 | 0.0159 | 0.02 |
| raw_question | 0.1086 | 0.09 | 0.0033 | 0.0111 | 0.0042 | 0.0186 |

## Top Invariant Neurons

| layer | neuron | mean_abs_activation | activation_std | family_mean_std | sharedness | family_sensitivity | invariance_score | prompt_sensitive_score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 10 | 232 | 0.1691 | 0.0012 | 0.0002 | 146.6058 | 0.0013 | 146.4215 | 0.0 |
| 9 | 880 | 0.1684 | 0.0022 | 0.0007 | 75.3274 | 0.0042 | 75.0116 | 0.0001 |
| 5 | 1401 | 0.1679 | 0.0022 | 0.0006 | 74.7508 | 0.0038 | 74.4675 | 0.0001 |
| 0 | 1652 | 0.1676 | 0.0025 | 0.0013 | 66.8176 | 0.0078 | 66.3005 | 0.0002 |
| 16 | 1591 | 0.168 | 0.0029 | 0.001 | 58.7761 | 0.0061 | 58.417 | 0.0002 |
| 9 | 1350 | 0.168 | 0.0029 | 0.0007 | 57.7035 | 0.0043 | 57.4543 | 0.0001 |
| 5 | 1457 | 0.1664 | 0.0029 | 0.0008 | 56.4552 | 0.0048 | 56.1836 | 0.0001 |
| 17 | 1557 | 0.1671 | 0.003 | 0.0006 | 55.3824 | 0.0035 | 55.1897 | 0.0001 |

## Top Prompt-Sensitive Neurons

| layer | neuron | mean_abs_activation | activation_std | family_mean_std | sharedness | family_sensitivity | invariance_score | prompt_sensitive_score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 1765 | 1.8393 | 3.0652 | 3.0598 | 0.6001 | 1.6636 | 0.2253 | 5.628 |
| 0 | 1165 | 2.7337 | 1.7754 | 1.7529 | 1.5398 | 0.6412 | 0.9382 | 4.792 |
| 15 | 338 | 2.3776 | 1.5437 | 1.5185 | 1.5402 | 0.6387 | 0.9399 | 3.6104 |
| 1 | 283 | 1.8347 | 1.9693 | 1.9671 | 0.9316 | 1.0722 | 0.4496 | 3.6089 |
| 0 | 1392 | 4.1243 | 0.8781 | 0.8694 | 4.6967 | 0.2108 | 3.879 | 3.5858 |
| 0 | 1702 | 4.8715 | 0.6707 | 0.6603 | 7.2629 | 0.1355 | 6.396 | 3.2166 |
| 15 | 783 | 2.0835 | 1.2892 | 1.275 | 1.6161 | 0.612 | 1.0026 | 2.6565 |
| 6 | 725 | 1.27 | 2.0525 | 2.0173 | 0.6188 | 1.5885 | 0.239 | 2.562 |

## Strongest Selectivity Comparisons

| relation | metric | family_a | family_b | mean_diff | ci_low | ci_high | sign_test_pvalue | num_pairs |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| capital | target_selectivity | chat_template | qa | -0.2759 | -0.4612 | -0.1074 | 0.0312 | 12 |
| capital | target_selectivity | chat_template | raw_question | -0.1648 | -0.3686 | 0.0223 | 0.375 | 12 |
| capital | target_selectivity | declarative | qa | -0.1497 | -0.2134 | -0.0823 | 0.0078 | 12 |
| capital | target_selectivity | chat_template | declarative | -0.1262 | -0.2713 | 0.0081 | 0.2891 | 12 |
| currency | target_selectivity | chat_template | raw_question | 0.1139 | -0.1892 | 0.3723 | 1.0 | 12 |
| capital | target_selectivity | qa | raw_question | 0.1111 | 0.0 | 0.2222 | 0.5 | 12 |
| currency | target_selectivity | chat_template | declarative | 0.1084 | -0.0447 | 0.224 | 0.1094 | 12 |
| headquarters | target_selectivity | chat_template | raw_question | -0.1046 | -0.2639 | 0.0366 | 1.0 | 12 |

## Neuron Ablation Summary

| candidate_type | prompt_family | answer_f1_drop | contains_drop | target_selectivity_drop | same_subject_control_f1_increase | same_relation_control_f1_increase | lexical_distractor_f1_increase | max_control_f1_increase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| invariant | chat_template | 0.1348 | 0.2 | 0.1306 | 0.0 | 0.0 | -0.0042 | -0.0042 |
| invariant | declarative | 0.0136 | 0.0 | 0.0103 | 0.0 | 0.0 | -0.0033 | -0.0033 |
| invariant | qa | 0.0044 | 0.0 | 0.0044 | 0.0 | 0.0 | 0.0 | 0.0 |
| invariant | raw_question | -0.0144 | 0.0 | -0.0311 | 0.0 | 0.0 | -0.0167 | -0.0167 |
| prompt_sensitive | chat_template | 0.0181 | 0.0667 | 0.0435 | 0.0 | 0.0 | 0.0254 | 0.0254 |
| prompt_sensitive | declarative | 0.0136 | 0.0 | 0.0069 | 0.0 | 0.0 | -0.0067 | -0.0067 |
| prompt_sensitive | qa | -0.0439 | -0.0667 | -0.0454 | 0.0 | 0.0 | -0.0015 | -0.0015 |
| prompt_sensitive | raw_question | -0.1049 | -0.2 | -0.1068 | 0.0 | 0.0 | -0.0019 | -0.0019 |