# Prompt Invariance Report: gemma_270m_it

- Prompts analyzed: 160
- Mean answer F1: 0.2378
- Best prompt family by answer F1: raw_question

## Family Summary

| relation | prompt_family | target_rank | target_margin | full_exact_match | contains_expected | answer_f1 | answer_similarity |
| --- | --- | --- | --- | --- | --- | --- | --- |
| birth_place | chat_template | 5605.25 | -15.8438 | 0.25 | 0.25 | 0.25 | 0.5182 |
| birth_place | declarative | 13.0 | -3.2266 | 0.0 | 0.375 | 0.1631 | 0.311 |
| birth_place | qa | 62.0 | -6.7109 | 0.125 | 0.375 | 0.2708 | 0.3837 |
| birth_place | raw_question | 595.625 | -15.0 | 0.0 | 0.5 | 0.3403 | 0.4251 |
| capital | chat_template | 1647.375 | -9.7891 | 0.375 | 0.375 | 0.375 | 0.6388 |
| capital | declarative | 12.875 | 2.4531 | 0.0 | 0.625 | 0.2153 | 0.3167 |
| capital | qa | 5.5 | 0.4844 | 0.0 | 0.5 | 0.2097 | 0.4279 |
| capital | raw_question | 33.0 | -10.3906 | 0.125 | 0.5 | 0.3417 | 0.5931 |
| currency | chat_template | 5856.5 | -12.4653 | 0.0 | 0.0 | 0.1 | 0.465 |
| currency | declarative | 210.25 | -7.9844 | 0.0 | 0.25 | 0.2798 | 0.4103 |
| currency | qa | 253.375 | -3.7266 | 0.0 | 0.25 | 0.1938 | 0.3656 |
| currency | raw_question | 1849.75 | -12.1719 | 0.0 | 0.125 | 0.2 | 0.4023 |
| headquarters | chat_template | 9385.875 | -16.5391 | 0.125 | 0.125 | 0.2708 | 0.5138 |
| headquarters | declarative | 172.0 | -1.9844 | 0.0 | 0.5 | 0.3057 | 0.4594 |
| headquarters | qa | 207.375 | -6.8164 | 0.0 | 0.5 | 0.3326 | 0.4657 |
| headquarters | raw_question | 1932.875 | -14.5898 | 0.0 | 0.25 | 0.175 | 0.337 |
| official_language | chat_template | 566.5 | -11.5352 | 0.25 | 0.25 | 0.25 | 0.7161 |
| official_language | declarative | 3073.0 | -10.4102 | 0.0 | 0.125 | 0.025 | 0.1421 |
| official_language | qa | 35.0 | -3.6484 | 0.0 | 0.375 | 0.075 | 0.1881 |
| official_language | raw_question | 216.25 | -11.2148 | 0.0 | 0.75 | 0.3833 | 0.5525 |

## Top Invariant Neurons

| layer | neuron | mean_abs_activation | activation_std | family_mean_std | sharedness | family_sensitivity | invariance_score | prompt_sensitive_score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4 | 1713 | 0.1685 | 0.002 | 0.001 | 82.901 | 0.006 | 82.408 | 0.0002 |
| 5 | 1392 | 0.1684 | 0.0024 | 0.001 | 71.3621 | 0.0058 | 70.951 | 0.0002 |
| 5 | 885 | 0.1672 | 0.0028 | 0.0012 | 59.0136 | 0.0073 | 58.5877 | 0.0002 |
| 8 | 159 | 0.167 | 0.0029 | 0.0011 | 58.5171 | 0.0065 | 58.1398 | 0.0002 |
| 2 | 938 | 0.1669 | 0.0029 | 0.0014 | 57.3927 | 0.0084 | 56.9167 | 0.0002 |
| 5 | 501 | 0.1677 | 0.0029 | 0.0024 | 57.0945 | 0.014 | 56.3044 | 0.0004 |
| 4 | 933 | 0.1683 | 0.003 | 0.0017 | 56.1584 | 0.01 | 55.6032 | 0.0003 |
| 5 | 203 | 0.1662 | 0.003 | 0.0023 | 56.0547 | 0.0139 | 55.286 | 0.0004 |

## Top Prompt-Sensitive Neurons

| layer | neuron | mean_abs_activation | activation_std | family_mean_std | sharedness | family_sensitivity | invariance_score | prompt_sensitive_score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 1765 | 1.9944 | 3.3594 | 3.3565 | 0.5937 | 1.683 | 0.2213 | 6.6941 |
| 0 | 1392 | 4.843 | 1.3591 | 1.3556 | 3.5635 | 0.2799 | 2.7842 | 6.565 |
| 0 | 983 | 2.5332 | 2.3 | 2.2945 | 1.1014 | 0.9058 | 0.5779 | 5.8125 |
| 0 | 1165 | 2.6969 | 1.9557 | 1.9162 | 1.379 | 0.7105 | 0.8062 | 5.1679 |
| 0 | 1302 | 2.5031 | 1.8663 | 1.8559 | 1.3412 | 0.7414 | 0.7702 | 4.6456 |
| 0 | 1702 | 5.3758 | 0.8585 | 0.8504 | 6.2615 | 0.1582 | 5.4063 | 4.5718 |
| 0 | 550 | 2.7795 | 1.6325 | 1.6313 | 1.7026 | 0.5869 | 1.0729 | 4.5343 |
| 1 | 283 | 1.6855 | 2.1891 | 2.1847 | 0.77 | 1.2962 | 0.3353 | 3.6824 |

## Neuron Ablation Summary

| candidate_type | prompt_family | answer_f1_drop | contains_drop |
| --- | --- | --- | --- |
| invariant | chat_template | -0.0767 | -0.3 |
| invariant | declarative | 0.043 | 0.2 |
| invariant | qa | 0.081 | 0.2 |
| invariant | raw_question | 0.2133 | 0.4 |
| prompt_sensitive | chat_template | 0.34 | 0.3 |
| prompt_sensitive | declarative | -0.0222 | 0.1 |
| prompt_sensitive | qa | 0.0189 | 0.0 |
| prompt_sensitive | raw_question | 0.1233 | 0.3 |