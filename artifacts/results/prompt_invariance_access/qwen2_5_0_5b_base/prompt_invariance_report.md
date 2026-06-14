# Prompt Invariance Report: qwen2_5_0_5b_base

- Prompts analyzed: 240
- Mean answer F1: 0.2658
- Best prompt family by answer F1: qa

## Family Summary

| relation | prompt_family | target_rank | target_margin | full_exact_match | contains_expected | answer_f1 | answer_similarity |
| --- | --- | --- | --- | --- | --- | --- | --- |
| birth_place | chat_template | 107112.75 | -20.1305 | 0.0 | 0.3333 | 0.2722 | 0.4213 |
| birth_place | declarative | 70.5833 | -2.987 | 0.0 | 0.25 | 0.1573 | 0.3558 |
| birth_place | qa | 459.1667 | -4.776 | 0.0833 | 0.25 | 0.2056 | 0.4207 |
| birth_place | raw_question | 3169.75 | -8.5836 | 0.0 | 0.1667 | 0.1333 | 0.341 |
| capital | chat_template | 29794.0 | -10.2129 | 0.0 | 0.5833 | 0.2417 | 0.2839 |
| capital | declarative | 4.6667 | -0.349 | 0.0 | 0.5 | 0.1747 | 0.2924 |
| capital | qa | 1.1667 | 1.8229 | 0.75 | 0.75 | 0.8472 | 0.979 |
| capital | raw_question | 28.4167 | -3.9375 | 0.25 | 0.3333 | 0.3011 | 0.3942 |
| currency | chat_template | 12201.9167 | -6.6686 | 0.0 | 0.3333 | 0.1574 | 0.3567 |
| currency | declarative | 76.8333 | -5.8411 | 0.0 | 0.5 | 0.2917 | 0.4135 |
| currency | qa | 7.5 | -1.1198 | 0.0 | 0.3333 | 0.4028 | 0.6703 |
| currency | raw_question | 125.3333 | -4.138 | 0.0 | 0.1667 | 0.1472 | 0.3606 |
| headquarters | chat_template | 62244.8333 | -14.876 | 0.0 | 0.6667 | 0.2831 | 0.3368 |
| headquarters | declarative | 39.0 | -2.5052 | 0.0 | 0.3333 | 0.168 | 0.3204 |
| headquarters | qa | 31.6667 | -1.974 | 0.0833 | 0.75 | 0.3263 | 0.377 |
| headquarters | raw_question | 1172.25 | -8.2057 | 0.0 | 0.5 | 0.2525 | 0.3774 |
| official_language | chat_template | 23386.4167 | -11.1549 | 0.0 | 0.0833 | 0.0167 | 0.1746 |
| official_language | declarative | 5.75 | -0.7708 | 0.0 | 0.8333 | 0.2778 | 0.4294 |
| official_language | qa | 1.0833 | 1.1719 | 0.5833 | 0.6667 | 0.6042 | 0.8095 |
| official_language | raw_question | 28.1667 | -3.8281 | 0.0 | 0.3333 | 0.0556 | 0.2098 |

## Control Selectivity Summary

| prompt_family | answer_f1 | target_selectivity | same_subject_control_f1 | same_relation_control_f1 | lexical_distractor_f1 | max_control_f1 |
| --- | --- | --- | --- | --- | --- | --- |
| chat_template | 0.1942 | 0.1791 | 0.003 | 0.012 | 0.0037 | 0.0151 |
| declarative | 0.2139 | 0.1847 | 0.0 | 0.0067 | 0.0225 | 0.0292 |
| qa | 0.4772 | 0.3935 | 0.0 | 0.012 | 0.0754 | 0.0837 |
| raw_question | 0.1779 | 0.1368 | 0.0 | 0.012 | 0.0328 | 0.0411 |

## Top Invariant Neurons

| layer | neuron | mean_abs_activation | activation_std | family_mean_std | sharedness | family_sensitivity | invariance_score | prompt_sensitive_score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 8 | 4766 | 0.2776 | 0.0014 | 0.0008 | 199.3996 | 0.0029 | 198.8262 | 0.0002 |
| 9 | 2519 | 0.2767 | 0.0018 | 0.0008 | 150.1786 | 0.0028 | 149.7564 | 0.0002 |
| 9 | 1736 | 0.2761 | 0.0021 | 0.001 | 133.6217 | 0.0034 | 133.1623 | 0.0003 |
| 0 | 308 | 0.2751 | 0.0021 | 0.0016 | 128.0265 | 0.006 | 127.2637 | 0.0005 |
| 15 | 1024 | 0.277 | 0.0023 | 0.0007 | 121.6797 | 0.0024 | 121.3903 | 0.0002 |
| 9 | 568 | 0.2762 | 0.0025 | 0.0005 | 111.7289 | 0.002 | 111.5113 | 0.0001 |
| 1 | 3191 | 0.2761 | 0.0027 | 0.0019 | 101.0826 | 0.0068 | 100.4011 | 0.0005 |
| 0 | 918 | 0.2768 | 0.0028 | 0.0013 | 100.0329 | 0.0047 | 99.5667 | 0.0004 |

