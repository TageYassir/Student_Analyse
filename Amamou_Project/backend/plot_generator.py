# plot_generator.py
import matplotlib.pyplot as plt
import seaborn as sns
import os
import pandas as pd

# Configuration
sns.set_style("whitegrid")
plt.rcParams["figure.figsize"] = (10, 6)
plt.rcParams['figure.facecolor'] = 'white'

# Helper function to wrap long labels
def wrap_labels(text, max_length):
    return '\n'.join([text[i:i + max_length] for i in range(0, len(text), max_length)])

def generate_all_plots(csv_path, output_dir="individual_plots"):
    df = pd.read_csv(csv_path)
    os.makedirs(output_dir, exist_ok=True)

    # ===== 1. Numeric Columns =====
    numeric_cols = ['Mark', 'Validated_Semesters', 'Repeated_Semesters', 'Failed_Semesters', 'Duration']
    for col in numeric_cols:
        if col in df.columns:
            plt.figure()
            sns.histplot(df[col], kde=True, bins=30, color='skyblue')
            plt.title(f'Distribution of {col}', pad=20)
            plt.xlabel(col)
            plt.ylabel("Frequency")
            plt.tight_layout()
            plt.savefig(f"{output_dir}/{col}_distribution.png", dpi=300, bbox_inches='tight')
            plt.close()

    # ===== 2. Categorical Columns =====
    categorical_cols = ['Gender', 'Scholarship', 'Nationality', 'Baccalaureat_Type', 'Start_Year', 'Graduated']
    for col in categorical_cols:
        if col in df.columns:
            plt.figure(figsize=(10, 6))
            ax = sns.countplot(x=df[col], palette="Set2", order=df[col].value_counts().index)
            plt.title(f'Distribution of {col}', pad=20)
            plt.xlabel(col)
            plt.ylabel("Count")

            if len(df[col].unique()) > 5:
                plt.xticks(rotation=45)

            total = len(df[col])
            for p in ax.patches:
                height = p.get_height()
                ax.text(p.get_x() + p.get_width() / 2., height + 3,
                        f'{height / total:.1%}',
                        ha="center", fontsize=10)

            plt.tight_layout()
            plt.savefig(f"{output_dir}/{col}_countplot.png", dpi=300, bbox_inches='tight')
            plt.close()

    # ===== 3. School and Specialty =====
    special_columns = {
        'School': {
            'figsize': (12, 8), 'rotation': 75, 'label_wrap': 15,
            'palette': "viridis", 'max_categories': 15
        },
        'Specialty': {
            'figsize': (14, 10), 'rotation': 90, 'label_wrap': 20,
            'max_categories': 15, 'palette': "rocket"
        }
    }

    for col in ['School', 'Specialty']:
        if col in df.columns:
            config = special_columns[col]
            top_categories = df[col].value_counts().nlargest(config['max_categories']).index
            plot_data = df[df[col].isin(top_categories)]

            plt.figure(figsize=config['figsize'])
            ax = sns.countplot(
                x=col,
                data=plot_data,
                order=plot_data[col].value_counts().index,
                palette=config['palette']
            )

            labels = [wrap_labels(str(x.get_text()), config['label_wrap']) for x in ax.get_xticklabels()]
            ax.set_xticklabels(labels, rotation=config['rotation'], ha='right')

            plt.title(f'Distribution of {col} (Top {config["max_categories"]} Categories)', pad=20)
            plt.xlabel("")
            plt.ylabel("Count")

            total = len(plot_data[col].dropna())
            for p in ax.patches:
                height = p.get_height()
                ax.annotate(
                    f'{height}\n({height / total:.1%})',
                    (p.get_x() + p.get_width() / 2., height),
                    ha='center', va='center',
                    xytext=(0, 5),
                    textcoords='offset points'
                )

            plt.tight_layout()
            plt.savefig(f"{output_dir}/{col}_countplot.png", dpi=300, bbox_inches='tight')
            plt.close()

    # ===== 4. Semester Performance Trends =====
    semester_cols = [f'S{i}' for i in range(1, 13)]
    if all(col in df.columns for col in semester_cols):
        semester_stats = pd.DataFrame({
            'Semester': semester_cols,
            'Validation_Rate': [df[col].eq('validate').mean() for col in semester_cols],
            'Repeated_Rate': [df[col].eq('repeated').mean() for col in semester_cols],
            'Failed_Rate': [df[col].eq('no validate').mean() for col in semester_cols]
        })

        semester_stats = semester_stats.melt(id_vars='Semester', var_name='Status', value_name='Rate')

        plt.figure(figsize=(12, 6))
        sns.lineplot(data=semester_stats, x='Semester', y='Rate', hue='Status',
                     marker='o', palette='Set2')
        plt.title('Semester Performance Trends', pad=20)
        plt.ylabel('Proportion of Students')
        plt.xticks(rotation=45)
        plt.ylim(0, 1)
        plt.tight_layout()
        plt.savefig(f"{output_dir}/semester_performance_trends.png", dpi=300, bbox_inches='tight')
        plt.close()

    print(f"✅ Plots saved in '{output_dir}/'")
