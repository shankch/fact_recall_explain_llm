# Prompt Invariance Report: smollm2_360m_base

- Prompts analyzed: 360
- Mean answer F1: 0.2895
- Analysis-selected best family: qa
- Analysis-selected best selectivity family: qa

## Holdout Family Summary

| relation | prompt_family | target_rank | target_margin | full_exact_match | contains_expected | answer_f1 | answer_similarity |
| --- | --- | --- | --- | --- | --- | --- | --- |
| birth_place | chat_template | 902.25 | -5.0 | 0.0 | 0.0 | 0.0 | 0.2038 |
| birth_place | declarative | 211.75 | -3.8125 | 0.0 | 0.25 | 0.1875 | 0.4029 |
| birth_place | qa | 409.25 | -4.9844 | 0.0 | 0.25 | 0.15 | 0.3849 |
| birth_place | raw_question | 2311.5 | -11.1953 | 0.0 | 0.0 | 0.0 | 0.2359 |
| capital | chat_template | 9.75 | -1.4062 | 0.5 | 0.75 | 0.5714 | 0.6684 |
| capital | declarative | 1.0 | 1.5938 | 0.0 | 1.0 | 0.3583 | 0.4557 |
| capital | qa | 1.25 | 2.1875 | 0.0 | 1.0 | 0.3292 | 0.5026 |
| capital | raw_question | 31.5 | -6.7344 | 0.0 | 0.5 | 0.1429 | 0.4351 |
| currency | chat_template | 5.5 | -0.2188 | 0.25 | 1.0 | 0.7262 | 0.7539 |
| currency | declarative | 2.25 | -2.125 | 0.0 | 1.0 | 0.5625 | 0.6388 |
| currency | qa | 4.75 | -0.8906 | 0.0 | 1.0 | 0.5218 | 0.6037 |
| currency | raw_question | 27.75 | -6.5469 | 0.0 | 0.5 | 0.1556 | 0.3485 |
| headquarters | chat_template | 30.5 | -1.8594 | 0.0 | 0.25 | 0.0714 | 0.3245 |
| headquarters | declarative | 37.0 | -2.4531 | 0.0 | 0.25 | 0.0833 | 0.2631 |
| headquarters | qa | 55.5 | -3.0625 | 0.0 | 0.5 | 0.3667 | 0.4794 |
| headquarters | raw_question | 147.75 | -6.7656 | 0.0 | 0.25 | 0.1548 | 0.2446 |
| official_language | chat_template | 1.25 | 0.9375 | 0.0 | 0.75 | 0.2875 | 0.3865 |
| official_language | declarative | 1.0 | 2.4531 | 0.0 | 1.0 | 0.225 | 0.2617 |
| official_language | qa | 1.0 | 1.75 | 0.0 | 1.0 | 0.25 | 0.2918 |
| official_language | raw_question | 8.5 | -5.2812 | 0.0 | 1.0 | 0.25 | 0.2837 |

## Control Selectivity Summary

| prompt_family | answer_f1 | target_selectivity | same_subject_control_f1 | same_relation_control_f1 | lexical_distractor_f1 | max_control_f1 |
| --- | --- | --- | --- | --- | --- | --- |
| chat_template | 0.3313 | 0.2262 | 0.0 | 0.0 | 0.1051 | 0.1051 |
| declarative | 0.2833 | 0.215 | 0.0 | 0.0125 | 0.0558 | 0.0683 |
| qa | 0.3235 | 0.2106 | 0.0 | 0.05 | 0.0629 | 0.1129 |
| raw_question | 0.1406 | 0.107 | 0.0 | 0.0 | 0.0336 | 0.0336 |

## Top Invariant Neurons

| layer | neuron | mean_abs_activation | activation_std | family_mean_std | sharedness | family_sensitivity | invariance_score | prompt_sensitive_score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 6 | 156 | 0.2755 | 0.0031 | 0.0025 | 90.2246 | 0.0091 | 89.4096 | 0.0007 |
| 12 | 490 | 0.2753 | 0.0034 | 0.0014 | 80.3312 | 0.0052 | 79.9136 | 0.0004 |
| 2 | 1170 | 0.2756 | 0.0037 | 0.0014 | 74.1474 | 0.0052 | 73.7659 | 0.0004 |
| 14 | 449 | 0.2743 | 0.004 | 0.0022 | 69.2493 | 0.0079 | 68.7082 | 0.0006 |
| 17 | 1709 | 0.2758 | 0.004 | 0.0015 | 68.6522 | 0.0054 | 68.2851 | 0.0004 |
| 17 | 29 | 0.2739 | 0.0041 | 0.0035 | 66.145 | 0.0129 | 65.3003 | 0.001 |
| 1 | 538 | 0.2746 | 0.0042 | 0.0033 | 65.6176 | 0.0119 | 64.8487 | 0.0009 |
| 17 | 2550 | 0.2756 | 0.0042 | 0.0013 | 64.9515 | 0.0046 | 64.6511 | 0.0004 |

