# Prompt Invariance Report: gemma_270m_it

- Prompts analyzed: 360
- Mean answer F1: 0.2137
- Analysis-selected best family: raw_question
- Analysis-selected best selectivity family: raw_question

## Holdout Family Summary

| relation | prompt_family | target_rank | target_margin | full_exact_match | contains_expected | answer_f1 | answer_similarity |
| --- | --- | --- | --- | --- | --- | --- | --- |
| birth_place | chat_template | 13001.25 | -24.793 | 0.0 | 0.0 | 0.0 | 0.2067 |
| birth_place | declarative | 359.5 | -7.9688 | 0.0 | 0.0 | 0.0714 | 0.3329 |
| birth_place | qa | 4232.0 | -9.3301 | 0.0 | 0.0 | 0.0 | 0.137 |
| birth_place | raw_question | 14912.25 | -17.2148 | 0.0 | 0.0 | 0.1 | 0.3605 |
| capital | chat_template | 65.5 | -9.5 | 0.25 | 0.25 | 0.25 | 0.5933 |
| capital | declarative | 1.0 | 3.5312 | 0.0 | 1.0 | 0.2464 | 0.3169 |
| capital | qa | 2.0 | -1.1875 | 0.0 | 0.5 | 0.2222 | 0.3628 |
| capital | raw_question | 58.25 | -10.8438 | 0.0 | 0.5 | 0.2 | 0.3457 |
| currency | chat_template | 230.75 | -10.4609 | 0.0 | 0.25 | 0.35 | 0.6013 |
| currency | declarative | 33.75 | -7.1562 | 0.0 | 0.75 | 0.379 | 0.4548 |
| currency | qa | 28.25 | -2.2656 | 0.0 | 0.25 | 0.3194 | 0.4904 |
| currency | raw_question | 880.5 | -10.4141 | 0.0 | 0.75 | 0.6 | 0.6707 |
| headquarters | chat_template | 21406.0 | -17.2002 | 0.0 | 0.0 | 0.1667 | 0.4528 |
| headquarters | declarative | 37.0 | -3.2812 | 0.0 | 0.25 | 0.0556 | 0.2564 |
| headquarters | qa | 51.0 | -4.5 | 0.0 | 0.25 | 0.1181 | 0.2488 |
| headquarters | raw_question | 392.0 | -10.9375 | 0.0 | 0.25 | 0.127 | 0.274 |
| official_language | chat_template | 1036.5 | -11.0107 | 0.25 | 0.25 | 0.25 | 0.7141 |
| official_language | declarative | 360.0 | -7.0781 | 0.0 | 0.0 | 0.0625 | 0.1686 |
| official_language | qa | 11.5 | -1.7812 | 0.0 | 0.0 | 0.0 | 0.253 |
| official_language | raw_question | 42.25 | -8.9375 | 0.0 | 0.5 | 0.325 | 0.5363 |

## Control Selectivity Summary

| prompt_family | answer_f1 | target_selectivity | same_subject_control_f1 | same_relation_control_f1 | lexical_distractor_f1 | max_control_f1 |
| --- | --- | --- | --- | --- | --- | --- |
| chat_template | 0.2033 | 0.1617 | 0.0 | 0.025 | 0.0167 | 0.0417 |
| declarative | 0.163 | 0.106 | 0.0 | 0.0111 | 0.0458 | 0.0569 |
| qa | 0.1319 | 0.0701 | 0.0 | 0.0091 | 0.0528 | 0.0619 |
| raw_question | 0.2704 | 0.1521 | 0.0 | 0.0333 | 0.085 | 0.1183 |

## Top Invariant Neurons

| layer | neuron | mean_abs_activation | activation_std | family_mean_std | sharedness | family_sensitivity | invariance_score | prompt_sensitive_score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4 | 1713 | 0.1685 | 0.0021 | 0.001 | 78.4339 | 0.0061 | 77.9548 | 0.0002 |
| 5 | 1392 | 0.1684 | 0.0023 | 0.001 | 73.7077 | 0.0058 | 73.2811 | 0.0002 |
| 4 | 933 | 0.1684 | 0.0028 | 0.0015 | 61.1783 | 0.0089 | 60.6362 | 0.0003 |
| 5 | 885 | 0.1672 | 0.0029 | 0.0013 | 58.3315 | 0.0075 | 57.8948 | 0.0002 |
| 8 | 159 | 0.167 | 0.0029 | 0.0012 | 57.7807 | 0.0072 | 57.3664 | 0.0002 |
| 5 | 501 | 0.1677 | 0.0029 | 0.0023 | 58.0939 | 0.0137 | 57.3088 | 0.0004 |
| 5 | 203 | 0.1662 | 0.0029 | 0.0023 | 56.5817 | 0.0139 | 55.8061 | 0.0004 |
| 9 | 907 | 0.1672 | 0.0032 | 0.0019 | 53.037 | 0.0115 | 52.4317 | 0.0003 |

