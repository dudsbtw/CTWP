import sys
import random

# =============================================================================
# JOVI ALIVE - FrameAI + ReplayLens
# Simulação em terminal do sistema inteligente de captura e seleção de frames
# Engenharia de Software — FIAP | Challenge JOVI Smartphone 2026 | Sprint 2
# =============================================================================

# --- ESTRUTURAS DE DADOS GLOBAIS ---

# Cada frame é armazenado como uma lista:
# [id, cena, enquadramento, nitidez, expressao, iluminacao, pontuacao]
buffer_frames = []

# Histórico de preferências: registra quando o usuário diverge da IA
# Cada entrada: [id_frame_ia, id_frame_usuario, cena]
historico_preferencias = []

# Configurações do modo Alive
configuracoes = {
    "modo_alive_ativo": True,
    "tempo_buffer": 5,       # segundos de buffer (3 a 10)
    "auto_salvar": True      # salva automaticamente o frame da IA se o usuário não decidir
}

# Contador para IDs únicos de frames
proximo_id = [1]

# =============================================================================
# FUNÇÕES DE DADOS — REPLAYLENS
# =============================================================================

def gerar_frame_simulado(cena):
    """
    Simula a captura de um frame com valores aleatórios de qualidade.
    Na vida real, esses valores viriam da Camera2 API e do ML Kit.
    Retorna uma lista com os dados do frame.
    """
    frame_id = proximo_id[0]
    proximo_id[0] += 1

    enquadramento = round(random.uniform(4.0, 10.0), 1)
    nitidez       = round(random.uniform(4.0, 10.0), 1)
    expressao     = round(random.uniform(4.0, 10.0), 1)
    iluminacao    = round(random.uniform(4.0, 10.0), 1)

    # Pontuação final: média simples dos 4 critérios (FrameAI)
    pontuacao = round((enquadramento + nitidez + expressao + iluminacao) / 4, 2)

    return [frame_id, cena, enquadramento, nitidez, expressao, iluminacao, pontuacao]

def capturar_frames(cena, quantidade):
    """
    Adiciona 'quantidade' frames simulados ao buffer global.
    Representa o disparo retroativo do ReplayLens.
    """
    novos = []
    for _ in range(quantidade):
        frame = gerar_frame_simulado(cena)
        buffer_frames.append(frame)
        novos.append(frame)
    return novos

def limpar_buffer():
    """Descarta todos os frames do buffer (simula o descarte automático de RAM)."""
    buffer_frames.clear()

# =============================================================================
# FUNÇÕES DE ANÁLISE — FRAMEAI
# =============================================================================

def melhor_frame(frames):
    """
    Recebe uma lista de frames e retorna o frame com maior pontuação.
    Representa a lógica central do FrameAI.
    """
    if not frames:
        return None

    melhor = frames[0]
    for frame in frames:
        if frame[6] > melhor[6]:   # índice 6 = pontuação
            melhor = frame
    return melhor

def indice_frame_por_id(frame_id):
    """Encontra o índice de um frame no buffer a partir do seu ID."""
    i = 0
    for frame in buffer_frames:
        if frame[0] == frame_id:
            return i
        i += 1
    return -1

# =============================================================================
# FUNÇÕES DE HISTÓRICO — PREFERÊNCIAS DO USUÁRIO
# =============================================================================

def registrar_preferencia(frame_ia, frame_usuario, cena):
    """
    Registra no histórico quando o usuário escolhe um frame diferente do IA.
    Usado para personalização futura do FrameAI (RF09).
    """
    historico_preferencias.append([frame_ia[0], frame_usuario[0], cena])

def total_divergencias():
    """Retorna quantas vezes o usuário divergiu da sugestão da IA."""
    return len(historico_preferencias)

# =============================================================================
# FUNÇÕES DE EXIBIÇÃO
# =============================================================================

def exibir_frame(frame, destaque=False):
    """
    Exibe os dados de um frame formatados no terminal.
    Se destaque=True, marca com borda dourada (sugestão da IA).
    """
    marcador = "★ RECOMENDADO PELO FrameAI" if destaque else ""
    print(f"  {'─'*40}")
    print(f"  Frame #{frame[0]} | Cena: {frame[1]}  {marcador}")
    print(f"  Enquadramento : {frame[2]:.1f}")
    print(f"  Nitidez       : {frame[3]:.1f}")
    print(f"  Expressão     : {frame[4]:.1f}")
    print(f"  Iluminação    : {frame[5]:.1f}")
    print(f"  Pontuação IA  : {frame[6]:.2f} / 10.00")

def exibir_configuracoes():
    """Exibe as configurações atuais do modo Alive."""
    status = "ATIVO ✓" if configuracoes["modo_alive_ativo"] else "INATIVO ✗"
    auto   = "Sim" if configuracoes["auto_salvar"] else "Não"
    print(f"  Modo Alive    : {status}")
    print(f"  Buffer        : {configuracoes['tempo_buffer']} segundos")
    print(f"  Auto-salvar   : {auto}")

