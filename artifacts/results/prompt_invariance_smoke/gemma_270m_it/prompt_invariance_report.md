# Prompt Invariance Report: gemma_270m_it

- Prompts analyzed: 80
- Mean answer F1: 0.2167
- Best prompt family by answer F1: raw_question

## Family Summary

| relation | prompt_family | target_rank | target_margin | full_exact_match | contains_expected | answer_f1 | answer_similarity |
| --- | --- | --- | --- | --- | --- | --- | --- |
| birth_place | chat_template | 10546.5 | -18.0859 | 0.25 | 0.25 | 0.25 | 0.5064 |
| birth_place | declarative | 18.75 | -3.8125 | 0.0 | 0.25 | 0.1429 | 0.347 |
| birth_place | qa | 44.25 | -7.2969 | 0.25 | 0.5 | 0.375 | 0.4746 |
| birth_place | raw_question | 479.0 | -14.7344 | 0.0 | 0.5 | 0.3472 | 0.4665 |
| capital | chat_template | 1630.0 | -8.2188 | 0.25 | 0.25 | 0.25 | 0.6311 |
| capital | declarative | 1.0 | 3.7188 | 0.0 | 0.5 | 0.2125 | 0.3465 |
| capital | qa | 2.25 | 1.5312 | 0.0 | 0.25 | 0.0972 | 0.4056 |
| capital | raw_question | 28.25 | -9.8438 | 0.0 | 0.25 | 0.1667 | 0.5455 |
| currency | chat_template | 195.5 | -8.5156 | 0.0 | 0.0 | 0.0 | 0.3338 |
| currency | declarative | 111.75 | -7.9219 | 0.0 | 0.25 | 0.2381 | 0.3516 |
| currency | qa | 427.5 | -4.1406 | 0.0 | 0.25 | 0.2625 | 0.3638 |
| currency | raw_question | 3455.0 | -12.4141 | 0.0 | 0.25 | 0.3 | 0.4812 |
| headquarters | chat_template | 8609.25 | -18.0469 | 0.25 | 0.25 | 0.4167 | 0.5216 |
| headquarters | declarative | 80.75 | -1.2188 | 0.0 | 0.5 | 0.35 | 0.495 |
| headquarters | qa | 229.75 | -7.2109 | 0.0 | 0.5 | 0.3586 | 0.5128 |
| headquarters | raw_question | 1997.25 | -14.3516 | 0.0 | 0.25 | 0.225 | 0.3754 |
| official_language | chat_template | 335.25 | -10.7188 | 0.0 | 0.0 | 0.0 | 0.6655 |
| official_language | declarative | 5436.75 | -12.1172 | 0.0 | 0.0 | 0.0 | 0.1376 |
| official_language | qa | 63.0 | -5.1406 | 0.0 | 0.25 | 0.05 | 0.1799 |
| official_language | raw_question | 400.75 | -12.4922 | 0.0 | 0.5 | 0.2917 | 0.5274 |

## Top Invariant Neurons

| layer | neuron | mean_abs_activation | activation_std | family_mean_std | sharedness | family_sensitivity | invariance_score | prompt_sensitive_score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4 | 1713 | 0.1685 | 0.0021 | 0.0011 | 78.5742 | 0.0065 | 78.0651 | 0.0002 |
| 5 | 885 | 0.1675 | 0.0023 | 0.0012 | 72.6091 | 0.0069 | 72.1124 | 0.0002 |
| 5 | 1392 | 0.1683 | 0.0026 | 0.0011 | 63.7545 | 0.0065 | 63.3402 | 0.0002 |
| 8 | 159 | 0.1671 | 0.0027 | 0.0009 | 61.9155 | 0.0053 | 61.5867 | 0.0001 |
| 2 | 938 | 0.167 | 0.0028 | 0.0014 | 59.6944 | 0.0085 | 59.1933 | 0.0002 |
| 5 | 501 | 0.1678 | 0.0028 | 0.0022 | 59.3401 | 0.0133 | 58.5637 | 0.0004 |
| 5 | 203 | 0.1661 | 0.003 | 0.0022 | 55.4665 | 0.0134 | 54.7327 | 0.0004 |
| 4 | 933 | 0.1683 | 0.0031 | 0.0018 | 54.7662 | 0.0106 | 54.1923 | 0.0003 |

## Top Prompt-Sensitive Neurons

| layer | neuron | mean_abs_activation | activation_std | family_mean_std | sharedness | family_sensitivity | invariance_score | prompt_sensitive_score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 1765 | 1.9994 | 3.3688 | 3.3655 | 0.5935 | 1.6832 | 0.2212 | 6.7291 |
| 0 | 1392 | 4.8549 | 1.3623 | 1.3591 | 3.5638 | 0.2799 | 2.7843 | 6.5983 |
| 0 | 983 | 2.5362 | 2.3038 | 2.298 | 1.1009 | 0.9061 | 0.5776 | 5.8282 |
| 0 | 1165 | 2.6975 | 1.9597 | 1.9203 | 1.3765 | 0.7119 | 0.8041 | 5.18 |
| 0 | 1302 | 2.5034 | 1.8707 | 1.8605 | 1.3382 | 0.7432 | 0.7677 | 4.6575 |
| 0 | 1702 | 5.3795 | 0.8609 | 0.8527 | 6.2489 | 0.1585 | 5.3939 | 4.5873 |
| 0 | 550 | 2.7848 | 1.6354 | 1.6341 | 1.7029 | 0.5868 | 1.0732 | 4.5506 |
| 1 | 283 | 1.686 | 2.1891 | 2.1849 | 0.7702 | 1.2959 | 0.3354 | 3.6837 |

## Neuron Ablation Summary

| candidate_type | prompt_family | answer_f1_drop | contains_drop |
| --- | --- | --- | --- |
| invariant | chat_template | -0.2 | 0.0 |
| invariant | declarative | 0.0473 | 0.2 |
| invariant | qa | 0.0697 | 0.0 |
| invariant | raw_question | -0.0364 | 0.0 |
| prompt_sensitive | chat_template | 0.0 | 0.0 |
| prompt_sensitive | declarative | 0.0 | 0.0 |
| prompt_sensitive | qa | 0.0297 | 0.0 |
| prompt_sensitive | raw_question | -0.1733 | -0.4 |