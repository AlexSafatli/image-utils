import io
import os

import PySimpleGUI as sg
from PIL import Image


file_icon = b'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8' \
            b'/9hAAAACXBIWXMAAAsSAAALEgHS3X78AAABU0lEQVQ4y52TzStEURiHn' \
            b'/ecc6XG54JSdlMkNhYWsiILS0lsJaUsLW2Mv8CfIDtr2VtbY4GUEvmIZnKbZsY977Uwt2HcyW1+dTZvt6fn9557BGB+aaNQKBR2ifkbgWR+cX13ubO1svz++niVTA1ArDHDg91UahHFsMxbKWycYsjze4muTsP64vT43v7hSf/A0FgdjQPQWAmco68nB+T+SFSqNUQgcIbN1bn8Z3RwvL22MAvcu8TACFgrpMVZ4aUYcn77BMDkxGgemAGOHIBXxRjBWZMKoCPA2h6qEUSRR2MF6GxUUMUaIUgBCNTnAcm3H2G5YQfgvccYIXAtDH7FoKq/AaqKlbrBj2trFVXfBPAea4SOIIsBeN9kkCwxsNkAqRWy7+B7Z00G3xVc2wZeMSI4S7sVYkSk5Z/4PyBWROqvox3A28PN2cjUwinQC9QyckKALxj4kv2auK0xAAAAAElFTkSuQmCC '


def _check_valid_dir(directory: str):
    directory += os.sep
    if not os.path.isdir(directory):
        raise FileNotFoundError(f"Directory: " + directory + " does not exist")


def get_all_file_paths(directory: str) -> list:
    li = []
    for root, dirs, files in os.walk(directory):
        li.extend([os.path.join(root, f) for f in files])
    return li


def delete_images(image_set: set):
    i = 0
    for f in image_set:
        try:
            os.remove(f)
            print('Deleted:', f)
            i += 1
        except:
            pass
    print("\n***\nDeleted", i, "images.")


def show_duplicate_image_results_in_window(ans: dict) -> bool:
    layout = []
    root = sg.TreeData()
    for k in ans:
        root.Insert('', ans[k]['loc'], ans[k]['fname'],
                    values=[ans[k]['loc'], ans[k]['size']],
                    icon=file_icon)
        for dupe, dupe_size in ans[k]['dupes']:
            root.Insert(ans[k]['loc'], dupe, os.path.basename(dupe),
                        values=[dupe, dupe_size])
    layout.append([sg.Tree(data=root, headings=['Path', 'Size (MB)'],
                           auto_size_columns=True,
                           num_rows=15, col0_width=30, key='-TREE-',
                           show_expanded=False, enable_events=True,
                           expand_y=True, expand_x=True),
                   sg.Image(key='-IMAGE-', size=(550, 550))])
    layout.append([sg.Button('Delete Duplicates'), sg.Button('Cancel')])
    window = sg.Window('find_duplicates', layout, resizable=True)
    inp = False
    while True:
        e, v = window.read()
        if e in (sg.WINDOW_CLOSED, 'Cancel'):
            break
        elif e == 'Delete Duplicates':
            inp = True
            break
        else:
            window['-IMAGE-'].update(data='')
            img_paths = v['-TREE-']
            if len(img_paths) == 0:
                continue
            img = Image.open(img_paths[0])
            img.thumbnail((550, 550))
            bio = io.BytesIO()
            img.save(bio, format='PNG')
            window['-IMAGE-'].update(data=bio.getvalue())
    window.close()
    return inp
