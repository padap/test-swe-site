---
header: Dynamic alternative to SWE-bench
navHome: Main
navLeaderboard: Leaderboard
posterAlt: SWE-MERA EMNLP poster
---
# Introduction

SWE-bench is the current standard for evaluating coding agents on tasks derived from real GitHub repositories. However, the dataset is static, has not been updated for over two years, and has likely partially leaked into model training data (both during pretraining and SFT). This undermines evaluation reliability, as models may reproduce memorized solutions instead of genuinely solving tasks.

**SWE-MERA** addresses these issues through a dynamic approach: tasks are automatically collected from GitHub and regularly updated. This helps maintain relevance, reduce the risk of data leakage, and provide a more reliable evaluation.

<section class="paper-section">
<p class="paper-publication">Paper was published at <a href="https://aclanthology.org/2025.emnlp-demos.30/" target="_blank" rel="noopener noreferrer">EMNLP 2025</a>.</p>
<button class="poster-thumb-button" type="button" onclick="openPoster()" aria-label="Open SWE-MERA poster">
<img src="./assets/EMNLP_SWE-MERA.png" alt="SWE-MERA EMNLP poster" />
</button>
</section>

## Resources
- **Paper:** [SWE-MERA: A Dynamic Benchmark for Agenticly Evaluating Large Language Models on Software Engineering Tasks (EMNLP 2025)](https://aclanthology.org/2025.emnlp-demos.30/)
- **Dataset:** [Hugging Face](https://huggingface.co/datasets/MERA-evaluation/SWE-MERA)
- **Python Package:** [repositorytest on PyPI](https://pypi.org/project/repositorytest)
- **Source Code:** [GitHub Repository](https://github.com/MERA-Evaluation/repotest)
- **Submissions:** [GitHub Submissions](https://github.com/MERA-Evaluation/SWE-MERA-submissions)
- **Leaderboard:** [View Rankings](#/leaderboard)
- **Contact:** [mera@a-ai.ru](mailto:mera@a-ai.ru)

# Details
## Methodology

### Seven-Stage Collection Pipeline

SWE-MERA implements a robust seven-stage pipeline that effectively ensures quality and minimizes contamination risks:

1. **Repository Selection:** Python repositories with 10+ stars, 10+ forks, recent activity, and open-source licenses
2. **PR-Issue Mapping Construction:** One-to-one mappings between merged pull requests and closed issues
3. **Metadata Extraction and Filtering:** Issue and PR metadata parsed and filtered by description length
4. **Patch Extraction and Validation:** Git diffs validated to ensure both source code and test modifications
5. **Repository Build Validation:** Docker-based environment setup with pytest execution verification
6. **End-to-End Task Execution:** Controlled environment testing for reproducibility
7. **LLM-based Quality Assessment:** Qwen3-32B model evaluates task correctness, test correctness, test completeness, and complexity

### Dataset Statistics

- **Scale:** Approximately 10,000 potential tasks identified
- **Current Availability:** 728 validated samples from 200+ repositories
- **Update Frequency:** Quarterly updates with new real-world issues
- **Execution Environment:** Docker-based containers with standardized base images
- **Quality Assurance:** Multi-stage filtering and LLM-based validation

The entire pipeline is implemented as a [Python package](https://pypi.org/project/repositorytest) and can be executed for any GitHub repository, facilitating reproducibility and extensibility.

## Key Features

### Dynamic Updates

Unlike static benchmarks, SWE-MERA is refreshed quarterly with new, unseen issues. This continuous update cycle:
- Reflects the latest software development challenges
- Minimizes risks of model memorization
- Maintains benchmark discriminative power over time
- Enables detection of data contamination through temporal analysis

### Quality Validation

Each task undergoes rigorous validation:
- **Automated Testing:** pytest-based verification in isolated Docker environments
- **LLM-based Filtering:** Bottom quartile tasks filtered based on correctness and completeness scores
- **Real-world Relevance:** Only tasks with actual solutions and comprehensive tests are retained
- **Complexity Balance:** Both easy and difficult tasks preserved for comprehensive evaluation

### Contamination Detection

The [interactive leaderboard](#/leaderboard) features a temporal slider enabling users to visualize evaluation metrics across different time periods, identify potential contamination events in model training data, compare performance on pre- and post-cutoff tasks, and ensure transparent and reproducible evaluation.

## Evaluation

SWE-MERA demonstrates strong discriminative power across state-of-the-art models. Evaluation using the Aider coding agent on a dozen recent LLMs shows clear performance stratification. The benchmark employs two key metrics: pass@1 (success rate on the first attempt) and pass@6 (success rate across six independent attempts).

Year-over-year comparison reveals interesting patterns, with certain models showing performance differences between 2024 and 2025 tasks, potentially indicating varying degrees of data exposure.

![Model Performance Comparison](./assets/metrics.png)

Detailed evaluation results and model trajectories are available on the [leaderboard](#/leaderboard).

## Submission Workflow

To participate in SWE-MERA evaluation:

1. **Download Dataset:** Access from [Hugging Face](https://huggingface.co/datasets/MERA-evaluation/SWE-MERA)
2. **Run Agent:** Execute your software engineering agent on the dataset
3. **Submit Results:** Create a pull request to the [submissions repository](https://github.com/MERA-Evaluation/SWE-MERA-submissions)
4. **Leaderboard Update:** Valid submissions appear within two working days