## Top Prompt-Sensitive Neurons

| layer | neuron | mean_abs_activation | activation_std | family_mean_std | sharedness | family_sensitivity | invariance_score | prompt_sensitive_score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 23 | 537 | 8.1825 | 2.6211 | 2.4269 | 3.1218 | 0.2966 | 2.4077 | 19.8578 |
| 23 | 1863 | 12.7743 | 1.2945 | 1.1102 | 9.8684 | 0.0869 | 9.0794 | 14.1816 |
| 23 | 2345 | 9.7083 | 1.2596 | 1.1418 | 7.7076 | 0.1176 | 6.8965 | 11.0853 |
| 23 | 2505 | 13.8479 | 1.0216 | 0.7594 | 13.5548 | 0.0548 | 12.8501 | 10.5165 |
| 23 | 3935 | 14.525 | 0.9956 | 0.7088 | 14.5898 | 0.0488 | 13.911 | 10.2956 |
| 23 | 3423 | 11.058 | 1.0508 | 0.9074 | 10.5234 | 0.0821 | 9.7254 | 10.0345 |
| 23 | 4144 | 13.367 | 1.0311 | 0.7234 | 12.9644 | 0.0541 | 12.2988 | 9.6698 |
| 23 | 2337 | 4.852 | 2.0575 | 1.9907 | 2.3582 | 0.4103 | 1.6722 | 9.6587 |

## Strongest Selectivity Comparisons

| relation | metric | family_a | family_b | mean_diff | ci_low | ci_high | sign_test_pvalue | num_pairs |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| capital | target_selectivity | declarative | qa | 0.6725 | 0.5055 | 0.837 | 0.001 | 12 |
| capital | target_selectivity | chat_template | qa | 0.6056 | 0.4155 | 0.7709 | 0.0063 | 12 |
| capital | target_selectivity | qa | raw_question | -0.5461 | -0.7708 | -0.2961 | 0.0078 | 12 |
| official_language | target_selectivity | chat_template | qa | 0.3527 | 0.0916 | 0.633 | 0.2188 | 12 |
| official_language | target_selectivity | qa | raw_question | -0.3356 | -0.5833 | -0.1064 | 0.0625 | 12 |
| currency | target_selectivity | qa | raw_question | -0.2556 | -0.4444 | -0.0778 | 0.125 | 12 |
| birth_place | target_selectivity | chat_template | raw_question | -0.2056 | -0.4278 | 0.0 | 0.25 | 12 |
| official_language | target_selectivity | chat_template | declarative | 0.204 | 0.0929 | 0.297 | 0.0391 | 12 |

## Neuron Ablation Summary

| candidate_type | prompt_family | answer_f1_drop | contains_drop | target_selectivity_drop | same_subject_control_f1_increase | same_relation_control_f1_increase | lexical_distractor_f1_increase | max_control_f1_increase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| invariant | chat_template | -0.0259 | -0.0667 | 0.0607 | 0.0 | 0.0 | 0.0867 | 0.0867 |
| invariant | declarative | 0.027 | 0.0667 | 0.0285 | 0.0 | 0.0 | 0.0015 | 0.0015 |
| invariant | qa | 0.0067 | 0.0 | 0.0 | 0.0 | 0.0 | -0.0067 | -0.0067 |
| invariant | raw_question | 0.0 | 0.0 | -0.0148 | 0.0 | 0.0 | -0.0148 | -0.0148 |
| prompt_sensitive | chat_template | -0.1 | -0.0667 | -0.0611 | 0.0 | 0.0 | 0.0389 | 0.0389 |
| prompt_sensitive | declarative | 0.0444 | 0.0667 | 0.0346 | 0.0 | 0.0 | -0.0098 | -0.0098 |
| prompt_sensitive | qa | 0.1281 | 0.2667 | 0.0681 | 0.0 | 0.0 | -0.06 | -0.06 |
| prompt_sensitive | raw_question | -0.0395 | 0.0 | -0.101 | 0.0 | 0.0 | -0.0615 | -0.0615 |