import pandas as pd
import re

rain = pd.read_csv("data/state_rainfall.csv")
crops = pd.read_csv("data/crop_production.csv")
temp = pd.read_csv("data/climate_temp.csv")

STATES = sorted(set(rain['state'].unique().tolist() + crops['state'].unique().tolist() + temp['state'].unique().tolist()))

def extract_states(question):
    q = question.lower()
    found = []
    for s in STATES:
        if s.lower() in q:
            found.append(s)
    return list(dict.fromkeys(found))  # preserve order, unique

def extract_number(question, default=None):
    m = re.search(r'last\s+(\d+)\s+years?', question.lower())
    if m:
        return int(m.group(1))
    m2 = re.search(r'last\s+year', question.lower())
    if m2:
        return 1
    return default

def extract_top_m(question, default=3):
    m = re.search(r'top\s+(\d+)', question.lower())
    if m:
        return int(m.group(1))
    return default

def extract_crop(question):
    q = question.lower()
    crops_list = sorted(set(crops['crop'].unique().tolist()), key=lambda x: -len(x))
    for c in crops_list:
        if c.lower() in q:
            return c
    return None

def answer_question(question: str):
    q = question.lower()
    states = extract_states(question)
    if not states:
        # default demo states
        states = ['Karnataka', 'Maharashtra']

    N = extract_number(question, default=3)
    M = extract_top_m(question, default=3)

    # determine years to use: take latest N years available across rain dataset
    years = sorted(rain['year'].unique())[-N:]

    # rainfall comparison
    if 'rainfall' in q or 'rain' in q:
        df = rain[rain['state'].isin(states) & rain['year'].isin(years)]
        avg = df.groupby('state')['avg_rainfall_mm'].mean().reset_index()
        text_lines = [f"Average annual rainfall ({years[0]}–{years[-1]}):"]
        for _, row in avg.iterrows():
            text_lines.append(f"{row['state']}: {row['avg_rainfall_mm']:.1f} mm (source: IMD rainfall dataset)")
        text = ' '.join(text_lines)
        provenance = [{
            'title': 'IMD – Rainfall in India (sample)',
            'url': 'https://data.gov.in/dataset/rainfall-india',
            'rows_used': f"states={states}, years={years}"
        }]
        # also include a small table for UI
        return text, avg, provenance

    # top M crops
    if 'top' in q and 'crop' in q:
        df = crops[crops['state'].isin(states) & crops['year'].isin(years)]
        agg = df.groupby(['state','crop'])['production_tonnes'].sum().reset_index()
        topm = agg.sort_values(['state','production_tonnes'], ascending=[True,False]).groupby('state').head(M)
        text_lines = [f"Top {M} crops by production ({years[0]}–{years[-1]}):"]
        for _, row in topm.iterrows():
            text_lines.append(f"{row['state']}: {row['crop']} ({int(row['production_tonnes'])} t)")
        text = ' '.join(text_lines)
        provenance = [{
            'title': 'Ministry of Agriculture – Crop Production (sample)',
            'url': 'https://data.gov.in/dataset/crop-production',
            'rows_used': f"states={states}, years={years}"
        }]
        return text, topm, provenance

    # trend analysis: production trend correlated with temp
    if 'trend' in q or 'correlate' in q:
        crop = extract_crop(question)
        if not crop:
            return "Please specify which crop to analyze.", None, []
        df_prod = crops[(crops['state'].isin(states)) & (crops['crop'].str.lower() == crop.lower()) & (crops['year'].isin(years))]
        df_temp = temp[(temp['state'].isin(states)) & (temp['year'].isin(years))]
        merged = pd.merge(df_prod, df_temp, on=['state','year'], how='inner')
        # compute simple correlation per state
        corr = merged.groupby('state').apply(lambda d: d['production_tonnes'].corr(d['avg_temp_c'])).reset_index().rename(columns={0:'corr_temp_prod'})
        text_lines = [f"Trend & correlation for {crop} ({years[0]}–{years[-1]}):"]
        for _, r in corr.iterrows():
            text_lines.append(f"{r['state']}: correlation (temp vs production) = {r['corr_temp_prod']:.2f}")
        text = ' '.join(text_lines)
        provenance = [
            {'title':'Crop Production (sample)','url':'https://data.gov.in/dataset/crop-production','rows_used':f"crop={crop},states={states},years={years}"},
            {'title':'IMD Temperature (sample)','url':'https://data.gov.in/dataset/imd-temperature','rows_used':f"states={states},years={years}"}
        ]
        return text, merged, provenance

    return "Sorry, I can currently handle rainfall comparisons, top crop lists, and simple trend correlations.", None, []
