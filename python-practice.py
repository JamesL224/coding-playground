# Changed code - synthetic patient dataset generator
import sys
import csv
import random
import sqlite3
import uuid
from datetime import datetime, timedelta

# Try to use Faker if installed for richer fake data; degrade gracefully.
try:
    from faker import Faker
    faker = Faker()
    Faker.seed(42)
except Exception:
    faker = None

random.seed(42)

GENDERS = ["M", "F", "Other"]
RACES = ["White", "Black", "Asian", "Hispanic", "Other"]
DIAGNOSES = [
    ("E11", "Type 2 diabetes mellitus"),
    ("I10", "Essential (primary) hypertension"),
    ("J45", "Asthma"),
    ("F32", "Major depressive disorder"),
    ("M54", "Back pain"),
    ("R51", "Headache"),
]
MEDICATIONS = [
    "metformin", "lisinopril", "albuterol", "sertraline", "ibuprofen", "atorvastatin"
]
LABS = [
    ("HbA1c", 4.5, 14.0),
    ("WBC", 3.0, 12.0),
    ("Creatinine", 0.4, 2.0),
    ("Cholesterol", 100, 300),
]

def random_dob(min_age=0, max_age=100):
    today = datetime.today()
    age_days = random.randint(min_age*365, max_age*365)
    dob = today - timedelta(days=age_days)
    return dob.date().isoformat()

def fake_name():
    if faker:
        name = faker.name().split()
        return name[0], name[-1]
    # fallback
    firsts = ["James","Mary","John","Pat","Chris","Alex","Sam","Taylor"]
    lasts = ["Smith","Johnson","Lee","Brown","Garcia","Miller","Davis"]
    return random.choice(firsts), random.choice(lasts)

def fake_zip():
    if faker:
        return faker.postcode()
    return str(random.randint(10000, 99999))

def gen_patients(n):
    for _ in range(n):
        pid = str(uuid.uuid4())
        first, last = fake_name()
        dob = random_dob(0, 100)
        gender = random.choice(GENDERS)
        race = random.choice(RACES)
        zipcode = fake_zip()
        yield {
            "patient_id": pid,
            "first_name": first,
            "last_name": last,
            "dob": dob,
            "gender": gender,
            "race": race,
            "zip": zipcode,
        }

def gen_encounters(patient_id, max_enc=5):
    count = random.randint(1, max_enc)
    for _ in range(count):
        enc_id = str(uuid.uuid4())
        enc_date = (datetime.today() - timedelta(days=random.randint(0, 3650))).date().isoformat()
        diag_code, diag_desc = random.choice(DIAGNOSES)
        med = random.choice(MEDICATIONS)
        lab_name, low, high = random.choice(LABS)
        lab_value = round(random.uniform(low, high), 2)
        yield {
            "encounter_id": enc_id,
            "patient_id": patient_id,
            "encounter_date": enc_date,
            "diagnosis_code": diag_code,
            "diagnosis_desc": diag_desc,
            "medication": med,
            "lab_name": lab_name,
            "lab_value": lab_value,
        }

def write_csv(patients, encounters, out_pat="patients.csv", out_enc="encounters.csv"):
    with open(out_pat, "w", newline="", encoding="utf-8") as pf:
        writer = csv.DictWriter(pf, fieldnames=list(next(iter(patients),{}).keys()))
        writer.writeheader()
        for p in patients:
            writer.writerow(p)
    with open(out_enc, "w", newline="", encoding="utf-8") as ef:
        writer = csv.DictWriter(ef, fieldnames=list(next(iter(encounters),{}).keys()))
        writer.writeheader()
        for e in encounters:
            writer.writerow(e)

def create_sqlite_db(patients, encounters, db_path="patients.db"):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS patients (
        patient_id TEXT PRIMARY KEY,
        first_name TEXT,
        last_name TEXT,
        dob TEXT,
        gender TEXT,
        race TEXT,
        zip TEXT
    )""")
    cur.execute("""
    CREATE TABLE IF NOT EXISTS encounters (
        encounter_id TEXT PRIMARY KEY,
        patient_id TEXT,
        encounter_date TEXT,
        diagnosis_code TEXT,
        diagnosis_desc TEXT,
        medication TEXT,
        lab_name TEXT,
        lab_value REAL,
        FOREIGN KEY(patient_id) REFERENCES patients(patient_id)
    )""")
    p_rows = [(p["patient_id"], p["first_name"], p["last_name"], p["dob"], p["gender"], p["race"], p["zip"]) for p in patients]
    e_rows = [(e["encounter_id"], e["patient_id"], e["encounter_date"], e["diagnosis_code"], e["diagnosis_desc"], e["medication"], e["lab_name"], e["lab_value"]) for e in encounters]
    cur.executemany("INSERT INTO patients VALUES (?, ?, ?, ?, ?, ?, ?)", p_rows)
    cur.executemany("INSERT INTO encounters VALUES (?, ?, ?, ?, ?, ?, ?, ?)", e_rows)
    conn.commit()
    conn.close()

def main():
    n = 1000
    if len(sys.argv) > 1:
        try:
            n = int(sys.argv[1])
        except Exception:
            pass
    patients = list(gen_patients(n))
    encounters = []
    for p in patients:
        encounters.extend(list(gen_encounters(p["patient_id"], max_enc=5)))
    # write CSVs
    write_csv(patients, encounters, out_pat="patients.csv", out_enc="encounters.csv")
    # write sqlite
    create_sqlite_db(patients, encounters, db_path="patients.db")
    print(f"Generated {len(patients)} patients and {len(encounters)} encounters.")
    print("Wrote patients.csv, encounters.csv, patients.db")

if __name__ == "__main__":
    main()

