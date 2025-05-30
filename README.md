<h1 align='center' style="text-align:center; font-weight:bold; font-size:2.0em;letter-spacing:2.0px;">
                VideoConviction: A Multimodal Benchmark for Human Conviction and Stock Market Recommendations</h1>                

<p align="center">
  <a href="https://arxiv.org/abs/2502.02696">
    <img src="https://img.shields.io/badge/arXiv-2502.02696-b31b1b" alt="arXiv PDF">
  </a>
  <a href="[https://videoconviction.com/leaderboard](https://huggingface.co/spaces/gtfintechlab/VideoConvictionLeaderboard)">
    <img src="https://img.shields.io/badge/Leaderboard-View-blueviolet?logo=ranking" alt="Leaderboard">
  </a>
  <a href="https://huggingface.co/datasets/gtfintechlab/VideoConviction">
    <img src="https://img.shields.io/badge/Dataset-HuggingFace-orange?logo=huggingface" alt="Hugging Face Dataset">
  </a>
  <a href="https://youtu.be/4tJTEmNbt-Y?si=NyUCWoTovQIhYZG5">
    <img src="https://img.shields.io/badge/Presentation-YouTube-red?logo=youtube" alt="YouTube Presentation">
  </a>
</p>

<p align="center">
  <a href="https://www.linkedin.com/in/michaelgalarnyk/">Michael Galarnyk*</a>,
  <a href="https://www.linkedin.com/in/veerkejriwal/">Veer Kejriwal*</a>,
  <a href="https://shahagam4.github.io/">Agam Shah*</a>,
  <a href="https://www.linkedin.com/in/yash-bhardwaj-tech/">Yash Bhardwaj</a>,
  <a href="https://www.linkedin.com/in/nicholaswatney/">Nicholas Watney Meyer</a>,<br/>
  <a href="https://www.linkedin.com/in/anandmkrishnan/">Anand Krishnan</a>,
  <a href="https://www.scheller.gatech.edu/directory/faculty/chava/index.html">Sudheer Chava</a><br/>
Georgia Institute of Technology<br/>
</p>

<p align="center"><em>*Authors contributed equally</em></p>


## Abstract

Social media has amplified the reach of financial influencers known as "finfluencers," who share stock recommendations on platforms like YouTube. Understanding their influence requires analyzing
multimodal signals like tone, delivery style, and facial expressions, which extend beyond text based financial analysis. We introduce VideoConviction, a multimodal dataset with 6,000+ expert annotations, produced through 457 hours of human effort, to benchmark multimodal large language models (MLLMs) and text-based large language models (LLMs) in financial discourse. Our results show that while multimodal inputs improve stock ticker extraction (e.g., extracting Apple’s ticker AAPL), both MLLMs and LLMs struggle to distinguish investment actions and conviction—the strength of belief conveyed through confident delivery and detailed reasoning—often misclassifying general commentary as definitive recommendations. While high-conviction recommendations perform better than low-conviction ones, they still underperform the popular S&P 500 index fund. An inverse strategy—betting against finfluencer recommendations—outperforms the S&P 500 by 6.8% in annual returns but carries greater risk (Sharpe ratio of 0.41 vs. 0.65). Our benchmark enables a diverse evaluation of multimodal tasks, comparing model performance on both full video and segmented video inputs. This enables deeper advancements in multimodal financial research. 

## Repository Overview
This repository contains the code and data pipelines used in our research on multimodal financial recommendations from YouTube content. It is organized into five primary subdirectories:

```
VideoConviction
├── back_testing/
├── data_analysis/
├── process_annotations_pipeline/
├── prompting/
├── youtube_data_pipeline/
├── .gitignore
├── LICENSE
└── README.md
```
Below is a high-level summary of each subdirectory’s purpose. Please refer to each subdirectory’s `README.md` for detailed instructions, usage examples, and more specific documentation.

----------

### 1. back_testing/

**Purpose**:  
Implements a comprehensive framework for **backtesting** various equity trading strategies derived from finfluencer recommendations.

----------

### 2. data_analysis/

**Purpose**:  
Houses Jupyter notebooks for **exploratory data analysis (EDA)** on the annotated dataset.

----------

### 3. process_annotations_pipeline/

**Purpose**:  
Provides a multi-step pipeline to **validate**, **clean**, and **merge** annotations with video transcripts and metadata.

----------

### 4. prompting/

**Purpose**:  
Contains code and notebooks for **prompt engineering** and **model inference** with large language models (LLMs) and multimodal large language models (MLLMs).

----------

### 5. youtube_data_pipeline/

**Purpose**:  
Implements an **end-to-end YouTube data pipeline**. 

----------

## Getting Started

1.  **Clone the Repository**
    
    ```
    git clone https://github.com/yourusername/VideoConviction.git
    cd VideoConviction
    ```
    
2.  **Install Dependencies**  
    - If the subdirectory is .py based, it will have includes its own `environment.yaml` file (if files are .py based) and installation scripts (`install.sh` or instructions in the README). 
    - If it has .ipynb notebooks, the respective will have the necessary commands to add those dependencies
4.  **Explore Subdirectories**
    -   **Data Collection**: Start with `youtube_data_pipeline` to collect and transcribe videos.
    -   **Annotation & Merging**: Move to `process_annotations_pipeline` to generate the final annotated dataset (`complete_dataset.csv`).
    -   **Analysis & Modeling**: Use `data_analysis` for EDA, `prompting` for LLM/MLLM inference, and `back_testing` to test trading strategies based on the recommendations.

----------

## Usage Flow (High-Level)

1.  **YouTube Data Collection**
    -   Gather videos (metadata, comments, transcripts) using `youtube_data_pipeline`.
2.  **Annotation & Merging**
    -   Combine and clean annotations, transcripts, and metadata in `process_annotations_pipeline`.
3.  **Exploratory Data Analysis**
    -   Perform EDA in `data_analysis` to understand distributions, correlations, and dataset quality.
4.  **Model Prompting & Inference**
    -   Generate prompts for text or multimodal LLMs in `prompting`, run inference, and evaluate performance.
5.  **Backtesting**
    -   Evaluate different trading strategies on the annotated dataset in `back_testing`, measuring returns, Sharpe ratio, etc.

----------

## License

The dataset is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC-BY-NC-SA 4.0) license, which allows others to share, copy, distribute, and transmit the work, as well as to adapt the work, provided that appropriate credit is given, a link to the license is provided, and any changes made are indicated.

## Citation

```bibtex
@inproceedings{,
    title = { VideoConviction: A Multimodal Benchmark for Human Conviction and Stock Market Recommendations},
    author = {},
    booktitle = "",
    publisher = "",
    year = {2025},
    url = "",
    doi = ""
    pages = "",
    abstract = ""
}
```