## Top Prompt-Sensitive Neurons

| layer | neuron | mean_abs_activation | activation_std | family_mean_std | sharedness | family_sensitivity | invariance_score | prompt_sensitive_score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 31 | 1777 | 10.2958 | 2.5012 | 2.1728 | 4.1163 | 0.211 | 3.399 | 22.3702 |
| 31 | 1034 | 16.4083 | 1.4876 | 1.1474 | 11.0298 | 0.0699 | 10.3089 | 18.8266 |
| 31 | 2064 | 16.1362 | 1.6239 | 1.15 | 9.9368 | 0.0713 | 9.2757 | 18.5566 |
| 31 | 446 | 16.6828 | 1.4687 | 1.0802 | 11.3586 | 0.0648 | 10.6678 | 18.0212 |
| 31 | 2464 | 15.5112 | 1.5073 | 1.1485 | 10.2909 | 0.074 | 9.5814 | 17.8146 |
| 31 | 2276 | 16.6828 | 1.401 | 1.053 | 11.9074 | 0.0631 | 11.2004 | 17.5674 |
| 31 | 2169 | 15.3339 | 1.5362 | 1.1429 | 9.9816 | 0.0745 | 9.2892 | 17.5245 |
| 31 | 2373 | 15.9114 | 1.4281 | 1.1005 | 11.1416 | 0.0692 | 10.4208 | 17.5109 |

## Strongest Selectivity Comparisons

| relation | metric | family_a | family_b | mean_diff | ci_low | ci_high | sign_test_pvalue | num_pairs |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| currency | target_selectivity | qa | raw_question | -0.1828 | -0.2921 | -0.0819 | 0.002 | 18 |
| currency | target_selectivity | chat_template | raw_question | -0.1751 | -0.3197 | -0.0315 | 0.0225 | 18 |
| currency | target_selectivity | declarative | raw_question | -0.1713 | -0.2938 | -0.0317 | 0.0768 | 18 |
| capital | target_selectivity | chat_template | declarative | -0.1616 | -0.3429 | 0.0102 | 0.1435 | 18 |
| capital | target_selectivity | chat_template | qa | -0.1596 | -0.3412 | 0.0036 | 0.2101 | 18 |
| birth_place | target_selectivity | chat_template | qa | 0.1546 | -0.004 | 0.3489 | 0.1797 | 18 |
| birth_place | target_selectivity | chat_template | raw_question | 0.137 | -0.0558 | 0.3409 | 0.2188 | 18 |
| headquarters | target_selectivity | chat_template | qa | 0.1277 | -0.0797 | 0.3221 | 0.3438 | 18 |

## Neuron Ablation Summary

| candidate_type | prompt_family | answer_f1_drop | contains_drop | target_selectivity_drop | same_subject_control_f1_increase | same_relation_control_f1_increase | lexical_distractor_f1_increase | max_control_f1_increase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| invariant | chat_template | 0.0456 | 0.05 | 0.0425 | 0.0 | 0.0 | -0.0032 | -0.0032 |
| invariant | declarative | 0.0279 | 0.05 | 0.0297 | 0.0 | 0.0 | 0.0018 | 0.0018 |
| invariant | qa | -0.0179 | 0.05 | -0.0496 | 0.0 | -0.03 | -0.0018 | -0.0318 |
| invariant | raw_question | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| prompt_sensitive | chat_template | 0.1494 | 0.2 | 0.1127 | 0.0 | 0.0 | -0.0367 | -0.0367 |
| prompt_sensitive | declarative | 0.034 | 0.0 | 0.0273 | 0.0 | -0.0025 | -0.0042 | -0.0067 |
| prompt_sensitive | qa | 0.1206 | 0.25 | 0.0529 | 0.0 | -0.05 | -0.0177 | -0.0677 |
| prompt_sensitive | raw_question | -0.0681 | 0.0 | -0.0448 | 0.0 | 0.0 | 0.0233 | 0.0233 |