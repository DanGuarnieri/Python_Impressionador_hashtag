import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# ============================================================
# 🔹 1. Leitura e preparação dos dados
# ============================================================

df = pd.read_excel("sorteios_random.xlsx")

# Mantém apenas as colunas com as bolas
cols_bolas = [col for col in df.columns if 'bola' in col.lower()]
df_bolas = df[cols_bolas].astype(int)

print(f"Total de sorteios carregados: {len(df_bolas)}")
print(f"Colunas identificadas: {cols_bolas}")

# ============================================================
# 🔹 2. Probabilidade ponderada (dá mais peso a sorteios recentes)
# ============================================================

n = len(df_bolas)
pesos = np.linspace(1, 3, n)  # de 1x até 3x mais peso nos mais recentes
freq_ponderada = pd.Series(0, index=range(1, int(df_bolas.values.max()) + 1), dtype=float)

for i, row in enumerate(df_bolas.values):
    for num in row:
        freq_ponderada[num] += pesos[i]

prob = freq_ponderada / freq_ponderada.sum()

# ============================================================
# 🔹 3. Matriz de coocorrência
# ============================================================

max_num = int(df_bolas.values.max())
cooc = np.zeros((max_num + 1, max_num + 1))

for row in df_bolas.values:
    for i in row:
        for j in row:
            if i != j:
                cooc[i, j] += 1

cooc = cooc / cooc.max()  # normaliza

# ============================================================
# 🔹 4. Função de pontuação
# ============================================================

def score_combination(combination, prob, cooc):
    p_score = np.sum(np.log(prob.loc[list(combination)] + 1e-6))
    c_score = np.mean([cooc[i, j] for i in combination for j in combination if i != j])
    return p_score + c_score

# ============================================================
# 🔹 5. Simulação Monte Carlo (gera e avalia combinações)
# ============================================================

num_simulacoes = 100_000
qtd_bolas = df_bolas.shape[1]
numeros_possiveis = prob.index.tolist()

melhores = []
np.random.seed(42)

for _ in range(num_simulacoes):
    combo = np.random.choice(
        numeros_possiveis,
        size=qtd_bolas,
        replace=False,
        p=prob.values / prob.values.sum()
    )
    sc = score_combination(combo, prob, cooc)
    melhores.append((sc, combo))

melhores.sort(reverse=True, key=lambda x: x[0])

# ============================================================
# 🔹 6. Exibição dos 10 melhores jogos
# ============================================================

top10 = [sorted(map(int, x[1])) for x in melhores[:10]]
print("\n🎯 Top 10 combinações mais promissoras (estatístico + coocorrência):\n")

for i, comb in enumerate(top10, 1):
    print(f"{i:02d}: {comb} | Score: {melhores[i-1][0]:.4f}")

# ============================================================
# 🔹 7. Salvar resultados em Excel
# ============================================================

df_out = pd.DataFrame(top10)
df_out.index = [f"Jogo {i+1}" for i in range(len(df_out))]
df_out.to_excel("previsoes_otimizadas.xlsx")

print("\n📂 Resultados salvos em: previsoes_otimizadas.xlsx")

# ============================================================
# 🔹 8. Visualização gráfica
# ============================================================

plt.figure(figsize=(10,5))
sns.barplot(x=prob.index, y=prob.values, color="royalblue")
plt.title("Probabilidade ponderada de cada número (histórico + peso recente)")
plt.xlabel("Número")
plt.ylabel("Probabilidade estimada")
plt.tight_layout()
plt.show()
