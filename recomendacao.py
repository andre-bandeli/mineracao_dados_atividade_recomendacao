# Script escrito por André Luiz Bandeli Júnior (231363) e Débora Batista Delfino (233473)

from math import sqrt

avaliacoes = {
    "Maria": {"desbrota": 9, "adubação": 6, "embalagem": 8, "seleção": 8},
    "Antônio": {"colheita": 6, "capina": 8},
    "João": {"desbrota": 3, "capina": 7, "embalagem": 4, "seleção": 2},
    "Pedro": {"colheita": 7, "pulverização": 9, "capina": 7},
    "Lara": {"desbrota": 4, "capina": 6, "seleção": 7},
    "Miguel": {"desbrota": 6, "adubação": 6},
    "Julia": {"pulverização": 7, "capina": 5, "seleção": 8},
    "Clara": {"colheita": 8, "embalagem": 6},
    "Ana": {"desbrota": 4, "pulverização": 5, "adubação": 7}
}

def similaridade_euclidiana(avaliacao, funcionario1, funcionario2):
    tarefas_comuns = {}
    for tarefa in avaliacao[funcionario1]:
        if tarefa in avaliacao[funcionario2]:
            tarefas_comuns[tarefa] = 1
    
    if len(tarefas_comuns) == 0:
        return 0
    
    soma = sum([pow(avaliacao[funcionario1][tarefa] - avaliacao[funcionario2][tarefa], 2) 
              for tarefa in tarefas_comuns])
    return 1 / (1 + sqrt(soma))

def recomendar_pulverizacao(avaliacao, tarefa_alvo):
    scores = {}
    for pessoa in avaliacao:
        if tarefa_alvo in avaliacao[pessoa]:
            scores[pessoa] = avaliacao[pessoa][tarefa_alvo]
        else:
            total = 0
            sum_sim = 0
            for pessoa2 in avaliacao:
                if pessoa2 == pessoa:
                    continue
                if tarefa_alvo not in avaliacao[pessoa2]:
                    continue
                sim = similaridade_euclidiana(avaliacao, pessoa, pessoa2)
                if sim > 0:
                    total += sim * avaliacao[pessoa2][tarefa_alvo]
                    sum_sim += sim
            if sum_sim > 0:
                predicted_score = total / sum_sim
                scores[pessoa] = predicted_score
    rankings = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return rankings

def recomendar_tarefas(avaliacao, funcionario_alvo):
    totais = {}
    soma_similaridade = {}
    
    for outro_funcionario in avaliacao:
        if outro_funcionario == funcionario_alvo:
            continue
        
        sim = similaridade_euclidiana(avaliacao, funcionario_alvo, outro_funcionario)
        if sim <= 0:
            continue
        
        for tarefa in avaliacao[outro_funcionario]:
            if tarefa not in avaliacao[funcionario_alvo]:
                totais.setdefault(tarefa, 0)
                totais[tarefa] += avaliacao[outro_funcionario][tarefa] * sim
                soma_similaridade.setdefault(tarefa, 0)
                soma_similaridade[tarefa] += sim
    
    if not totais:
        return []
    
    rankings = [(total / soma_similaridade[tarefa], tarefa) 
                for tarefa, total in totais.items()]
    rankings.sort(reverse=True)
    return rankings

# Recomendações para pulverização
print("\nPessoas recomendadas para pulverização:")
recomendacoes_pulverizacao = recomendar_pulverizacao(avaliacoes, "pulverização")
for pessoa, score in recomendacoes_pulverizacao:
    print(f"- {pessoa}: Score {score:.2f}")

# Recomendações para Júlia
recomendacoes_pessoa = recomendar_tarefas(avaliacoes, "Julia")
print("Tarefas recomendadas para Julia:")
for score, tarefa in recomendacoes_pessoa:
    print(f"- {tarefa}: Score {score:.2f}")