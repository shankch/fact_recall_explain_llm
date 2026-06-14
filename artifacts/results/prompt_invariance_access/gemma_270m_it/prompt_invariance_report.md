# Prompt Invariance Report: gemma_270m_it

- Prompts analyzed: 240
- Mean answer F1: 0.2238
- Best prompt family by answer F1: raw_question

## Family Summary

| relation | prompt_family | target_rank | target_margin | full_exact_match | contains_expected | answer_f1 | answer_similarity |
| --- | --- | --- | --- | --- | --- | --- | --- |
| birth_place | chat_template | 8070.5833 | -18.8268 | 0.1667 | 0.1667 | 0.1667 | 0.4144 |
| birth_place | declarative | 128.5 | -4.8073 | 0.0 | 0.25 | 0.1325 | 0.3183 |
| birth_place | qa | 1452.0 | -7.584 | 0.0833 | 0.25 | 0.1806 | 0.3015 |
| birth_place | raw_question | 5367.8333 | -15.7383 | 0.0 | 0.3333 | 0.2602 | 0.4036 |
| capital | chat_template | 1102.25 | -8.5365 | 0.4167 | 0.4167 | 0.4167 | 0.6438 |
| capital | declarative | 8.9167 | 3.1979 | 0.0 | 0.75 | 0.2245 | 0.2945 |
| capital | qa | 4.0 | 0.7292 | 0.0 | 0.6667 | 0.2509 | 0.4219 |
| capital | raw_question | 33.9167 | -10.2708 | 0.0833 | 0.5833 | 0.3375 | 0.5361 |
| currency | chat_template | 4073.5 | -12.2425 | 0.0 | 0.0 | 0.1083 | 0.5077 |
| currency | declarative | 152.5833 | -7.5156 | 0.0 | 0.25 | 0.2659 | 0.4216 |
| currency | qa | 195.6667 | -3.3333 | 0.0 | 0.25 | 0.1708 | 0.4084 |
| currency | raw_question | 1853.8333 | -12.0026 | 0.0 | 0.1667 | 0.2667 | 0.4685 |
| headquarters | chat_template | 6361.8333 | -15.5885 | 0.1667 | 0.1667 | 0.3194 | 0.553 |
| headquarters | declarative | 117.0833 | -1.625 | 0.0 | 0.5 | 0.2408 | 0.3891 |
| headquarters | qa | 147.9167 | -5.7839 | 0.0 | 0.5 | 0.2819 | 0.3942 |
| headquarters | raw_question | 1382.75 | -13.2995 | 0.0 | 0.3333 | 0.1798 | 0.3145 |
| official_language | chat_template | 753.6667 | -11.6732 | 0.25 | 0.25 | 0.25 | 0.652 |
| official_language | declarative | 2310.5 | -9.9818 | 0.0 | 0.1667 | 0.0333 | 0.154 |
| official_language | qa | 26.3333 | -3.3281 | 0.0 | 0.25 | 0.05 | 0.1833 |
| official_language | raw_question | 161.5833 | -10.9714 | 0.0 | 0.6667 | 0.3389 | 0.5544 |

## Control Selectivity Summary

| prompt_family | answer_f1 | target_selectivity | same_subject_control_f1 | same_relation_control_f1 | lexical_distractor_f1 | max_control_f1 |
| --- | --- | --- | --- | --- | --- | --- |
| chat_template | 0.2522 | 0.1956 | 0.0067 | 0.0167 | 0.05 | 0.0567 |
| declarative | 0.1794 | 0.1716 | 0.0 | 0.0042 | 0.0079 | 0.0079 |
| qa | 0.1868 | 0.1798 | 0.0 | 0.0037 | 0.007 | 0.007 |
| raw_question | 0.2766 | 0.2447 | 0.0 | 0.0153 | 0.0208 | 0.0319 |

## Top Invariant Neurons

| layer | neuron | mean_abs_activation | activation_std | family_mean_std | sharedness | family_sensitivity | invariance_score | prompt_sensitive_score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4 | 1713 | 0.1685 | 0.002 | 0.001 | 84.0979 | 0.006 | 83.5956 | 0.0002 |
| 5 | 1392 | 0.1684 | 0.0023 | 0.001 | 72.7489 | 0.0058 | 72.3325 | 0.0002 |
| 5 | 885 | 0.1673 | 0.0028 | 0.0012 | 60.5812 | 0.0072 | 60.1471 | 0.0002 |
| 8 | 159 | 0.167 | 0.0028 | 0.0011 | 59.4229 | 0.0065 | 59.0396 | 0.0002 |
| 2 | 938 | 0.167 | 0.0028 | 0.0014 | 58.7211 | 0.0083 | 58.2354 | 0.0002 |
| 4 | 933 | 0.1683 | 0.0029 | 0.0016 | 57.6864 | 0.0097 | 57.1341 | 0.0003 |
| 5 | 501 | 0.1677 | 0.0029 | 0.0024 | 56.885 | 0.0142 | 56.0869 | 0.0004 |
| 5 | 203 | 0.1663 | 0.003 | 0.0023 | 56.2786 | 0.0141 | 55.497 | 0.0004 |

