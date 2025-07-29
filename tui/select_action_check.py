import curses
from tui.action import action
from time import sleep

def custom_print(stdscr, text, y, x):
    stdscr.addstr(y, x, text)
    y0, x0 = stdscr.getyx()
    stdscr.refresh()
    return y0

def custom_input(stdscr, prompt, y, x):
    curses.echo()
    stdscr.addstr(y, x, prompt)
    stdscr.refresh()
    
    input_str = stdscr.getstr(y, x + len(prompt)).decode('utf-8')
    curses.noecho()
    return input_str

def select_action_check(stdscr, result, target):
    stdscr.clear()
    stdscr.refresh()
    if target not in result:
        stdscr.addstr("Please diagnose first.\n\nPress any key to continue.")
        stdscr.getch()
        return
    total_playbooks = len(result[target])
    checked = [False] * total_playbooks
    show_reason = -1

    cursor = [0, 0]
    index = []

    for i in result[target]:
        if result[target][i]['weak'] == True:
            index.append(int(i))

    if not index:
        stdscr.addstr("There is no subject to be inspected.\n\nPress any key to continue.")
        stdscr.getch()
        return

    size = len(index)
    cursor[0] = 0

    while True:
        stdscr.clear()
        current_line = 0

        for i in range(1, total_playbooks+1):
            if result[target][str(i)]['weak'] == 'passed':
                # line = [f'{i:2} {result[target][f'{i}']['diag'].ljust(70, '-')} Passed', curses.A_DIM]
                stdscr.addstr(current_line, 0, f'{i:2} {result[target][f'{i}']['diag'].ljust(70, '-')} Passed', curses.A_DIM)
            elif result[target][f'{i}']['weak'] == None:
                # line = [f"{i:2} {result[target][f'{i}']['diag'].ljust(72, '-')} (N/A)", None]
                stdscr.addstr(current_line, 0, f"{i:2} {result[target][f'{i}']['diag'].ljust(72, '-')} (N/A)")
            elif result[target][f'{i}']['weak'] == True:
                # line = [f"{i:2} {result[target][f'{i}']['diag'].ljust(74, '-')} ❌", None]
                stdscr.addstr(current_line, 0, f"{i:2} {result[target][f'{i}']['diag'].ljust(74, '-')} ❌")
                
                if cursor[0]<size and index[cursor[0]]==i and cursor[1]==0:
                    stdscr.addstr(current_line, 82, '[detail]', curses.A_REVERSE)
                else:
                    stdscr.addstr(current_line, 82, '[detail]')
                
                if cursor[0]<size and index[cursor[0]]==i and cursor[1]==1:
                    stdscr.addstr(current_line, 92, "[✓]" if checked[i-1] else "[ ]", curses.A_REVERSE)
                else:
                    stdscr.addstr(current_line, 92, "[✓]" if checked[i-1] else "[ ]")
                
                if show_reason != -1 and index[show_reason] == i:
                    for a in result[target][str(i)]['reason']:
                        current_line += 1
                        stdscr.addstr(current_line, 0, ">>>> "+a)
                        y,x = stdscr.getyx()
                        current_line = y + 1
            else:
                # line = [f"{i:2} {result[target][f'{i}']['diag'].ljust(74, '-')} ✅", None]
                stdscr.addstr(current_line, 0, f"{i:2} {result[target][f'{i}']['diag'].ljust(74, '-')} ✅")
            current_line += 1
        
        stdscr.addstr(current_line, 0, "[뒤로]", curses.A_REVERSE if cursor == [size, 0] else 0)
        stdscr.addstr(current_line, 90, "[조치]", curses.A_REVERSE if cursor == [size, 1] else 0)

        stdscr.refresh()
        key = stdscr.getch()

        if key == curses.KEY_DOWN:
            if cursor[0] < size:
                cursor[0] += 1
        elif key == curses.KEY_UP:
            if cursor[0] > 0:
                cursor[0] -= 1
        elif key == curses.KEY_RIGHT:
            if cursor[1] == 0:
                cursor[1] = 1
        elif key == curses.KEY_LEFT:
            if cursor[1] == 1:
                cursor[1] = 0
        elif key == curses.KEY_ENTER or key in [10, 13, 32]:  # 선택 시
            if cursor[0] < size:
                if cursor[1] == 0:
                    if show_reason == -1:
                        show_reason = cursor[0]
                    else:
                        show_reason = -1
                else:
                    if checked[index[cursor[0]]-1]:
                        checked[index[cursor[0]]-1] = False
                    else:
                        current_line += 1

                        data = result[target][str(index[cursor[0]])]

                        if 'bypass' not in data:
                            data['bypass'] = []
                        bypass_data = data.get('bypass')
                        dual_select = data.get('dual_select')
                        dual_second = data.get('dual_second')
                        
                        for s in data['how_action']:
                            current_line = custom_print(stdscr, s, current_line,0)
                            current_line += 1
                        user_input = custom_input(stdscr, "[Y/N]: ", current_line, 0).strip().upper()
                        current_line += 1

                        if user_input == 'Y':
                            if dual_select:
                            # dual_select의 옵션을 동적으로 출력하고 숫자 선택받기
                                current_line = custom_print(stdscr, "Select an option:", current_line, 0)
                                current_line += 1

                                options = dual_select[0]
                                for key, value in options.items():
                                    current_line = custom_print(stdscr, f"{key}: {value}", current_line, 0)
                                    current_line += 1
                                
                                # 사용자로부터 숫자 입력 받기
                                selected_option = custom_input(stdscr, f"Enter the number of your choice ({'/'.join(options.keys())}): ", current_line, 0).strip()
                                current_line += 1

                                # 선택한 옵션을 확인하고, 해당 값을 bypass_data에 추가
                                selected_value = options.get(selected_option)
                                
                                if selected_value:
                                    # bypass_data에 사용자가 선택한 옵션 추가
                                    bypass_data.append({selected_option: selected_value})
                                    current_line = custom_print(stdscr, f"You selected option {selected_option}: {selected_value}", current_line, 0)
                                    current_line += 1
                                    #dual_second의 첫번째 원소가 dual_select에서 선택한거랑 같으면
                                    if selected_value == dual_second[0]:
                                        current_line = custom_print(stdscr, "The selected option matches the first element of dual_second.", current_line, 0)
                                        current_line += 1
                                        weak_key = [key for key in bypass_data[0].keys() if key.startswith("weak_")][0]
                                        weak_values = bypass_data[0][weak_key]

                                        # 사용자에게 weak_* 리스트에 맞는 값을 입력받아 리스트로 저장
                                        input_values = []
                                        for item in weak_values:
                                            input_value = custom_input(stdscr, f"{dual_second[1]} for {item}: ", current_line, 0).strip()
                                            current_line += 1
                                            input_values.append(input_value)
                                        
                                        # bypass_data에 dual_second[1] key로 input_values 리스트 추가
                                        bypass_data.append({dual_second[1]: input_values})
                                        
                                        checked[index[cursor[0]]-1] = not checked[index[cursor[0]]-1]
                                            
                                    else:
                                        current_line = custom_print(stdscr, "The selected option does not match the first element of dual_second.", current_line ,0)
                                        current_line += 1
                                else:
                                    current_line = custom_print(stdscr, "Invalid option selected.", current_line ,0)
                                    current_line += 1
                            else:
                                current_line = custom_print(stdscr, "No dual_select options available.", current_line ,0)
                                current_line += 1
                                checked[index[cursor[0]]-1] = not checked[index[cursor[0]]-1]
                            current_line = custom_print(stdscr, "Press any key to continue", current_line,0)
                            current_line += 1
                            stdscr.getch()
            else:
                if cursor[0] == 0:
                    break
                else:
                    action(stdscr, result, target, checked)
                    break
        
        elif key == 27:  # ESC 키
            break