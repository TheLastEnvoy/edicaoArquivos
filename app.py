import streamlit as st
import PyPDF2
import pdfplumber
from io import BytesIO

def carregar_pdf(label):
    return st.sidebar.file_uploader(label, type=["pdf"])

def visualizar_paginas(uploaded_file):
    pdf_pages = []
    with pdfplumber.open(uploaded_file) as pdf:
        for page_num, page in enumerate(pdf.pages, 1):
            with BytesIO() as img_buffer:
                page.to_image().save(img_buffer, format='PNG')
                img_buffer.seek(0)
                pdf_pages.append(img_buffer.read())
    return pdf_pages

def reordenar_paginas_pdf(uploaded_file, ordem):
    reader = PyPDF2.PdfReader(uploaded_file)
    writer = PyPDF2.PdfWriter()
    for i in ordem:
        writer.add_page(reader.pages[i - 1])
    output = BytesIO()
    writer.write(output)
    output.seek(0)
    return output, "pdf_reordenado.pdf"

def main():
    st.title("Editor de PDFs Interativo")

    st.sidebar.header("Upload de Arquivos PDF")
    uploaded_pdf = carregar_pdf("Selecionar PDF")

    if uploaded_pdf:
        pdf_pages = visualizar_paginas(uploaded_pdf)
        num_paginas = len(pdf_pages)
        
        st.header("Visualização das Páginas")
        for page_num, page_img in enumerate(pdf_pages, 1):
            st.image(page_img, caption=f'Página {page_num}', use_column_width=True)

        st.sidebar.header("Reordenar Páginas")
        ordem_input = st.sidebar.text_input(f"Insira a nova ordem das páginas (1-{num_paginas}), separado por vírgulas")
        if st.sidebar.button("Reordenar Páginas"):
            if ordem_input:
                try:
                    ordem = list(map(int, ordem_input.split(',')))
                    if all(1 <= x <= num_paginas for x in ordem):
                        output, nome_arquivo = reordenar_paginas_pdf(uploaded_pdf, ordem)
                        st.download_button(label="Baixar PDF Reordenado", data=output, file_name=nome_arquivo, mime="application/pdf")
                    else:
                        st.warning("Ordem das páginas inválida.")
                except ValueError:
                    st.warning("Por favor, insira números válidos separados por vírgulas.")

if __name__ == "__main__":
    main()
