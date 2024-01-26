import git
import os
import pypandoc
from concurrent.futures import ProcessPoolExecutor

# Download pandoc
pypandoc.download_pandoc()

# Clone the GitHub repository
repo_url = 'https://github.com/MicrosoftDocs/memdocs.git'
local_repo_path = 'memdocs'
pdf_output_path = 'pdf_docs'

# Clone only if the repo does not exist locally
if not os.path.isdir(local_repo_path):
    git.Repo.clone_from(repo_url, local_repo_path)

# Function to convert Markdown to PDF
def convert_md_to_pdf(md_path, pdf_path):
    # Additional Pandoc arguments
    extra_args = ['--from=markdown-raw_tex', '--pdf-engine=xelatex']
    
    # Error handling
    try:
        pypandoc.convert_file(md_path, 'pdf', outputfile=pdf_path, extra_args=extra_args)
        print(f'Converted {md_path} to {pdf_path}')
    except Exception as e:
        print(f'Error converting {md_path}: {e}')

# Traverse the directory and convert files
for root, dirs, files in os.walk(local_repo_path):
    for file in files:
        if file.endswith('.md'):
            md_file_path = os.path.join(root, file)
            pdf_dir = root.replace(local_repo_path, pdf_output_path)
            os.makedirs(pdf_dir, exist_ok=True)
            pdf_file_path = os.path.join(pdf_dir, file.replace('.md', '.pdf'))
            convert_md_to_pdf(md_file_path, pdf_file_path)

