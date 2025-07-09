import os
import subprocess
def open_files(paths):
    for path in paths:
        if os.path.exists(path):
            try:
                if path.lower().endswith('.exe'):
                    subprocess.Popen(path)
                else:
                    try:
                        os.startfile(path)
                    except AttributeError:
                        # os.startfileが無い環境(一部PyInstaller exe)用
                        import subprocess
                        subprocess.Popen(['cmd', '/c', 'start', '', path], shell=True)
            except Exception as e:
                pass
        else:
            pass
def load_paths_from(txt_path):
    if not os.path.exists(txt_path):
        return []
    with open(txt_path, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip()]
if __name__ == '__main__':
    import sys
    import os
    if getattr(sys, 'frozen', False):
        # exeで実行時
        base_dir = os.path.dirname(sys.executable)
    else:
        base_dir = os.path.dirname(os.path.abspath(__file__))
    txt_path = os.path.join(base_dir, os.path.basename(r"pdf1.txt"))
    paths = load_paths_from(txt_path)
    open_files(paths)
