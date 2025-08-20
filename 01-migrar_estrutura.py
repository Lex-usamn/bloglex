import os
import shutil

# --- CONFIGURAÇÃO ---
# Altere este caminho para o diretório de posts do seu site Hugo
posts_dir = r"E:\site\usa\content\posts"

print("Iniciando a migração para a estrutura de Page Bundle...")

# Itera sobre todos os arquivos no diretório de posts
for filename in os.listdir(posts_dir):
    filepath = os.path.join(posts_dir, filename)

    # Verifica se é um arquivo Markdown e não uma pasta
    if filename.endswith(".md") and os.path.isfile(filepath):
        # Remove a extensão .md para obter o nome da pasta
        folder_name = os.path.splitext(filename)[0]
        new_post_dir = os.path.join(posts_dir, folder_name)

        # Cria a nova pasta para o post
        os.makedirs(new_post_dir, exist_ok=True)
        print(f"  - Criada pasta: {new_post_dir}")

        # Define o novo caminho do arquivo como index.md dentro da nova pasta
        new_filepath = os.path.join(new_post_dir, "index.md")

        # Move o arquivo .md para a nova pasta com o nome index.md
        shutil.move(filepath, new_filepath)
        print(f"  - Movido '{filename}' para '{new_filepath}'")

print("\nMigração concluída com sucesso!")
print("Agora você pode usar o script principal de processamento.")