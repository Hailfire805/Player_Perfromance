# Performance Score Dev Log

## 1.1 9/9/2024

- Explored different ways to calculate performance score
- I feel that the ideal system will be one focused on evaluating contributions per death
- I feel this is because the most important factor is how much a player accomplishes with their deaths
- One issue is that this excessively rewards players who have low deaths even if their actual outputs are low
- I want to also find a means to cap the maximum scores at a reasonable number without imposing a true hard limit
- I don't want to reward players playing purely for KDA without having significant contributions to the team
- I want to reward the players who are also playing roles focused on taking damage or on taking structures too
- I want to also find a way to ensure the system is objective and does not rely on the personal values of the coder.
- I do not want to use thresholds that I arbitrarily decide, but rather have the system objectively decide through some kind of method.
- I am looking to explore adding a logarithmic scale to the score to diminish returns as it grows larger for players with low deaths.