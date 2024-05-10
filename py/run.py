from interpreter import interpreter, crisp_decompiler
from pathlib import Path
import os



interpretation_search_folder = './asm'
interpretation_file_suffix = '.s'

decompilation_search_folder = './crisp'
decompilation_file_suffix = '.crisp'



def cli():
    while True:
        inp = input('> ').strip().casefold()
        if inp in ('exit', 'quit'): break
        elif inp == 'help':
            print("\n'exit/quit': exits the program\n" +
                  "'help': print this message\n" +
                  "'run [path]': runs the given file\n" +
                  "'compile [path]': compiles the given file into the CRISP format(for more information type 'crisphelp')\n" +
                  "'decompile [path]': decompiles the given CRISP file and runs it\n" +
                  "'decompile-f [path]': decompiles the given CRISP file and and saves it as a '-decomp.s' file\n")
        elif inp == 'crisphelp':
            print("\nThe CRISP(no, I'm not British) format is a bytecode format for the RISCPY interpreter.\n" +
                  "While yes, it is entirely useless, it does have *some* perks.\n" +
                  "It's smaller than a normal .s file because it forfeits all those useless things like 'spaces' and 'comments'(ew)," +
                  "\nallowing for less space used.\n\n" +
                  "TL;DR, it's like Java bytecode, but it's not Java so it's automatically superior.\n")
        elif inp.startswith('run '):
            file = Path(interpretation_search_folder, inp.removeprefix('run ').removesuffix(interpretation_file_suffix) + interpretation_file_suffix)
            if not file.exists(): print(f"path '{file}' does not exist"); continue
            with open(file, 'rt') as f: content = f.read()
            interpreter(content)
        elif inp.startswith('compile '):
            file = Path(interpretation_search_folder, inp.removeprefix('compile ').removesuffix(interpretation_file_suffix) + interpretation_file_suffix)
            if not file.exists(): print(f"path '{file}' does not exist"); continue
            with open(file, 'rt') as f: content = f.read()
            interpreter(content, True, str(file).rsplit('/')[-1].removesuffix(interpretation_file_suffix))
        elif inp.startswith('decompile '):
            file = Path(decompilation_search_folder, inp.removeprefix('decompile ').removesuffix(decompilation_file_suffix) + decompilation_file_suffix)
            if not file.exists(): print(f"path '{file}' does not exist"); continue
            with open(file, 'rb') as f: content = f.read()
            decompiled = crisp_decompiler(content)
            #print(decompiled)
            interpreter(decompiled)
        elif inp.startswith('decompile-f '):
            file = Path(decompilation_search_folder, inp.removeprefix('decompile-f ').removesuffix(decompilation_file_suffix) + decompilation_file_suffix)
            if not file.exists(): print(f"path '{file}' does not exist"); continue
            with open(file, 'rb') as f: content = f.read()
            decompiled = crisp_decompiler(content)
            out_path = f'./asm/{str(file).rsplit('/')[-1].removesuffix(decompilation_file_suffix)}-decomp.s'
            if os.path.exists(out_path): print(f"cannot decompile, file '{out_path}' already exists"); continue
            with open(out_path, 'xt') as out_decomp:
                out_decomp.write(decompiled)



if __name__ == "__main__":
    cli()