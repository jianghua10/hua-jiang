import random
record = {} #以字典形式记录玩家数据
player_flag = 1
continue_flag = 'go'

#外循环，记录总共玩了几局游戏
while continue_flag == 'go':
    #判断新玩家还是老玩家，新玩家则新建记录（盘数，平均成绩，最好成绩，总共成绩）
    if player_flag:
        player_flag = 0
        player_name = input('pls type your name\n')
        if player_name in record:
            print('happy to see u again %s, wish u a good grade'%player_name)
        else:
            print('welcome new player %s, let\'s begin the game\n'%player_name)
            record[player_name] = {'game_round':0,'average_times':0,'best_grade':0,'total_times':0}
            
    random_number = random.randint(1,100)
    game_times = 1 #记录每盘的次数
    
    #判断玩家的输入是否为100以下的整数
    def isint():
        try:
            given_number = int(input('pls input an integer below 100\n'))
            while given_number > 100:
                given_number = int(input('the typed number is larger than 100\n'))
            return given_number
        except ValueError:   
            print('only an integer below 100 is valid\n')
            return isint()
        
    #内循环，判断是否猜中，且记录猜中的次数   
    given_number = isint()
    while random_number != given_number:
        game_times += 1
        if given_number < random_number:
            print('the given number %d is small, type a bigger one again'%given_number)
            given_number = isint()
        else:
            print('the given number %d is big, a small one is needed'%given_number)
            given_number = isint()
            
    #更新玩家的数据        
    record[player_name]['game_round'] += 1
    record[player_name]['total_times'] += game_times
    record[player_name]['average_times'] = record[player_name]['total_times']/float(record[player_name]['game_round'])
    if record[player_name]['best_grade'] == 0 or game_times < record[player_name]['best_grade']:
        record[player_name]['best_grade'] = game_times
    
    print('''\n congratulations, the answer is %d,
    u have tried it for %d times.
    u've played %d rounds.
    u successfully guessed the right answer in average %.2f times.
    And the best grade is %d times\n'''%(random_number,game_times,record[player_name]['game_round'],\
                                       record[player_name]['average_times'],record[player_name]['best_grade']))
    #判断是否继续下一盘游戏
    continue_flag = input('would u play again, go for yes, otherwise quit the game')
    if continue_flag =='go':
        player_flag = int(input('would u change another player,1/yes,0/no\n'))
       