## Top Prompt-Sensitive Neurons

| layer | neuron | mean_abs_activation | activation_std | family_mean_std | sharedness | family_sensitivity | invariance_score | prompt_sensitive_score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 1765 | 1.9969 | 3.364 | 3.361 | 0.5936 | 1.6831 | 0.2212 | 6.7117 |
| 0 | 1392 | 4.8458 | 1.359 | 1.3554 | 3.5657 | 0.2797 | 2.7863 | 6.5682 |
| 0 | 983 | 2.5322 | 2.3014 | 2.2959 | 1.1003 | 0.9067 | 0.5771 | 5.8138 |
| 0 | 1165 | 2.6923 | 1.958 | 1.9197 | 1.375 | 0.7131 | 0.8027 | 5.1685 |
| 0 | 1302 | 2.5035 | 1.8668 | 1.8563 | 1.3411 | 0.7415 | 0.7701 | 4.6471 |
| 0 | 1702 | 5.3734 | 0.86 | 0.8522 | 6.248 | 0.1586 | 5.3928 | 4.5789 |
| 0 | 550 | 2.7805 | 1.6339 | 1.6327 | 1.7018 | 0.5872 | 1.0722 | 4.5398 |
| 1 | 283 | 1.6804 | 2.1871 | 2.1829 | 0.7683 | 1.2991 | 0.3342 | 3.6681 |

## Strongest Selectivity Comparisons

| relation | metric | family_a | family_b | mean_diff | ci_low | ci_high | sign_test_pvalue | num_pairs |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| official_language | target_selectivity | qa | raw_question | 0.208 | 0.1098 | 0.3074 | 0.0039 | 18 |
| official_language | target_selectivity | declarative | raw_question | 0.2065 | 0.0944 | 0.3259 | 0.0215 | 18 |
| currency | target_selectivity | chat_template | raw_question | 0.1796 | 0.0166 | 0.3297 | 0.146 | 18 |
| capital | target_selectivity | chat_template | declarative | -0.1705 | -0.3861 | 0.0462 | 1.0 | 18 |
| currency | target_selectivity | qa | raw_question | 0.1664 | 0.0222 | 0.3152 | 0.0654 | 18 |
| capital | target_selectivity | chat_template | qa | -0.1599 | -0.3698 | 0.0617 | 0.7744 | 18 |
| official_language | target_selectivity | chat_template | qa | -0.1099 | -0.3114 | 0.0778 | 1.0 | 18 |
| official_language | target_selectivity | chat_template | declarative | -0.1083 | -0.3167 | 0.0694 | 1.0 | 18 |

## Neuron Ablation Summary

| candidate_type | prompt_family | answer_f1_drop | contains_drop | target_selectivity_drop | same_subject_control_f1_increase | same_relation_control_f1_increase | lexical_distractor_f1_increase | max_control_f1_increase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| invariant | chat_template | -0.115 | -0.35 | -0.0034 | 0.0 | -0.0159 | 0.1275 | 0.1116 |
| invariant | declarative | 0.025 | 0.0 | 0.0279 | 0.0 | -0.002 | 0.005 | 0.0029 |
| invariant | qa | 0.05 | 0.05 | 0.0222 | 0.0 | 0.0 | -0.0278 | -0.0278 |
| invariant | raw_question | 0.091 | 0.15 | 0.0987 | 0.0 | -0.0333 | 0.0411 | 0.0078 |
| prompt_sensitive | chat_template | 0.2033 | 0.15 | 0.1617 | 0.0 | -0.025 | -0.0167 | -0.0417 |
| prompt_sensitive | declarative | 0.0185 | 0.05 | 0.0157 | 0.0 | -0.0111 | 0.0083 | -0.0028 |
| prompt_sensitive | qa | 0.1093 | 0.2 | 0.0475 | 0.0 | -0.0091 | -0.0528 | -0.0619 |
| prompt_sensitive | raw_question | 0.1854 | 0.3 | 0.0771 | 0.0 | -0.0233 | -0.085 | -0.1083 |