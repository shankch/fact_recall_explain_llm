# Prompt Invariance Report: qwen2_5_0_5b_base

- Prompts analyzed: 160
- Mean answer F1: 0.2749
- Best prompt family by answer F1: qa

## Family Summary

| relation | prompt_family | target_rank | target_margin | full_exact_match | contains_expected | answer_f1 | answer_similarity |
| --- | --- | --- | --- | --- | --- | --- | --- |
| birth_place | chat_template | 108609.875 | -19.6792 | 0.0 | 0.5 | 0.3667 | 0.4829 |
| birth_place | declarative | 20.625 | -2.5547 | 0.0 | 0.375 | 0.2048 | 0.3693 |
| birth_place | qa | 213.625 | -4.4062 | 0.125 | 0.375 | 0.3083 | 0.4946 |
| birth_place | raw_question | 1531.5 | -7.625 | 0.0 | 0.25 | 0.2 | 0.3815 |
| capital | chat_template | 39863.625 | -10.9229 | 0.0 | 0.5 | 0.1875 | 0.2676 |
| capital | declarative | 4.625 | -0.2031 | 0.0 | 0.375 | 0.151 | 0.2867 |
| capital | qa | 1.25 | 1.6719 | 0.625 | 0.625 | 0.7708 | 0.9685 |
| capital | raw_question | 35.125 | -3.8438 | 0.25 | 0.25 | 0.2955 | 0.4098 |
| currency | chat_template | 15733.125 | -6.7021 | 0.0 | 0.375 | 0.2361 | 0.3832 |
| currency | declarative | 107.625 | -6.4023 | 0.0 | 0.375 | 0.2911 | 0.409 |
| currency | qa | 9.875 | -1.375 | 0.0 | 0.25 | 0.4167 | 0.6345 |
| currency | raw_question | 156.75 | -4.2852 | 0.0 | 0.0 | 0.05 | 0.292 |
| headquarters | chat_template | 84304.0 | -16.7412 | 0.0 | 0.625 | 0.3157 | 0.3992 |
| headquarters | declarative | 47.375 | -2.4688 | 0.0 | 0.375 | 0.2163 | 0.3533 |
| headquarters | qa | 41.625 | -2.5 | 0.125 | 0.75 | 0.3492 | 0.4224 |
| headquarters | raw_question | 1554.875 | -9.4492 | 0.0 | 0.5 | 0.3117 | 0.4499 |
| official_language | chat_template | 21859.375 | -11.2246 | 0.0 | 0.125 | 0.025 | 0.1792 |
| official_language | declarative | 5.125 | -0.5391 | 0.0 | 0.75 | 0.2417 | 0.396 |
| official_language | qa | 1.125 | 1.1719 | 0.5 | 0.625 | 0.5312 | 0.7202 |
| official_language | raw_question | 34.875 | -4.0625 | 0.0 | 0.25 | 0.0278 | 0.1994 |

## Top Invariant Neurons

| layer | neuron | mean_abs_activation | activation_std | family_mean_std | sharedness | family_sensitivity | invariance_score | prompt_sensitive_score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 8 | 4766 | 0.2775 | 0.0014 | 0.0008 | 197.4046 | 0.0029 | 196.83 | 0.0002 |
| 9 | 2519 | 0.2766 | 0.0019 | 0.0008 | 148.572 | 0.0029 | 148.143 | 0.0002 |
| 9 | 1736 | 0.2761 | 0.0021 | 0.001 | 133.5 | 0.0035 | 133.0341 | 0.0003 |
| 0 | 308 | 0.2751 | 0.0022 | 0.0017 | 125.3564 | 0.0061 | 124.5926 | 0.0005 |
| 15 | 1024 | 0.277 | 0.0023 | 0.0006 | 121.1617 | 0.0023 | 120.8813 | 0.0002 |
| 9 | 568 | 0.2762 | 0.0024 | 0.0005 | 116.0712 | 0.0017 | 115.8756 | 0.0001 |
| 1 | 3191 | 0.2761 | 0.0028 | 0.0018 | 100.0826 | 0.0067 | 99.4171 | 0.0005 |
| 0 | 918 | 0.2768 | 0.0028 | 0.0013 | 99.4308 | 0.0048 | 98.951 | 0.0004 |

## Top Prompt-Sensitive Neurons

| layer | neuron | mean_abs_activation | activation_std | family_mean_std | sharedness | family_sensitivity | invariance_score | prompt_sensitive_score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 23 | 537 | 8.1643 | 2.6054 | 2.4056 | 3.1335 | 0.2946 | 2.4204 | 19.6399 |
| 23 | 1863 | 12.7766 | 1.2998 | 1.1038 | 9.8295 | 0.0864 | 9.0478 | 14.1031 |
| 23 | 2345 | 9.7033 | 1.254 | 1.1304 | 7.7378 | 0.1165 | 6.9304 | 10.969 |
| 23 | 2505 | 13.8523 | 1.0258 | 0.7538 | 13.5039 | 0.0544 | 12.807 | 10.4417 |
| 23 | 3935 | 14.5441 | 0.9986 | 0.7056 | 14.5646 | 0.0485 | 13.8907 | 10.2623 |
| 23 | 3423 | 11.0695 | 1.0488 | 0.9021 | 10.5548 | 0.0815 | 9.7595 | 9.9864 |
| 23 | 2337 | 4.8604 | 2.0501 | 1.9834 | 2.3708 | 0.4081 | 1.6837 | 9.6404 |
| 23 | 4144 | 13.3621 | 1.0389 | 0.7156 | 12.8618 | 0.0536 | 12.2081 | 9.5614 |

## Neuron Ablation Summary

| candidate_type | prompt_family | answer_f1_drop | contains_drop |
| --- | --- | --- | --- |
| invariant | chat_template | 0.02 | 0.1 |
| invariant | declarative | -0.0222 | -0.1 |
| invariant | qa | 0.0667 | 0.1 |
| invariant | raw_question | 0.0222 | 0.1 |
| prompt_sensitive | chat_template | -0.1459 | 0.0 |
| prompt_sensitive | declarative | 0.0805 | 0.2 |
| prompt_sensitive | qa | 0.0667 | 0.1 |
| prompt_sensitive | raw_question | -0.0556 | 0.0 |