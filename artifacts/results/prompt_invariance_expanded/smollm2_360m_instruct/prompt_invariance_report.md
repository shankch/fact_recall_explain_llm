# Prompt Invariance Report: smollm2_360m_instruct

- Prompts analyzed: 160
- Mean answer F1: 0.1366
- Best prompt family by answer F1: chat_template

## Family Summary

| relation | prompt_family | target_rank | target_margin | full_exact_match | contains_expected | answer_f1 | answer_similarity |
| --- | --- | --- | --- | --- | --- | --- | --- |
| birth_place | chat_template | 4364.625 | -14.0159 | 0.25 | 0.5 | 0.369 | 0.4313 |
| birth_place | declarative | 16.625 | -2.1797 | 0.0 | 0.0 | 0.025 | 0.1923 |
| birth_place | qa | 1884.875 | -11.0215 | 0.0 | 0.0 | 0.0 | 0.0 |
| birth_place | raw_question | 1638.875 | -12.5117 | 0.0 | 0.0 | 0.0 | 0.0 |
| capital | chat_template | 228.625 | -7.1211 | 0.5 | 0.625 | 0.6333 | 0.8087 |
| capital | declarative | 2.5 | 2.7578 | 0.0 | 0.75 | 0.2812 | 0.3841 |
| capital | qa | 241.75 | -9.6719 | 0.0 | 0.0 | 0.0 | 0.0 |
| capital | raw_question | 5133.625 | -13.2812 | 0.0 | 0.0 | 0.0 | 0.0 |
| currency | chat_template | 932.0 | -9.4053 | 0.0 | 0.0 | 0.1027 | 0.4533 |
| currency | declarative | 19.375 | -5.6172 | 0.0 | 0.125 | 0.2097 | 0.3592 |
| currency | qa | 1343.125 | -10.4434 | 0.0 | 0.0 | 0.0 | 0.0185 |
| currency | raw_question | 6323.375 | -16.3411 | 0.0 | 0.0 | 0.0 | 0.0417 |
| headquarters | chat_template | 7320.625 | -14.1562 | 0.0 | 0.625 | 0.2982 | 0.3812 |
| headquarters | declarative | 170.625 | -0.3867 | 0.0 | 0.625 | 0.5271 | 0.648 |
| headquarters | qa | 1036.75 | -11.0938 | 0.0 | 0.0 | 0.0 | 0.0 |
| headquarters | raw_question | 1949.625 | -13.8457 | 0.0 | 0.0 | 0.0 | 0.0 |
| official_language | chat_template | 235.125 | -7.2539 | 0.0 | 0.5 | 0.1354 | 0.2656 |
| official_language | declarative | 1.25 | 1.2266 | 0.0 | 0.625 | 0.151 | 0.2665 |
| official_language | qa | 404.625 | -10.5117 | 0.0 | 0.0 | 0.0 | 0.0 |
| official_language | raw_question | 2723.875 | -14.2212 | 0.0 | 0.0 | 0.0 | 0.0911 |

## Top Invariant Neurons

| layer | neuron | mean_abs_activation | activation_std | family_mean_std | sharedness | family_sensitivity | invariance_score | prompt_sensitive_score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 538 | 0.2775 | 0.0021 | 0.0009 | 129.5236 | 0.0032 | 129.1081 | 0.0002 |
| 13 | 1014 | 0.2766 | 0.0025 | 0.0008 | 111.3787 | 0.0029 | 111.0538 | 0.0002 |
| 12 | 2285 | 0.2751 | 0.0032 | 0.001 | 84.8005 | 0.0036 | 84.4952 | 0.0003 |
| 14 | 1185 | 0.2757 | 0.0033 | 0.0017 | 82.8255 | 0.0061 | 82.322 | 0.0005 |
| 18 | 1865 | 0.276 | 0.0034 | 0.0013 | 81.7915 | 0.0048 | 81.403 | 0.0004 |
| 6 | 156 | 0.2732 | 0.0039 | 0.0028 | 70.7711 | 0.0104 | 70.0452 | 0.0008 |
| 17 | 71 | 0.2748 | 0.0041 | 0.0019 | 67.5093 | 0.0069 | 67.0467 | 0.0005 |
| 17 | 980 | 0.2742 | 0.0041 | 0.0016 | 67.2878 | 0.0059 | 66.8904 | 0.0004 |

## Top Prompt-Sensitive Neurons

| layer | neuron | mean_abs_activation | activation_std | family_mean_std | sharedness | family_sensitivity | invariance_score | prompt_sensitive_score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 31 | 2496 | 13.2129 | 2.0715 | 1.865 | 6.3785 | 0.1412 | 5.5895 | 24.6423 |
| 31 | 2464 | 12.2855 | 1.9322 | 1.7285 | 6.3584 | 0.1407 | 5.5741 | 21.235 |
| 31 | 1620 | 11.2621 | 2.0201 | 1.8491 | 5.5751 | 0.1642 | 4.7888 | 20.8251 |
| 31 | 1777 | 5.5849 | 3.5991 | 3.4358 | 1.5518 | 0.6152 | 0.9607 | 19.1885 |
| 31 | 2301 | 11.7176 | 1.8638 | 1.5944 | 6.2869 | 0.1361 | 5.5339 | 18.6826 |
| 31 | 2169 | 11.6824 | 1.8368 | 1.5914 | 6.3602 | 0.1362 | 5.5977 | 18.5916 |
| 31 | 2276 | 13.0836 | 1.6062 | 1.4063 | 8.1455 | 0.1075 | 7.355 | 18.3989 |
| 31 | 1767 | 12.2395 | 1.69 | 1.4892 | 7.2421 | 0.1217 | 6.4565 | 18.2276 |

## Neuron Ablation Summary

| candidate_type | prompt_family | answer_f1_drop | contains_drop |
| --- | --- | --- | --- |
| invariant | chat_template | 0.0 | 0.0 |
| invariant | declarative | 0.0083 | 0.0 |
| invariant | qa | 0.0 | 0.0 |
| invariant | raw_question | 0.0 | 0.0 |
| prompt_sensitive | chat_template | -0.0286 | 0.0 |
| prompt_sensitive | declarative | 0.0413 | 0.1 |
| prompt_sensitive | qa | -0.065 | -0.1 |
| prompt_sensitive | raw_question | -0.08 | -0.1 |