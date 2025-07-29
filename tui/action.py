import subprocess
from tui.modules.ProgressBar import ProgressBar
import json
import os
# from tui.select_action_check import select_action_check

def run_playbook(target, num, bypass):
    bypass_json = json.dumps({"bypass": bypass})
    command = f"ansible-playbook ./{target}/action/{num}.yml -e '{bypass_json}'"  # 여기 조치 코드 이름에 들어있는 숫자는 점검 result의 num을 사용하자
    with open(f'./log/{target}/ansible/action/{num}.log', 'w') as f:
        subprocess.run(['ansible-playbook', f'./{target}/action/{num}.yml', '-e', f"{bypass_json}"], stdout=f, stderr=subprocess.DEVNULL)

def action(stdscr, result, target, checked):
    # 초기 설정
    if target not in result:
        result[target] = dict()
    os.makedirs(f'./log/{target}/action', exist_ok=True)
    os.makedirs(f'./log/{target}/ansible/action', exist_ok=True)
    stdscr.clear()

    index = []

    for i, a in enumerate(checked):
        if a:
            index.append(i)
    
    total = len(index)

    progress_bar = ProgressBar(stdscr=stdscr, x0=0, y0=total + 1, total=total, position=0, leave=True, ncols=80)

    for cur in range(total):
        # 진행 전 출력
        stdscr.addstr(0, 0, "Playbook Execution Progress:")

        for i in range(total):
            if i < cur:
                if 'status' in result[target][f'{index[i]+1}'] and result[target][f'{index[i]+1}']['status'] == "Action Completed":
                    stdscr.addstr(i + 1, 0, f"{index[i]+1:2} {result[target][f'{index[i]+1}']['diag'].ljust(74, '-')} ✅")
                else:
                    stdscr.addstr(i + 1, 0, f"{index[i]+1:2} {result[target][f'{index[i]+1}']['diag'].ljust(74, '-')} ❌")
            elif i == cur:
                stdscr.addstr(i + 1, 0, f"{index[i]+1:2} {result[target][f'{index[i]+1}']['diag'].ljust(74, '-')} 🔄")
            else:
                stdscr.addstr(i + 1, 0, f"{index[i]+1:2} {result[target][f'{index[i]+1}']['diag'].ljust(74, '-')} ⏳")
        progress_bar.update(0)
        stdscr.refresh()

        # 진행 중
        run_playbook(target, index[cur] + 1, result[target][str(index[cur]+1)]['bypass'])
        with open(f'./log/{target}/action/{index[cur] + 1}.json') as f:
            json_data = json.load(f)
        result[target][f'{index[cur]+1}'] |= json_data

        progress_bar.update(1)

        stdscr.refresh()

        for i in range(total):
            if i <= cur:
                if 'status' in result[target][f'{index[i]+1}'] and result[target][f'{index[i]+1}']['status'] == "Action Completed":
                    stdscr.addstr(i + 1, 0, f"{index[i]+1:2} {result[target][f'{index[i]+1}']['diag'].ljust(74, '-')} ✅")
                else:
                    stdscr.addstr(i + 1, 0, f"{index[i]+1:2} {result[target][f'{index[i]+1}']['diag'].ljust(74, '-')} ❌")
            else:
                stdscr.addstr(i + 1, 0, f"{index[i]+1:2} {result[target][f'{index[i]+1}']['diag'].ljust(74, '-')} ⏳")
    progress_bar.close()
    for i in result[target]:
        if 'status' not in result[target][i]:
            result[target][i]['status']=''
        if 'details' not in result[target][i]:
            result[target][i]['details']=[]

    stdscr.addstr(total + 3, 0, "All playbooks executed successfully! ✅\n")
    stdscr.addstr(total + 5, 0, 'Press any key to continue')
    stdscr.refresh()
    stdscr.getch()
