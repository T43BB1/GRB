import curses
from tui.select_diagnosis_target import select_diagnosis_target
from tui.select_action_check import select_action_check
from tui.select_action_target import select_action_target
from tui.excel import excel
from os import system, path
import json

def main_page(stdscr):
    curses.curs_set(0)  # 커서 숨기기
    stdscr.clear()
    
    options = ["점검", "조치", "초기화", "report 저장", "종료"]
    current_row = 0

    targets = ["linux", "oracle", "nginx", "nodejs", "docker"]
    checklist = {}

    for target in targets:
        with open(f'./{target}/checklist.json') as f:
            checklist[target] = json.load(f)
    
    result = {}
    if path.exists('./log.json'):
        with open('./log.json', "r", encoding="utf-8") as file:
            result |= json.load(file)
    try:
        while True:
            stdscr.clear()
            
            # 메인 메뉴 출력
            for idx, option in enumerate(options):
                if idx == current_row:
                    stdscr.addstr(idx, 0, option, curses.A_REVERSE)  # 강조 표시
                else:
                    stdscr.addstr(idx, 0, option)

            stdscr.refresh()

            key = stdscr.getch()

            if key == curses.KEY_UP and current_row > 0:
                current_row -= 1
            elif key == curses.KEY_DOWN and current_row < len(options) - 1:
                current_row += 1
            elif key == curses.KEY_ENTER or key in [10, 13, 32]:
                if current_row == 0:
                    target = select_diagnosis_target(stdscr, checklist, result)
                    if target is not None:
                        select_action_check(stdscr, result, target)
                elif current_row ==1:
                    select_action_target(stdscr, result)
                elif current_row == 2:
                    system(r'rm -rf log')
                    stdscr.addstr(len(options) + 1, 0, '초기화 완료')
                    stdscr.getch()
                elif current_row == 3:
                    excel(result)
                    stdscr.addstr('Press any key to quit.')
                    stdscr.refresh()
                    stdscr.getch()
                else:  # "종료" 선택 시
                    # stdscr.addstr(str(result))
                    # stdscr.refresh()
                    # stdscr.getch()
                    break  # 프로그램 종료

            # ESC 키로 종료
            if key == 27:
                break
    except:
        with open("log.json", "w", encoding="utf-8") as file:
            json.dump(result, file, ensure_ascii=False, indent=4)