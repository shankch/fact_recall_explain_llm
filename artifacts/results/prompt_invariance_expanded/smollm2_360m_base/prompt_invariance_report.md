# Prompt Invariance Report: smollm2_360m_base

- Prompts analyzed: 160
- Mean answer F1: 0.2870
- Best prompt family by answer F1: qa

## Family Summary

| relation | prompt_family | target_rank | target_margin | full_exact_match | contains_expected | answer_f1 | answer_similarity |
| --- | --- | --- | --- | --- | --- | --- | --- |
| birth_place | chat_template | 88.625 | -3.1484 | 0.0 | 0.0 | 0.0 | 0.1714 |
| birth_place | declarative | 14.125 | -1.6797 | 0.0 | 0.25 | 0.1464 | 0.2862 |
| birth_place | qa | 37.375 | -2.7188 | 0.0 | 0.5 | 0.2431 | 0.3666 |
| birth_place | raw_question | 480.0 | -9.3594 | 0.25 | 0.25 | 0.25 | 0.3224 |
| capital | chat_template | 5.0 | -0.3203 | 0.125 | 0.375 | 0.2798 | 0.4817 |
| capital | declarative | 1.25 | 1.4688 | 0.0 | 0.75 | 0.3021 | 0.374 |
| capital | qa | 1.125 | 2.7188 | 0.0 | 0.625 | 0.3036 | 0.4734 |
| capital | raw_question | 20.375 | -5.3672 | 0.125 | 0.625 | 0.3536 | 0.4718 |
| currency | chat_template | 56.25 | -1.9375 | 0.0 | 0.375 | 0.4792 | 0.6071 |
| currency | declarative | 6.5 | -4.6641 | 0.0 | 0.5 | 0.3857 | 0.5062 |
| currency | qa | 30.625 | -3.1172 | 0.0 | 0.375 | 0.5083 | 0.6466 |
| currency | raw_question | 168.875 | -8.1719 | 0.0 | 0.0 | 0.275 | 0.5081 |
| headquarters | chat_template | 389.125 | -4.0781 | 0.0 | 0.5 | 0.2857 | 0.4371 |
| headquarters | declarative | 190.625 | -0.9062 | 0.0 | 0.625 | 0.4911 | 0.6083 |
| headquarters | qa | 382.25 | -5.75 | 0.25 | 0.625 | 0.5333 | 0.5736 |
| headquarters | raw_question | 885.625 | -9.9922 | 0.125 | 0.5 | 0.3377 | 0.4212 |
| official_language | chat_template | 2.375 | 0.2422 | 0.0 | 0.375 | 0.1312 | 0.3305 |
| official_language | declarative | 1.0 | 1.5391 | 0.0 | 0.625 | 0.1821 | 0.3347 |
| official_language | qa | 1.375 | 0.5312 | 0.0 | 0.625 | 0.1589 | 0.2886 |
| official_language | raw_question | 18.0 | -5.9531 | 0.0 | 0.375 | 0.0938 | 0.2352 |

## Top Invariant Neurons

| layer | neuron | mean_abs_activation | activation_std | family_mean_std | sharedness | family_sensitivity | invariance_score | prompt_sensitive_score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 6 | 156 | 0.2756 | 0.0029 | 0.0024 | 94.6444 | 0.0088 | 93.8226 | 0.0007 |
| 12 | 490 | 0.2752 | 0.0034 | 0.0015 | 79.7428 | 0.0056 | 79.302 | 0.0004 |
| 17 | 2550 | 0.276 | 0.0036 | 0.0011 | 76.2182 | 0.004 | 75.9111 | 0.0003 |
| 2 | 1170 | 0.2756 | 0.0037 | 0.0014 | 74.6976 | 0.0052 | 74.3132 | 0.0004 |
| 14 | 449 | 0.2745 | 0.0037 | 0.002 | 73.7199 | 0.0074 | 73.1819 | 0.0006 |
| 8 | 2286 | 0.2753 | 0.004 | 0.0008 | 68.0793 | 0.003 | 67.8763 | 0.0002 |
| 17 | 29 | 0.2739 | 0.0042 | 0.0036 | 65.7544 | 0.013 | 64.9129 | 0.001 |
| 1 | 538 | 0.2745 | 0.0042 | 0.0034 | 65.6479 | 0.0123 | 64.8475 | 0.0009 |

## Top Prompt-Sensitive Neurons

| layer | neuron | mean_abs_activation | activation_std | family_mean_std | sharedness | family_sensitivity | invariance_score | prompt_sensitive_score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 31 | 1777 | 10.3449 | 2.4804 | 2.1551 | 4.1707 | 0.2083 | 3.4516 | 22.2944 |
| 31 | 1034 | 16.3906 | 1.4912 | 1.1514 | 10.9913 | 0.0703 | 10.2699 | 18.8729 |
| 31 | 2064 | 16.1461 | 1.6435 | 1.1568 | 9.8242 | 0.0716 | 9.1674 | 18.6778 |
| 31 | 2464 | 15.4945 | 1.5214 | 1.1747 | 10.1845 | 0.0758 | 9.4668 | 18.2007 |
| 31 | 446 | 16.7039 | 1.4628 | 1.0782 | 11.4193 | 0.0645 | 10.7269 | 18.0103 |
| 31 | 2169 | 15.3074 | 1.5471 | 1.1565 | 9.8941 | 0.0755 | 9.1991 | 17.7025 |
| 31 | 2276 | 16.6699 | 1.3985 | 1.0589 | 11.9195 | 0.0635 | 11.2076 | 17.651 |
| 31 | 2496 | 17.3312 | 1.4 | 1.0134 | 12.3796 | 0.0585 | 11.6957 | 17.5643 |

## Neuron Ablation Summary

| candidate_type | prompt_family | answer_f1_drop | contains_drop |
| --- | --- | --- | --- |
| invariant | chat_template | -0.0012 | 0.0 |
| invariant | declarative | 0.0 | 0.0 |
| invariant | qa | -0.0267 | -0.1 |
| invariant | raw_question | -0.0267 | 0.0 |
| prompt_sensitive | chat_template | 0.1308 | 0.0 |
| prompt_sensitive | declarative | -0.0054 | -0.1 |
| prompt_sensitive | qa | 0.0486 | 0.1 |
| prompt_sensitive | raw_question | 0.0071 | 0.0 |