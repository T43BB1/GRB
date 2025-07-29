import pandas as pd

def excel(result):
    # 엑셀 파일에 여러 시트를 추가
    output_file_path = './report.xlsx'  # 경로 바꿔주세요~
    with pd.ExcelWriter(output_file_path, engine='xlsxwriter') as writer:
        # 각 그룹에 대해 반복
        for group_name, group_data in result.items():
            data = [
                {
                    'num': item['num'],
                    'diag': item['diag'],
                    'weak': 'vulnerable' if item['weak'] is True else 'good' if item['weak'] is False else 'N/A',
                    'reason': ', '.join(item['reason']) if isinstance(item['reason'], list) else item['reason'],
                    'how_action': ', '.join(item['how_action']) if item['weak'] is True else "N/A",
                    'status': item['status'] if item['weak'] is True else "N/A",
                    'details': "Please check manually" if item['status'] == "No Action Required" and item['weak'] is True else (
                        ', '.join(item['details']) if item['weak'] is True else "N/A"
                    ),
                    
                }
                for item in group_data.values()
            ]
            
            # DataFrame 생성
            df = pd.DataFrame(data, columns=['num', 'diag', 'weak', 'reason', 'how_action', 'status', 'details'])
            
            # 각 그룹별로 시트에 쓰기
            df.to_excel(writer, sheet_name=group_name, index=False)
            
            # 워크북과 워크시트 객체 얻기
            workbook  = writer.book
            worksheet = writer.sheets[group_name]
            
            # 서식 지정
            header_format = workbook.add_format({'bold': True, 'align': 'center', 'valign': 'center', 'bg_color': '#D9EAD3'})
            cell_format = workbook.add_format({'text_wrap': True, 'valign': 'top'})
            highlight_format = workbook.add_format({'bg_color': '#ffff9c'})  # 하이라이트

            # 열 너비 조정 및 헤더에 서식 적용
            worksheet.set_column('A:A', 5)    # num 열 너비
            worksheet.set_column('B:B', 25)   # diag 열 너비
            worksheet.set_column('C:C', 15)   # weak 열 너비
            worksheet.set_column('D:D', 30)   # reason 열 너비
            worksheet.set_column('E:E', 35)   # how_action 열 너비
            worksheet.set_column('F:F', 20)   # status 열 너비
            worksheet.set_column('G:G', 40)   # details 열 너비
            
            # 헤더 셀에 서식 적용
            for col_num, value in enumerate(df.columns.values):
                worksheet.write(0, col_num, value, header_format)
            
            # 데이터 셀에 서식 적용
            for row in range(1, len(df) + 1):
                for col in range(len(df.columns)):
                    worksheet.write(row, col, df.iloc[row - 1, col], cell_format)
            
            # weak 값이 'vulnerable'일 때 하이라이트
            worksheet.conditional_format('C2:C{}'.format(len(df) + 1), 
                                        {'type': 'text', 'criteria': 'containing', 'value': 'vulnerable', 'format': highlight_format})

            # status 값이 'No Action Required'일 때 하이라이트
            worksheet.conditional_format('F2:F{}'.format(len(df) + 1), 
                                        {'type': 'text', 'criteria': 'containing', 'value': 'No Action Required', 'format': highlight_format})