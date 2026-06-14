# Prompt Invariance Report: gemma_270m_base

- Prompts analyzed: 160
- Mean answer F1: 0.1121
- Best prompt family by answer F1: declarative

## Family Summary

| relation | prompt_family | target_rank | target_margin | full_exact_match | contains_expected | answer_f1 | answer_similarity |
| --- | --- | --- | --- | --- | --- | --- | --- |
| birth_place | chat_template | 731.5 | -5.9531 | 0.0 | 0.0 | 0.0 | 0.1662 |
| birth_place | declarative | 110.875 | -3.2188 | 0.0 | 0.125 | 0.05 | 0.2259 |
| birth_place | qa | 235.375 | -3.6172 | 0.0 | 0.125 | 0.0312 | 0.2094 |
| birth_place | raw_question | 997.75 | -8.6953 | 0.0 | 0.25 | 0.1458 | 0.2142 |
| capital | chat_template | 34.125 | -2.0547 | 0.0 | 0.25 | 0.1639 | 0.3444 |
| capital | declarative | 30.375 | -0.8594 | 0.0 | 0.5 | 0.1468 | 0.2685 |
| capital | qa | 8.25 | -2.1016 | 0.0 | 0.0 | 0.0 | 0.1877 |
| capital | raw_question | 38.875 | -4.7578 | 0.0 | 0.0 | 0.0833 | 0.2508 |
| currency | chat_template | 124.75 | -3.1484 | 0.0 | 0.125 | 0.1833 | 0.4089 |
| currency | declarative | 201.125 | -5.5938 | 0.0 | 0.375 | 0.2397 | 0.3753 |
| currency | qa | 71.5 | -2.8516 | 0.0 | 0.25 | 0.213 | 0.3495 |
| currency | raw_question | 459.625 | -6.8906 | 0.0 | 0.25 | 0.1833 | 0.4191 |
| headquarters | chat_template | 615.875 | -5.5938 | 0.125 | 0.125 | 0.125 | 0.3445 |
| headquarters | declarative | 141.125 | -1.9219 | 0.0 | 0.375 | 0.15 | 0.3623 |
| headquarters | qa | 139.875 | -2.4297 | 0.0 | 0.375 | 0.1895 | 0.3904 |
| headquarters | raw_question | 660.625 | -8.3594 | 0.0 | 0.25 | 0.0556 | 0.2193 |
| official_language | chat_template | 43.125 | -2.3359 | 0.0 | 0.125 | 0.0312 | 0.2121 |
| official_language | declarative | 1.75 | -0.0469 | 0.0 | 0.375 | 0.0806 | 0.2127 |
| official_language | qa | 5.125 | -0.3594 | 0.0 | 0.5 | 0.1111 | 0.2281 |
| official_language | raw_question | 87.25 | -5.7578 | 0.0 | 0.25 | 0.059 | 0.2036 |

## Top Invariant Neurons

| layer | neuron | mean_abs_activation | activation_std | family_mean_std | sharedness | family_sensitivity | invariance_score | prompt_sensitive_score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 10 | 232 | 0.169 | 0.0011 | 0.0002 | 149.8306 | 0.0011 | 149.6588 | 0.0 |
| 5 | 1401 | 0.1679 | 0.0022 | 0.0007 | 76.0318 | 0.0041 | 75.7219 | 0.0001 |
| 9 | 880 | 0.1684 | 0.0023 | 0.0008 | 72.3923 | 0.0048 | 72.0484 | 0.0001 |
| 0 | 1652 | 0.1676 | 0.0026 | 0.0013 | 65.5843 | 0.0078 | 65.077 | 0.0002 |
| 5 | 1457 | 0.1664 | 0.0028 | 0.0007 | 59.6027 | 0.004 | 59.3631 | 0.0001 |
| 9 | 1350 | 0.1679 | 0.0029 | 0.0008 | 57.3662 | 0.0046 | 57.1026 | 0.0001 |
| 16 | 1591 | 0.1679 | 0.003 | 0.001 | 56.8531 | 0.006 | 56.5117 | 0.0002 |
| 5 | 501 | 0.1663 | 0.003 | 0.0023 | 56.1909 | 0.014 | 55.4168 | 0.0004 |

## Top Prompt-Sensitive Neurons

| layer | neuron | mean_abs_activation | activation_std | family_mean_std | sharedness | family_sensitivity | invariance_score | prompt_sensitive_score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 1765 | 1.8416 | 3.0691 | 3.0637 | 0.6001 | 1.6636 | 0.2253 | 5.6423 |
| 0 | 1165 | 2.7387 | 1.7733 | 1.7502 | 1.5444 | 0.6391 | 0.9422 | 4.7933 |
| 15 | 338 | 2.3838 | 1.5461 | 1.5223 | 1.5418 | 0.6386 | 0.9409 | 3.6289 |
| 1 | 283 | 1.8371 | 1.9676 | 1.9653 | 0.9336 | 1.0698 | 0.4511 | 3.6104 |
| 0 | 1392 | 4.1239 | 0.8777 | 0.8689 | 4.6985 | 0.2107 | 3.8808 | 3.5834 |
| 0 | 1702 | 4.8743 | 0.6682 | 0.6575 | 7.295 | 0.1349 | 6.4279 | 3.205 |
| 15 | 783 | 2.0913 | 1.2918 | 1.2782 | 1.6189 | 0.6112 | 1.0048 | 2.6731 |
| 6 | 725 | 1.2647 | 2.0461 | 2.0105 | 0.6181 | 1.5898 | 0.2387 | 2.5426 |

## Neuron Ablation Summary

| candidate_type | prompt_family | answer_f1_drop | contains_drop |
| --- | --- | --- | --- |
| invariant | chat_template | 0.08 | 0.1 |
| invariant | declarative | -0.0208 | -0.1 |
| invariant | qa | -0.04 | 0.0 |
| invariant | raw_question | 0.0 | 0.0 |
| prompt_sensitive | chat_template | 0.105 | 0.2 |
| prompt_sensitive | declarative | -0.0067 | 0.0 |
| prompt_sensitive | qa | -0.0772 | 0.0 |
| prompt_sensitive | raw_question | 0.0617 | 0.2 |