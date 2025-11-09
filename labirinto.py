"""
Wrapper script - versão desktop movida para `desktop/`.

Para rodar a versão Pygame execute:

    cd desktop
    python3 labirinto.py

Este arquivo existe apenas para compatibilidade. Veja `desktop/README.md` para mais detalhes.
"""

if __name__ == '__main__':
    print("A versão desktop foi movida para a pasta 'desktop/'. Rode: cd desktop && python3 labirinto.py")
                passos = len(caminho_solucao_bfs) - 1
                tempo_ms = tempo_bfs * 1000
                texto_algo = fonte.render("ALGORITMO: BFS", True, TEXTO_COR)
                texto_stats = fonte.render(f"TEMPO: {tempo_ms:.2f} ms | PASSOS: {passos}", True, TEXTO_COR)
                tela.blit(texto_algo, texto_algo.get_rect(midleft=(15, INFO_BAR_HEIGHT // 2)))
                tela.blit(texto_stats, texto_stats.get_rect(midright=(largura_tela - 15, INFO_BAR_HEIGHT // 2)))
            
            elif mostrar_solucao_dfs and caminho_solucao_dfs:
                passos = len(caminho_solucao_dfs) - 1
                tempo_ms = tempo_dfs * 1000
                texto_algo = fonte.render("ALGORITMO: DFS", True, TEXTO_COR)
                texto_stats = fonte.render(f"TEMPO: {tempo_ms:.2f} ms | PASSOS: {passos}", True, TEXTO_COR)
                tela.blit(texto_algo, texto_algo.get_rect(midleft=(15, INFO_BAR_HEIGHT // 2)))
                tela.blit(texto_stats, texto_stats.get_rect(midright=(largura_tela - 15, INFO_BAR_HEIGHT // 2)))
            else:
                 tela.blit(texto_ajuda, texto_ajuda_rect)

            tela.blit(surface_labirinto, (0, INFO_BAR_HEIGHT))

        if jogador_pos == fim and not fim_de_jogo:
            fim_de_jogo = True 
            if jump_scare_pronto:
                tela.fill(PRETO)
                tela.blit(susto_imagem, (0, 0))
                susto_som.play()
                pygame.display.flip()
                pygame.time.wait(2000)
                rodando = False
            else:
                print("Parabéns, você venceu!")
                pygame.time.wait(1000)
                rodando = False
        
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()