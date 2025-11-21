import os

def check_syntax(package_dir='finance_dashboard'):
    base = os.path.join(os.getcwd(), package_dir)
    if not os.path.isdir(base):
        print(f'Pasta do pacote não encontrada: {base}')
        return
    py_files = [os.path.join(base, f) for f in os.listdir(base) if f.endswith('.py')]
    results = []
    for p in py_files:
        try:
            src = open(p, 'r', encoding='utf-8').read()
            compile(src, p, 'exec')
            results.append((p, 'OK', None))
        except Exception as e:
            results.append((p, 'ERROR', f"{type(e).__name__}: {e}"))
    for p, status, err in results:
        if status == 'OK':
            print(f"{os.path.basename(p)} OK")
        else:
            print(f"{os.path.basename(p)} ERROR -> {err}")

if __name__ == '__main__':
    check_syntax()
