
# セットアップ作成・実行モード対応 FreeSimpleGUI
import FreeSimpleGUI as fsg
import os
import subprocess

def open_files(paths):
    for path in paths:
        if os.path.exists(path):
            try:
                if path.lower().endswith('.exe'):
                    subprocess.Popen(path)
                else:
                    os.startfile(path)
            except Exception as e:
                pass  # メッセージはGUIで表示
        else:
            pass

def save_paths_to(txt_path, paths):
    with open(txt_path, 'w', encoding='utf-8') as f:
        for p in paths:
            f.write(p + '\n')

def load_paths_from(txt_path):
    if not os.path.exists(txt_path):
        return []
    with open(txt_path, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip()]

def setup_create():
    def get_txt_files():
        return [f for f in os.listdir('.') if f.endswith('.txt')]
    txt_files = get_txt_files()
    paths = []
    layout = [
        [fsg.Text('既存セットアップ(txt)を選択'),
         fsg.Combo(txt_files, key='-TXTSEL-', enable_events=True, readonly=True, size=(30,1)),
         fsg.Button('読込'), fsg.Button('選択txt削除', key='-DELTXT-'), fsg.Button('複製', key='-COPYTXT-'), fsg.Button('名前変更', key='-RENAMETXT-')],
        [fsg.Input(key='-IN-', enable_events=True, change_submits=True),
         fsg.FilesBrowse('Browse', key='-BROWSE-', target='-IN-'),
         fsg.Button('pathを追加', key='-PATHADD-'), fsg.Button('pathを削除', key='-PATHDEL-')],
        [fsg.Text('登録済みファイル一覧')],
        [fsg.Listbox(values=paths, size=(60, 10), key='-LIST-', select_mode='extended', enable_events=True, horizontal_scroll=True)],
        [fsg.Text('', size=(60, 2), key='-MSG-', text_color='yellow')],
        [fsg.Input('', key='-TXTNAME-', enable_events=True, disabled_readonly_background_color='#e0e0e0'), fsg.Text('.txt'), fsg.Button('保存名で作成')],
        [fsg.Button('完了')]
    ]
    window = fsg.Window('セットアップ作成', layout, return_keyboard_events=True, finalize=True)
    txt_path = ''
    # osはグローバルimport済み
    # Appボタン・アプリ選択関連の関数を削除

    while True:
        event, values = window.read()
        if event in (None, '完了'):
            # 完了時も保存名があれば保存
            name = values['-TXTNAME-'].strip()
            if name:
                txt_path = name + '.txt'
                save_paths_to(txt_path, paths)
            break
        elif event == '読込':
            sel = values['-TXTSEL-']
            if sel:
                paths = load_paths_from(sel)
                window['-LIST-'].update(paths)
                # .txtを除いた名前だけを入力欄に反映
                if sel.endswith('.txt'):
                    window['-TXTNAME-'].update(sel[:-4])
                else:
                    window['-TXTNAME-'].update(sel)
                window['-MSG-'].update(f"{sel} を読み込みました。")
                # txtファイルリストを最新化
                txt_files = get_txt_files()
                window['-TXTSEL-'].update(values=txt_files)
            else:
                window['-MSG-'].update("txtファイルを選択してください。")
        elif event == '-DELTXT-':
            sel = values['-TXTSEL-']
            if sel and os.path.exists(sel):
                try:
                    os.remove(sel)
                    window['-MSG-'].update(f"{sel} を削除しました。")
                    # txtファイルリスト更新
                    txt_files = get_txt_files()
                    window['-TXTSEL-'].update(values=txt_files)
                    window['-TXTSEL-'].update('')
                except Exception as e:
                    window['-MSG-'].update(f"削除失敗: {e}")
            else:
                window['-MSG-'].update("削除するtxtファイルを選択してください。")
        elif event == '-COPYTXT-':
            sel = values['-TXTSEL-']
            if sel and os.path.exists(sel):
                import shutil
                base = sel[:-4] if sel.endswith('.txt') else sel
                newname = base + '_copy'
                i = 1
                while os.path.exists(newname + '.txt'):
                    newname = f"{base}_copy{i}"
                    i += 1
                shutil.copyfile(sel, newname + '.txt')
                window['-MSG-'].update(f"{sel} を {newname}.txt として複製しました。")
                txt_files = get_txt_files()
                window['-TXTSEL-'].update(values=txt_files)
            else:
                window['-MSG-'].update("複製するtxtファイルを選択してください。")
        elif event == '-RENAMETXT-':
            sel = values['-TXTSEL-']
            newname = values['-TXTNAME-'].strip()
            if sel and newname and os.path.exists(sel):
                newfile = newname + '.txt'
                if os.path.exists(newfile):
                    window['-MSG-'].update("同名のファイルが既に存在します。")
                else:
                    os.rename(sel, newfile)
                    window['-MSG-'].update(f"{sel} を {newfile} に名前変更しました。")
                    txt_files = get_txt_files()
                    window['-TXTSEL-'].update(values=txt_files)
                    window['-TXTSEL-'].update(newfile)
            else:
                window['-MSG-'].update("名前変更するtxtファイルと新しい名前を指定してください。")
        elif event == '保存名で作成':
            name = values['-TXTNAME-'].strip()
            if name:
                txt_path = name + '.txt'
                save_paths_to(txt_path, paths)
                window['-MSG-'].update(f"保存ファイル名: {txt_path}")
                # txtファイルリスト更新
                txt_files = [f for f in os.listdir('.') if f.endswith('.txt')]
                window['-TXTSEL-'].update(values=txt_files)
            else:
                window['-MSG-'].update("保存名を入力してください。")
        elif event == '-PATHADD-' or (event == '-IN-' and values['-IN-']):
            # ドラッグ&ドロップやBrowseでの追加も対応
            file_paths = values['-IN-'].strip()
            add_files = []
            if file_paths:
                for f in file_paths.split(';'):
                    f = f.strip()
                    if f and f not in paths:
                        add_files.append(f)
                if add_files:
                    paths.extend(add_files)
                    window['-LIST-'].update(paths)
                    window['-IN-'].update('')
                    window['-MSG-'].update(f"{len(add_files)}件追加しました。")
                    name = values['-TXTNAME-'].strip()
                    if name:
                        txt_path = name + '.txt'
                        save_paths_to(txt_path, paths)
                else:
                    window['-MSG-'].update("新しいファイルはありません。")
            else:
                window['-MSG-'].update("パスを入力またはBrowseで選択してください。")
        # Appボタン関連のイベント処理を削除
        elif event == '-PATHDEL-':
            selected = values['-LIST-']
            if selected:
                paths = [p for p in paths if p not in selected]
                window['-LIST-'].update(paths)
                window['-MSG-'].update(f"{len(selected)}件削除しました。")
                name = values['-TXTNAME-'].strip()
                if name:
                    txt_path = name + '.txt'
                    save_paths_to(txt_path, paths)
            else:
                window['-MSG-'].update("削除するファイルをリストから選択してください。")
        # ファイル存在チェック警告（リスト選択時のみ）
        if event == '-LIST-':
            selected = values['-LIST-']
            if selected:
                notfound = [p for p in selected if not os.path.exists(p)]
                if notfound:
                    window['-MSG-'].update(f"存在しないファイル: {', '.join(notfound)}")
                else:
                    window['-MSG-'].update("")
    window.close()

