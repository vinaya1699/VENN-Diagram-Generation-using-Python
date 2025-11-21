**🧬 Venn Diagram Generator for RNA-seq Normalized Counts**

This script creates 2-set Venn diagrams and Excel summaries from normalized RNA-seq count data.
It compares two user-specified experimental groups and identifies:

Genes unique to Group 1

Genes unique to Group 2

Common genes expressed in both groups

It also exports gene lists and summary statistics to an Excel file.

**📌 Usage**

python Venn_Diagram.py normCounts.csv metadata.txt group1 group2

**Inputs**

1.normCounts.csv
CSV file with normalized counts
First column must contain gene IDs (named Unnamed: 0)
Remaining columns are sample names

2.metadata.txt
Tab-delimited file
Must contain columns:
Sample → sample names matching columns in normCounts.csv
Condition → group/condition label for each sample

3.group1, group2
Condition names exactly as present in metadata.txt

🛠️ Dependencies
pandas
numpy
matplotlib
matplotlib-venn
openpyxl

📁 Output Example Structure
venn_Treated_vs_Control.png
Venn_Analysis_Treated_vs_Control.xlsx
    ├── Summary
    ├── Treated_Unique
    ├── Control_Unique
    └── Common

<img width="1906" height="1518" alt="venn_Salinity_Stress_vs_Control" src="https://github.com/user-attachments/assets/e911ce47-8eaf-4d5b-bd39-485b73e48d49" />




