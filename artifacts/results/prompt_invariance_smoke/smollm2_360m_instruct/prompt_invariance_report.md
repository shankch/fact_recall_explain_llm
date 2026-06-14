# Prompt Invariance Report: smollm2_360m_instruct

- Prompts analyzed: 80
- Mean answer F1: 0.1401
- Best prompt family by answer F1: chat_template

## Family Summary

| relation | prompt_family | target_rank | target_margin | full_exact_match | contains_expected | answer_f1 | answer_similarity |
| --- | --- | --- | --- | --- | --- | --- | --- |
| birth_place | chat_template | 2485.25 | -13.7388 | 0.5 | 0.75 | 0.6667 | 0.65 |
| birth_place | declarative | 19.0 | -2.0781 | 0.0 | 0.0 | 0.05 | 0.2021 |
| birth_place | qa | 997.5 | -9.8125 | 0.0 | 0.0 | 0.0 | 0.0 |
| birth_place | raw_question | 986.0 | -11.6562 | 0.0 | 0.0 | 0.0 | 0.0 |
| capital | chat_template | 151.0 | -6.0469 | 0.25 | 0.25 | 0.4167 | 0.7644 |
| capital | declarative | 4.0 | 2.7188 | 0.0 | 0.5 | 0.1181 | 0.2978 |
| capital | qa | 262.75 | -9.7344 | 0.0 | 0.0 | 0.0 | 0.0 |
| capital | raw_question | 9182.5 | -14.1914 | 0.0 | 0.0 | 0.0 | 0.0 |
| currency | chat_template | 307.0 | -8.5117 | 0.0 | 0.0 | 0.2054 | 0.409 |
| currency | declarative | 23.25 | -5.8125 | 0.0 | 0.25 | 0.1806 | 0.2531 |
| currency | qa | 1767.25 | -11.6484 | 0.0 | 0.0 | 0.0 | 0.0 |
| currency | raw_question | 10232.25 | -17.9683 | 0.0 | 0.0 | 0.0 | 0.0 |
| headquarters | chat_template | 4051.75 | -12.5635 | 0.0 | 0.75 | 0.3464 | 0.4216 |
| headquarters | declarative | 1.0 | 1.3906 | 0.0 | 0.75 | 0.6732 | 0.7932 |
| headquarters | qa | 701.25 | -10.4922 | 0.0 | 0.0 | 0.0 | 0.0 |
| headquarters | raw_question | 1697.5 | -13.3633 | 0.0 | 0.0 | 0.0 | 0.0 |
| official_language | chat_template | 144.75 | -6.5469 | 0.0 | 0.25 | 0.0833 | 0.2247 |
| official_language | declarative | 1.5 | 1.0781 | 0.0 | 0.25 | 0.0625 | 0.2131 |
| official_language | qa | 499.0 | -10.5781 | 0.0 | 0.0 | 0.0 | 0.0 |
| official_language | raw_question | 4289.75 | -14.8838 | 0.0 | 0.0 | 0.0 | 0.0778 |

## Top Invariant Neurons

| layer | neuron | mean_abs_activation | activation_std | family_mean_std | sharedness | family_sensitivity | invariance_score | prompt_sensitive_score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 538 | 0.2772 | 0.0026 | 0.0012 | 107.857 | 0.0043 | 107.3963 | 0.0003 |
| 13 | 1014 | 0.2766 | 0.0027 | 0.0009 | 101.7911 | 0.0034 | 101.449 | 0.0003 |
| 18 | 1865 | 0.2764 | 0.0028 | 0.0012 | 97.622 | 0.0044 | 97.1977 | 0.0003 |
| 14 | 1185 | 0.2759 | 0.0031 | 0.0016 | 88.6433 | 0.0057 | 88.1417 | 0.0004 |
| 12 | 2285 | 0.2749 | 0.0035 | 0.001 | 79.4385 | 0.0037 | 79.147 | 0.0003 |
| 12 | 595 | 0.2756 | 0.0037 | 0.0019 | 74.2896 | 0.007 | 73.7745 | 0.0005 |
| 18 | 73 | 0.2733 | 0.0039 | 0.0025 | 70.4206 | 0.0091 | 69.7857 | 0.0007 |
| 6 | 156 | 0.2732 | 0.0039 | 0.0029 | 69.3217 | 0.0107 | 68.5862 | 0.0008 |

## Top Prompt-Sensitive Neurons

| layer | neuron | mean_abs_activation | activation_std | family_mean_std | sharedness | family_sensitivity | invariance_score | prompt_sensitive_score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 31 | 2496 | 13.2312 | 2.1405 | 1.8955 | 6.1815 | 0.1433 | 5.4069 | 25.0797 |
| 31 | 2464 | 12.2938 | 1.9821 | 1.7566 | 6.2025 | 0.1429 | 5.4271 | 21.5954 |
| 31 | 1620 | 11.309 | 2.0795 | 1.8834 | 5.4382 | 0.1665 | 4.6619 | 21.2988 |
| 31 | 1777 | 5.6159 | 3.5808 | 3.4411 | 1.5683 | 0.6127 | 0.9725 | 19.3251 |
| 31 | 2301 | 11.7477 | 1.9126 | 1.6285 | 6.1424 | 0.1386 | 5.3946 | 19.1314 |
| 31 | 2169 | 11.6633 | 1.8794 | 1.5906 | 6.206 | 0.1364 | 5.4612 | 18.5514 |
| 31 | 2276 | 13.0914 | 1.6474 | 1.4163 | 7.9467 | 0.1082 | 7.1709 | 18.5418 |
| 31 | 1767 | 12.2445 | 1.7414 | 1.5042 | 7.0312 | 0.1229 | 6.262 | 18.4187 |

## Neuron Ablation Summary

| candidate_type | prompt_family | answer_f1_drop | contains_drop |
| --- | --- | --- | --- |
| invariant | chat_template | 0.0 | 0.0 |
| invariant | declarative | 0.01 | 0.0 |
| invariant | qa | 0.0 | 0.0 |
| invariant | raw_question | 0.0 | 0.0 |
| prompt_sensitive | chat_template | 0.0 | -0.2 |
| prompt_sensitive | declarative | 0.0065 | -0.2 |
| prompt_sensitive | qa | -0.12 | -0.2 |
| prompt_sensitive | raw_question | 0.0 | 0.0 |