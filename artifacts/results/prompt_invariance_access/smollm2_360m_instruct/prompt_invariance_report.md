# Prompt Invariance Report: smollm2_360m_instruct

- Prompts analyzed: 240
- Mean answer F1: 0.1369
- Best prompt family by answer F1: chat_template

## Family Summary

| relation | prompt_family | target_rank | target_margin | full_exact_match | contains_expected | answer_f1 | answer_similarity |
| --- | --- | --- | --- | --- | --- | --- | --- |
| birth_place | chat_template | 4837.0 | -14.4806 | 0.25 | 0.4167 | 0.3294 | 0.4093 |
| birth_place | declarative | 50.25 | -2.7604 | 0.0 | 0.0833 | 0.0792 | 0.2516 |
| birth_place | qa | 2759.9167 | -11.5104 | 0.0 | 0.0 | 0.0 | 0.0 |
| birth_place | raw_question | 2560.6667 | -12.9006 | 0.0 | 0.0 | 0.0 | 0.0 |
| capital | chat_template | 252.0 | -6.7344 | 0.5 | 0.6667 | 0.6222 | 0.7412 |
| capital | declarative | 2.0 | 3.2188 | 0.0 | 0.8333 | 0.2736 | 0.348 |
| capital | qa | 203.1667 | -9.7422 | 0.0 | 0.0 | 0.0 | 0.0 |
| capital | raw_question | 3763.0833 | -12.7109 | 0.0 | 0.0 | 0.0 | 0.0 |
| currency | chat_template | 643.1667 | -8.6478 | 0.0 | 0.1667 | 0.1669 | 0.4699 |
| currency | declarative | 14.5 | -4.8542 | 0.0 | 0.25 | 0.2329 | 0.3686 |
| currency | qa | 1128.0833 | -9.6419 | 0.0 | 0.0 | 0.0 | 0.0123 |
| currency | raw_question | 5079.3333 | -15.5316 | 0.0 | 0.0 | 0.0 | 0.0278 |
| headquarters | chat_template | 5181.75 | -12.7982 | 0.0 | 0.5833 | 0.2649 | 0.3303 |
| headquarters | declarative | 118.0 | -0.4557 | 0.0 | 0.5833 | 0.4428 | 0.5415 |
| headquarters | qa | 855.5833 | -10.138 | 0.0 | 0.0 | 0.0 | 0.0 |
| headquarters | raw_question | 1814.8333 | -13.4466 | 0.0 | 0.0 | 0.0 | 0.0 |
| official_language | chat_template | 217.0833 | -7.4688 | 0.0 | 0.5833 | 0.1528 | 0.3225 |
| official_language | declarative | 1.25 | 1.151 | 0.0 | 0.6667 | 0.1548 | 0.2723 |
| official_language | qa | 737.4167 | -10.8125 | 0.0 | 0.0 | 0.0 | 0.0 |
| official_language | raw_question | 2518.9167 | -14.166 | 0.0 | 0.0833 | 0.0185 | 0.0823 |

## Control Selectivity Summary

| prompt_family | answer_f1 | target_selectivity | same_subject_control_f1 | same_relation_control_f1 | lexical_distractor_f1 | max_control_f1 |
| --- | --- | --- | --- | --- | --- | --- |
| chat_template | 0.3072 | 0.2739 | 0.0 | 0.0153 | 0.0222 | 0.0333 |
| declarative | 0.2367 | 0.2086 | 0.0 | 0.0122 | 0.0214 | 0.0281 |
| qa | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| raw_question | 0.0037 | 0.0 | 0.0 | 0.0 | 0.0037 | 0.0037 |

## Top Invariant Neurons

| layer | neuron | mean_abs_activation | activation_std | family_mean_std | sharedness | family_sensitivity | invariance_score | prompt_sensitive_score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 538 | 0.2775 | 0.0021 | 0.0009 | 130.6871 | 0.0033 | 130.2591 | 0.0003 |
| 13 | 1014 | 0.2766 | 0.0024 | 0.0008 | 113.6947 | 0.0029 | 113.3699 | 0.0002 |
| 12 | 2285 | 0.2752 | 0.0032 | 0.001 | 87.1075 | 0.0037 | 86.7906 | 0.0003 |
| 14 | 1185 | 0.2757 | 0.0033 | 0.0017 | 84.773 | 0.0061 | 84.2621 | 0.0005 |
| 18 | 1865 | 0.2761 | 0.0033 | 0.0013 | 83.222 | 0.0046 | 82.8415 | 0.0004 |
| 6 | 156 | 0.2732 | 0.0039 | 0.0029 | 70.0519 | 0.0107 | 69.3124 | 0.0008 |
| 17 | 71 | 0.2748 | 0.0041 | 0.0019 | 67.7974 | 0.0071 | 67.3221 | 0.0005 |
| 17 | 980 | 0.2742 | 0.0041 | 0.0017 | 66.9631 | 0.0062 | 66.5497 | 0.0005 |

