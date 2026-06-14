# Prompt Invariance Report: qwen2_5_0_5b_instruct

- Prompts analyzed: 160
- Mean answer F1: 0.2407
- Best prompt family by answer F1: chat_template

## Family Summary

| relation | prompt_family | target_rank | target_margin | full_exact_match | contains_expected | answer_f1 | answer_similarity |
| --- | --- | --- | --- | --- | --- | --- | --- |
| birth_place | chat_template | 3772.625 | -9.856 | 0.125 | 0.125 | 0.125 | 0.371 |
| birth_place | declarative | 26.375 | -2.3945 | 0.0 | 0.25 | 0.1429 | 0.2926 |
| birth_place | qa | 109.5 | -4.0977 | 0.0 | 0.125 | 0.0556 | 0.2436 |
| birth_place | raw_question | 1411.75 | -9.6465 | 0.0 | 0.0 | 0.0 | 0.2257 |
| capital | chat_template | 26.125 | -3.8359 | 0.5 | 0.5 | 0.5833 | 0.7931 |
| capital | declarative | 10.625 | -1.8281 | 0.0 | 0.25 | 0.0767 | 0.2561 |
| capital | qa | 1.5 | 1.6094 | 0.0 | 0.625 | 0.1986 | 0.3038 |
| capital | raw_question | 15.625 | -3.25 | 0.0 | 0.625 | 0.3542 | 0.5931 |
| currency | chat_template | 249.0 | -6.1211 | 0.125 | 0.25 | 0.4714 | 0.778 |
| currency | declarative | 234.125 | -7.7188 | 0.0 | 0.25 | 0.2383 | 0.3572 |
| currency | qa | 19.375 | -2.5312 | 0.0 | 0.25 | 0.3199 | 0.4803 |
| currency | raw_question | 357.75 | -5.3516 | 0.0 | 0.375 | 0.3705 | 0.4953 |
| headquarters | chat_template | 1432.5 | -7.9492 | 0.375 | 0.375 | 0.5 | 0.6277 |
| headquarters | declarative | 60.25 | -2.4805 | 0.0 | 0.125 | 0.1056 | 0.2882 |
| headquarters | qa | 67.5 | -3.5 | 0.0 | 0.75 | 0.303 | 0.3572 |
| headquarters | raw_question | 1217.125 | -9.0957 | 0.0 | 0.75 | 0.2832 | 0.3463 |
| official_language | chat_template | 26.375 | -6.2031 | 0.25 | 0.25 | 0.25 | 0.5406 |
| official_language | declarative | 10.75 | -1.1562 | 0.0 | 0.75 | 0.2482 | 0.3812 |
| official_language | qa | 1.125 | 2.3281 | 0.0 | 0.625 | 0.134 | 0.2382 |
| official_language | raw_question | 41.25 | -4.4688 | 0.0 | 0.25 | 0.0528 | 0.2107 |

## Top Invariant Neurons

| layer | neuron | mean_abs_activation | activation_std | family_mean_std | sharedness | family_sensitivity | invariance_score | prompt_sensitive_score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 8 | 4766 | 0.2779 | 0.0011 | 0.0003 | 264.1187 | 0.001 | 263.8577 | 0.0001 |
| 9 | 2112 | 0.2769 | 0.0018 | 0.0007 | 156.0603 | 0.0025 | 155.6635 | 0.0002 |
| 12 | 4708 | 0.2764 | 0.0018 | 0.0004 | 152.3054 | 0.0014 | 152.085 | 0.0001 |
| 0 | 308 | 0.2751 | 0.0023 | 0.0016 | 120.5628 | 0.006 | 119.8443 | 0.0005 |
| 15 | 443 | 0.276 | 0.0024 | 0.0003 | 115.4189 | 0.0012 | 115.2784 | 0.0001 |
| 7 | 3747 | 0.2764 | 0.0026 | 0.0013 | 108.1412 | 0.0046 | 107.6483 | 0.0003 |
| 15 | 1024 | 0.2763 | 0.0026 | 0.001 | 106.9191 | 0.0035 | 106.5496 | 0.0003 |
| 13 | 41 | 0.2768 | 0.003 | 0.0014 | 93.3039 | 0.0051 | 92.8297 | 0.0004 |

## Top Prompt-Sensitive Neurons

| layer | neuron | mean_abs_activation | activation_std | family_mean_std | sharedness | family_sensitivity | invariance_score | prompt_sensitive_score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 23 | 537 | 6.9355 | 3.0524 | 2.8661 | 2.2721 | 0.4132 | 1.6077 | 19.8777 |
| 23 | 1396 | 13.0883 | 1.4185 | 1.225 | 9.2266 | 0.0936 | 8.437 | 16.0334 |
| 23 | 1121 | 13.3254 | 1.3507 | 1.1125 | 9.8652 | 0.0835 | 9.105 | 14.8249 |
| 23 | 3935 | 13.5055 | 1.3168 | 1.0744 | 10.2562 | 0.0796 | 9.5004 | 14.51 |
| 23 | 1863 | 11.9254 | 1.4063 | 1.2052 | 8.48 | 0.1011 | 7.7017 | 14.3722 |
| 23 | 2505 | 12.6418 | 1.348 | 1.132 | 9.3785 | 0.0895 | 8.6077 | 14.311 |
| 23 | 4144 | 12.2945 | 1.4226 | 1.1563 | 8.6423 | 0.094 | 7.8993 | 14.2161 |
| 23 | 1341 | 11.8254 | 1.2288 | 1.0325 | 9.6238 | 0.0873 | 8.851 | 12.2099 |

## Neuron Ablation Summary

| candidate_type | prompt_family | answer_f1_drop | contains_drop |
| --- | --- | --- | --- |
| invariant | chat_template | 0.0 | 0.0 |
| invariant | declarative | 0.0333 | 0.1 |
| invariant | qa | 0.0 | 0.0 |
| invariant | raw_question | -0.0022 | 0.0 |
| prompt_sensitive | chat_template | 0.04 | 0.0 |
| prompt_sensitive | declarative | -0.0161 | -0.2 |
| prompt_sensitive | qa | -0.1058 | -0.2 |
| prompt_sensitive | raw_question | -0.0045 | -0.1 |