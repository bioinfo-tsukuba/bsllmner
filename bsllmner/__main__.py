import argparse
from .lib import util
from .lib import ollama_chat


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices=["extract", "select", "all"])
    parser.add_argument('input_filename', help='BioSample JSON file')
    parser.add_argument('-r', '--metasra_tsv', help='MetaSRA output tsv file. Required for selection mode.')
    parser.add_argument('-l', '--llmner_tsv', help='Extraction output tsv file. Required for selection mode.')
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('-t', '--test', action='store_true')
    parser.add_argument('-m', '--model')
    parser.add_argument('-p', '--prompt_filename', default="")
    parser.add_argument('-i', '--prompt_indices', help='Comma-separated prompt ids (required for extract/select)')
    parser.add_argument('-e', '--server', default="ollama", choices=["ollama", "vllm"])
    parser.add_argument('-u', '--host_url', default="")
    parser.add_argument('-o', '--output', default="", help='Output file path (default: stdout)')
    args = parser.parse_args()

    mode = args.mode
    input_json = util.load_json(args.input_filename)
    metasra_tsv = args.metasra_tsv
    llmner_tsv = args.llmner_tsv
    verbose = args.verbose
    test = args.test
    model = args.model
    prompt_filename = args.prompt_filename
    prompt_indices = args.prompt_indices.split(",") if args.prompt_indices else None
    host_url = args.host_url
    server = args.server
    output_path = args.output
    util.print_time()

    # 出力先を決定
    out_handle = open(output_path, "w") if output_path != "" else None

    if mode in ["extract", "select"] and prompt_indices is None:
        parser.error("--prompt_indices is required for extract/select modes")

    if mode == "extract":
        bsner = ollama_chat.BsNer(input_json, model, prompt_filename, prompt_indices, host_url, server, out_handle)
        bsner.ner(verbose, test)
    elif mode == "select":
        bsselect = ollama_chat.BsSelect(input_json, model, prompt_filename, prompt_indices, host_url, metasra_tsv, llmner_tsv, server, out_handle)
        bsselect.select(verbose, test)
    elif mode == "all":
        bsall = ollama_chat.BsAll(input_json, model, prompt_filename, prompt_indices, host_url, server, out_handle)
        bsall.run_all(verbose, test)
    util.print_time()
    if out_handle:
        out_handle.close()
    return


if __name__ == "__main__":
    main()