# =============================================================================
# MENUS
# =============================================================================

def menu_principal():
    """Menu principal do sistema JOVI Alive."""
    while True:
        print()
        print("        JOVI ALIVE — FrameAI      ")
        print("  1. Capturar frames (ReplayLens) ")
        print("  2. Analisar frames (FrameAI)    ")
        print("  3. Histórico de preferências    ")
        print("  4. Configurações do modo Alive  ")
        print("  5. Sair                         ")

        opcao = input("Opção: ").strip()

        if opcao == "1":
            menu_captura()
        elif opcao == "2":
            menu_frameai()
        elif opcao == "3":
            menu_historico()
        elif opcao == "4":
            menu_configuracoes()
        elif opcao == "5":
            print("\nEncerrando JOVI Alive. Até logo!")
            sys.exit()
        else:
            print("  Opção inválida. Tente novamente.")

# -----------------------------------------------------------------------------

def menu_captura():
    """
    Funcionalidade 1 — ReplayLens
    Simula a captura retroativa de frames para o buffer.
    """
    print()
    print("--- REPLAYLENS: Captura de Frames ---")

    # Verifica se o modo Alive está ativo (RN03)
    if not configuracoes["modo_alive_ativo"]:
        print("  ⚠ Modo Alive está desativado. Ative nas Configurações.")
        return

    print("  1. Capturar nova sessão")
    print("  2. Limpar buffer atual")
    print("  3. Ver frames no buffer")
    print("  4. Voltar")

    opcao = input("  Opção: ").strip()

    if opcao == "1":
        cena = input("  Descreva a cena (ex: aniversário, formatura): ").strip()

        # Valida entrada da cena
        if not cena:
            print("  ⚠ A descrição da cena não pode ser vazia.")
            menu_captura()
            return

        # Quantidade de frames baseada no tempo de buffer configurado
        quantidade = configuracoes["tempo_buffer"] * 6   # ~6 frames por segundo
        print(f"\n  Capturando {quantidade} frames dos últimos {configuracoes['tempo_buffer']}s...")

        novos_frames = capturar_frames(cena, quantidade)

        print(f"  ✓ {len(novos_frames)} frames adicionados ao buffer.")
        print(f"  Total no buffer: {len(buffer_frames)} frames.")

    elif opcao == "2":
        # RN04 — descarte automático do buffer
        confirmacao = input("  Tem certeza que deseja limpar o buffer? (s/n): ").strip().lower()
        if confirmacao == "s":
            limpar_buffer()
            print("  ✓ Buffer limpo. Todos os frames descartados da memória.")
        else:
            print("  Operação cancelada.")

    elif opcao == "3":
        if not buffer_frames:
            print("  Buffer vazio. Capture uma sessão primeiro.")
        else:
            print(f"\n  Frames no buffer ({len(buffer_frames)} no total):")
            for frame in buffer_frames:
                exibir_frame(frame)
    elif opcao == "4":
        return
    else:
        print("  Opção inválida.")
        menu_captura()

# -----------------------------------------------------------------------------

def menu_frameai():
    """
    Funcionalidade 2 — FrameAI
    Analisa os frames do buffer e recomenda o melhor.
    Permite ao usuário confirmar ou escolher outro frame.
    """
    print()
    print("--- FRAMEAI: Análise Inteligente de Frames ---")

    if not buffer_frames:
        print("  Buffer vazio. Vá em 'Capturar frames' primeiro.")
        return

    # Análise automática: encontra o melhor frame
    recomendado = melhor_frame(buffer_frames)

    print(f"\n  Analisando {len(buffer_frames)} frames...")
    print("\n  ── Sugestão do FrameAI ──")
    exibir_frame(recomendado, destaque=True)

    print()
    print("  O que deseja fazer?")
    print("  1. Confirmar frame recomendado pela IA  (RN01)")
    print("  2. Escolher outro frame manualmente")
    print("  3. Ver todos os frames e suas pontuações")
    print("  4. Voltar")

    opcao = input("  Opção: ").strip()

    if opcao == "1":
        # Usuário aceita a sugestão da IA
        print(f"\n  ✓ Frame #{recomendado[0]} salvo como foto final!")
        print(f"  Cena: {recomendado[1]} | Pontuação: {recomendado[6]:.2f}/10")
        limpar_buffer()   # RN04 — descarta o restante

    elif opcao == "2":
        # Usuário quer escolher outro frame (RF06)
        print("\n  Frames disponíveis:")
        for i, frame in enumerate(buffer_frames):
            print(f"  {i + 1}. Frame #{frame[0]} | {frame[1]} | Pontuação: {frame[6]:.2f}")

        while True:
            escolha = input("\n  Digite o número do frame desejado: ").strip()

            # Valida se é número e se está no intervalo
            if not escolha.isdigit():
                print("  ⚠ Digite apenas um número.")
                continue

            indice = int(escolha) - 1
            if indice < 0 or indice >= len(buffer_frames):
                print(f"  ⚠ Número inválido. Escolha entre 1 e {len(buffer_frames)}.")
                continue

            frame_escolhido = buffer_frames[indice]
            break

        # Registra divergência se o usuário escolheu diferente da IA (RF09)
        if frame_escolhido[0] != recomendado[0]:
            registrar_preferencia(recomendado, frame_escolhido, frame_escolhido[1])
            print(f"\n  Preferência registrada para personalização futura do FrameAI.")

        print(f"\n  ✓ Frame #{frame_escolhido[0]} salvo como foto final!")
        limpar_buffer()   # RN04

    elif opcao == "3":
        # Exibe todos os frames ordenados por pontuação (maior primeiro)
        frames_ordenados = sorted(buffer_frames, key=lambda f: f[6], reverse=True)
        print(f"\n  Todos os frames — ordenados por pontuação:")
        for frame in frames_ordenados:
            destaque = (frame[0] == recomendado[0])
            exibir_frame(frame, destaque=destaque)
        menu_frameai()
        return

    elif opcao == "4":
        return

    else:
        print("  Opção inválida.")
        menu_frameai()

