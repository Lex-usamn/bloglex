import os
import re
import shutil

# --- CONFIGURAÇÃO ---
posts_dir = r"E:\site\usa\content\posts"
attachments_dir = r"E:\telos\Vida"
# O diretório static/images não é mais o destino principal para imagens de posts
# static_images_dir = r"E:\site\usa\static\images" 

print("Iniciando o processamento de posts e thumbnails...")

# Itera sobre cada item no diretório de posts
for post_folder_name in os.listdir(posts_dir):
    post_folder_path = os.path.join(posts_dir, post_folder_name)

    # Garante que estamos processando apenas diretórios (pastas de posts)
    if os.path.isdir(post_folder_path):
        index_md_path = os.path.join(post_folder_path, "index.md")

        # Verifica se o arquivo index.md existe no diretório
        if not os.path.exists(index_md_path):
            continue

        print(f"\n--- Processando post: {post_folder_name} ---")

        # --- ETAPA 1: PROCESSAR A THUMBNAIL ---
        # Pergunta ao usuário pelo caminho da imagem de thumbnail
        thumbnail_path_input = input(f"    Arraste a imagem para a THUMBNAIL de '{post_folder_name}' e pressione Enter (ou deixe em branco para pular): ")
        
        # Limpa o caminho (remove aspas extras que o 'arrastar e soltar' pode adicionar)
        thumbnail_source_path = thumbnail_path_input.strip().strip('"')

        if thumbnail_source_path and os.path.exists(thumbnail_source_path):
            # Pega a extensão do arquivo original
            _, extension = os.path.splitext(thumbnail_source_path)
            # Define o destino como 'featured.ext' dentro da pasta do post
            thumbnail_dest_path = os.path.join(post_folder_path, f"featured{extension}")
            
            # Copia e renomeia a thumbnail
            shutil.copy(thumbnail_source_path, thumbnail_dest_path)
            print(f"    ✅ Thumbnail copiada para: {thumbnail_dest_path}")
        elif thumbnail_source_path:
            print(f"    ⚠️  Aviso: Caminho da thumbnail não encontrado. Pulando.")
        else:
            print("    - Thumbnail pulada.")

        # --- ETAPA 2: PROCESSAR IMAGENS DENTRO DO POST ---
        with open(index_md_path, "r", encoding="utf-8") as file:
            content = file.read()
        
        # Encontra todos os links de imagem do Obsidian
        images_found = re.findall(r'\[\[([^]]*\.(?:png|jpg|jpeg|gif|webp))\]\]', content)
        
        if not images_found:
            print("    - Nenhuma imagem interna encontrada no post.")
            continue

        content_changed = False
        for image_filename in images_found:
            # Constrói o caminho de origem da imagem no vault do Obsidian
            image_source_path = os.path.join(attachments_dir, image_filename)

            if os.path.exists(image_source_path):
                # O destino da imagem agora é a própria pasta do post
                image_dest_path = os.path.join(post_folder_path, image_filename)
                shutil.copy(image_source_path, image_dest_path)
                
                # ATUALIZA O LINK NO MARKDOWN para ser relativo
                # De: [[Pasted image 2024.png]]
                # Para: ![Image Description](Pasted%20image%202024.png)
                # OBS: O Hugo é inteligente o suficiente para lidar com espaços, mas usar %20 é mais seguro.
                markdown_image_link = f"![Image Description]({image_filename.replace(' ', '%20')})"
                
                # Substitui no conteúdo
                content = content.replace(f"[[{image_filename}]]", markdown_image_link)
                content_changed = True
                print(f"    - Imagem '{image_filename}' processada e link atualizado.")
            else:
                print(f"    ⚠️  Aviso: Imagem '{image_filename}' não encontrada no diretório de anexos.")
        
        # Escreve o conteúdo atualizado de volta no arquivo index.md se algo mudou
        if content_changed:
            with open(index_md_path, "w", encoding="utf-8") as file:
                file.write(content)
            print("    ✅ Conteúdo do post atualizado.")

print("\n\nProcesso finalizado!")