## Top Prompt-Sensitive Neurons

| layer | neuron | mean_abs_activation | activation_std | family_mean_std | sharedness | family_sensitivity | invariance_score | prompt_sensitive_score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 31 | 2496 | 13.2163 | 2.0492 | 1.8544 | 6.4494 | 0.1403 | 5.6558 | 24.5081 |
| 31 | 2464 | 12.3038 | 1.9231 | 1.729 | 6.3978 | 0.1405 | 5.6095 | 21.2736 |
| 31 | 1620 | 11.2736 | 2.0054 | 1.8447 | 5.6217 | 0.1636 | 4.8311 | 20.7965 |
| 31 | 1777 | 5.5734 | 3.6016 | 3.4331 | 1.5475 | 0.616 | 0.9576 | 19.1339 |
| 31 | 2169 | 11.6997 | 1.8196 | 1.5898 | 6.4296 | 0.1359 | 5.6605 | 18.6001 |
| 31 | 2301 | 11.7181 | 1.844 | 1.5852 | 6.3548 | 0.1353 | 5.5976 | 18.575 |
| 31 | 2276 | 13.091 | 1.5882 | 1.3988 | 8.2427 | 0.1068 | 7.447 | 18.3112 |
| 31 | 1767 | 12.2486 | 1.6736 | 1.4801 | 7.3186 | 0.1208 | 6.5296 | 18.1286 |

## Strongest Selectivity Comparisons

| relation | metric | family_a | family_b | mean_diff | ci_low | ci_high | sign_test_pvalue | num_pairs |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| capital | target_selectivity | chat_template | raw_question | -0.6222 | -0.8389 | -0.3831 | 0.0039 | 12 |
| capital | target_selectivity | chat_template | qa | -0.6222 | -0.8389 | -0.3831 | 0.0039 | 12 |
| headquarters | target_selectivity | declarative | raw_question | -0.415 | -0.577 | -0.252 | 0.0039 | 12 |
| headquarters | target_selectivity | declarative | qa | -0.415 | -0.577 | -0.252 | 0.0039 | 12 |
| capital | target_selectivity | chat_template | declarative | -0.3486 | -0.5621 | -0.1231 | 0.0654 | 12 |
| birth_place | target_selectivity | chat_template | qa | -0.2738 | -0.5484 | 0.0041 | 0.2188 | 12 |
| birth_place | target_selectivity | chat_template | raw_question | -0.2738 | -0.5484 | 0.0041 | 0.2188 | 12 |
| capital | target_selectivity | declarative | qa | -0.2736 | -0.3713 | -0.1874 | 0.002 | 12 |

## Neuron Ablation Summary

| candidate_type | prompt_family | answer_f1_drop | contains_drop | target_selectivity_drop | same_subject_control_f1_increase | same_relation_control_f1_increase | lexical_distractor_f1_increase | max_control_f1_increase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| invariant | chat_template | -0.0027 | 0.0 | -0.0045 | 0.0 | 0.0 | -0.0019 | -0.0019 |
| invariant | declarative | -0.0062 | 0.0 | -0.0062 | 0.0 | 0.0 | 0.0 | 0.0 |
| invariant | qa | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| invariant | raw_question | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| prompt_sensitive | chat_template | -0.0508 | 0.0 | -0.0064 | 0.0 | 0.0 | 0.0444 | 0.0444 |
| prompt_sensitive | declarative | 0.0611 | 0.1333 | 0.0913 | 0.0 | 0.0222 | 0.0079 | 0.0302 |
| prompt_sensitive | qa | -0.0926 | -0.0667 | -0.0481 | 0.0 | 0.0 | 0.0444 | 0.0444 |
| prompt_sensitive | raw_question | -0.1222 | -0.1333 | 0.0111 | 0.0 | 0.0 | 0.1333 | 0.1333 |