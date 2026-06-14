# Prompt Invariance Report: qwen2_5_0_5b_instruct

- Prompts analyzed: 240
- Mean answer F1: 0.2393
- Best prompt family by answer F1: chat_template

## Family Summary

| relation | prompt_family | target_rank | target_margin | full_exact_match | contains_expected | answer_f1 | answer_similarity |
| --- | --- | --- | --- | --- | --- | --- | --- |
| birth_place | chat_template | 3398.9167 | -10.2633 | 0.0833 | 0.0833 | 0.0833 | 0.3442 |
| birth_place | declarative | 70.75 | -3.0339 | 0.0 | 0.1667 | 0.1138 | 0.2839 |
| birth_place | qa | 361.1667 | -4.5742 | 0.0 | 0.0833 | 0.0537 | 0.2539 |
| birth_place | raw_question | 2049.6667 | -10.1198 | 0.0 | 0.0 | 0.0 | 0.2288 |
| capital | chat_template | 19.0 | -3.4844 | 0.6667 | 0.6667 | 0.7222 | 0.8621 |
| capital | declarative | 8.5833 | -1.4792 | 0.0 | 0.4167 | 0.1212 | 0.2704 |
| capital | qa | 1.3333 | 1.9896 | 0.0 | 0.75 | 0.2141 | 0.2896 |
| capital | raw_question | 12.8333 | -3.349 | 0.0 | 0.75 | 0.3653 | 0.5497 |
| currency | chat_template | 172.1667 | -6.1432 | 0.0833 | 0.25 | 0.3847 | 0.681 |
| currency | declarative | 163.4167 | -7.0156 | 0.0 | 0.3333 | 0.2293 | 0.3611 |
| currency | qa | 13.9167 | -2.1094 | 0.0 | 0.25 | 0.2633 | 0.4416 |
| currency | raw_question | 296.5 | -5.4974 | 0.0 | 0.3333 | 0.3192 | 0.4747 |
| headquarters | chat_template | 1052.8333 | -7.2552 | 0.3333 | 0.4167 | 0.4583 | 0.6115 |
| headquarters | declarative | 50.6667 | -2.6797 | 0.0 | 0.25 | 0.118 | 0.2727 |
| headquarters | qa | 50.3333 | -2.8958 | 0.0 | 0.6667 | 0.252 | 0.3108 |
| headquarters | raw_question | 916.8333 | -7.7826 | 0.0 | 0.6667 | 0.224 | 0.293 |
| official_language | chat_template | 35.0 | -6.2865 | 0.3333 | 0.4167 | 0.375 | 0.6409 |
| official_language | declarative | 10.3333 | -1.2656 | 0.0 | 0.75 | 0.2393 | 0.3858 |
| official_language | qa | 1.0833 | 2.401 | 0.0 | 0.6667 | 0.1435 | 0.256 |
| official_language | raw_question | 34.4167 | -4.4062 | 0.0 | 0.5 | 0.106 | 0.229 |

## Control Selectivity Summary

| prompt_family | answer_f1 | target_selectivity | same_subject_control_f1 | same_relation_control_f1 | lexical_distractor_f1 | max_control_f1 |
| --- | --- | --- | --- | --- | --- | --- |
| chat_template | 0.4047 | 0.3297 | 0.0 | 0.0083 | 0.075 | 0.075 |
| declarative | 0.1643 | 0.1529 | 0.0 | 0.0 | 0.0114 | 0.0114 |
| qa | 0.1853 | 0.1663 | 0.0 | 0.0079 | 0.0149 | 0.0191 |
| raw_question | 0.2029 | 0.1755 | 0.0 | 0.0074 | 0.0237 | 0.0274 |

## Top Invariant Neurons

| layer | neuron | mean_abs_activation | activation_std | family_mean_std | sharedness | family_sensitivity | invariance_score | prompt_sensitive_score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 8 | 4766 | 0.2779 | 0.0011 | 0.0003 | 263.0829 | 0.001 | 262.8131 | 0.0001 |
| 9 | 2112 | 0.277 | 0.0017 | 0.0007 | 158.6916 | 0.0025 | 158.2984 | 0.0002 |
| 12 | 4708 | 0.2765 | 0.0018 | 0.0004 | 155.7274 | 0.0014 | 155.5054 | 0.0001 |
| 0 | 308 | 0.2752 | 0.0022 | 0.0016 | 122.8402 | 0.0059 | 122.1236 | 0.0004 |
| 15 | 443 | 0.276 | 0.0024 | 0.0004 | 113.1378 | 0.0014 | 112.985 | 0.0001 |
| 15 | 1024 | 0.2763 | 0.0026 | 0.001 | 106.6112 | 0.0036 | 106.2269 | 0.0003 |
| 7 | 3747 | 0.2764 | 0.0027 | 0.0014 | 103.7029 | 0.005 | 103.1907 | 0.0004 |
| 13 | 41 | 0.2768 | 0.0029 | 0.0014 | 94.3193 | 0.005 | 93.85 | 0.0004 |

