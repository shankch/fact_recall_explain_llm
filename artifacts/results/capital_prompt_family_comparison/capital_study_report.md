# Capital Prompt Study

- Prompts analyzed: 400
- Mean exact match: 0.4825
- Mean contains-expected: 0.4850
- Mean target rank: 695.51
- Mean target margin: -4.3584
- Strongest shared layer by mean MLP activity: 0
- Best prompt family by target rank: qa

## Prompt family comparison

| prompt_family | target_rank_mean | target_rank_median | target_margin_mean | target_margin_median | exact_match_mean | exact_match_median | contains_expected_mean | contains_expected_median |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| chat_template | 2550.54 | 25.0 | -9.4086 | -6.6875 | 0.41 | 0.0 | 0.41 | 0.0 |
| declarative | 41.1 | 1.0 | 2.3306 | 3.375 | 0.63 | 1.0 | 0.63 | 1.0 |
| qa | 16.2 | 1.0 | -0.3456 | 0.125 | 0.5 | 0.5 | 0.5 | 0.5 |
| raw_question | 174.19 | 34.5 | -10.01 | -9.75 | 0.39 | 0.0 | 0.4 | 0.0 |

## Shared neuron candidates

| layer | neuron | mean_abs_activation | activation_std | sharedness |
| --- | --- | --- | --- | --- |
| 3 | 5 | 1.64962890625 | 0.0385586598368393 | 42.78121003219975 |
| 6 | 410 | 1.8966796875 | 0.0530326489346642 | 35.7637033393016 |
| 5 | 1966 | 1.49931640625 | 0.0605732521929076 | 24.751711362035586 |
| 8 | 65 | 2.2178125 | 0.091137291266391 | 24.334585048533377 |
| 6 | 1548 | 2.190703125 | 0.0934343318338306 | 23.44619623009463 |
| 17 | 492 | 2.25060546875 | 0.0966073336421834 | 23.29618350613271 |
| 10 | 1112 | 2.698984375 | 0.1181675425623905 | 22.840125776917265 |
| 6 | 1277 | 1.44912109375 | 0.0674345221653055 | 21.488987513105496 |
| 7 | 224 | 1.4473046875 | 0.0680338118022196 | 21.27300199943789 |
| 9 | 173 | 1.40306640625 | 0.0695560190038438 | 20.171456832738397 |
| 17 | 798 | 2.2093359375 | 0.1153443529748361 | 19.15409576996128 |
| 10 | 1454 | 1.569296875 | 0.083481634804365 | 18.79788387941424 |

## Best prompt outcomes

| country | prompt_family | expected_capital | top_prediction | target_rank | exact_match | contains_expected |
| --- | --- | --- | --- | --- | --- | --- |
| Afghanistan | declarative | Kabul | Kabul | 1 | 1.0 | 1.0 |
| Afghanistan | qa | Kabul | Kabul | 1 | 1.0 | 1.0 |
| Afghanistan | chat_template | Kabul | Kabul | 1 | 1.0 | 1.0 |
| Angola | declarative | Luanda | Lu | 1 | 1.0 | 1.0 |
| Argentina | declarative | Buenos Aires | Buenos | 1 | 1.0 | 1.0 |
| Argentina | qa | Buenos Aires | Buenos | 1 | 1.0 | 1.0 |
| Armenia | declarative | Yerevan | Yerevan | 1 | 1.0 | 1.0 |
| Armenia | qa | Yerevan | Yerevan | 1 | 1.0 | 1.0 |
| Armenia | chat_template | Yerevan | Yerevan | 1 | 1.0 | 1.0 |
| Australia | declarative | Canberra | Canberra | 1 | 1.0 | 1.0 |