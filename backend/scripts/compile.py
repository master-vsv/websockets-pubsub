from pathlib import Path
import subprocess
import os
import shutil

ROOT_DIR = "app/src"
ROOT_COMPILE_DIR = "./compiled"

def pause():
    import signal
    
    print("Pause...t")
    try:
        signal.pause()
    except KeyboardInterrupt:
        pass


def compile_modules_to_pyc():
    print()
    print("Compilation started...")

    try:
        for module in Path(ROOT_DIR).rglob('*.py'):
                       
            module_path_name, module_file_name = os.path.split(module)
            print("-"*100)
            print(f"Module '{module.name}' compilation started...")

            compile_path_name, compile_file_name = os.path.split(module)
            command = f"python -OO -m py_compile {module}"
            result = subprocess.run(command, shell=True, encoding='utf-8', capture_output=True, text=False, check=True)
            
            print(f"Compiled module '{module}'")
            
            compile_files = Path(f"{module_path_name}/__pycache__").glob('*.pyc')
            
            for compile_file in compile_files:
                compile_path_name, compile_file_name = os.path.split(compile_file)
                new_compile_file_name = f'{compile_file_name.split(".")[0]}.pyc'
                dst_path=Path.joinpath(Path(module_path_name), new_compile_file_name)
                print(f"Moved compiled module: '{compile_file}' to '{dst_path}'")
                shutil.move(src=compile_file, dst=dst_path)
            os.remove(module)
            print(f"Removed python module: '{module}'")
    except Exception as error:
        print(f"Compilation failed - '{error}'")
            
    print("-"*100)
    print("Compilation completed.")
    print()
    
def compile_modules_to_so():
    print()
    print("Compilation started...")

    try:
        for module in Path(ROOT_DIR).rglob('*.py'):
            
            if module.name.startswith("settings"):
            
                module_path_name, module_file_name = os.path.split(module)
                print("-"*100)
                print(f"Module '{module.name}' compilation started...")

                
                # command = f"python -m nuitka --module --static-libpython=no --follow-imports --remove-output --no-pyi-file --output-dir={ROOT_COMPILE_DIR}/{module} --jobs=8 {module}"
                command = f'python -m nuitka --module --nofollow-imports --static-libpython=no --remove-output --no-pyi-file --output-dir={ROOT_COMPILE_DIR}/{module} --jobs=4 {module}'
                result = subprocess.run(command, shell=True, encoding='utf-8', capture_output=True, text=False, check=True)
                               
                print(f"Compiled module '{module}'")
                
                compile_files = Path(f"{ROOT_COMPILE_DIR}/{module}").glob('*.so')
                
                for compile_file in compile_files:
                    compile_path_name, compile_file_name = os.path.split(compile_file)
                    new_compile_file_name = f'{compile_file_name.split(".")[0]}.so'
                    dst_path=Path.joinpath(Path(module_path_name), new_compile_file_name)
                    print(f"Moved compiled module: '{compile_file}' to '{dst_path}'")
                    shutil.move(src=compile_file, dst=dst_path)
                os.remove(module)
                print(f"Removed python module: '{module}'")
    except Exception as error:
        print(f"Compilation failed - '{error}'")

    shutil.rmtree(ROOT_COMPILE_DIR)
        
    print("-"*100)
    print("Compilation completed.")
    print()

if __name__ == "__main__":
    compile_modules_to_so()
    compile_modules_to_pyc()

    
    