## Top Prompt-Sensitive Neurons

| layer | neuron | mean_abs_activation | activation_std | family_mean_std | sharedness | family_sensitivity | invariance_score | prompt_sensitive_score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 23 | 537 | 6.9544 | 3.0463 | 2.8634 | 2.2829 | 0.4117 | 1.6171 | 19.9131 |
| 23 | 1396 | 13.0774 | 1.4144 | 1.227 | 9.2459 | 0.0938 | 8.4528 | 16.0465 |
| 23 | 1121 | 13.2844 | 1.3602 | 1.1137 | 9.7663 | 0.0838 | 9.0108 | 14.7949 |
| 23 | 3935 | 13.4788 | 1.317 | 1.0732 | 10.2343 | 0.0796 | 9.4795 | 14.4661 |
| 23 | 1863 | 11.9257 | 1.3956 | 1.1987 | 8.5453 | 0.1005 | 7.7649 | 14.2948 |
| 23 | 2505 | 12.6344 | 1.3431 | 1.1276 | 9.4066 | 0.0892 | 8.6359 | 14.2462 |
| 23 | 4144 | 12.2997 | 1.4167 | 1.1535 | 8.6817 | 0.0938 | 7.9373 | 14.1877 |
| 23 | 1341 | 11.8201 | 1.2314 | 1.0319 | 9.5988 | 0.0873 | 8.8281 | 12.1968 |

## Strongest Selectivity Comparisons

| relation | metric | family_a | family_b | mean_diff | ci_low | ci_high | sign_test_pvalue | num_pairs |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| capital | target_selectivity | chat_template | declarative | -0.601 | -0.8001 | -0.3781 | 0.0039 | 12 |
| capital | target_selectivity | chat_template | qa | -0.5081 | -0.6965 | -0.27 | 0.0654 | 12 |
| capital | target_selectivity | chat_template | raw_question | -0.3569 | -0.5071 | -0.1527 | 0.0215 | 12 |
| capital | target_selectivity | declarative | raw_question | 0.244 | 0.1121 | 0.3751 | 0.0039 | 12 |
| headquarters | target_selectivity | chat_template | declarative | -0.2153 | -0.4793 | 0.1098 | 0.1797 | 12 |
| birth_place | target_selectivity | declarative | raw_question | -0.1989 | -0.3796 | -0.0476 | 0.125 | 12 |
| birth_place | target_selectivity | chat_template | raw_question | -0.1685 | -0.354 | -0.0185 | 0.25 | 12 |
| currency | target_selectivity | chat_template | declarative | -0.1554 | -0.3194 | -0.0156 | 0.2891 | 12 |

## Neuron Ablation Summary

| candidate_type | prompt_family | answer_f1_drop | contains_drop | target_selectivity_drop | same_subject_control_f1_increase | same_relation_control_f1_increase | lexical_distractor_f1_increase | max_control_f1_increase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| invariant | chat_template | 0.0 | 0.0 | -0.0222 | 0.0 | 0.0 | -0.0222 | -0.0222 |
| invariant | declarative | -0.0032 | 0.0 | -0.0032 | 0.0 | 0.0 | 0.0 | 0.0 |
| invariant | qa | 0.0267 | 0.0667 | 0.0415 | 0.0 | 0.0 | 0.0148 | 0.0148 |
| invariant | raw_question | 0.0152 | 0.0667 | 0.0152 | 0.0 | 0.0 | 0.0 | 0.0 |
| prompt_sensitive | chat_template | 0.0667 | 0.0667 | -0.0222 | 0.0 | 0.0 | -0.0889 | -0.0889 |
| prompt_sensitive | declarative | 0.0277 | -0.0667 | 0.0277 | 0.0 | 0.0 | 0.0 | 0.0 |
| prompt_sensitive | qa | 0.0191 | 0.0667 | 0.0324 | 0.0 | 0.0 | 0.0133 | 0.0133 |
| prompt_sensitive | raw_question | 0.0185 | 0.0667 | 0.0185 | 0.0 | 0.0 | 0.0 | 0.0 |