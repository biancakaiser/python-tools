# PDF to JSON

Aplicação de linha de comando para ler arquivos PDF e gerar um JSON com metadados,
campos de formulário e o texto extraído de cada página.

## Instalação

Requer Python 3.10 ou mais recente.

```bash
python -m pip install -e .
```

## Uso

Imprima o resultado no terminal:

```bash
pdf-to-json documento.pdf --pretty
```

Grave o resultado em um arquivo:

```bash
pdf-to-json documento.pdf --output documento.json --pretty
```

O JSON contém `metadata`, `pages` e `form_fields`. Cada item de `pages` tem o
número da página e o texto extraído. PDFs escaneados como imagem não têm uma
camada de texto e precisam passar por OCR antes da extração.

Para executar sem instalar o comando:

```bash
python -m pdf_to_json documento.pdf
```

## Testes

```bash
python -m unittest discover -s tests -v
```