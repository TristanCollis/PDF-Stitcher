import argparse
import pypdf


def join_pdfs(args: argparse.Namespace):
    destination: str = args.destination
    name: str = args.name
    files: list[str] = args.files

    out_path = f"{destination}/{name}"

    if not out_path.endswith(".pdf"):
        out_path += ".pdf"

    out_pdf = pypdf.PdfWriter()

    for file in files:
        print(f"Appending {file}")

        with open(file) as f:
            pdf = pypdf.PdfReader(file)

        for i, page in enumerate(pdf.pages):
            print(f"Page {i}")
            out_pdf.add_page(page)

    print(f"Writing to {out_path}")
    with open(out_path, "wb") as out:
        out_pdf.write(out)


def split_pdf(args: argparse.Namespace):
    destination: str = args.destination
    name: str = args.name.replace(".pdf", "")
    file: str = args.file
    position: int = args.position

    out_prefix = f"{destination}/{name}"

    out_pdf_1 = pypdf.PdfWriter()
    out_pdf_2 = pypdf.PdfWriter()

    with open(file, "rb") as f:
        pdf = pypdf.PdfReader(f)

        for page in pdf.pages[:position]:
            out_pdf_1.add_page(page)
        
        for page in pdf.pages[position:]:
            out_pdf_2.add_page(page)
    
    out_path = f"{out_prefix}_1-{position}.pdf"
    with open(out_path, "wb") as out:
        print(f"Writing to {out_path}")
        out_pdf_1.write(out)

    out_path = f"{out_prefix}_{position+1}-{pdf.get_num_pages()}.pdf"
    with open(out_path, "wb") as out:
        print(f"Writing to {out_path}")
        out_pdf_2.write(out)


parser = argparse.ArgumentParser("PDF Stitcher")
parser.add_argument("destination")
parser.add_argument("name")

subparsers = parser.add_subparsers(required=True)

parser_join = subparsers.add_parser("join")
parser_join.add_argument("files", nargs=argparse.ONE_OR_MORE)
parser_join.set_defaults(func=join_pdfs)

parser_split = subparsers.add_parser("split")
parser_split.add_argument("file")
parser_split.add_argument("position", type=int)
parser_split.set_defaults(func=split_pdf)


args = parser.parse_args()
args.func(args)

print("Done!")