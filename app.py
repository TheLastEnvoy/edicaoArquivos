import streamlit as st
from PyPDF2 import PdfReader, PdfWriter
from io import BytesIO

def carregar_pdf(label):
    return st.sidebar.file_uploader(label, type=["pdf"])

def extrair_texto_pdf(uploaded_file):
    reader = PdfReader(uploaded_file)
    texto = ""
    for page in reader.pages:
        texto += page.extract_text()
    return texto

def reordenar_paginas_pdf(uploaded_file, ordem):
    reader = PdfReader(uploaded_file)
    writer = PdfWriter()
    for i in ordem:
        writer.add_page(reader.pages[i - 1])
    output = BytesIO()
    writer.write(output)
    output.seek(0)
    return output, "pdf_reordenado.pdf"

def mesclar_pdfs(uploaded_files):
    writer = PdfWriter()
    for uploaded_file in uploaded_files:
        reader = PdfReader(uploaded_file)
        for page in reader.pages:
            writer.add_page(page)
    output = BytesIO()
    writer.write(output)
    output.seek(0)
    return output, "pdf_mesclado.pdf"

def dividir_pdf(uploaded_file, intervalo):
    reader = PdfReader(uploaded_file)
    writer = PdfWriter()
    for i in range(intervalo[0] - 1, intervalo[1]):
        writer.add_page(reader.pages[i])
    output = BytesIO()
    writer.write(output)
    output.seek(0)
    return output, f"pdf_dividido_{intervalo[0]}_{intervalo[1]}.pdf"

def remover_paginas_pdf(uploaded_file, paginas):
    reader = PdfReader(uploaded_file)
    writer = PdfWriter()
    total_pages = len(reader.pages)
    paginas_a_manter = [i for i in range(total_pages) if i + 1 not in paginas]
    for i in paginas_a_manter:
        writer.add_page(reader.pages[i])
    output = BytesIO()
    writer.write(output)
    output.seek(0)
    return output, "pdf_paginas_removidas.pdf"

def main():
    st.title("Editor de PDFs")

    st.sidebar.header("Upload de Arquivos PDF")
    uploaded_pdf = carregar_pdf("Selecionar PDF")
    uploaded_pdfs = st.sidebar.file_uploader("Selecionar Vários PDFs para Mesclar", type=["pdf"], accept_multiple_files=True)

    st.sidebar.header("Extrair Texto")
    if uploaded_pdf:
        if st.sidebar.button("Extrair Texto"):
            texto = extrair_texto_pdf(uploaded_pdf)
            st.text_area("Texto Extraído", texto, height=300)

    st.sidebar.header("Reordenar Páginas")
    if uploaded_pdf:
        num_paginas = len(PdfReader(uploaded_pdf).pages)
        ordem = st.sidebar.text_input(f"Insira a nova ordem das páginas (1-{num_paginas}), separado por vírgulas")
        if st.sidebar.button("Reordenar Páginas"):
            if ordem:
                ordem = list(map(int, ordem.split(',')))
                if all(1 <= x <= num_paginas for x in ordem):
                    output, nome_arquivo = reordenar_paginas_pdf(uploaded_pdf, ordem)
                    st.download_button(label="Baixar PDF Reordenado", data=output, file_name=nome_arquivo, mime="application/pdf")
                else:
                    st.warning("Ordem das páginas inválida.")

    st.sidebar.header("Mesclar PDFs")
    if len(uploaded_pdfs) > 0:
        if st.sidebar.button("Mesclar PDFs"):
            output, nome_arquivo = mesclar_pdfs(uploaded_pdfs)
            st.download_button(label="Baixar PDF Mesclado", data=output, file_name=nome_arquivo, mime="application/pdf")

    st.sidebar.header("Dividir PDF")
    if uploaded_pdf:
        num_paginas = len(PdfReader(uploaded_pdf).pages)
        inicio = st.sidebar.number_input("Página Inicial", min_value=1, max_value=num_paginas, value=1)
        fim = st.sidebar.number_input("Página Final", min_value=1, max_value=num_paginas, value=num_paginas)
        if st.sidebar.button("Dividir PDF"):
            if inicio <= fim:
                output, nome_arquivo = dividir_pdf(uploaded_pdf, (inicio, fim))
                st.download_button(label="Baixar PDF Dividido", data=output, file_name=nome_arquivo, mime="application/pdf")
            else:
                st.warning("O valor da Página Inicial deve ser menor ou igual ao valor da Página Final.")

    st.sidebar.header("Remover Páginas")
    if uploaded_pdf:
        paginas = st.sidebar.text_input("Páginas para remover, separadas por vírgulas")
        if st.sidebar.button("Remover Páginas"):
            if paginas:
                paginas = list(map(int, paginas.split(',')))
                output, nome_arquivo = remover_paginas_pdf(uploaded_pdf, paginas)
                st.download_button(label="Baixar PDF com Páginas Removidas", data=output, file_name=nome_arquivo, mime="application/pdf")

if __name__ == "__main__":
    main()
