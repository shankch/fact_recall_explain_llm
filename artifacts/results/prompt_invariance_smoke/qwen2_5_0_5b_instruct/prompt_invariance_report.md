# Prompt Invariance Report: qwen2_5_0_5b_instruct

- Prompts analyzed: 80
- Mean answer F1: 0.2513
- Best prompt family by answer F1: chat_template

## Family Summary

| relation | prompt_family | target_rank | target_margin | full_exact_match | contains_expected | answer_f1 | answer_similarity |
| --- | --- | --- | --- | --- | --- | --- | --- |
| birth_place | chat_template | 6022.5 | -8.5049 | 0.25 | 0.25 | 0.25 | 0.4429 |
| birth_place | declarative | 27.5 | -1.6719 | 0.0 | 0.5 | 0.2857 | 0.4376 |
| birth_place | qa | 15.5 | -2.6875 | 0.0 | 0.25 | 0.1111 | 0.3168 |
| birth_place | raw_question | 298.0 | -8.7266 | 0.0 | 0.0 | 0.0 | 0.2378 |
| capital | chat_template | 7.0 | -3.2344 | 0.25 | 0.25 | 0.4167 | 0.7612 |
| capital | declarative | 4.75 | -1.4844 | 0.0 | 0.25 | 0.0625 | 0.2361 |
| capital | qa | 1.5 | 1.75 | 0.0 | 0.5 | 0.1056 | 0.2426 |
| capital | raw_question | 4.75 | -1.5156 | 0.0 | 0.5 | 0.2917 | 0.6311 |
| currency | chat_template | 21.0 | -6.25 | 0.25 | 0.25 | 0.6 | 0.9395 |
| currency | declarative | 242.5 | -8.4766 | 0.0 | 0.25 | 0.2121 | 0.3193 |
| currency | qa | 6.0 | -2.9062 | 0.0 | 0.5 | 0.4833 | 0.6279 |
| currency | raw_question | 572.75 | -5.7969 | 0.0 | 0.25 | 0.3288 | 0.4653 |
| headquarters | chat_template | 418.25 | -6.1484 | 0.5 | 0.5 | 0.6667 | 0.6883 |
| headquarters | declarative | 8.0 | -1.2656 | 0.0 | 0.25 | 0.2111 | 0.407 |
| headquarters | qa | 14.75 | -1.9219 | 0.0 | 0.75 | 0.3131 | 0.3922 |
| headquarters | raw_question | 295.75 | -7.6719 | 0.0 | 1.0 | 0.3644 | 0.4039 |
| official_language | chat_template | 41.5 | -5.9062 | 0.0 | 0.0 | 0.0 | 0.2989 |
| official_language | declarative | 15.75 | -1.8438 | 0.0 | 0.5 | 0.1548 | 0.3212 |
| official_language | qa | 1.25 | 1.6562 | 0.0 | 0.5 | 0.1125 | 0.2432 |
| official_language | raw_question | 32.75 | -4.5312 | 0.0 | 0.25 | 0.0556 | 0.2145 |

## Top Invariant Neurons

| layer | neuron | mean_abs_activation | activation_std | family_mean_std | sharedness | family_sensitivity | invariance_score | prompt_sensitive_score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 8 | 4766 | 0.2779 | 0.0012 | 0.0003 | 240.4953 | 0.0009 | 240.268 | 0.0001 |
| 12 | 4708 | 0.2764 | 0.0018 | 0.0004 | 155.7851 | 0.0016 | 155.5378 | 0.0001 |
| 9 | 2112 | 0.2767 | 0.0019 | 0.0007 | 146.0745 | 0.0024 | 145.7231 | 0.0002 |
| 15 | 443 | 0.276 | 0.0023 | 0.0002 | 118.5725 | 0.0007 | 118.486 | 0.0001 |
| 15 | 1024 | 0.2765 | 0.0024 | 0.001 | 116.6661 | 0.0036 | 116.245 | 0.0003 |
| 0 | 308 | 0.2751 | 0.0024 | 0.0018 | 114.5227 | 0.0064 | 113.7965 | 0.0005 |
| 7 | 3747 | 0.2764 | 0.0026 | 0.0015 | 106.9939 | 0.0053 | 106.4347 | 0.0004 |
| 13 | 41 | 0.2769 | 0.0029 | 0.0013 | 97.0751 | 0.0047 | 96.6164 | 0.0004 |

## Top Prompt-Sensitive Neurons

| layer | neuron | mean_abs_activation | activation_std | family_mean_std | sharedness | family_sensitivity | invariance_score | prompt_sensitive_score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 23 | 537 | 6.9251 | 3.0592 | 2.8868 | 2.2637 | 0.4169 | 1.5977 | 19.9913 |
| 23 | 1396 | 13.0195 | 1.4258 | 1.2262 | 9.1317 | 0.0942 | 8.3457 | 15.965 |
| 23 | 3935 | 13.4578 | 1.3328 | 1.0945 | 10.0977 | 0.0813 | 9.3382 | 14.73 |
| 23 | 1121 | 13.3023 | 1.3308 | 1.105 | 9.9954 | 0.0831 | 9.2288 | 14.6987 |
| 23 | 1863 | 11.8984 | 1.4214 | 1.2174 | 8.3708 | 0.1023 | 7.5938 | 14.4856 |
| 23 | 2505 | 12.5734 | 1.3617 | 1.1515 | 9.2337 | 0.0916 | 8.459 | 14.4786 |
| 23 | 4144 | 12.3516 | 1.398 | 1.1602 | 8.8351 | 0.0939 | 8.0765 | 14.3304 |
| 23 | 1341 | 11.8469 | 1.2214 | 1.0266 | 9.6995 | 0.0867 | 8.9261 | 12.1615 |

## Neuron Ablation Summary

| candidate_type | prompt_family | answer_f1_drop | contains_drop |
| --- | --- | --- | --- |
| invariant | chat_template | 0.0 | 0.0 |
| invariant | declarative | 0.0 | 0.0 |
| invariant | qa | 0.0 | 0.0 |
| invariant | raw_question | -0.08 | 0.0 |
| prompt_sensitive | chat_template | 0.3333 | 0.4 |
| prompt_sensitive | declarative | 0.0 | 0.0 |
| prompt_sensitive | qa | 0.0 | 0.0 |
| prompt_sensitive | raw_question | 0.0 | 0.0 |