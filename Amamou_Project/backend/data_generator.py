import pandas as pd
import numpy as np
import random
from faker import Faker
from datetime import datetime

# Initialize with reproducible randomness
fake = Faker()
Faker.seed(42)
random.seed(42)
np.random.seed(42)

# Constants
N = 100_000  # Total students
ID_START = 20000
YEARS = list(range(2016, 2025))
SCHOLARSHIPS_PER_YEAR = 300

# Realistic bac type distribution
bac_distribution = {
    "Science Math": 0.35,
    "Science Physique": 0.30,
    "Technologie": 0.25,
    "Lettre": 0.10
}

# School definitions with durations, mark parameters, and graduation rates
schools = {
    "Euromed Polytechnic School (EPS)": {
        "bac_types": ["Science Physique", "Science Math", "Technologie"],
        "duration": 5,
        "mark_params": {"loc": 14.5, "scale": 2.5},
        "grad_rate": 0.92
    },
    "Ecole d'Ingénierie Digitale et d'Intelligence Artificielle (EIDIA)": {
        "bac_types": ["Science Physique", "Science Math", "Technologie"],
        "duration": 5,
        "mark_params": {"loc": 14.5, "scale": 2.5},
        "grad_rate": 0.91
    },
    "Ecole Euromed d'Architecture de Design et d'Urbanisme (EMADU)": {
        "bac_types": ["Science Physique", "Science Math", "Technologie"],
        "duration": 6,
        "mark_params": {"loc": 14.0, "scale": 2.0},
        "grad_rate": 0.88
    },
    "Faculté des Sciences Humaines et Sociales": {
        "bac_types": ["Lettre"],
        "duration": 5,
        "mark_params": {"loc": 13.5, "scale": 2.0},
        "grad_rate": 0.85
    },
    "Euromed Business School": {
        "bac_types": ["Lettre", "Science Physique", "Technologie"],
        "duration": 5,
        "mark_params": {"loc": 13.5, "scale": 2.0},
        "grad_rate": 0.87
    },
    "Institut Euromed des Sciences Juridiques et Politiques": {
        "bac_types": ["Lettre", "Science Physique", "Technologie"],
        "duration": 5,
        "mark_params": {"loc": 13.5, "scale": 2.0},
        "grad_rate": 0.86
    },
    "Faculté Euromed de Pharmacie": {
        "bac_types": ["Science Physique", "Science Math", "Technologie"],
        "duration": 6,
        "mark_params": {"loc": 14.0, "scale": 2.0},
        "grad_rate": 0.89
    },
    "Ecole d'ingénieur BiomedTech": {
        "bac_types": ["Science Physique", "Science Math", "Technologie"],
        "duration": 5,
        "mark_params": {"loc": 14.0, "scale": 2.0},
        "grad_rate": 0.90
    },
    "Faculté Euromed de Médecine": {
        "bac_types": ["Science Physique", "Science Math", "Technologie"],
        "duration": 6,
        "mark_params": {"loc": 14.0, "scale": 2.0},
        "grad_rate": 0.85
    },
    "Faculté Euromed de Médecine Dentaire": {
        "bac_types": ["Science Physique", "Science Math", "Technologie"],
        "duration": 6,
        "mark_params": {"loc": 14.0, "scale": 2.0},
        "grad_rate": 0.84
    },
    "Faculté des Sciences Infirmières et Techniques de Santé": {
        "bac_types": ["Science Physique", "Science Math", "Technologie"],
        "duration": 5,
        "mark_params": {"loc": 13.5, "scale": 2.0},
        "grad_rate": 0.88
    }
}

# Specialties with matching school names
specialties = {
    "Euromed Polytechnic School (EPS)": [
        "Génie Civil", "Génie des Opérations et de la Logistique", "Génie des Procédés",
        "Génie Mécanique, Productique et Thermique", "Génie Électrique EEA",
        "Accompagnement Entrepreneurial et Management Technologique",
        "Transports et Mobilité Durable", "Génie Environnemental et Gestion de l'Eau",
        "Conception et Ingénierie de Bâtiments Verts", "Matériaux Fonctionnels et Fabrication Additive"
    ],
    "Ecole d'Ingénierie Digitale et d'Intelligence Artificielle (EIDIA)": [
        "Intelligence Artificielle", "Robotique et Cobotique", "Cyber-sécurité",
        "Ingénierie d'Applications Web & Mobile", "Big Data Analytics",
        "ICT Security and Artificial Intelligence"
    ],
    "Ecole Euromed d'Architecture de Design et d'Urbanisme (EMADU)": [
        "Architecture", "Design", "Urbanisme et ses Territoires"
    ],
    "Faculté des Sciences Humaines et Sociales": [
        "Traduction", "Méthodes et Métiers de l'Ingénierie Culturelle",
        "Sciences Sociales et Management de la Santé",
        "Communication des Entreprises et des Institutions", "Journalisme et Nouveaux Médias"
    ],
    "Euromed Business School": [
        "Management des Organisations", "Marketing et Communication",
        "Finance et Contrôle de Gestion", "Entrepreneuriat et Innovation"
    ],
    "Institut Euromed des Sciences Juridiques et Politiques": [
        "Droit Public", "Droit Privé", "Sciences Politiques",
        "Droit International", "Gouvernance et Politiques Publiques"
    ],
    "Faculté Euromed de Pharmacie": [
        "Docteur en Pharmacie (Officine)", "Docteur en Pharmacie (Biologie Médicale)",
        "Docteur en Pharmacie (Industrie Pharmaceutique)", "Docteur en Pharmacie (Produits de Santé)",
        "Docteur en Pharmacie (Secteur Public)"
    ],
    "Ecole d'ingénieur BiomedTech": [
        "Biotechnologie", "Sciences Biomédicales",
        "Génie Biologique", "Biotechnologie Appliquée"
    ],
    "Faculté Euromed de Médecine": [
        "Médecine Générale", "Spécialités Médicales",
        "Recherche Médicale", "Santé Publique"
    ],
    "Faculté Euromed de Médecine Dentaire": [
        "Chirurgie Dentaire", "Orthodontie",
        "Parodontologie", "Prothèses Dentaires"
    ],
    "Faculté des Sciences Infirmières et Techniques de Santé": [
        "Sciences Infirmières", "Sciences de Rééducation et Réhabilitation",
        "Sciences de la Nutrition", "Techniques de Santé"
    ]
}

