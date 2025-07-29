import curses
from tui.diagnose import diagnose

def select_diagnosis_check(stdscr, checklist, result, target):
    items = [f"{int(i):2} {checklist[i]['diag']}" for i in checklist]  # 32개 항목
    current_index = 0  # 현재 선택된 항목의 인덱스
    option_index = 0 # 뒤로=0 진단=1
    page_size = 10  # 페이지당 항목 수
    total_pages = (len(items) + page_size - 1) // page_size  # 총 페이지 수
    current_page = 0  # 현재 페이지
    last_page_size = len(items) % page_size if len(items) // page_size != 0 else page_size
    passed = [False] * len(items)

    while True:
        stdscr.clear()

        # 현재 페이지의 항목 출력
        start_index = current_page * page_size
        end_index = min(start_index + page_size, len(items))

        for idx in range(start_index, end_index):
            checkbox = "[✓]" if not passed[idx] else "[ ]"  # 체크 표시
            if idx == start_index + current_index:
                stdscr.addstr(idx - start_index, 0, f"{checkbox} {items[idx]}", curses.A_REVERSE)  # 강조 표시
            else:
                stdscr.addstr(idx - start_index, 0, f"{checkbox} {items[idx]}")

        # 페이지 정보 출력
        stdscr.addstr(page_size, 0, f"(페이지 {current_page + 1}/{total_pages})".center(40,'-'))

        # "진단 시작"과 "뒤로" 출력
        stdscr.addstr(page_size + 1, 0, "[뒤로]", curses.A_REVERSE if current_index == 10 and option_index == 0 else 0)
        stdscr.addstr(page_size + 1, 36, "[진단]", curses.A_REVERSE if current_index == 10 and option_index == 1 else 0)

        stdscr.refresh()

        key = stdscr.getch()

        if key == curses.KEY_DOWN:
            if current_index < page_size -1:
                current_index += 1
                if current_page == total_pages - 1 and current_index == last_page_size:
                    current_index = 10
            elif current_index == page_size - 1:
                current_index = 10
        elif key == curses.KEY_UP:
            if current_index == 10:
                current_index = page_size - 1
                if current_page == total_pages - 1 and current_index > last_page_size - 1:
                    current_index = last_page_size - 1
            elif current_index > 0:
                current_index -= 1
        elif key == curses.KEY_LEFT:
            if current_index < 10 and current_page > 0:
                current_page -= 1
            elif current_index == 10 and option_index == 1:
                option_index = 0
        elif key == curses.KEY_RIGHT:
            if current_index < 10 and current_page < total_pages - 1:
                current_page = current_page + 1
                if current_page == total_pages - 1 and current_index > last_page_size - 1:
                    current_index = last_page_size -1
            elif current_index == 10 and option_index == 0:
                option_index = 1
        elif key == curses.KEY_ENTER or key in [10, 13, 32]:
            if current_index < 10:
                passed[start_index + current_index] = not passed[start_index + current_index]
            elif option_index == 0:
                break
            else:
                diagnose(stdscr, result, target, passed)
                return target
        elif key == 27:  # ESC 키
            break