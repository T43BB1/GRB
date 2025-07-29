import subprocess
import json

####README####
# 테스트인데 경로랑 파일들 이름만 자기한테 맞게 잘 바꿔주고 테스트해주세요~
# 점검 코드 이름 숫자에 넣어서 테스트해주세요~
outside_num = 7
command = f"ansible-playbook oracle/diag/{outside_num}.yml"

result = subprocess.run(command, shell=True, capture_output=True, text=True)
print("stdout:", result.stdout) # 정신사나우면
print("stderr:", result.stderr) # 없애
print("Return code:", result.returncode)


####
# JSON 파일 읽기
def read_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data
####
#####
# 조치 후 결과 출력
def print_new_json_data():
    new_file_path = f'log/oracle/action/{outside_num}.json'
    new_json_data = read_json_file(new_file_path)
    
    # actest JSON 파일에서 데이터 가져오기
    # new_item = new_json_data[0]
    new_item = new_json_data
    details = new_item.get('details', [''])[0]
    status = new_item.get('status', 'Unknown')
    
    # 조치 결과 출력 포맷
    print(f"[Checklist #{new_item['num']}. {new_item['diag']}] {status}, {details}")
#####

# 이게 메인임
def main_task(json_data):
    # first_item = json_data[0]
    first_item = json_data
    # 필요한 데이터 가져와
    num = first_item.get('num')
    diag = first_item.get('diag', 'something wrong its for debug')
    is_weak = first_item.get('weak')
    reason = first_item['reason'][0]
    how_action = first_item.get('how_action', [''])[0]
    bypass_data = first_item.get('bypass', [])
    # print(reason) # 그냥 test용임

    if is_weak is True:
        # weak가 True일 때 취약은 영어로 vulnerable임
        print(f"[Checklist #{num}. {diag}] is vulnerable, because {reason}")
        print(how_action.strip())
        # Y/N 입력 받아, 이거는 구현이꺼에서 체크하는걸로 한다고 생각. 임시임
        # 그래서 결국 최종적으로는 이 안에 들은거는 밖으로 따로 뺄듯. 상위 작업은 체크하는걸로 가고
        user_input = input("[Y/N]: ").strip().upper()
        
        if user_input == 'Y':
            #만약 dual_select가 존재한다면 몇번 선택지를 고를지 사용자 입력으로 결정
            #결정되면 그 원소를 bypass에 넣어서 보냄. 
            #근데 dual_second가 존재한다면? 
            # dual_select 확인
            dual_select = first_item.get('dual_select')
            dual_second = first_item.get('dual_second')
            
            
            if dual_select:
            # dual_select의 옵션을 동적으로 출력하고 숫자 선택받기
                print("Select an option:")
                options = dual_select[0]
                for key, value in options.items():
                    print(f"{key}: {value}")
                
                # 사용자로부터 숫자 입력 받기
                selected_option = input(f"Enter the number of your choice ({'/'.join(options.keys())}): ").strip()
                
                # 선택한 옵션을 확인하고, 해당 값을 bypass_data에 추가
                selected_value = options.get(selected_option)
                if selected_value:
                    # bypass_data에 사용자가 선택한 옵션 추가
                    bypass_data.append({selected_option: selected_value})
                    print(f"You selected option {selected_option}: {selected_value}")
                    #dual_second의 첫번째 원소가 dual_select에서 선택한거랑 같으면
                    if selected_value == dual_second[0]:
                        print("The selected option matches the first element of dual_second.")
                        weak_key = [key for key in bypass_data[0].keys() if key.startswith("weak_")][0]
                        weak_values = bypass_data[0][weak_key]

                        # 사용자에게 weak_* 리스트에 맞는 값을 입력받아 리스트로 저장
                        input_values = []
                        for item in weak_values:
                            input_value = input(f"{dual_second[1]} for {item}: ").strip()
                            input_values.append(input_value)
                        
                        # bypass_data에 dual_second[1] key로 input_values 리스트 추가
                        bypass_data.append({dual_second[1]: input_values})
                        
                            
                    else:
                        print("The selected option does not match the first element of dual_second.")
                else:
                    print("Invalid option selected.")
                    return
            
            else:
                print("No dual_select options available.")



            print("Proceeding with action...")
            # bypass 넣어서 조치 코드 명령어 실행
            bypass_json = json.dumps({"bypass": bypass_data})
            print({bypass_json})
            command = f"ansible-playbook oracle/action/{num}.yml -e '{bypass_json}'"  # 여기 조치 코드 이름에 들어있는 숫자는 점검 result의 num을 사용하자
            

            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            print("stdout:", result.stdout)
            print("stderr:", result.stderr)
            print("Return code:", result.returncode)
            #조치후 조치결과
            print_new_json_data()
        elif user_input == 'N':
            print("OK, But please check manually. It may be vulnerable.")
        else:
            print("Invalid input, please enter Y or N.")

    elif is_weak is False:
        # 양호일때
        print(f"[Checklist #{num}. {diag}] is good, because {reason}")

    elif is_weak is None:
        # 해당없음일떄
        print(f"[Checklist #{num}. {diag}] is N/A, because {reason}")

# JSON 파일 경로
file_path = f'log/oracle/diag/{outside_num}.json'
# JSON 데이터 읽기
json_data = read_json_file(file_path)

main_task(json_data)
