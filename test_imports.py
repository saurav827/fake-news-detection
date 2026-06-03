import sys, traceback, importlib
sys.path.append('c:/projects/fake-news-detection')
mods = ['app','backend.database','backend.predictor','frontend.ui']
for m in mods:
    try:
        importlib.import_module(m)
        print(f'{m} imported OK')
    except Exception as e:
        print(f'Error importing {m}: {e}')
        traceback.print_exc()
