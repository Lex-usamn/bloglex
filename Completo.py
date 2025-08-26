import os
import re
import shutil
import subprocess

# --- CONFIGURAÇÃO DE PASTAS ---

# 1. Pasta onde você escreve os posts no Obsidian
obsidian_posts_source_dir = r"E:\telos\Vida\posts"

# 2. Pasta de destino final dos posts no seu site Hugo
hugo_posts_dest_dir = r"E:\site\gblog\bloglex\content\posts"

# 3. Pasta geral de anexos (imagens) do seu cofre Obsidian
attachments_source_dir = r"E:\telos\Vida" 

# 4. Pasta para arquivar os posts do Obsidian que já foram processados
processed_posts_archive_dir = r"E:\telos\Vida\posts_processados"

# 5. (NOVO) Caminho para a pasta principal do seu site (onde fica o repositório Git)
hugo_site_git_repo_path = r"E:\site\gblog\bloglex"

# --- FIM DA CONFIGURAÇÃO ---


def atualizar_github(repo_path, commit_message):
    """
    Executa os comandos git para adicionar, commitar e enviar as alterações.
    """
    print("\n--- ETAPA 5: ATUALIZANDO O GITHUB ---")
    try:
        # Comando 1: git add -A
        print("    - Executando 'git add -A'...")
        subprocess.run(
            ["git", "add", "-A"], 
            cwd=repo_path, 
            check=True, 
            capture_output=True
        )
        print("    ✅ Arquivos adicionados ao stage.")

        # Comando 2: git commit
        print(f"    - Executando 'git commit' com a mensagem: \"{commit_message}\"")
        subprocess.run(
            ["git", "commit", "-m", commit_message], 
            cwd=repo_path, 
            check=True, 
            capture_output=True
        )
        print("    ✅ Alterações commitadas.")

        # Comando 3: git push
        print("    - Executando 'git push'...")
        subprocess.run(
            ["git", "push"], 
            cwd=repo_path, 
            check=True, 
            capture_output=True
        )
        print("    ✅ Push para o repositório remoto realizado com sucesso!")
        return True

    except FileNotFoundError:
        print("\n[ERRO] O comando 'git' não foi encontrado.")
        print("      Verifique se o Git está instalado e no PATH do seu sistema.")
        return False
    except subprocess.CalledProcessError as e:
        print(f"\n[ERRO] Um comando do Git falhou:")
        print(f"      Comando: {' '.join(e.cmd)}")
        print(f"      Erro: {e.stderr.decode('utf-8', errors='ignore')}")
        return False


# --- INÍCIO DO SCRIPT PRINCIPAL ---
print("="*50)
print("INICIANDO PROCESSADOR DE POSTS OBSIDIAN PARA HUGO")
print("="*50)

os.makedirs(processed_posts_archive_dir, exist_ok=True)

try:
    source_files = [f for f in os.listdir(obsidian_posts_source_dir) if f.endswith('.md')]
    if not source_files:
        print(f"\nNenhum post (.md) encontrado em: '{obsidian_posts_source_dir}'")
        print("Processo finalizado.")
        exit()
except FileNotFoundError:
    print(f"\n[ERRO] A pasta de origem dos posts não foi encontrada: '{obsidian_posts_source_dir}'")
    print("Verifique o caminho na configuração do script.")
    exit()

posts_foram_processados = False
for md_filename in source_files:
    source_md_path = os.path.join(obsidian_posts_source_dir, md_filename)
    
    # ETAPA 1: COPIAR O POST E CRIAR A ESTRUTURA
    folder_name = os.path.splitext(md_filename)[0]
    hugo_post_folder_path = os.path.join(hugo_posts_dest_dir, folder_name)

    print(f"\n--- Processando post: {md_filename} ---")

    if os.path.exists(hugo_post_folder_path):
        overwrite = input(f"    ⚠️  Aviso: O post '{folder_name}' já existe. Deseja sobrescrevê-lo? (s/n): ").lower()
        if overwrite != 's':
            print("    - Post pulado pelo usuário.")
            continue

    os.makedirs(hugo_post_folder_path, exist_ok=True)
    dest_md_path = os.path.join(hugo_post_folder_path, "index.md")
    shutil.copy2(source_md_path, dest_md_path)
    print(f"    ✅ Post copiado e estruturado em: {dest_md_path}")

    # ETAPA 2: PROCESSAR A THUMBNAIL
    thumbnail_path_input = input(f"    Arraste a imagem para a THUMBNAIL e pressione Enter (ou pule): ")
    thumbnail_source_path = thumbnail_path_input.strip().strip('"')

    if thumbnail_source_path and os.path.exists(thumbnail_source_path):
        _, extension = os.path.splitext(thumbnail_source_path)
        thumbnail_dest_path = os.path.join(hugo_post_folder_path, f"featured{extension}")
        shutil.copy(thumbnail_source_path, thumbnail_dest_path)
        print(f"    ✅ Thumbnail copiada para: {thumbnail_dest_path}")
    elif thumbnail_source_path:
        print(f"    ⚠️  Aviso: Caminho da thumbnail não encontrado.")
    else:
        print("    - Thumbnail pulada.")

    # ETAPA 3: PROCESSAR IMAGENS INTERNAS
    with open(dest_md_path, "r", encoding="utf-8") as file:
        content = file.read()
    
    images_found = re.findall(r'\[\[([^]]*\.(?:png|jpg|jpeg|gif|webp))\]\]', content)
    
    if not images_found:
        print("    - Nenhuma imagem interna encontrada no post.")
    else:
        content_changed = False
        for image_filename in images_found:
            image_source_path = os.path.join(attachments_source_dir, image_filename)
            if os.path.exists(image_source_path):
                shutil.copy(image_source_path, os.path.join(hugo_post_folder_path, image_filename))
                markdown_image_link = f"![Image Description]({image_filename.replace(' ', '%20')})"
                content = content.replace(f"[[{image_filename}]]", markdown_image_link)
                content_changed = True
            else:
                print(f"      ⚠️  Aviso: Imagem '{image_filename}' não encontrada.")
        if content_changed:
            with open(dest_md_path, "w", encoding="utf-8") as file:
                file.write(content)
            print("    ✅ Conteúdo do post (links de imagem) atualizado.")

    # ETAPA 4: ARQUIVAR O POST ORIGINAL
    archive_path = os.path.join(processed_posts_archive_dir, md_filename)
    shutil.move(source_md_path, archive_path)
    print(f"    ✅ Post original movido para a pasta de arquivados.")
    posts_foram_processados = True

# --- FINALIZAÇÃO E PUBLICAÇÃO ---
if posts_foram_processados:
    publicar = input("\n\nProcessamento de arquivos finalizado. Deseja publicar as alterações no GitHub agora? (s/n): ").lower()
    if publicar == 's':
        commit_msg = input("    - Digite a mensagem do commit (ex: 'adiciona novo post sobre X'): ")
        if not commit_msg:
            commit_msg = "build: atualiza conteúdo do blog via script"
            print(f"    - Nenhuma mensagem fornecida. Usando mensagem padrão: '{commit_msg}'")
        
        atualizar_github(hugo_site_git_repo_path, commit_msg)
    else:
        print("\nPublicação no GitHub pulada pelo usuário.")

print("\n\nProcesso finalizado!")