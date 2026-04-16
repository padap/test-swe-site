---
header: SWE-MERA – a dynamic alternative to SWE-bench
navHome: Main
navLeaderboard: Leaderboard
---

# Introduction

The rapid advancement of Large Language Models (LLMs) in software engineering has revealed critical limitations in existing benchmarks, particularly the widely used SWE-bench dataset. Recent studies have uncovered severe data contamination issues, where a significant portion of successful patches involve direct solution leakage or pass due to inadequate test cases. **SWE-MERA** addresses these fundamental challenges through an automated collection of real-world GitHub issues and rigorous quality validation.

The complexity of real-world software development encompasses coding agents and a range of text-to-code tasks. While SWE-bench was created from GitHub issues and their corresponding pull requests, its **static nature** leads to two major problems: *data leakage* (models memorizing solutions) and *benchmark saturation* (losing effectiveness as models achieve near-perfect scores).

SWE-MERA introduces **dynamic quarterly updates** to ensure: (1) real-world relevance — tasks reflect the latest challenges in software development; (2) fair evaluation — models are tested on fresh problems, minimizing data leakage; (3) continuous improvement — the benchmark evolves with advancements in AI and software engineering practices.

# Methodology

## Seven-Stage Collection Pipeline

SWE-MERA implements a robust seven-stage pipeline that effectively ensures quality and minimizes contamination risks:

1. **Repository Selection:** Python repositories with 10+ stars, 10+ forks, recent activity, and open-source licenses
2. **PR-Issue Mapping Construction:** One-to-one mappings between merged pull requests and closed issues
3. **Metadata Extraction and Filtering:** Issue and PR metadata parsed and filtered by description length
4. **Patch Extraction and Validation:** Git diffs validated to ensure both source code and test modifications
5. **Repository Build Validation:** Docker-based environment setup with pytest execution verification
6. **End-to-End Task Execution:** Controlled environment testing for reproducibility
7. **LLM-based Quality Assessment:** Qwen3-32B model evaluates task correctness, test correctness, test completeness, and complexity

## Dataset Statistics

- **Scale:** Approximately 10,000 potential tasks identified
- **Current Availability:** 728 validated samples from 200+ repositories
- **Update Frequency:** Quarterly updates with new real-world issues
- **Execution Environment:** Docker-based containers with standardized base images
- **Quality Assurance:** Multi-stage filtering and LLM-based validation

The entire pipeline is implemented as a [Python package](https://pypi.org/project/repositorytest) and can be executed for any GitHub repository, facilitating reproducibility and extensibility.

# Key Features

## Dynamic Updates

Unlike static benchmarks, SWE-MERA is refreshed quarterly with new, unseen issues. This continuous update cycle:
- Reflects the latest software development challenges
- Minimizes risks of model memorization
- Maintains benchmark discriminative power over time
- Enables detection of data contamination through temporal analysis

## Quality Validation

Each task undergoes rigorous validation:
- **Automated Testing:** pytest-based verification in isolated Docker environments
- **LLM-based Filtering:** Bottom quartile tasks filtered based on correctness and completeness scores
- **Real-world Relevance:** Only tasks with actual solutions and comprehensive tests are retained
- **Complexity Balance:** Both easy and difficult tasks preserved for comprehensive evaluation

## Contamination Detection

The [interactive leaderboard](#/leaderboard) features a temporal slider enabling users to visualize evaluation metrics across different time periods, identify potential contamination events in model training data, compare performance on pre- and post-cutoff tasks, and ensure transparent and reproducible evaluation.

# Evaluation

SWE-MERA demonstrates strong discriminative power across state-of-the-art models. Evaluation using the Aider coding agent on a dozen recent LLMs shows clear performance stratification. The benchmark employs two key metrics: pass@1 (success rate on the first attempt) and pass@6 (success rate across six independent attempts).

Year-over-year comparison reveals interesting patterns, with certain models showing performance differences between 2024 and 2025 tasks, potentially indicating varying degrees of data exposure.

![Model Performance Comparison](./assets/metrics.png)

Detailed evaluation results and model trajectories are available on the [leaderboard](#/leaderboard).

# Submission Workflow

To participate in SWE-MERA evaluation:

1. **Download Dataset:** Access from [Hugging Face](https://huggingface.co/datasets/MERA-evaluation/SWE-MERA)
2. **Run Agent:** Execute your software engineering agent on the dataset
3. **Submit Results:** Create a pull request to the [submissions repository](https://github.com/MERA-Evaluation/SWE-MERA-submissions)
4. **Leaderboard Update:** Valid submissions appear within two working days

# Resources

- **Dataset:** [Hugging Face](https://huggingface.co/datasets/MERA-evaluation/SWE-MERA)
- **Python Package:** [repositorytest on PyPI](https://pypi.org/project/repositorytest)
- **Source Code:** [GitHub Repository](https://github.com/MERA-Evaluation/repotest)
- **Submissions:** [GitHub Submissions](https://github.com/MERA-Evaluation/SWE-MERA-submissions)
- **Leaderboard:** [View Rankings](#/leaderboard)
- **Contact:** [mera@a-ai.ru](mailto:mera@a-ai.ru)
