import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# === 1. Leitura dos dados ===
df = pd.read_excel("sorteios_random.xlsx")

# Mantém apenas as colunas das bolas
cols_bolas = [col for col in df.columns if 'bola' in col]
df_bolas = df[cols_bolas].astype(int)

# === 2. Cálculo de frequência ponderada ===
# Pesos maiores para sorteios recentes
n = len(df_bolas)
pesos = np.linspace(1, 3, n)  # peso mais forte para os mais novos
freq_ponderada = (
    pd.Series(np.repeat(df_bolas.values, 1))
    .value_counts()
    .sort_index()
)

# Ajustar frequências com pesos
for i, row in enumerate(df_bolas.values):
    for num in row:
        freq_ponderada[num] += pesos[i]

# Normalizar para probabilidades
prob = freq_ponderada / freq_ponderada.sum()

# === 3. Análise de correlação entre números ===
# Cria uma matriz de coocorrência (números que aparecem juntos)
max_num = int(df_bolas.values.max())
cooc = np.zeros((max_num+1, max_num+1))

for row in df_bolas.values:
    for i in row:
        for j in row:
            if i != j:
                cooc[i, j] += 1

# Normaliza coocorrência
cooc = cooc / cooc.max()

# === 4. Função de score para avaliar combinações ===
def score_combination(combination, prob, cooc):
    """Score = soma log das probabilidades individuais + média da coocorrência"""
    p_score = np.sum(np.log(prob.loc[list(combination)] + 1e-6))
    c_score = np.mean([cooc[i, j] for i in combination for j in combination if i != j])
    return p_score + c_score

# === 5. Simulação Monte Carlo ===
melhores = []
num_simulacoes = 100_000
qtd_bolas = df_bolas.shape[1]
numeros_possiveis = prob.index.tolist()

for _ in range(num_simulacoes):
    combo = np.random.choice(numeros_possiveis, size=qtd_bolas, replace=False, p=prob.values/prob.values.sum())
    sc = score_combination(combo, prob, cooc)
    melhores.append((sc, combo))

# Ordena pelos melhores scores
melhores.sort(reverse=True, key=lambda x: x[0])

# === 6. Exibir o melhor resultado ===
melhor_score, melhor_comb = melhores[0]
melhor_comb = sorted(map(int, melhor_comb))

print("\n💡 Melhor combinação prevista (base probabilística e coocorrência):")
print(melhor_comb)
print(f"Score: {melhor_score:.4f}")

# === 7. Visualização das probabilidades ===
plt.figure(figsize=(10,5))
sns.barplot(x=prob.index, y=prob.values)
plt.title("Probabilidade ponderada de cada número (histórico + peso recente)")
plt.xlabel("Número")
plt.ylabel("Probabilidade estimada")
plt.show()
