import pandas as pd

df = pd.read_csv("results_Multiq.csv")
df['cmp_T_L'] = df['cmp_T_L'].astype(str).str.strip()

has_m = df.groupby(['K2','K4'])['cmp_T_L'].apply(lambda v: (v=='m').any())
has_y = df.groupby(['K2','K4'])['cmp_T_L'].apply(lambda v: (v=='y').any())

totale = len(has_y)
solo_y_senza_m = (has_y & ~has_m).sum()
y_e_m_insieme  = (has_y & has_m).sum()

print(f"Totale punti K2,K4: {totale}")
print(f"Punti con 'y' ma MAI 'm': {solo_y_senza_m}")
print(f"Punti con 'y' E 'm' insieme: {y_e_m_insieme}")

has_m_senza_y = (has_m & ~has_y).sum()
print(f"Punti con 'm' ma MAI 'y': {has_m_senza_y}")
print(f"Punti con 'm' totali: {has_m.sum()}")