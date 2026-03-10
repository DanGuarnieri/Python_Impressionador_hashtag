import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# ============================================================
# 1. Leitura e preparação dos dados
# ============================================================

df = pd.read_excel("sorteios_random.xlsx")

# Mantém apenas as colunas com as bolas
cols_bolas = [col for col in df.columns if 'bola' in col.lower()]
df_bolas = df[cols_bolas].astype(int)

print(f"Total de sorteios carregados: {len(df_bolas)}")
print(f"Colunas identificadas: {cols_bolas}")

# ============================================================
# 2. Probabilidade ponderada (peso maior aos sorteios recentes)
# ============================================================

n = len(df_bolas)
pesos = np.linspace(1, 3, n)  # mais peso para os sorteios recentes

# Frequência ponderada
freq_ponderada = pd.Series(0, index=range(0, 100), dtype=float)

for i, row in enumerate(df_bolas.values):
    for num in row:
        freq_ponderada[num] += pesos[i]

prob = freq_ponderada / freq_ponderada.sum()

# ============================================================
# 3. Matriz de coocorrência
# ============================================================

cooc = np.zeros((100, 100))

for row in df_bolas.values:
    for i in row:
        for j in row:
            if i != j:
                cooc[i, j] += 1

# Normaliza entre 0–1
cooc = cooc / cooc.max()

# ============================================================
# 4. Cálculo do "score total" de cada número
# ============================================================

# O score de cada número = probabilidade individual + média de coocorrência
score_num = []

for num in range(100):
    cooc_score = np.mean(cooc[num])  # média de associação com outros números
    total_score = prob.loc[num] + 0.5 * cooc_score  # peso da coocorrência = 0.5
    score_num.append((num, total_score))

score_num = sorted(score_num, key=lambda x: x[1], reverse=True)

# ============================================================
# 5. Escolher os 50 melhores números
# ============================================================

melhores_50 = [num for num, score in score_num[:50]]

print("\n🎯 Melhores 50 números para tentar acertar os 20:")
print(sorted(melhores_50))

# ============================================================
# 6. Visualização do ranking
# ============================================================

top_plot = pd.DataFrame(score_num, columns=["Número", "Score"]).set_index("Número")

plt.figure(figsize=(12,6))
sns.barplot(x=top_plot.index, y=top_plot["Score"], color="royalblue")
plt.title("Ranking de probabilidade + coocorrência (0–99)")
plt.xlabel("Número")
plt.ylabel("Score combinado")
plt.tight_layout()
plt.show()

# ============================================================
# 7. Salvar em Excel
# ============================================================

pd.DataFrame(sorted(melhores_50), columns=["Melhores 50 Números"]).to_excel("melhores_50_numeros.xlsx", index=False)

print("\n📂 Resultados salvos em: melhores_50_numeros.xlsx")
