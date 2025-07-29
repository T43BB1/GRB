import subprocess
import json

# 실행할 항목 번호를 미리 지정
to_run = [1,2,3,4,5,6,7,8,9,10,11,12]

# JSON 파일 읽기
def read_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

# 조치 후 결과 출력
def print_new_json_data(outside_num):
    new_file_path = f'log/oracle/action/{outside_num}.json'
    new_json_data = read_json_file(new_file_path)
    
    new_item = new_json_data
    details = new_item.get('details', [''])[0]
    status = new_item.get('status', 'Unknown')
    
    print(f"[Checklist #{new_item['num']}. {new_item['diag']}] {status}, {details}")

# 메인은 똑같음
def main_task(outside_num):
    # 점검 코드 실행
    command = f"ansible-playbook oracle/diag/{outside_num}.yml"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    # print("stdout:", result.stdout)# 정신 사나워
    # print("stderr:", result.stderr)
    print("Return code:", result.returncode)

    # 점검 JSON 파일
    file_path = f'log/oracle/diag/{outside_num}.json'
    json_data = read_json_file(file_path)
    
    first_item = json_data #나중에 first_item을 바꿔
    num = first_item.get('num')
    diag = first_item.get('diag', 'something wrong its for debug')
    is_weak = first_item.get('weak')
    reason = first_item['reason'][0]
    how_action = first_item.get('how_action', [''])[0]
    bypass_data = first_item.get('bypass', [])
    # print(reason) # test용임
    
    if is_weak is True:
        print(f"[Checklist #{num}. {diag}] is vulnerable, because {reason}")
        print(how_action.strip())
        while True:
            user_input = input("[Y/N]: ").strip().upper()
            
            if user_input == 'Y':
                dual_select = first_item.get('dual_select')
                dual_second = first_item.get('dual_second')
                

                if dual_select:
                    while True:
                        print("Select an option:")
                        options = dual_select[0]
                        for key, value in options.items():
                            print(f"{key}: {value}")
                        
                        selected_option = input(f"Enter the number of your choice ({'/'.join(options.keys())}): ").strip()
                        selected_value = options.get(selected_option)
                        if selected_value:
                            bypass_data.append({selected_option: selected_value})
                            print(f"You selected option {selected_option}: {selected_value}")
                            
                            if selected_value == dual_second[0]:
                                print("Please enter input for the selected option.")
                                weak_key = [key for key in bypass_data[0].keys() if key.startswith("weak_")][0]
                                weak_values = bypass_data[0][weak_key]

                                input_values = []
                                for item in weak_values:
                                    input_value = input(f"{dual_second[1]} for {item}: ").strip()
                                    input_values.append(input_value)
                                
                                bypass_data.append({dual_second[1]: input_values})
                            else:
                                print("Solution will apply a temporary action for the selected option. Further manual action may be required..")
                            break
                        else:
                            print("Invalid option selected. Please select a valid option.")

                print("Proceeding with action...")
                bypass_json = json.dumps({"bypass": bypass_data})
                # print({bypass_json}) # test용임
                command = f"ansible-playbook oracle/action/{num}.yml -e '{bypass_json}'"
                
                result = subprocess.run(command, shell=True, capture_output=True, text=True)
                # print("stdout:", result.stdout)
                # print("stderr:", result.stderr)
                print("Return code:", result.returncode)
                print_new_json_data(outside_num)
                break
            
            elif user_input == 'N':
                print("OK, But please check manually. It may be vulnerable.")
                break
            else:
                print("Invalid input, please enter Y or N.")

    elif is_weak is False:
        print(f"[Checklist #{num}. {diag}] is good, because {reason}")
    elif is_weak is None:
        print(f"[Checklist #{num}. {diag}] is N/A, because {reason}")

# 지정한 체크리스트들 전부 순서대로 실행
for outside_num in to_run:
    print(f"\n--- Running checklist {outside_num} ---")
    main_task(outside_num)