## Top Prompt-Sensitive Neurons

| layer | neuron | mean_abs_activation | activation_std | family_mean_std | sharedness | family_sensitivity | invariance_score | prompt_sensitive_score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 1765 | 1.9948 | 3.3601 | 3.3571 | 0.5937 | 1.683 | 0.2213 | 6.6967 |
| 0 | 1392 | 4.8443 | 1.3596 | 1.3561 | 3.5631 | 0.2799 | 2.7838 | 6.5693 |
| 0 | 983 | 2.533 | 2.301 | 2.2956 | 1.1008 | 0.9063 | 0.5775 | 5.8146 |
| 0 | 1165 | 2.6954 | 1.9567 | 1.9177 | 1.3775 | 0.7115 | 0.8049 | 5.169 |
| 0 | 1302 | 2.5041 | 1.8666 | 1.8562 | 1.3415 | 0.7413 | 0.7704 | 4.6481 |
| 0 | 1702 | 5.3759 | 0.8587 | 0.8507 | 6.2605 | 0.1582 | 5.4051 | 4.5734 |
| 0 | 550 | 2.7802 | 1.6332 | 1.632 | 1.7023 | 0.587 | 1.0727 | 4.5374 |
| 1 | 283 | 1.6828 | 2.1883 | 2.1841 | 0.769 | 1.2979 | 0.3347 | 3.6755 |

## Strongest Selectivity Comparisons

| relation | metric | family_a | family_b | mean_diff | ci_low | ci_high | sign_test_pvalue | num_pairs |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| official_language | target_selectivity | declarative | raw_question | 0.2222 | 0.0748 | 0.3778 | 0.125 | 12 |
| official_language | target_selectivity | qa | raw_question | 0.2222 | 0.0944 | 0.3503 | 0.0312 | 12 |
| official_language | target_selectivity | chat_template | raw_question | 0.2056 | 0.0 | 0.3778 | 0.125 | 12 |
| capital | target_selectivity | chat_template | declarative | -0.1921 | -0.4422 | 0.062 | 1.0 | 12 |
| capital | target_selectivity | chat_template | qa | -0.1657 | -0.44 | 0.1296 | 1.0 | 12 |
| currency | target_selectivity | chat_template | raw_question | 0.1583 | -0.0419 | 0.3421 | 0.2891 | 12 |
| currency | target_selectivity | chat_template | declarative | 0.1575 | 0.0546 | 0.2497 | 0.1094 | 12 |
| capital | target_selectivity | declarative | raw_question | 0.113 | -0.09 | 0.2849 | 0.1797 | 12 |

## Neuron Ablation Summary

| candidate_type | prompt_family | answer_f1_drop | contains_drop | target_selectivity_drop | same_subject_control_f1_increase | same_relation_control_f1_increase | lexical_distractor_f1_increase | max_control_f1_increase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| invariant | chat_template | -0.1592 | -0.4 | -0.0177 | 0.0 | 0.0 | 0.1415 | 0.1415 |
| invariant | declarative | 0.0372 | 0.0667 | 0.0372 | 0.0 | 0.0 | 0.0 | 0.0 |
| invariant | qa | -0.0042 | 0.0 | 0.0124 | 0.0 | 0.0 | 0.0167 | 0.0167 |
| invariant | raw_question | 0.0773 | 0.1333 | 0.1143 | 0.0 | -0.0444 | 0.0815 | 0.037 |
| prompt_sensitive | chat_template | 0.1111 | 0.0667 | 0.1111 | 0.0 | 0.0 | 0.0 | 0.0 |
| prompt_sensitive | declarative | -0.0159 | 0.0 | -0.0085 | 0.0 | 0.0 | 0.0074 | 0.0074 |
| prompt_sensitive | qa | 0.0796 | 0.2 | 0.0796 | 0.0 | 0.0 | 0.0 | 0.0 |
| prompt_sensitive | raw_question | 0.1105 | 0.2 | 0.0661 | 0.0 | -0.0444 | 0.0 | -0.0444 |