# 🃏 Heart of the Cards

This is the repository for the **Heart of the Cards** blog series, a data science project focused on Yu-Gi-Oh! (YGO) card data. The project leverages datasets routinely pulled from the YGOProDeck API to practice data science techniques, including NLP topic modeling, LLM-based categorization, utility modeling (Bradley-Terry), pricing trends, and banlist prediction.

You can find the blog here: [Include Link].

---

## 📂 Repository Structure

The project is organized into the following directories:

### ⚙️ [Code](file:///Users/mlchrzan/github/Heart-of-the-Cards/Code)
Contains the analysis notebooks, pipeline scripts, and utility modules:
- [full_pull.py](file:///Users/mlchrzan/github/Heart-of-the-Cards/Code/full_pull.py) / [full_pull.ipynb](file:///Users/mlchrzan/github/Heart-of-the-Cards/Code/full_pull.ipynb): Fetches full card set details, pricing, banlist statuses, and release dates from the YGOProDeck API.
- [utils.py](file:///Users/mlchrzan/github/Heart-of-the-Cards/Code/utils.py): Utility functions for loading daily/full pulls and configuring frame colors by card type.
- [LLM_categorization.ipynb](file:///Users/mlchrzan/github/Heart-of-the-Cards/Code/LLM_categorization.ipynb): Categorizes cards into functional roles (e.g., Starter, Extender, Board Breaker, Hand Trap) using LLMs.
- [ygo topic BERT.ipynb](file:///Users/mlchrzan/github/Heart-of-the-Cards/Code/ygo%20topic%20BERT.ipynb): Performs topic modeling and NLP on card description texts using BERT.
- [pairadigm.ipynb](file:///Users/mlchrzan/github/Heart-of-the-Cards/Code/pairadigm.ipynb): Analyzes card pairings and computes utility ratings.
- [banlist_scrape_YGOPRO.ipynb](file:///Users/mlchrzan/github/Heart-of-the-Cards/Code/banlist_scrape_YGOPRO.ipynb): Scrapes historical banlist data.
- [demograph explore.ipynb](file:///Users/mlchrzan/github/Heart-of-the-Cards/Code/demograph%20explore.ipynb): Exploratory data analysis (EDA) of card- and set-level demographics.
- **[In the Works/](file:///Users/mlchrzan/github/Heart-of-the-Cards/Code/In%20the%20Works)**: Active experiments including archetype support analysis (`archtype support.ipynb`) and banlist predictions (`predict_banlist.ipynb`).

### 📊 [Data](file:///Users/mlchrzan/github/Heart-of-the-Cards/Data)
Hosts both automated pulls and curated reference datasets:
- **Auto Pulls/ & Auto Set Pulls/**: Automated daily incremental snapshots of card details based on an R script that's a few years old that runs automatically on my local device. Too lazy to turn it off.
- **Full Pulls/**: Full-scale periodic snapshots of the entire card database. Was originally run manually, but on 07/18/2026 it was automated via GitHub Actions to run daily at 8PM EST. 
- `banlist_history_*.csv`: Historical banlist records. Scrapped periodically from YGOPRODECK. 
- `categorized_cards.csv`: Annotation file I was working on with some friends. Currently on hold. 
- `cgcot_*.csv`: Card pairings, annotations, and Bradley-Terry score tables for practicing with the `pairadigm` package.
- `ygo_cards_w_topics.csv`: Cards labeled with topics generated from BERT topic modeling.

### 📈 [Results](file:///Users/mlchrzan/github/Heart-of-the-Cards/Results)
(WIP) Contains models and prepped data for visualization.

---

## 🤖 Automation Workflow

We run an automated pipeline to pull the latest card data from the YGOProDeck API.
- **Daily Pull Job**: Triggered daily at **8:00 PM EST** via a GitHub Actions workflow defined in [.github/workflows/daily_pull.yml](file:///Users/mlchrzan/github/Heart-of-the-Cards/.github/workflows/daily_pull.yml). It runs the [full_pull.py](file:///Users/mlchrzan/github/Heart-of-the-Cards/Code/full_pull.py) script and pushes the updated data back to the repository.

---

## 📝 Data Quality Notes

### Better Late than Never, but Also Sometimes Never
Since I used to pull the code automatically using a script that runs whenever my laptop is open, if I forget to open my laptop any evening (😅) it doesn't run. I usually do a good job, but there have been a few "morning after" pulls, so to speak. Here are the dates for those. You can also use the dates in the file names to indicate days that were completely missed.

- `2025_08_10` pulled on the morning of `2025_08_11`
- `2025_09_12` pulled on the morning of `2025_09_13`
- `2025_10_04` pulled on the morning of `2025_10_05`
- `2025_10_21` pulled right after midnight on `2025_10_22`, 29 minutes after the 11:59 time noted
- `2025_11_09` pulled right after midnight on `2025_11_08`, 17 minutes after the 11:59 time noted
- `2025_11_30` pulled on the morning of `2025_12_01`
- `2025_12_23` pulled on the morning of `2025_12_24`
- `2025_12_24` pulled on the morning of `2025_12_25`
 