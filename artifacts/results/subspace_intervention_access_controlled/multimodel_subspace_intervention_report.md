# Subspace Intervention Summary

| model_name | best_family | worst_family | patch_fact_align | patch_ctrl_align | project_fact_align | project_ctrl_align | patch_fact_f1 | patch_ctrl_f1 | project_fact_f1 | project_ctrl_f1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| gemma_270m_base | declarative | qa | 0.0098 | -0.0415 | -0.1113 | -0.0388 | 0.0583 | -0.0038 | -0.0752 | -0.0914 |
| gemma_270m_it | raw_question | declarative | -0.0126 | -0.0252 | -0.0581 | -0.0134 | -0.0817 | -0.0937 | -0.1530 | -0.0932 |
| qwen2_5_0_5b_base | qa | raw_question | 0.0005 | -0.0022 | -0.0184 | -0.0057 | -0.0063 | -0.0143 | -0.0681 | -0.0081 |
| qwen2_5_0_5b_instruct | chat_template | declarative | -0.0128 | -0.0304 | -0.0450 | -0.0106 | -0.0191 | -0.0182 | -0.0583 | -0.0183 |
| smollm2_360m_base | qa | chat_template | -0.0018 | -0.0053 | -0.0186 | -0.0053 | -0.0206 | -0.0342 | -0.0901 | -0.0582 |
| smollm2_360m_instruct | chat_template | qa | -0.0010 | -0.0034 | -0.0127 | 0.0018 | 0.0000 | 0.0000 | 0.0500 | 0.0601 |