# -----------------------------------------------------------------------------

def menu_historico():
    """
    Funcionalidade 3 — Histórico de Preferências
    Mostra quando o usuário divergiu da IA e estatísticas de uso (RF09).
    """
    print()
    print("--- HISTÓRICO DE PREFERÊNCIAS DO USUÁRIO ---")

    total_divergencias_registradas = total_divergencias()

    if total_divergencias_registradas == 0:
        print("  Nenhuma divergência registrada ainda.")
        print("  Quando você escolher um frame diferente da IA, aparecerá aqui.")
        return

    print(f"  Total de divergências com o FrameAI: {total_divergencias_registradas}")
    print()
    print("  Detalhes:")

    for i, entrada in enumerate(historico_preferencias):
        id_ia, id_usuario, cena = entrada
        print(f"  {i + 1}. Cena: '{cena}'")
        print(f"     IA sugeriu Frame #{id_ia} → Usuário preferiu Frame #{id_usuario}")

    # Dica de personalização
    if total_divergencias_registradas >= 3:
        print()
        print("  💡 Com base no seu histórico, o FrameAI está ajustando")
        print("     seus critérios ao seu perfil de preferências.")

# -----------------------------------------------------------------------------

def menu_configuracoes():
    """
    Funcionalidade 4 — Configurações do modo Alive
    Permite ativar/desativar o modo e ajustar parâmetros (RN03).
    """
    while True:
        print()
        print("--- CONFIGURAÇÕES DO MODO ALIVE ---")
        print()
        exibir_configuracoes()
        print()
        print("  1. Ativar / Desativar modo Alive")
        print("  2. Alterar tempo de buffer")
        print("  3. Ativar / Desativar auto-salvar")
        print("  4. Voltar")

        opcao = input("  Opção: ").strip()

        if opcao == "1":
            # Alterna o estado do modo Alive (RN03)
            configuracoes["modo_alive_ativo"] = not configuracoes["modo_alive_ativo"]
            estado = "ATIVADO ✓" if configuracoes["modo_alive_ativo"] else "DESATIVADO ✗"
            print(f"  Modo Alive {estado}.")

            # Ao desativar, descarta o buffer (RN04)
            if not configuracoes["modo_alive_ativo"] and buffer_frames:
                limpar_buffer()
                print("  Buffer descartado automaticamente.")

        elif opcao == "2":
            while True:
                novo_tempo = input("  Novo tempo de buffer (3 a 10 segundos): ").strip()

                if not novo_tempo.isdigit():
                    print("  ⚠ Digite apenas um número inteiro.")
                    continue

                tempo = int(novo_tempo)
                if tempo < 3 or tempo > 10:
                    print("  ⚠ O tempo deve estar entre 3 e 10 segundos.")
                    continue

                configuracoes["tempo_buffer"] = tempo
                print(f"  ✓ Buffer configurado para {tempo} segundos.")
                break

        elif opcao == "3":
            configuracoes["auto_salvar"] = not configuracoes["auto_salvar"]
            estado = "ATIVADO ✓" if configuracoes["auto_salvar"] else "DESATIVADO ✗"
            print(f"  Auto-salvar {estado}.")

        elif opcao == "4":
            return

        else:
            print("  Opção inválida.")

# =============================================================================
# PONTO DE ENTRADA
# =============================================================================

def main():
    print()
    print("  Bem-vindo ao JOVI Alive — FrameAI + ReplayLens")
    print("  Challenge JOVI Smartphone 2026 | FIAP")
    menu_principal()

main()