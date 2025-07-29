import subprocess
from tui.modules.ProgressBar import ProgressBar
import json
import os
# from tui.select_action_check import select_action_check

def run_playbook(target, playbook_number):
    playbook_path = f'{target}/diag/{playbook_number}.yml'
    with open(f'./log/{target}/ansible/diag/{playbook_number}.log', 'w') as f:
        subprocess.run(['ansible-playbook', playbook_path], stdout=f, stderr=subprocess.DEVNULL)

def diagnose(stdscr, result, target, passed):
    # 초기 설정
    if target not in result:
        result[target] = dict()
    os.makedirs(f'./log/{target}/diag', exist_ok=True)
    os.makedirs(f'./log/{target}/ansible/diag', exist_ok=True)
    stdscr.clear()

    total_playbooks = len(passed)
    with open(f'{target}/checklist.json') as f:
        playbooks = json.load(f)

    progress_bar = ProgressBar(stdscr=stdscr, x0=0, y0=total_playbooks + 1, total=total_playbooks, position=0, leave=True, ncols=80)

    for cur in range(total_playbooks):
        # 진행 전 출력
        stdscr.addstr(0, 0, "Playbook Execution Progress:")

        for i in range(total_playbooks):
            if passed[i]:
                stdscr.addstr(i + 1, 0, f'{i+1:2} {playbooks[f'{i+1}']['diag'].ljust(70, '-')} Passed')
            elif i < cur:
                if result[target][f'{i + 1}']['weak'] == None:
                    stdscr.addstr(i + 1, 0, f"{i+1:2} {playbooks[f'{i+1}']['diag'].ljust(72, '-')} (N/A)")
                elif result[target][f'{i + 1}']['weak']:
                    stdscr.addstr(i + 1, 0, f"{i+1:2} {playbooks[f'{i+1}']['diag'].ljust(74, '-')} ❌")
                else:
                    stdscr.addstr(i + 1, 0, f"{i+1:2} {playbooks[f'{i+1}']['diag'].ljust(74, '-')} ✅")
            elif i == cur:
                stdscr.addstr(i + 1, 0, f"{i+1:2} {playbooks[f'{i+1}']['diag'].ljust(74, '-')} 🔄")
            else:
                stdscr.addstr(i + 1, 0, f"{i+1:2} {playbooks[f'{i+1}']['diag'].ljust(74, '-')} ⏳")
        progress_bar.update(0)
        stdscr.refresh()

        # 진행 중
        if not passed[cur]:
            run_playbook(target, cur + 1)
            with open(f'./log/{target}/diag/{cur + 1}.json') as f:
                json_data = json.load(f)
            result[target][f'{cur + 1}'] = json_data
        else:
            result[target][f'{cur + 1}'] = {'weak':'passed'} | playbooks[f'{cur+1}']

        progress_bar.update(1)

        stdscr.refresh()

    for i in range(total_playbooks):
        if passed[i]:
            stdscr.addstr(i + 1, 0, f'{i+1:2} {playbooks[f'{i+1}']['diag'].ljust(70, '-')} Passed')
        else:
            if result[target][f'{i + 1}']['weak'] == None:
                stdscr.addstr(i + 1, 0, f"{i+1:2} {playbooks[f'{i+1}']['diag'].ljust(72, '-')} (N/A)")
            elif result[target][f'{i + 1}']['weak']:
                stdscr.addstr(i + 1, 0, f"{i+1:2} {playbooks[f'{i+1}']['diag'].ljust(74, '-')} ❌")
            else:
                stdscr.addstr(i + 1, 0, f"{i+1:2} {playbooks[f'{i+1}']['diag'].ljust(74, '-')} ✅")

    progress_bar.close()

    stdscr.addstr(total_playbooks + 3, 0, "All playbooks executed successfully! ✅\n")
    stdscr.addstr(total_playbooks + 5, 0, 'Press any key to continue')
    stdscr.refresh()
    stdscr.getch()
    # select_action_check(stdscr, result, target, passed)
