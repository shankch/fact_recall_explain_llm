# Prompt Invariance Report: gemma_270m_base

- Prompts analyzed: 16
- Mean answer F1: 0.1295
- Best prompt family by answer F1: chat_template

## Family Summary

| relation | prompt_family | target_rank | target_margin | full_exact_match | contains_expected | answer_f1 | answer_similarity |
| --- | --- | --- | --- | --- | --- | --- | --- |
| capital | chat_template | 33.5 | -2.4062 | 0.5 | 0.5 | 0.5 | 0.5789 |
| capital | declarative | 1.0 | 0.75 | 0.0 | 1.0 | 0.2857 | 0.3018 |
| capital | qa | 5.5 | -2.5625 | 0.0 | 0.0 | 0.0 | 0.1432 |
| capital | raw_question | 30.0 | -5.0625 | 0.0 | 0.0 | 0.0 | 0.1438 |
| official_language | chat_template | 96.5 | -2.4062 | 0.0 | 0.0 | 0.0 | 0.3854 |
| official_language | declarative | 1.5 | 0.375 | 0.0 | 0.5 | 0.125 | 0.2151 |
| official_language | qa | 10.0 | -0.0625 | 0.0 | 0.5 | 0.125 | 0.2424 |
| official_language | raw_question | 221.0 | -6.2812 | 0.0 | 0.0 | 0.0 | 0.2544 |

## Control Selectivity Summary

| prompt_family | answer_f1 | target_selectivity | same_subject_control_f1 | same_relation_control_f1 | lexical_distractor_f1 | max_control_f1 |
| --- | --- | --- | --- | --- | --- | --- |
| chat_template | 0.25 | 0.25 | 0.0 | 0.0 | 0.0 | 0.0 |
| declarative | 0.2054 | 0.2054 | 0.0 | 0.0 | 0.0 | 0.0 |
| qa | 0.0625 | 0.0625 | 0.0 | 0.0 | 0.0 | 0.0 |
| raw_question | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |

## Top Invariant Neurons

| layer | neuron | mean_abs_activation | activation_std | family_mean_std | sharedness | family_sensitivity | invariance_score | prompt_sensitive_score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 10 | 232 | 0.1693 | 0.0008 | 0.0005 | 221.8068 | 0.003 | 221.1494 | 0.0001 |
| 9 | 880 | 0.1689 | 0.001 | 0.0006 | 167.9162 | 0.0036 | 167.3145 | 0.0001 |
| 6 | 545 | 0.1693 | 0.001 | 0.0007 | 164.4467 | 0.0039 | 163.8107 | 0.0001 |
| 12 | 830 | 0.1687 | 0.0011 | 0.0006 | 158.3774 | 0.0037 | 157.7952 | 0.0001 |
| 0 | 265 | 0.1691 | 0.0011 | 0.0005 | 148.3573 | 0.003 | 147.9169 | 0.0001 |
| 5 | 1682 | 0.1694 | 0.0012 | 0.0007 | 135.9954 | 0.0042 | 135.4264 | 0.0001 |
| 5 | 474 | 0.1687 | 0.0013 | 0.0009 | 132.8783 | 0.0053 | 132.1755 | 0.0002 |
| 13 | 1982 | 0.1686 | 0.0013 | 0.0006 | 131.7678 | 0.0033 | 131.3347 | 0.0001 |

## Top Prompt-Sensitive Neurons

| layer | neuron | mean_abs_activation | activation_std | family_mean_std | sharedness | family_sensitivity | invariance_score | prompt_sensitive_score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 1765 | 1.9278 | 3.2021 | 3.2014 | 0.602 | 1.6607 | 0.2263 | 6.1716 |
| 0 | 1165 | 2.7844 | 1.6569 | 1.655 | 1.6805 | 0.5944 | 1.054 | 4.6083 |
| 0 | 1392 | 4.1123 | 0.9181 | 0.9174 | 4.479 | 0.2231 | 3.662 | 3.7728 |
| 1 | 283 | 1.8484 | 1.9898 | 1.9889 | 0.929 | 1.076 | 0.4475 | 3.6763 |
| 15 | 338 | 2.3049 | 1.4641 | 1.4534 | 1.5743 | 0.6305 | 0.9655 | 3.3499 |
| 0 | 1702 | 4.8828 | 0.6827 | 0.6811 | 7.1525 | 0.1395 | 6.277 | 3.3255 |
| 15 | 783 | 2.0587 | 1.2587 | 1.2489 | 1.6355 | 0.6067 | 1.018 | 2.5711 |
| 0 | 1516 | 2.4651 | 1.0354 | 1.0333 | 2.3809 | 0.4192 | 1.6777 | 2.5473 |

## Strongest Selectivity Comparisons

| relation | metric | family_a | family_b | mean_diff | ci_low | ci_high | sign_test_pvalue | num_pairs |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| capital | target_selectivity | chat_template | qa | -0.5 | -1.0 | 0.0 | 1.0 | 2 |
| capital | target_selectivity | chat_template | raw_question | -0.5 | -1.0 | 0.0 | 1.0 | 2 |
| capital | target_selectivity | declarative | qa | -0.2857 | -0.2857 | -0.2857 | 0.5 | 2 |
| capital | target_selectivity | declarative | raw_question | -0.2857 | -0.2857 | -0.2857 | 0.5 | 2 |
| capital | target_selectivity | chat_template | declarative | -0.2143 | -0.7143 | 0.2857 | 1.0 | 2 |
| official_language | target_selectivity | chat_template | declarative | 0.125 | 0.0 | 0.25 | 1.0 | 2 |
| official_language | target_selectivity | chat_template | qa | 0.125 | 0.0 | 0.25 | 1.0 | 2 |
| official_language | target_selectivity | qa | raw_question | -0.125 | -0.25 | 0.0 | 1.0 | 2 |

## Neuron Ablation Summary

| candidate_type | prompt_family | answer_f1_drop | contains_drop | target_selectivity_drop | same_subject_control_f1_increase | same_relation_control_f1_increase | lexical_distractor_f1_increase | max_control_f1_increase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| invariant | chat_template | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| invariant | declarative | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| invariant | qa | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| invariant | raw_question | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| prompt_sensitive | chat_template | -0.5 | -0.5 | -0.5 | 0.0 | 0.0 | 0.0 | 0.0 |
| prompt_sensitive | declarative | 0.1429 | 0.5 | 0.1429 | 0.0 | 0.0 | 0.0 | 0.0 |
| prompt_sensitive | qa | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| prompt_sensitive | raw_question | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |