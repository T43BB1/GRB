import curses
from tui.select_action_check import select_action_check

def select_action_target(stdscr, result):
    targets = ["linux", "docker", "oracle", "nodejs", "nginx", "뒤로"]
    current_row = 0

    while True:
        stdscr.clear()
        
        # 진단 옵션 출력
        for idx, option in enumerate(targets):
            if idx == current_row:
                stdscr.addstr(idx, 0, option, curses.A_REVERSE)  # 강조 표시
            else:
                stdscr.addstr(idx, 0, option)

        stdscr.refresh()

        key = stdscr.getch()

        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(targets) - 1:
            current_row += 1
        elif key == curses.KEY_ENTER or key in [10, 13, 32]:
            if current_row == len(targets) - 1:  # "뒤로" 선택 시
                break  # 메인 메뉴로 돌아감
            else:
                select_action_check(stdscr, result, targets[current_row])
                break

        # ESC 키로 종료
        if key == 27:
            break