import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib_venn import venn2
from matplotlib_venn import venn2_unweighted ,venn2_circles

plt.rcParams['font.family'] = 'FreeSerif'

# --- Parse Command Line Arguments ---
# Usage: python script.py normCounts.csv metadata.txt group1 group2

if len(sys.argv) != 5:
    print("Usage: python script.py normCounts.csv metadata.txt group1 group2")
    sys.exit(1)

norm_counts_file = sys.argv[1]
metadata_file = sys.argv[2]
group1 = sys.argv[3]
group2 = sys.argv[4]

# --- Load Data ---
ncts = pd.read_csv(norm_counts_file, sep=",")
ncts.set_index('Unnamed: 0', inplace=True)
metadata = pd.read_table(metadata_file, sep="\t")
groups = metadata['Condition'].unique()

# --- Compute Average Counts ---
avg_counts = pd.DataFrame(index=ncts.index)
for group in groups:
    sample_names = metadata.loc[metadata['Condition'] == group, 'Sample'].tolist()
    avg_counts[group + '_avg_ncts'] = np.mean(ncts[sample_names].to_numpy(), axis=1)

# --- Define Gene Sets for User Groups ---
group1_genes = set(avg_counts.index[avg_counts[group1 + '_avg_ncts'] > 0])
group2_genes = set(avg_counts.index[avg_counts[group2 + '_avg_ncts'] > 0])

# --- Venn Diagram ---
plt.figure(figsize=(8, 6))
venn = venn2_unweighted([group1_genes, group2_genes], set_labels=(group1, group2))
for patch in venn.patches:
    if patch:
        patch.set_edgecolor("black")
        patch.set_linewidth(1)
plt.title(f"{group1} vs {group2}", fontsize=16, fontweight='bold')
plt.savefig(f"venn_{group1}_vs_{group2}.png", bbox_inches='tight', dpi=300)
plt.close()

# --- Set Operations & Excel Export ---
only_group1 = group1_genes - group2_genes
only_group2 = group2_genes - group1_genes
both_groups = group1_genes & group2_genes

summary_data = {
    'Comparison': [f'{group1} vs {group2}'],
    f'Unique in {group1}': [len(only_group1)],
    f'Unique in {group2}': [len(only_group2)],
    'Common': [len(both_groups)],
    f'Total {group1}': [len(group1_genes)],
    f'Total {group2}': [len(group2_genes)]
}

summary_df = pd.DataFrame(summary_data)

with pd.ExcelWriter(f'Venn_Analysis_{group1}_vs_{group2}.xlsx', engine='openpyxl') as writer:
    summary_df.to_excel(writer, sheet_name='Summary', index=False)
    pd.DataFrame({'Gene': sorted(only_group1)}).to_excel(writer, sheet_name=f'{group1}_Unique', index=True)
    pd.DataFrame({'Gene': sorted(only_group2)}).to_excel(writer, sheet_name=f'{group2}_Unique', index=True)
    pd.DataFrame({'Gene': sorted(both_groups)}).to_excel(writer, sheet_name='Common', index=True)

print(f"Excel file saved: Venn_Analysis_{group1}_vs_{group2}.xlsx")
