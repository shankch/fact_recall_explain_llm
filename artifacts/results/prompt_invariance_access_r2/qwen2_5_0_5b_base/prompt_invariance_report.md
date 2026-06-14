# Prompt Invariance Report: qwen2_5_0_5b_base

- Prompts analyzed: 360
- Mean answer F1: 0.2872
- Analysis-selected best family: qa
- Analysis-selected best selectivity family: qa

## Holdout Family Summary

| relation | prompt_family | target_rank | target_margin | full_exact_match | contains_expected | answer_f1 | answer_similarity |
| --- | --- | --- | --- | --- | --- | --- | --- |
| birth_place | chat_template | 104118.5 | -21.0332 | 0.0 | 0.0 | 0.0833 | 0.298 |
| birth_place | declarative | 170.5 | -3.8516 | 0.0 | 0.0 | 0.0625 | 0.3287 |
| birth_place | qa | 950.25 | -5.5156 | 0.0 | 0.0 | 0.0 | 0.273 |
| birth_place | raw_question | 6446.25 | -10.5007 | 0.0 | 0.0 | 0.0 | 0.26 |
| capital | chat_template | 64001.75 | -13.5575 | 0.0 | 0.5 | 0.2917 | 0.3284 |
| capital | declarative | 14.5 | -1.5938 | 0.0 | 0.75 | 0.2083 | 0.3202 |
| capital | qa | 1.25 | 0.9844 | 0.75 | 0.75 | 0.75 | 0.8289 |
| capital | raw_question | 95.5 | -6.3906 | 0.25 | 0.25 | 0.25 | 0.397 |
| currency | chat_template | 923.0 | 0.3125 | 0.0 | 0.75 | 0.3996 | 0.4428 |
| currency | declarative | 10.25 | -4.8281 | 0.0 | 0.75 | 0.302 | 0.3581 |
| currency | qa | 2.0 | -0.2031 | 0.25 | 0.75 | 0.5611 | 0.6537 |
| currency | raw_question | 48.0 | -1.0625 | 0.0 | 0.25 | 0.1705 | 0.3794 |
| headquarters | chat_template | 33603.75 | -12.9053 | 0.0 | 0.5 | 0.2125 | 0.2636 |
| headquarters | declarative | 30.25 | -3.4375 | 0.0 | 0.25 | 0.0714 | 0.3106 |
| headquarters | qa | 25.0 | -2.2344 | 0.0 | 0.5 | 0.2056 | 0.266 |
| headquarters | raw_question | 439.5 | -5.9844 | 0.0 | 0.25 | 0.1339 | 0.2505 |
| official_language | chat_template | 7754.25 | -5.25 | 0.0 | 0.0 | 0.0 | 0.2379 |
| official_language | declarative | 3.5 | -0.5156 | 0.0 | 0.75 | 0.2167 | 0.3374 |
| official_language | qa | 1.0 | 1.75 | 1.0 | 1.0 | 1.0 | 1.0 |
| official_language | raw_question | 5.75 | -1.0625 | 0.0 | 0.25 | 0.0 | 0.2536 |

## Control Selectivity Summary

| prompt_family | answer_f1 | target_selectivity | same_subject_control_f1 | same_relation_control_f1 | lexical_distractor_f1 | max_control_f1 |
| --- | --- | --- | --- | --- | --- | --- |
| chat_template | 0.1974 | 0.1633 | 0.0 | 0.0091 | 0.025 | 0.0341 |
| declarative | 0.1722 | 0.1077 | 0.0 | 0.01 | 0.0545 | 0.0645 |
| qa | 0.5033 | 0.3822 | 0.0 | 0.0 | 0.1211 | 0.1211 |
| raw_question | 0.1109 | 0.0368 | 0.0 | 0.0091 | 0.065 | 0.0741 |

## Top Invariant Neurons

| layer | neuron | mean_abs_activation | activation_std | family_mean_std | sharedness | family_sensitivity | invariance_score | prompt_sensitive_score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 8 | 4766 | 0.2776 | 0.0016 | 0.0008 | 174.6781 | 0.0028 | 174.1936 | 0.0002 |
| 9 | 2519 | 0.2767 | 0.0019 | 0.0007 | 146.53 | 0.0027 | 146.1395 | 0.0002 |
| 9 | 1736 | 0.2761 | 0.002 | 0.0009 | 136.9523 | 0.0034 | 136.4944 | 0.0003 |
| 0 | 308 | 0.2751 | 0.0021 | 0.0016 | 128.6864 | 0.0059 | 127.9274 | 0.0004 |
| 15 | 1024 | 0.277 | 0.0023 | 0.0007 | 122.4819 | 0.0024 | 122.1849 | 0.0002 |
| 9 | 568 | 0.2762 | 0.0026 | 0.0006 | 104.627 | 0.002 | 104.4153 | 0.0002 |
| 1 | 3191 | 0.2761 | 0.0026 | 0.0019 | 104.4149 | 0.0067 | 103.7173 | 0.0005 |
| 13 | 296 | 0.2759 | 0.0028 | 0.0003 | 98.687 | 0.0012 | 98.5723 | 0.0001 |

