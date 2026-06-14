# Prompt Invariance Report: smollm2_360m_base

- Prompts analyzed: 240
- Mean answer F1: 0.2745
- Best prompt family by answer F1: qa

## Family Summary

| relation | prompt_family | target_rank | target_margin | full_exact_match | contains_expected | answer_f1 | answer_similarity |
| --- | --- | --- | --- | --- | --- | --- | --- |
| birth_place | chat_template | 359.8333 | -3.7656 | 0.0 | 0.0 | 0.0 | 0.1822 |
| birth_place | declarative | 80.0 | -2.3906 | 0.0 | 0.25 | 0.1601 | 0.3251 |
| birth_place | qa | 161.3333 | -3.474 | 0.0 | 0.4167 | 0.212 | 0.3727 |
| birth_place | raw_question | 1090.5 | -9.9714 | 0.1667 | 0.1667 | 0.1667 | 0.2936 |
| capital | chat_template | 5.25 | -0.276 | 0.1667 | 0.5833 | 0.3865 | 0.5201 |
| capital | declarative | 1.1667 | 1.5417 | 0.0 | 0.8333 | 0.2852 | 0.3386 |
| capital | qa | 1.0833 | 2.625 | 0.0 | 0.75 | 0.2903 | 0.4309 |
| capital | raw_question | 22.8333 | -5.5365 | 0.1667 | 0.6667 | 0.4163 | 0.5084 |
| currency | chat_template | 40.0833 | -1.5677 | 0.0 | 0.4167 | 0.45 | 0.597 |
| currency | declarative | 5.5833 | -4.0104 | 0.0 | 0.5833 | 0.4053 | 0.5417 |
| currency | qa | 23.5 | -2.776 | 0.0 | 0.4167 | 0.4731 | 0.5993 |
| currency | raw_question | 136.0833 | -8.0156 | 0.0 | 0.0833 | 0.2583 | 0.4767 |
| headquarters | chat_template | 268.6667 | -3.1771 | 0.0 | 0.5 | 0.2351 | 0.3875 |
| headquarters | declarative | 136.75 | -1.1406 | 0.0 | 0.5 | 0.3552 | 0.4788 |
| headquarters | qa | 272.3333 | -4.7083 | 0.1667 | 0.6667 | 0.5194 | 0.5571 |
| headquarters | raw_question | 637.5 | -8.7969 | 0.0833 | 0.4167 | 0.2767 | 0.363 |
| official_language | chat_template | 2.0833 | 0.2969 | 0.0 | 0.4167 | 0.1417 | 0.3387 |
| official_language | declarative | 1.0 | 1.5833 | 0.0 | 0.6667 | 0.1839 | 0.3334 |
| official_language | qa | 1.25 | 0.6771 | 0.0 | 0.6667 | 0.1714 | 0.2945 |
| official_language | raw_question | 18.8333 | -6.151 | 0.0 | 0.4167 | 0.1019 | 0.2581 |

## Control Selectivity Summary

| prompt_family | answer_f1 | target_selectivity | same_subject_control_f1 | same_relation_control_f1 | lexical_distractor_f1 | max_control_f1 |
| --- | --- | --- | --- | --- | --- | --- |
| chat_template | 0.2427 | 0.2102 | 0.0 | 0.0042 | 0.0325 | 0.0325 |
| declarative | 0.2779 | 0.2534 | 0.0 | 0.0114 | 0.0179 | 0.0245 |
| qa | 0.3333 | 0.2919 | 0.0033 | 0.0153 | 0.0269 | 0.0414 |
| raw_question | 0.244 | 0.2116 | 0.0037 | 0.0167 | 0.012 | 0.0324 |

## Top Invariant Neurons

| layer | neuron | mean_abs_activation | activation_std | family_mean_std | sharedness | family_sensitivity | invariance_score | prompt_sensitive_score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 6 | 156 | 0.2756 | 0.003 | 0.0025 | 92.2912 | 0.009 | 91.471 | 0.0007 |
| 12 | 490 | 0.2752 | 0.0034 | 0.0015 | 80.3824 | 0.0055 | 79.9438 | 0.0004 |
| 17 | 2550 | 0.276 | 0.0035 | 0.0011 | 79.1857 | 0.004 | 78.8698 | 0.0003 |
| 2 | 1170 | 0.2757 | 0.0037 | 0.0014 | 75.0926 | 0.0051 | 74.7127 | 0.0004 |
| 14 | 449 | 0.2745 | 0.0037 | 0.002 | 73.55 | 0.0074 | 73.01 | 0.0006 |
| 1 | 538 | 0.2745 | 0.0041 | 0.0034 | 66.5536 | 0.0122 | 65.7505 | 0.0009 |
| 17 | 1709 | 0.2757 | 0.0042 | 0.0013 | 65.9173 | 0.0048 | 65.603 | 0.0004 |
| 13 | 1021 | 0.275 | 0.0042 | 0.0015 | 65.6546 | 0.0056 | 65.2911 | 0.0004 |

