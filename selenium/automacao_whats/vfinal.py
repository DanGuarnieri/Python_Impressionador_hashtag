import pandas as pd
import numpy as np

# ==============================
# 1. Leitura dos dados
# ==============================
df = pd.read_excel("sorteios_random.xlsx")
cols_bolas = [c for c in df.columns if 'bola' in c.lower()]
df_bolas = df[cols_bolas].astype(int)
n_sorteios = len(df_bolas)
max_num = 99

# ==============================
# 2. Probabilidade ponderada
# ==============================
pesos = np.linspace(1, 3, n_sorteios)  # mais peso para sorteios recentes
freq_ponderada = pd.Series(0, index=range(max_num+1), dtype=float)
for i, row in enumerate(df_bolas.values):
    for num in row:
        freq_ponderada[num] += pesos[i]

# ==============================
# 3. Coocorrência
# ==============================
cooc = np.zeros((max_num+1, max_num+1))
for row in df_bolas.values:
    for i in row:
        for j in row:
            if i != j:
                cooc[i,j] += 1
cooc = cooc / cooc.max()  # normalizar

# ==============================
# 4. Seleção otimizada por tubo
# ==============================
tubos = [list(range(i, i+10)) for i in range(0, 100, 10)]
num_por_tubo = 5
selected_numbers = []

for tubo in tubos:
    # calcular score de cada número no tubo
    scores = []
    for num in tubo:
        # média de coocorrência com os números já selecionados
        if selected_numbers:
            cooc_score = np.mean([cooc[num, s] for s in selected_numbers])
        else:
            cooc_score = 0
        score = freq_ponderada[num] + 0.5*cooc_score
        scores.append((score, num))
    # pegar os 5 melhores do tubo
    scores.sort(reverse=True)
    best_nums = [num for sc, num in scores[:num_por_tubo]]
    selected_numbers.extend(best_nums)

# ==============================
# 5. Simulação nos últimos 10 sorteios
# ==============================
ultimos_10 = df_bolas.tail(10).values
acertos_por_sorteio = [len(set(selected_numbers) & set(sorteio)) for sorteio in ultimos_10]
min_acertos = min(acertos_por_sorteio)
media_acertos = np.mean(acertos_por_sorteio)

# ==============================
# 6. Resultado
# ==============================
print("🔹 Números escolhidos (50):")
print(sorted(selected_numbers))
print("\n🔹 Simulação últimos 10 sorteios:")
print("Acertos por sorteio:", acertos_por_sorteio)
print("Mínimo de acertos:", min_acertos)
print("Média de acertos:", round(media_acertos,2))

# ==============================
# 7. Salvar em Excel
# ==============================
df_result = pd.DataFrame({
    "Números escolhidos": [', '.join(map(str, sorted(selected_numbers)))],
    "Acertos_Sorteio_1": [acertos_por_sorteio[0]],
    "Acertos_Sorteio_2": [acertos_por_sorteio[1]],
    "Acertos_Sorteio_3": [acertos_por_sorteio[2]],
    "Acertos_Sorteio_4": [acertos_por_sorteio[3]],
    "Acertos_Sorteio_5": [acertos_por_sorteio[4]],
    "Acertos_Sorteio_6": [acertos_por_sorteio[5]],
    "Acertos_Sorteio_7": [acertos_por_sorteio[6]],
    "Acertos_Sorteio_8": [acertos_por_sorteio[7]],
    "Acertos_Sorteio_9": [acertos_por_sorteio[8]],
    "Acertos_Sorteio_10": [acertos_por_sorteio[9]],
    "Mínimo de acertos": [min_acertos],
    "Média de acertos": [round(media_acertos,2)]
})

df_result.to_excel("50_numeros_otimizados.xlsx", index=False)
print("\n✅ Arquivo '50_numeros_otimizados.xlsx' gerado com sucesso!")