def setup_run():
    # txtファイル一覧取得
    txt_files = [f for f in os.listdir('.') if f.endswith('.txt')]
    layout = [
        [fsg.Text('実行するセットアップ(txt)を選択')],
        [fsg.Listbox(values=txt_files, size=(40, 8), key='-TXT-', select_mode='extended')],
        [fsg.Text('', size=(40, 2), key='-MSG-', text_color='yellow')],
        [fsg.Button('実行'), fsg.Button('戻る')]
    ]
    window = fsg.Window('セットアップ実行', layout)
    import sys
    while True:
        event, values = window.read()
        if event in (None, '終了', '戻る'):
            break
        elif event == '実行':
            selected = values['-TXT-']
            if selected:
                all_paths = []
                for sel in selected:
                    paths = load_paths_from(sel)
                    all_paths.extend(paths)
                if all_paths:
                    open_files(all_paths)
                    window['-MSG-'].update("全ファイルを実行しました。ウィンドウを閉じます。")
                    window.close()
                    sys.exit(0)
                else:
                    window['-MSG-'].update("選択したtxtにファイルがありません。")
            else:
                window['-MSG-'].update("txtファイルを選択してください。")
    window.close()

def main():
    layout = [
        [fsg.Button('セットアップ作成'), fsg.Button('セットアップ実行'), fsg.Button('終了')]
    ]
    window = fsg.Window('ファイルオープナー 起動', layout)
    while True:
        event, _ = window.read()
        if event in (None, '終了'):
            break
        elif event == 'セットアップ作成':
            window.hide()
            setup_create()
            window.un_hide()
        elif event == 'セットアップ実行':
            window.hide()
            setup_run()
            window.un_hide()
    window.close()

if __name__ == '__main__':
    main()