## Top Prompt-Sensitive Neurons

| layer | neuron | mean_abs_activation | activation_std | family_mean_std | sharedness | family_sensitivity | invariance_score | prompt_sensitive_score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 31 | 1777 | 10.3273 | 2.5008 | 2.1635 | 4.1295 | 0.2095 | 3.4142 | 22.3428 |
| 31 | 1034 | 16.4253 | 1.4658 | 1.1388 | 11.2055 | 0.0693 | 10.4789 | 18.7055 |
| 31 | 2064 | 16.1736 | 1.6042 | 1.1352 | 10.0821 | 0.0702 | 9.4209 | 18.3607 |
| 31 | 2464 | 15.5361 | 1.4931 | 1.1491 | 10.4054 | 0.074 | 9.6888 | 17.852 |
| 31 | 446 | 16.7274 | 1.443 | 1.0653 | 11.5921 | 0.0637 | 10.8981 | 17.8199 |
| 31 | 2276 | 16.6938 | 1.3762 | 1.0442 | 12.1299 | 0.0625 | 11.4159 | 17.4309 |
| 31 | 2169 | 15.349 | 1.5178 | 1.1348 | 10.1123 | 0.0739 | 9.4162 | 17.4175 |
| 31 | 2496 | 17.349 | 1.3721 | 0.9967 | 12.6445 | 0.0575 | 11.9575 | 17.2922 |

## Strongest Selectivity Comparisons

| relation | metric | family_a | family_b | mean_diff | ci_low | ci_high | sign_test_pvalue | num_pairs |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| headquarters | target_selectivity | chat_template | qa | 0.3052 | 0.1373 | 0.4968 | 0.0156 | 12 |
| headquarters | target_selectivity | qa | raw_question | -0.2219 | -0.3836 | -0.0479 | 0.1797 | 12 |
| headquarters | target_selectivity | declarative | qa | 0.1673 | -0.0045 | 0.3443 | 0.7539 | 12 |
| currency | target_selectivity | qa | raw_question | -0.1593 | -0.276 | -0.0489 | 0.0312 | 12 |
| currency | target_selectivity | chat_template | raw_question | -0.1583 | -0.2892 | -0.0083 | 0.0703 | 12 |
| birth_place | target_selectivity | chat_template | qa | 0.1565 | -0.0557 | 0.3371 | 0.2188 | 12 |
| currency | target_selectivity | declarative | raw_question | -0.147 | -0.3297 | 0.0434 | 0.2266 | 12 |
| headquarters | target_selectivity | chat_template | declarative | 0.1379 | 0.0078 | 0.2916 | 0.0215 | 12 |

## Neuron Ablation Summary

| candidate_type | prompt_family | answer_f1_drop | contains_drop | target_selectivity_drop | same_subject_control_f1_increase | same_relation_control_f1_increase | lexical_distractor_f1_increase | max_control_f1_increase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| invariant | chat_template | -0.0076 | 0.0 | -0.0076 | 0.0 | 0.0 | 0.0 | 0.0 |
| invariant | declarative | 0.0015 | 0.0 | 0.0015 | 0.0 | 0.0 | 0.0 | 0.0 |
| invariant | qa | -0.04 | 0.0 | -0.04 | 0.0 | 0.0 | 0.0 | 0.0 |
| invariant | raw_question | -0.0111 | -0.0667 | 0.0333 | 0.0 | 0.0 | 0.0444 | 0.0444 |
| prompt_sensitive | chat_template | 0.1382 | 0.2667 | 0.097 | 0.0 | 0.0 | -0.0412 | -0.0412 |
| prompt_sensitive | declarative | 0.0194 | 0.0 | 0.0194 | 0.0 | 0.0 | 0.0 | 0.0 |
| prompt_sensitive | qa | 0.1066 | 0.1333 | 0.0788 | 0.0 | 0.0 | -0.0278 | -0.0278 |
| prompt_sensitive | raw_question | 0.0228 | 0.0 | 0.0246 | 0.0 | 0.0 | 0.0019 | 0.0019 |