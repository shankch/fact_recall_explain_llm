# Prompt Invariance Report: smollm2_360m_instruct

- Prompts analyzed: 360
- Mean answer F1: 0.1485
- Analysis-selected best family: chat_template
- Analysis-selected best selectivity family: chat_template

## Holdout Family Summary

| relation | prompt_family | target_rank | target_margin | full_exact_match | contains_expected | answer_f1 | answer_similarity |
| --- | --- | --- | --- | --- | --- | --- | --- |
| birth_place | chat_template | 5781.75 | -15.4102 | 0.25 | 0.25 | 0.25 | 0.3654 |
| birth_place | declarative | 117.5 | -3.9219 | 0.0 | 0.25 | 0.1875 | 0.3702 |
| birth_place | qa | 4510.0 | -12.4883 | 0.0 | 0.0 | 0.0 | 0.0 |
| birth_place | raw_question | 4404.25 | -13.6782 | 0.0 | 0.0 | 0.0 | 0.0 |
| capital | chat_template | 219.5 | -8.0547 | 0.5 | 0.5 | 0.5 | 0.6097 |
| capital | declarative | 1.0 | 3.0312 | 0.0 | 1.0 | 0.3208 | 0.3932 |
| capital | qa | 214.25 | -10.2969 | 0.0 | 0.0 | 0.0 | 0.0 |
| capital | raw_question | 1209.75 | -11.334 | 0.0 | 0.0 | 0.0 | 0.0 |
| currency | chat_template | 62.75 | -6.0859 | 0.0 | 0.5 | 0.2714 | 0.5204 |
| currency | declarative | 2.5 | -2.375 | 0.0 | 1.0 | 0.4554 | 0.5439 |
| currency | qa | 285.5 | -5.2656 | 0.0 | 0.0 | 0.0 | 0.0 |
| currency | raw_question | 820.75 | -11.1172 | 0.0 | 0.0 | 0.0 | 0.0 |
| headquarters | chat_template | 1601.75 | -10.8516 | 0.0 | 0.25 | 0.1825 | 0.264 |
| headquarters | declarative | 17.75 | -1.7656 | 0.0 | 0.25 | 0.1742 | 0.2963 |
| headquarters | qa | 494.25 | -8.0234 | 0.0 | 0.0 | 0.0 | 0.0 |
| headquarters | raw_question | 1221.0 | -11.25 | 0.0 | 0.0 | 0.0 | 0.0 |
| official_language | chat_template | 99.0 | -6.1953 | 0.0 | 1.0 | 0.25 | 0.2837 |
| official_language | declarative | 1.0 | 2.1094 | 0.0 | 1.0 | 0.2236 | 0.2667 |
| official_language | qa | 117.0 | -7.2656 | 0.0 | 0.0 | 0.0 | 0.0 |
| official_language | raw_question | 517.5 | -10.2539 | 0.0 | 0.0 | 0.0 | 0.0845 |

## Control Selectivity Summary

| prompt_family | answer_f1 | target_selectivity | same_subject_control_f1 | same_relation_control_f1 | lexical_distractor_f1 | max_control_f1 |
| --- | --- | --- | --- | --- | --- | --- |
| chat_template | 0.2908 | 0.239 | 0.0 | 0.025 | 0.0268 | 0.0518 |
| declarative | 0.2723 | 0.1855 | 0.0 | 0.0393 | 0.0725 | 0.0868 |
| qa | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| raw_question | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |

## Top Invariant Neurons

| layer | neuron | mean_abs_activation | activation_std | family_mean_std | sharedness | family_sensitivity | invariance_score | prompt_sensitive_score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 538 | 0.2775 | 0.0024 | 0.001 | 116.7087 | 0.0035 | 116.3034 | 0.0003 |
| 13 | 1014 | 0.2765 | 0.0027 | 0.0006 | 101.2335 | 0.0023 | 101.0002 | 0.0002 |
| 12 | 2285 | 0.2753 | 0.0031 | 0.0009 | 89.5265 | 0.0032 | 89.2413 | 0.0002 |
| 14 | 1185 | 0.2759 | 0.0031 | 0.0016 | 88.7629 | 0.0058 | 88.2513 | 0.0004 |
| 18 | 1865 | 0.276 | 0.0034 | 0.0013 | 81.149 | 0.0046 | 80.7743 | 0.0004 |
| 17 | 980 | 0.2744 | 0.004 | 0.0018 | 69.3031 | 0.0065 | 68.8577 | 0.0005 |
| 6 | 156 | 0.2732 | 0.0041 | 0.0031 | 67.1423 | 0.0114 | 66.3867 | 0.0008 |
| 18 | 73 | 0.2734 | 0.0041 | 0.0024 | 66.4855 | 0.0087 | 65.9144 | 0.0006 |