# Generate students with strong patterns
students = []
for i in range(N):
    # Select bac type weighted by distribution
    bac_type = random.choices(
        list(bac_distribution.keys()),
        weights=list(bac_distribution.values()),
        k=1
    )[0]

    # Select school that accepts this bac type
    eligible_schools = [s for s, info in schools.items() if bac_type in info["bac_types"]]
    school = random.choice(eligible_schools)
    school_info = schools[school]

    # Generate mark with strong correlation to graduation
    base_mark = np.random.normal(**school_info["mark_params"])
    if bac_type == "Science Math":
        base_mark += np.random.uniform(1.0, 2.0)
    elif bac_type == "Lettre":
        base_mark -= np.random.uniform(0.5, 1.5)
    mark = round(np.clip(base_mark + np.random.normal(0, 1.0), 10, 20), 2)

    students.append({
        "ID": ID_START + i,
        "Name": fake.unique.name(),
        "Gender": random.choices(["M", "F"], weights=[0.55, 0.45])[0],
        "Nationality": "Moroccan" if random.random() < 0.94 else random.choice(["France", "Spain", "USA"]),
        "Baccalaureat_Type": bac_type,
        "School": school,
        "Specialty": random.choice(specialties[school]),
        "Start_Year": random.choice(YEARS),
        "Mark": mark,
        "Scholarship": False,
        "Duration": school_info["duration"]
    })

# Convert to DataFrame
df = pd.DataFrame(students)

# Scholarship allocation - strongly merit-based
for year in YEARS:
    yearly_students = df[df["Start_Year"] == year].copy()
    yearly_students = yearly_students.sample(frac=1, random_state=42).sort_values("Mark", ascending=False)
    df.loc[yearly_students.head(SCHOLARSHIPS_PER_YEAR).index, "Scholarship"] = True

# Generate semester outcomes with clear patterns
semester_cols = [f"S{i}" for i in range(1, 13)]
for col in semester_cols:
    df[col] = None

for idx, row in df.iterrows():
    duration = row["Duration"]
    start_year = row["Start_Year"]
    current_year = 2025
    semesters_completed = min((current_year - start_year) * 2, duration * 2)

    base_pass_prob = 0.5 + (row["Mark"] - 10) / 20
    if row["Scholarship"]:
        base_pass_prob += 0.15

    school_bonus = (schools[row["School"]]["grad_rate"] - 0.85) * 0.5
    base_pass_prob += school_bonus

    outcomes = []
    validated_count = 0

    for sem in range(1, semesters_completed + 1):
        current_prob = base_pass_prob + validated_count * 0.05
        outcome = random.choices(
            ["validate", "no validate", "repeated"],
            weights=[current_prob, 0.6 * (1 - current_prob), 0.4 * (1 - current_prob)],
            k=1
        )[0]

        if outcome == "validate":
            validated_count += 1
        outcomes.append(outcome)

    outcomes += [None] * (12 - len(outcomes))

    for i, col in enumerate(semester_cols):
        df.at[idx, col] = outcomes[i] if i < len(outcomes) else None

# Calculate semester counts
df["Validated_Semesters"] = df[semester_cols].apply(lambda x: sum(1 for s in x if s == "validate"), axis=1)
df["Repeated_Semesters"] = df[semester_cols].apply(lambda x: sum(1 for s in x if s == "repeated"), axis=1)
df["Failed_Semesters"] = df[semester_cols].apply(lambda x: sum(1 for s in x if s == "no validate"), axis=1)


# Determine graduation with clear rules
def determine_graduation(row):
    required_semesters = row["Duration"] * 2

    if row["Validated_Semesters"] >= required_semesters * 0.9:
        grad_prob = 0.98
    elif row["Validated_Semesters"] >= required_semesters * 0.8:
        grad_prob = 0.85
    elif row["Validated_Semesters"] >= required_semesters * 0.7:
        grad_prob = 0.65
    else:
        grad_prob = 0.15

    grad_prob += (row["Mark"] - 12) / 20

    if row["Scholarship"]:
        grad_prob += 0.1

    if row["Specialty"] in ["Traduction", "Communication des Entreprises et des Institutions"]:
        grad_prob += 0.15
    elif row["Specialty"] in ["Médecine Générale", "Chirurgie Dentaire"]:
        grad_prob -= 0.1

    return np.random.random() < np.clip(grad_prob, 0.01, 0.99)


df["Graduated"] = df.apply(determine_graduation, axis=1)
df["Graduated"] = df["Graduated"].mask(np.random.random(len(df)) < 0.01, ~df["Graduated"])

# Save to CSV
df.to_csv(r"C:\Users\fftt7\PycharmProjects\UniversityProject\.venv\data_v2_deepseek\generated_data_v3_1.csv", index=False)

print("Data generation complete with:")
print(f"- Graduation rate: {df['Graduated'].mean():.2%}")
print(f"- Mark distribution:\n{df['Mark'].describe()}")
print(f"- Scholarship rate: {df['Scholarship'].mean():.2%}")
print(f"- Average validated semesters: {df['Validated_Semesters'].mean():.1f}")