# Subspace Intervention Summary

| model_name | layer_strategy | best_family | worst_family | patch_fact_align | patch_ctrl_align | project_fact_align | project_ctrl_align | patch_fact_f1 | patch_ctrl_f1 | project_fact_f1 | project_ctrl_f1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| gemma_270m_base | plus_one | declarative | qa | 0.0086 | -0.0385 | -0.1146 | -0.0736 | 0.0824 | 0.0016 | -0.1425 | -0.1004 |
| gemma_270m_base | primary | declarative | qa | 0.0096 | -0.0486 | -0.1391 | -0.0439 | 0.0488 | -0.0684 | -0.0993 | -0.0709 |
| gemma_270m_it | plus_one | raw_question | declarative | 0.0018 | -0.0305 | -0.0836 | -0.0521 | -0.0405 | -0.1519 | -0.2704 | -0.2204 |
| gemma_270m_it | primary | raw_question | declarative | -0.0077 | -0.0325 | -0.0611 | -0.0110 | -0.1058 | -0.1283 | -0.1628 | -0.1004 |
| qwen2_5_0_5b_base | plus_one | qa | raw_question | -0.0012 | -0.0079 | -0.0265 | -0.0009 | -0.0125 | 0.0358 | 0.0578 | 0.0514 |
| qwen2_5_0_5b_base | primary | qa | raw_question | -0.0014 | -0.0061 | -0.0278 | -0.0031 | -0.0125 | -0.0125 | -0.0072 | 0.0028 |
| qwen2_5_0_5b_instruct | plus_one | chat_template | declarative | -0.0262 | -0.0396 | -0.0750 | -0.0056 | -0.0158 | -0.0186 | -0.0583 | -0.0072 |
| qwen2_5_0_5b_instruct | primary | chat_template | declarative | -0.0245 | -0.0402 | -0.0692 | -0.0055 | -0.0145 | -0.0063 | 0.0050 | -0.0303 |
| smollm2_360m_base | plus_one | qa | chat_template | -0.0009 | -0.0050 | -0.0164 | -0.0032 | -0.0512 | -0.0706 | -0.0985 | -0.0316 |
| smollm2_360m_base | primary | qa | chat_template | -0.0004 | -0.0050 | -0.0172 | -0.0058 | -0.0486 | -0.0835 | -0.0700 | -0.0514 |
| smollm2_360m_instruct | plus_one | chat_template | qa | 0.0036 | 0.0029 | -0.0154 | 0.0016 | 0.0824 | 0.1224 | -0.0461 | 0.1150 |
| smollm2_360m_instruct | primary | chat_template | qa | -0.0014 | -0.0030 | -0.0108 | 0.0047 | 0.0000 | 0.0400 | 0.0746 | 0.0621 |