## Top Prompt-Sensitive Neurons

| layer | neuron | mean_abs_activation | activation_std | family_mean_std | sharedness | family_sensitivity | invariance_score | prompt_sensitive_score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 31 | 2496 | 13.1993 | 2.0481 | 1.8571 | 6.4446 | 0.1407 | 5.6497 | 24.5128 |
| 31 | 2464 | 12.2859 | 1.9236 | 1.7314 | 6.387 | 0.1409 | 5.5981 | 21.2721 |
| 31 | 1620 | 11.2643 | 2.0148 | 1.8542 | 5.5907 | 0.1646 | 4.8005 | 20.8865 |
| 31 | 1777 | 5.5552 | 3.6053 | 3.4304 | 1.5409 | 0.6175 | 0.9526 | 19.0566 |
| 31 | 2169 | 11.6857 | 1.8126 | 1.5881 | 6.447 | 0.1359 | 5.6756 | 18.5587 |
| 31 | 2276 | 13.0824 | 1.5962 | 1.4088 | 8.196 | 0.1077 | 7.3992 | 18.4303 |
| 31 | 2301 | 11.6621 | 1.8334 | 1.5733 | 6.3608 | 0.1349 | 5.6047 | 18.3473 |
| 31 | 1767 | 12.2484 | 1.6751 | 1.4889 | 7.3118 | 0.1216 | 6.5194 | 18.2363 |

## Strongest Selectivity Comparisons

| relation | metric | family_a | family_b | mean_diff | ci_low | ci_high | sign_test_pvalue | num_pairs |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| capital | target_selectivity | chat_template | raw_question | -0.6037 | -0.7926 | -0.4147 | 0.0002 | 18 |
| capital | target_selectivity | chat_template | qa | -0.6037 | -0.7926 | -0.4147 | 0.0002 | 18 |
| capital | target_selectivity | chat_template | declarative | -0.3218 | -0.51 | -0.1182 | 0.049 | 18 |
| birth_place | target_selectivity | chat_template | qa | -0.2937 | -0.5373 | -0.0741 | 0.0703 | 18 |
| birth_place | target_selectivity | chat_template | raw_question | -0.2937 | -0.5373 | -0.0741 | 0.0703 | 18 |
| headquarters | target_selectivity | declarative | qa | -0.2835 | -0.4286 | -0.1035 | 0.0129 | 18 |
| headquarters | target_selectivity | declarative | raw_question | -0.2835 | -0.4286 | -0.1035 | 0.0129 | 18 |
| capital | target_selectivity | declarative | qa | -0.2819 | -0.356 | -0.2069 | 0.0 | 18 |

## Neuron Ablation Summary

| candidate_type | prompt_family | answer_f1_drop | contains_drop | target_selectivity_drop | same_subject_control_f1_increase | same_relation_control_f1_increase | lexical_distractor_f1_increase | max_control_f1_increase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| invariant | chat_template | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| invariant | declarative | 0.0132 | 0.0 | 0.0132 | 0.0 | 0.0 | 0.0 | 0.0 |
| invariant | qa | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| invariant | raw_question | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| prompt_sensitive | chat_template | 0.0581 | 0.1 | 0.0372 | 0.0 | -0.025 | 0.0042 | -0.0208 |
| prompt_sensitive | declarative | 0.0707 | 0.1 | 0.0623 | 0.0 | -0.0226 | -0.0107 | -0.0083 |
| prompt_sensitive | qa | -0.0504 | -0.05 | -0.0379 | 0.0 | 0.0 | 0.0125 | 0.0125 |
| prompt_sensitive | raw_question | -0.1233 | -0.1 | -0.0367 | 0.0 | 0.0 | 0.0867 | 0.0867 |