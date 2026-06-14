# Capital Prompt Study

- Prompts analyzed: 20
- Mean exact match: 0.3500
- Mean contains-expected: 0.3500
- Mean target rank: 380.25
- Mean target margin: -3.4188
- Strongest shared layer by mean MLP activity: 0
- Best prompt family by target rank: declarative

## Prompt family comparison

| prompt_family | target_rank_mean | target_rank_median | target_margin_mean | target_margin_median | exact_match_mean | exact_match_median | contains_expected_mean | contains_expected_median |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| chat_template | 1489.2 | 75.0 | -9.525 | -8.75 | 0.2 | 0.0 | 0.2 | 0.0 |
| declarative | 1.0 | 1.0 | 3.475 | 2.5 | 0.4 | 0.0 | 0.4 | 0.0 |
| qa | 3.4 | 1.0 | 0.9625 | 1.0 | 0.4 | 0.0 | 0.4 | 0.0 |
| raw_question | 27.4 | 24.0 | -8.5875 | -9.5625 | 0.4 | 0.0 | 0.4 | 0.0 |

## Shared neuron candidates

| layer | neuron | mean_abs_activation | activation_std | sharedness |
| --- | --- | --- | --- | --- |
| 3 | 5 | 1.63984375 | 0.0387408633381794 | 42.32743623314473 |
| 6 | 410 | 1.891015625 | 0.0491923912553748 | 38.440440407600285 |
| 5 | 1966 | 1.495703125 | 0.0542096871928521 | 27.5905582911927 |
| 14 | 490 | 1.88671875 | 0.0708960162293164 | 26.612103729406712 |
| 17 | 492 | 2.25234375 | 0.0896601384656944 | 25.120624035593497 |
| 8 | 65 | 2.22578125 | 0.0902301473576736 | 24.66754901361353 |
| 6 | 1277 | 1.427734375 | 0.0590283362667615 | 24.186861403080595 |
| 6 | 1548 | 2.18828125 | 0.0905003183264429 | 24.17955108793837 |
| 10 | 1112 | 2.6953125 | 0.1133754995854483 | 23.773114444838075 |
| 7 | 224 | 1.45859375 | 0.0618175633037448 | 23.59475329171297 |
| 17 | 798 | 2.184765625 | 0.1026169718902379 | 21.290282635256776 |
| 17 | 1026 | 2.659375 | 0.1380493288194477 | 19.263807791998268 |

## Best prompt outcomes

| country | prompt_family | expected_capital | top_prediction | target_rank | exact_match | contains_expected |
| --- | --- | --- | --- | --- | --- | --- |
| Afghanistan | declarative | Kabul | Kabul | 1 | 1.0 | 1.0 |
| Afghanistan | qa | Kabul | Kabul | 1 | 1.0 | 1.0 |
| Afghanistan | chat_template | Kabul | Kabul | 1 | 1.0 | 1.0 |
| Angola | declarative | Luanda | Lu | 1 | 1.0 | 1.0 |
| Angola | qa | Luanda | The | 8 | 1.0 | 1.0 |
| Angola | raw_question | Luanda | 

 | 24 | 1.0 | 1.0 |
| Afghanistan | raw_question | Kabul | 

 | 35 | 1.0 | 1.0 |
| Albania | declarative | Tirana | Tir | 1 | 0.0 | 0.0 |
| Albania | qa | Tirana | Tir | 1 | 0.0 | 0.0 |
| Algeria | declarative | Algiers | Al | 1 | 0.0 | 0.0 |