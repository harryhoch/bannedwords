#!/usr/bin/python

from docx import Document
import os
import json
import glob
import pdfplumber
import argparse

def search_word_paras(paras: list, word: str) -> list:
    """
    Search for paragraphs containing a specific word.

    Args:
        paras (list): List of paragraphs to search.
        word (str): Word to search for.

    Returns:
        list: List of paragraphs containing the word.
    """
    results = []
    for i in range(len(paras)):
        if word.lower() in paras[i]:
            results.append((i,paras[i]))
    return results

def get_word_paras(d:Document) -> list:
    """
    Get a list of paragraphs from a Document object.

    Args:
        d (Document): Document object to extract paragraphs from.

    Returns:
        list: List of paragraphs from the document.
    """
    paras = [p.text for p in d.paragraphs]
    paras = [p.lower() for p in paras if len(p) > 0]
    return paras

def search_doc_word(d: Document, word: str) -> list:
    paras = get_word_paras(d)
    return search_word_paras(paras,word)

def search_doc_for_categories(d: Document, categories:dict) -> dict:

    paras  =get_word_paras(d)
    return search_paras_for_categories(paras,categories)

def search_paras_for_categories(paras: list, categories:dict) -> dict:
    results = {}
    for category, keywords in categories.items():
        for keyword in keywords:
            hits = search_word_paras(paras,keyword)
            if (len(hits) > 0):
                res = { keyword: hits}
                if category not in results:
                    results[category]   = []
                results[category].append(res)
    return results

def get_pdf_paras(pdf_path: str) -> str:
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    parlist = text.split("\n")
    return [p for p in parlist if len(p) > 0]

def search_pdf_for_categories(pdf_path: str, categories:dict) -> dict:

    paras  =get_pdf_paras(pdf_path)
    return search_paras_for_categories(paras,categories)

def read_docs(directory: str) -> list:
    docx_files = glob.glob(os.path.join(directory, "*.docx"))
    doc_files = glob.glob(os.path.join(directory, "*.doc"))

    return docx_files + doc_files

def read_pdfs(directory: str) -> list:
    pdf_files = glob.glob(os.path.join(directory, "*.pdf"))
    return pdf_files

def check_files(docs: list, pdfs: list, categories: dict) -> dict:
    res = {}
    for d in docs:
        try :
            doc = Document(d)
            r = search_doc_for_categories(doc,categories)
            if len(r)>0:
                res[d]  = r
        except:
            print("unable to process..."+d)

    for p in pdfs: 
        ps = search_pdf_for_categories(p,categories)
        if len(ps)>0:
            res[p] =ps
    return res


def main():
    # get args
    parser = argparse.ArgumentParser(description='Search for banned words in NIH proposal content.')
    parser.add_argument('--category-file', help='Path to the category JSON file')
    parser.add_argument('--directory', help='Path to the directory containing documents to search')
    parser.add_argument('--file',help='Single file to process')
    args = parser.parse_args()

    # 1. read in the json
    # 2. read in docs and pdfs.
    # routine to do all of them together...
    if args.category_file is None:
        print("Please provide a  JSON file with the banned categoriesusing --category-file")
        return
    
    if args.directory is None and args.file is None:
        print("Please provide a directory containing documents to search using --directory or a file to process using --file")
        return
    with open(args.category_file, 'r') as f:
        categories = json.load(f)

    if args.directory is not None:
        docs = read_docs(args.directory)
        pdfs = read_pdfs(args.directory)
        results = check_files(docs,pdfs,categories)
    else:
        results = {}
        if args.file.endswith('.pdf'):
            results[args.file] = search_pdf_for_categories(args.file,categories)
        else:
            doc = Document(args.file)
            results[args.file] = search_doc_for_categories(doc,categories)
    print (json.dumps(results, indent=4))


if __name__ == "__main__":
    main()
