import os
new_recording = 1
balance_sheet_filepath = '/Users/jianghua/Desktop/python_examples_data/balance_sheet.txt'
transaction_log_filepath = '/Users/jianghua/Desktop/python_examples_data/transaction_log.txt'
#创建新的文件
if new_recording:
    asset = 0
    debt = 0
    with open(balance_sheet_filepath,'w') as f:
        f.writelines('结算日期 资产/w 负债/w 净资产/w\n')
    with open(transaction_log_filepath,'w') as f:
        f.writelines('交易对象 收入/w 支出/w 应收账款/w 应出账款/w 交易日期\n')

#判断输入的数是否为整数
def isint():
    try:
        service = int(input('\n choose the needed service: '))
        return service
    except ValueError:
        print('only integer is valid')
        return isint()

#从文件末尾返回行内容
#f：打开的文件
#filename：文件名字
#offset: 字节偏移量
#num_lines:文件的最后几行，=2表示找文件的最后一行，=3表示找文件的倒数第二行
#subservice_mode:查账下的子功能的模式，1/最后10条记录，2/与某公司的记录
def lastlines(f,filename,offset=50,num_lines=2,subservice_mode=1):
    f.seek(-offset,2)
    lines = f.readlines()
    filesize = os.path.getsize(filename)
    while True:
        if len(lines) >= num_lines:
            offset = 0
            for i in range(num_lines-1):
                offset += len(lines[-(i+1)])
            break
        else:
            offset *= 2
            #如果查找的字节数超过文件大小，则读取整个文件
            if offset >= filesize:
                f.seek(0,0)
                lines = f.readlines()
                #如果找不到指定的行数
                if not (len(lines) >= num_lines):
                    if subservice_mode == 1:
                        print('there are no more than 10 recordings')
                    #如果指定的行数是正好是最后一行
                    else:
                        print(lines[1].decode('UTF-8','strict'))
                    #返回表头
                    return lines[0].decode('UTF-8','strict')
            #继续找指定的行数
            else:
                f.seek(-offset,2)
                lines = f.readlines()
    #读取指定的行数
    f.seek(-offset,2)
    temp = f.readline().decode('UTF-8','strict')
    return temp
#写入记录
def writestr(data,asset,debt,balance):
    with open(balance_sheet_filepath,'a') as f:
        f.writelines(data+' '+str(asset)+' '+str(debt)+' '+str(balance)+'\n')

while True:
    print('\n 1:checking，2:recording')
    service_flag = isint()
    #查账模式
    if service_flag == 1:
        print('checking mode:\n 1.the last 10 recordings\n 2.the transaction with a certain company\n 3.the recently debt condition')
        subservice_flag = isint()
        #查找最后的10条记录
        if subservice_flag == 1:
            with open(transaction_log_filepath,'rb') as f:
                for i in range(10):
                    temp = lastlines(f,transaction_log_filepath,num_lines=(2+i))
                    if '交易对象' in temp:
                        break
                    else:
                        print(temp)
        #查找与某公司的交易记录
        elif subservice_flag == 2:
            company = input('type the company name,eg. company_A: ')
            with open(transaction_log_filepath,'rb') as f:
                num_lines = 2
                temp = lastlines(f,transaction_log_filepath,num_lines=num_lines,subservice_mode=2)
                company_recording = []
                while '交易对象' not in temp:
                    if company in temp:
                        temp = temp.split()
                        company_recording.append(temp)
                    num_lines += 1
                    temp = lastlines(f,transaction_log_filepath,num_lines=num_lines,subservice_mode=2)
                print('\n%d transaction executed with %s\n'%(len(company_recording),company))
                if len(company_recording) != 0 :
                    for element in company_recording:
                        #print(element)
                        print('\n data: %s\n income: %s\n expense: %s\n accounts_receive/w: %s\n accounts_payable/w: %s'\
                              %(element[5],element[1],element[2],element[3],element[4]))
        #查询公司的最新资产负债
        elif subservice_flag == 3:
            with open(balance_sheet_filepath,'rb') as f:
                temp = lastlines(f,balance_sheet_filepath)
                temp = temp.split()
                print('the current asset: %s\n the current debt: %s\n the current balance: %s\n data: %s\n'\
                      %(temp[1],temp[2],temp[3],temp[0]))
        #输入1，2，3之外的整数时
        else:
            print('type the correct number, 1 or 2 or 3')
    #记账模式
    elif service_flag == 2:
        print('\n recording mode\n')
        transaction_partner = input('type the transaction partner,eg.company_A: ').strip()
        income = input('type the amount of incoming/w, only number: ').strip()
        expense = input('type the amount of expense/w, only number: ').strip()
        accounts_receive = input('type the amount of accounts receivable/w, only number: ').strip()
        accounts_payable = input('type the amount of accounts payable/w, only number: ').strip()
        data = input('type the data, eg.dd-mm-year: ').strip()
    
        #写入交易记录
        with open(transaction_log_filepath,'a') as f:
            f.writelines(transaction_partner+' '+income+' '+expense+' '+accounts_receive+' '+accounts_payable+' '+\
                         data+'\n')
        #写入资产负债表
        if new_recording == 1:
            asset += float(income) - float(expense)
            debt += float(accounts_payable) - float(accounts_receive)
            balance = asset - debt
            writestr(data,asset,debt,balance)
            new_recording = 0
                             
        else:
            with open(balance_sheet_filepath,'rb') as f:
                temp = lastlines(f,balance_sheet_filepath)
                temp = temp.split()
                asset = float(temp[1]) + float(income) - float(expense)
                debt = float(temp[2]) + float(accounts_payable) - float(accounts_receive)
                balance = asset - debt
                writestr(data,asset,debt,balance)
        print('\n the transaction is recorded\n the current balance:\n updated asset: %.f\n updated debt: %.f\n updated balance: %.f'\
                                                   %(asset, debt, balance))
                                         #输入1，2之外的整数时提醒重新输入
    else:
        print('type the correct number, 1 or 2')