## Top Prompt-Sensitive Neurons

| layer | neuron | mean_abs_activation | activation_std | family_mean_std | sharedness | family_sensitivity | invariance_score | prompt_sensitive_score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 23 | 537 | 8.1608 | 2.6214 | 2.405 | 3.1132 | 0.2947 | 2.4046 | 19.6271 |
| 23 | 1863 | 12.7498 | 1.3172 | 1.103 | 9.6796 | 0.0865 | 8.9089 | 14.0627 |
| 23 | 2345 | 9.7066 | 1.256 | 1.1319 | 7.7284 | 0.1166 | 6.9213 | 10.9873 |
| 23 | 2505 | 13.7891 | 1.0587 | 0.7581 | 13.0241 | 0.055 | 12.3454 | 10.4529 |
| 23 | 3935 | 14.5054 | 1.0187 | 0.7025 | 14.2391 | 0.0484 | 13.5813 | 10.19 |
| 23 | 3423 | 11.0542 | 1.0575 | 0.9065 | 10.4529 | 0.082 | 9.6607 | 10.0203 |
| 23 | 4144 | 13.3496 | 1.0358 | 0.7196 | 12.8877 | 0.0539 | 12.2285 | 9.6065 |
| 23 | 2337 | 4.8551 | 2.044 | 1.973 | 2.3752 | 0.4064 | 1.6889 | 9.579 |

## Strongest Selectivity Comparisons

| relation | metric | family_a | family_b | mean_diff | ci_low | ci_high | sign_test_pvalue | num_pairs |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| capital | target_selectivity | declarative | qa | 0.6798 | 0.522 | 0.8208 | 0.0 | 18 |
| capital | target_selectivity | chat_template | qa | 0.5889 | 0.4227 | 0.7299 | 0.0003 | 18 |
| capital | target_selectivity | qa | raw_question | -0.5863 | -0.7917 | -0.3669 | 0.0005 | 18 |
| official_language | target_selectivity | chat_template | qa | 0.4573 | 0.2351 | 0.6887 | 0.0215 | 18 |
| official_language | target_selectivity | qa | raw_question | -0.446 | -0.6561 | -0.2361 | 0.0039 | 18 |
| currency | target_selectivity | qa | raw_question | -0.3615 | -0.5504 | -0.1934 | 0.0063 | 18 |
| official_language | target_selectivity | declarative | qa | 0.2657 | 0.0546 | 0.4964 | 0.5811 | 18 |
| headquarters | target_selectivity | declarative | qa | 0.2301 | 0.086 | 0.3826 | 0.2101 | 18 |

## Neuron Ablation Summary

| candidate_type | prompt_family | answer_f1_drop | contains_drop | target_selectivity_drop | same_subject_control_f1_increase | same_relation_control_f1_increase | lexical_distractor_f1_increase | max_control_f1_increase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| invariant | chat_template | 0.0042 | 0.0 | 0.0576 | 0.0 | 0.0009 | 0.0525 | 0.0534 |
| invariant | declarative | -0.0063 | 0.0 | -0.0031 | 0.0 | 0.0 | 0.0031 | 0.0031 |
| invariant | qa | -0.0578 | 0.0 | 0.0561 | 0.0 | 0.0167 | 0.0972 | 0.1139 |
| invariant | raw_question | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| prompt_sensitive | chat_template | -0.0372 | 0.0 | -0.0213 | 0.0 | -0.0008 | 0.0167 | 0.0159 |
| prompt_sensitive | declarative | 0.0243 | 0.05 | 0.0327 | 0.0 | 0.0082 | 0.0002 | 0.0084 |
| prompt_sensitive | qa | 0.0783 | 0.15 | 0.0764 | 0.0 | 0.0167 | -0.0186 | -0.0019 |
| prompt_sensitive | raw_question | -0.0475 | -0.05 | -0.0958 | 0.0 | 0.0 | -0.0483 | -0.0483 |