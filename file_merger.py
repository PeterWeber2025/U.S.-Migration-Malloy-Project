import subprocess
import sys

# Auto-install any missing dependencies
for package in ['pandas', 'us', 'addfips']:
    try:
        __import__(package)
    except ImportError:
        print(f"Installing {package}...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])

import os
import glob
import pandas as pd
import us
import addfips

# ── Build state FIPS → full name lookup ──────────────────────────────────────
FIPS_TO_STATE = {}
for state in us.states.STATES_AND_TERRITORIES:
    if state.fips:
        FIPS_TO_STATE[int(state.fips)] = state.name

# IRS-specific special codes (we will FILTER these out later)
AGGREGATE_STATE_CODES = {96, 97, 98, 99}

# ── Build county lookup ──────────────────────────────────────────────────────
county_file = os.path.join(os.path.dirname(addfips.__file__), 'data', 'counties_2020.csv')
county_df = pd.read_csv(county_file)

COUNTY_LOOKUP = {
    (int(row['statefp']), int(row['countyfp'])): row['name']
    for _, row in county_df.iterrows()
}

def resolve_county(state_fips, county_fips, fallback_name=None):
    try:
        sfips = int(state_fips)
        cfips = int(county_fips)

        if (sfips, cfips) in COUNTY_LOOKUP:
            return COUNTY_LOOKUP[(sfips, cfips)]

        if pd.notna(fallback_name) and str(fallback_name).strip():
            return str(fallback_name).strip()

        return None
    except:
        if pd.notna(fallback_name) and str(fallback_name).strip():
            return str(fallback_name).strip()
        return None

# ── Process files ────────────────────────────────────────────────────────────
csv_files = [f for f in glob.glob('data/*.csv') if f != 'Merged_County_Outflows.csv']

if not csv_files:
    print("No CSV files found.")
    sys.exit()

print(f"Found {len(csv_files)} CSV file(s)...\n")

dataframes = []

for file in csv_files:
    try:
        df = pd.read_csv(file, encoding='latin-1')
        df.columns = df.columns.str.strip().str.lower()

        # ─────────────────────────────────────────────
        # 🚨 FILTER BAD ROWS FIRST (CRITICAL FIX)
        # ─────────────────────────────────────────────

        # Convert to numeric for filtering
        df['y2_statefips'] = pd.to_numeric(df['y2_statefips'], errors='coerce')
        df['y2_countyfips'] = pd.to_numeric(df['y2_countyfips'], errors='coerce')

        # Keep ONLY real county destinations
        df = df[
            (df['y2_countyfips'] != 0) &  # remove totals like "000"
            (~df['y2_statefips'].isin(AGGREGATE_STATE_CODES))  # remove 96–99
        ]

        # Remove non-migrants explicitly
        if 'y2_countyname' in df.columns:
            df = df[
                ~df['y2_countyname'].str.contains('Non-migrants', na=False)
            ]

        # ─────────────────────────────────────────────
        # ✅ Use PEOPLE, not mixed units
        # ─────────────────────────────────────────────
        df['Total Filings'] = df['n2']

        df = df.drop(columns=['n1', 'n2', 'agi'], errors='ignore')

        # ─────────────────────────────────────────────
        # Resolve counties
        # ─────────────────────────────────────────────
        df['y1_county'] = df.apply(
            lambda r: resolve_county(r['y1_statefips'], r['y1_countyfips']), axis=1
        )

        df['y2_county'] = df.apply(
            lambda r: resolve_county(
                r['y2_statefips'],
                r['y2_countyfips'],
                r.get('y2_countyname')
            ), axis=1
        )

        # Drop unused columns
        drop_cols = ['y1_countyfips', 'y2_countyfips', 'y2_state']
        if 'y2_countyname' in df.columns:
            drop_cols.append('y2_countyname')

        df = df.drop(columns=drop_cols, errors='ignore')

        # ─────────────────────────────────────────────
        # Convert state FIPS → names
        # ─────────────────────────────────────────────
        df['y1_statefips'] = pd.to_numeric(df['y1_statefips'], errors='coerce')
        df['y2_statefips'] = pd.to_numeric(df['y2_statefips'], errors='coerce')

        df['y1_statefips'] = df['y1_statefips'].map(FIPS_TO_STATE)
        df['y2_statefips'] = df['y2_statefips'].map(FIPS_TO_STATE)

        # Rename columns
        df = df.rename(columns={
            'y1_statefips': 'Origin State',
            'y1_county':    'Origin County',
            'y2_statefips': 'Destination State',
            'y2_county':    'Destination County',
        })

        # ─────────────────────────────────────────────
        # Fix year handling
        # ─────────────────────────────────────────────
        year = int(file.split('.')[0][-2:])
        df['year'] = year

        dataframes.append(df)

        print(f"✓ {file} ({len(df):,} cleaned rows)")

    except Exception as e:
        print(f"✗ {file} — {e}")

if not dataframes:
    print("\nNo files processed.")
    sys.exit()

# ── Merge ────────────────────────────────────────────────────────────────────
merged_df = pd.concat(dataframes, ignore_index=True)

# Optional: enforce correct grain (extra safety)
merged_df = merged_df.groupby(
    ['year', 'Origin State', 'Origin County', 'Destination State', 'Destination County'],
    as_index=False
)['Total Filings'].sum()

merged_df = merged_df.sort_values(
    by=['year', 'Origin State', 'Destination State'],
    ignore_index=True
)

merged_df.to_csv('Merged_County_Outflows.csv', index=False, encoding='utf-8-sig')

print(f"\nDone. {len(merged_df):,} rows in final dataset.")