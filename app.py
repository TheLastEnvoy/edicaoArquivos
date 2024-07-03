import streamlit as st
import pandas as pd
from PyPDF2 import PdfReader, PdfWriter
from fpdf import FPDF
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from io import BytesIO

def carregar_arquivo(tipo):
    return st.sidebar.file_uploader(f"Selecionar Arquivo {tipo}", type=["xlsx", "csv", "pdf"])

def converter_excel_para_csv(uploaded_file):
    df = pd.read_excel(uploaded_file, engine='openpyxl')
    output = BytesIO()
    df.to_csv(output, index=False)
    output.seek(0)
    return output, uploaded_file.name.replace('.xlsx', '.csv')

def converter_csv_para_excel(uploaded_file):
    df = pd.read_csv(uploaded_file)
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
    output.seek(0)
    return output, uploaded_file.name.replace('.csv', '.xlsx')

def extrair_texto_pdf(uploaded_file):
    reader = PdfReader(uploaded_file)
    texto = ""
    for page in reader.pages:
        texto += page.extract_text()
    return texto

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

def main():
    st.title("Ferramentas de Conversão e Edição de Arquivos")
    
    st.sidebar.header("Carregar Arquivos")
    arquivo_excel = carregar_arquivo("Excel")
    arquivo_csv = carregar_arquivo("CSV")
    arquivo_pdf = carregar_arquivo("PDF")
    arquivos_pdfs = st.sidebar.file_uploader("Selecionar Vários PDFs para Mesclar", type=["pdf"], accept_multiple_files=True)

    st.sidebar.header("Opções de Conversão")
    if arquivo_excel is not None:
        if st.sidebar.button("Converter Excel para CSV"):
            output, nome_arquivo = converter_excel_para_csv(arquivo_excel)
            st.download_button(label="Baixar CSV", data=output, file_name=nome_arquivo, mime="text/csv")

    if arquivo_csv is not None:
        if st.sidebar.button("Converter CSV para Excel"):
            output, nome_arquivo = converter_csv_para_excel(arquivo_csv)
            st.download_button(label="Baixar Excel", data=output, file_name=nome_arquivo, mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    st.sidebar.header("Opções de Edição de PDF")
    if arquivo_pdf is not None:
        if st.sidebar.button("Extrair Texto do PDF"):
            texto = extrair_texto_pdf(arquivo_pdf)
            st.text_area("Texto Extraído", texto, height=300)

    if len(arquivos_pdfs) > 0:
        if st.sidebar.button("Mesclar PDFs"):
            output, nome_arquivo = mesclar_pdfs(arquivos_pdfs)
            st.download_button(label="Baixar PDF Mesclado", data=output, file_name=nome_arquivo, mime="application/pdf")

if __name__ == "__main__":
    main()
