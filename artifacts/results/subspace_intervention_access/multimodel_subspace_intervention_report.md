# Subspace Intervention Summary

| model_name | best_family | worst_family | patch_align_delta | project_align_delta | patch_f1_delta | project_f1_delta |
| --- | --- | --- | --- | --- | --- | --- |
| gemma_270m_base | declarative | qa | 0.0098 | -0.1113 | 0.0583 | -0.0752 |
| gemma_270m_it | raw_question | declarative | -0.0126 | -0.0581 | -0.0817 | -0.1530 |
| qwen2_5_0_5b_base | qa | raw_question | 0.0005 | -0.0184 | -0.0063 | -0.0681 |
| qwen2_5_0_5b_instruct | chat_template | declarative | -0.0128 | -0.0450 | -0.0191 | -0.0583 |
| smollm2_360m_base | qa | chat_template | -0.0018 | -0.0186 | -0.0206 | -0.0901 |
| smollm2_360m_instruct | chat_template | qa | -0.0010 | -0.0127 | 0.0000 | 0.0500 |