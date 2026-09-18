"""
Script de Inventário e Controle de Versões — Fase 0 da Auditoria 10/10.
Calcula SHA-256 de todos os arquivos relevantes em C:\MathDoCarvalho,
compara versões de CLG_FOUNDATIONS_ARXIV.tex, monografias, relatórios e scripts,
e verifica a identidade byte a byte entre arquivos externos e os pacotes ZIP.
"""
import os
import hashlib
import zipfile
import json
import re

ROOT_DIR = r"C:\MathDoCarvalho"
REPO_DIR = os.path.join(ROOT_DIR, "P_NP")
PUB_DIR = os.path.join(REPO_DIR, "Publicacoes")
MENS_DIR = os.path.join(ROOT_DIR, "Mensagens")

def sha256_file(filepath):
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()

def main():
    inventory = {}
    
    # 1. Hashes de ZIPs
    zips = {
        "Enviar_19_root": os.path.join(ROOT_DIR, "Enviar_19.zip"),
        "Enviar_19_mensagens": os.path.join(MENS_DIR, "Enviar_19.zip"),
        "arxiv_package_pub": os.path.join(PUB_DIR, "arxiv_package.zip")
    }
    zip_hashes = {}
    for k, p in zips.items():
        if os.path.exists(p):
            zip_hashes[k] = {
                "path": p,
                "size": os.path.getsize(p),
                "sha256": sha256_file(p)
            }
        else:
            zip_hashes[k] = "NOT_FOUND"
            
    # 2. Arquivos centrais do Artigo e Bibliografia
    core_files = [
        os.path.join(PUB_DIR, "CLG_FOUNDATIONS_ARXIV.tex"),
        os.path.join(PUB_DIR, "CLG_FOUNDATIONS_ARXIV.bbl"),
        os.path.join(PUB_DIR, "clg_references.bib"),
        os.path.join(PUB_DIR, "ESTUDO_ANALITICO_DO_CONJUNTO_CRITICO.md"),
        os.path.join(PUB_DIR, "CLG_FOUNDATIONS.md"),
        os.path.join(ROOT_DIR, "CLG_FOUNDATIONS_ARXIV.bbl"),
        os.path.join(ROOT_DIR, "clg_references.bib"),
        os.path.join(PUB_DIR, "fig_clg_teorema1_caixa_fracionaria.png"),
        os.path.join(PUB_DIR, "fig_clg_teorema3_4_harmonic_saddles_vertices.png"),
        os.path.join(PUB_DIR, "fig_clg_teorema5_6_softplus_convexity_bifurcation.png"),
        os.path.join(REPO_DIR, "tests", "test_parecer19_auditoria.py")
    ]
    file_hashes = {}
    for p in core_files:
        if os.path.exists(p):
            file_hashes[p] = {
                "size": os.path.getsize(p),
                "sha256": sha256_file(p)
            }
        else:
            file_hashes[p] = "NOT_FOUND"

    # 3. Comparação com o conteúdo interno de arxiv_package.zip
    arxiv_zip_content = {}
    arxiv_zip_path = os.path.join(PUB_DIR, "arxiv_package.zip")
    if os.path.exists(arxiv_zip_path):
        with zipfile.ZipFile(arxiv_zip_path, "r") as zf:
            for info in zf.infolist():
                data = zf.read(info.filename)
                arxiv_zip_content[info.filename] = {
                    "size": info.file_size,
                    "crc": info.CRC,
                    "sha256": sha256_bytes(data)
                }

    # 4. Comparação com o conteúdo interno de Enviar_19.zip
    enviar19_zip_content = {}
    enviar19_path = os.path.join(ROOT_DIR, "Enviar_19.zip")
    if os.path.exists(enviar19_path):
        with zipfile.ZipFile(enviar19_path, "r") as zf:
            for info in zf.infolist():
                data = zf.read(info.filename)
                enviar19_zip_content[info.filename] = {
                    "size": info.file_size,
                    "crc": info.CRC,
                    "sha256": sha256_bytes(data)
                }

    # 5. Análise de citações em CLG_FOUNDATIONS_ARXIV.tex
    tex_path = os.path.join(PUB_DIR, "CLG_FOUNDATIONS_ARXIV.tex")
    with open(tex_path, "r", encoding="utf-8") as f:
        tex_text = f.read()
    cites = re.findall(r"\\cite\{([^}]+)\}", tex_text)
    cited_keys = set()
    for c in cites:
        for k in c.split(','):
            cited_keys.add(k.strip())
            
    bib_path = os.path.join(PUB_DIR, "clg_references.bib")
    with open(bib_path, "r", encoding="utf-8") as f:
        bib_text = f.read()
    bib_keys = set(re.findall(r"@\w+\{([^,]+),", bib_text))
    
    bbl_path = os.path.join(PUB_DIR, "CLG_FOUNDATIONS_ARXIV.bbl")
    with open(bbl_path, "r", encoding="utf-8") as f:
        bbl_text = f.read()
    bbl_keys = set(re.findall(r"\\bibitem\{([^}]+)\}", bbl_text))

    missing_in_bib = sorted(list(cited_keys - bib_keys))
    missing_in_bbl = sorted(list(cited_keys - bbl_keys))
    
    # 6. Verificação de figuras referenciadas no LaTeX
    graphics = re.findall(r"\\includegraphics(?:\[.*?\])?\{([^}]+)\}", tex_text)
    missing_figs = []
    for g in graphics:
        p = os.path.join(PUB_DIR, g)
        if not os.path.exists(p):
            missing_figs.append(g)

    report = {
        "zip_hashes": zip_hashes,
        "file_hashes": file_hashes,
        "arxiv_zip_content": arxiv_zip_content,
        "enviar19_zip_content": enviar19_zip_content,
        "citation_analysis": {
            "num_cited_keys": len(cited_keys),
            "num_bib_keys": len(bib_keys),
            "num_bbl_keys": len(bbl_keys),
            "missing_in_bib": missing_in_bib,
            "missing_in_bbl": missing_in_bbl,
            "cited_keys": sorted(list(cited_keys))
        },
        "graphics_analysis": {
            "graphics_in_tex": graphics,
            "missing_figs": missing_figs
        }
    }
    
    out_path = os.path.join(ROOT_DIR, "FASE0_INVENTARIO_HASHES.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
    print(f"Inventário salvo com sucesso em {out_path}")

if __name__ == "__main__":
    main()
