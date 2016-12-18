"""
V2.0
1. add user system
2. orgnize the structure of codes
"""

import getpass
from random import randint
from Crypto.Cipher import AES

class GuessNumbers:
    def __init__(self,name):
        self.nums=""
        self.name=name
        self.hard=0
        self.retry=0
        self.profile_dic = self.get_user_dic()
                        
    def countdown(self):
        if self.hard == 0:
            self.hard = 2+int(input("""There are 4 levels in this game.\nEnter a numer between 1-4 to choose your level: """))
        self.nums = self.num_generator()

        if self.name == "test":
            print(self.nums)

        if self.retry == 0:
            print("""\nlet's begin！\nPlease enter %d numers from 0-9，
A means these numbers are right and in the right place，
B means these numbers are right, but not in the right place.
For example: the answer is 1234, type in 1543, and you will see 1A2B.
You only have 10 chances, be cautious!\n""" %self.hard)

        count=10
        while(count>0):
            a_cnt=0
            b_cnt=0
            in_nums=str(input("Please take a guess: "))
            in_nums=list(in_nums)
            
            while(len(set(in_nums))!=self.hard):
                if(len(set(in_nums)) == len(in_nums)):
                    in_nums=str(input("Please enter %d numbers: "%self.hard))
                else:
                    in_nums=str(input("These numbers must differ from each other: "))
            in_num = "".join(in_nums)
            i=self.hard-1
            while(i>=0):
                if(in_nums[i]==self.nums[i]):
                    a_cnt+=1
                    i-=1
                elif((in_nums[i] in self.nums) and in_nums[i]!=self.nums[i]):
                    b_cnt+=1
                    i-=1
                else:
                    i-=1
            count-=1
            if(a_cnt == self.hard):
                print("Congratulations,"+" %s, you guessed right in %d times!"%(self.name,10-count))
                isretry = input("Press 'enter' to retry, press 'q' to exit: ")    
                break
            elif(count>0):
                print("The result of %s is:%dA%dB\nChances remaining: %d\n"%(in_num,a_cnt,b_cnt,count))
            elif(count==0):
                s=input("You're out of chances, type in '%s is a fool' to check the right answer!\n"%self.name)
                if(s=="%s is a fool"%self.name or s=="%s是笨蛋"%self.name):
                    print("The right answer is %s!"%self.nums)
                    isretry = input("Press 'enter' to retry, press 'q' to exit: ") 
                else:
                    print("Wrong input, please contact the administrator!")
                    isretry = input("Or you can press 'enter' to retry, press 'q' to exit: ")
                    if(isretry == "%s is a fool"%self.name or s=="%s是笨蛋"%self.name):
                        print("The right answer is %s!"%self.nums)
                    
        user_score = count
        if(isretry != "q"):
            self.retry = 1
        else:
            self.retry = 0
        return user_score


    def coundown_gui(self, nums, in_nums):
        if self.name == "test":
            print(nums)

        a_cnt = 0
        b_cnt = 0
        in_nums = list(in_nums)

        while (len(set(in_nums)) != self.hard):
            if (len(set(in_nums)) == len(in_nums)):
                outstr = "Please enter " + str(self.hard) + " numbers!\n"
            else:
                outstr = "These numbers must differ from each other: \n"
            return (outstr, 0)


        i = self.hard - 1
        while (i >= 0):
            if (in_nums[i] == nums[i]):
                a_cnt += 1
                i -= 1
            elif ((in_nums[i] in nums) and in_nums[i] != nums[i]):
                b_cnt += 1
                i -= 1
            else:
                i -= 1

        if (a_cnt == self.hard):
            outstr = "Congratulations," + self.name + " are guenius!\n"
            return (outstr, 1)
        else:
            in_num = "".join(in_nums)
            outstr = "The result of " + in_num + ":" + str(a_cnt) + "A" + str(b_cnt) +"B\n"
            return (outstr, 1)



    # generate different digits
    def num_generator(self):
        nums=[]
        i = 0
        num_list=[0,1,2,3,4,5,6,7,8,9]
        while(i < self.hard):
            t = randint(0,9-i)
            nums.append(num_list[t])
            nums[i] = str(nums[i])
            num_list.remove(num_list[t])
            i += 1
        num="".join(nums)
        return num



    # reading user profile, it contains
    # {name:play_times(n),average_score(a),best_score(b)}
    def get_user_dic(self):
        try:
            f = open("profiles")
        except FileNotFoundError:
            print("Profiles not found, maybe this your first play.\nCreating profiles......")
            with open("profiles","w") as f:
                f.write("")
        else:
            f.close()
    
        with open("profiles") as f:
            profile_str = f.read()
        with open("profiles_bak","w") as f:
            f.write(profile_str)
        profile_str = profile_str.strip()
        profile_list = profile_str.split("\n")
        profile_dic={}
        i=0
        while i<len(profile_list):
            if(len(profile_list[i]) > 0):
                tmp_list = profile_list[i].split(":")
                profile_dic[tmp_list[0]] = list(tmp_list[1].split(","))
            i+=1
        return profile_dic

    # update user profile
    def update_profile(self,times,user_score):
        name = self.name
        profile_dic = self.profile_dic
        if(name in profile_dic):
            n = int(profile_dic[name][0])
            a = float(profile_dic[name][1])
            b = int(profile_dic[name][2])
            a = (a*n + user_score)/(n+1)
            n += times
            if b<user_score:
                b=user_score
            profile_dic[name] = [str(n),str(a),str(b)]
        else:
            profile_dic[name] = ["1",str(user_score),str(user_score)]

        new_str = ""
        for user in profile_dic:
            new_str = (new_str + user + ":" + profile_dic[user][0] + ","
                       + profile_dic[user][1] + "," + profile_dic[user][2] + "\n")
        with open("profiles","w") as f:
            f.write(new_str)

    # to check if the user already exists and the user's passwd
    @property
    def check_user(self):
        name = self.name
        try:
            f = open("key")
        except FileNotFoundError:
            key1 = input("keyfiles not found.\nPlease enter the first key: ")
            key2 = input("Please enter the second key: ")
            with open("key","w") as f:
                f.write(key1+":"+key2+"\n")
            return "new"

        else:
            key_str = f.read()
            f.close()
            key_str = key_str.strip()
            key_list = key_str.split("\n")
            key_tmp = list(key_list[0].split(":"))
            key1 = key_tmp[0]
            key2 = key_tmp[1]
            key_dic = {}
            i = 0
            while i<len(key_list):
                if(len(key_list[i]) > 0):
                    tmp_list = key_list[i].split(":")
                    key_dic[tmp_list[0]] = tmp_list[1]
                i+=1
            encry = AES.new(key1,AES.MODE_CBC,key2)
            if(name in key_dic):
                passwd = getpass.getpass("Please enter your password: ")
                if(len(passwd) < 16):
                    passwd = passwd + "_"*(16-len(passwd))
                if(str(encry.encrypt(passwd)) == key_dic[name]):
                    return "check"
                else:
                    while(str(encry.encrypt(passwd)) != key_dic[name]):
                        t = input("Password incorrect! Press 'r' to retry or 'c' to create a new account: ")
                        if(t == "r"):
                            passwd = getpass.getpass("Please enter your password: ")
                            if(len(passwd) < 16):
                                passwd += "_" * (16 - len(passwd))
                            encry2 = AES.new(key1, AES.MODE_CBC, key2)
                            if (str(encry2.encrypt(passwd)) == key_dic[name]):
                                print(passwd)
                                return "check"

                        elif(t == "c"):
                            break
                    return "new"
            else:
                return "new"


    def check_user_gui(self, passwd):
        name = self.name
        try:
            f = open("key")
        except FileNotFoundError:
            key1 = "hello i'm jarrod"
            key2 = "imlearningpython"
            with open("key","w") as f:
                f.write(key1+":"+key2+"\n")
            return False
        else:
            key_str = f.read()
            f.close()
            key_str = key_str.strip()
            key_list = key_str.split("\n")
            key_tmp = list(key_list[0].split(":"))
            key1 = key_tmp[0]
            key2 = key_tmp[1]
            key_dic = {}
            i = 0
            while i<len(key_list):
                if(len(key_list[i]) > 0):
                    tmp_list = key_list[i].split(":")
                    key_dic[tmp_list[0]] = tmp_list[1]
                i+=1
            encry = AES.new(key1,AES.MODE_CBC,key2)
            if(name in key_dic):
                if(len(passwd) < 16):
                    passwd = passwd + "_"*(16-len(passwd))
                if(str(encry.encrypt(passwd)) == key_dic[name]):
                    return True
                else:
                    return False


    # create a new user
    def create_user(self):
        name = self.name
        s1 = getpass.getpass("Please enter your password (6-16 charactors): ")
        s2 = getpass.getpass("Please reenter your password: ")
        while(s1 != s2):
            print("The two entries are inconsistent.")
            s1 = getpass.getpass("Please enter your password (6-16 charactors): ")
            s2 = getpass.getpass("Please reenter your password: ")
        if(len(s2) < 16):
            s = s2 + "_"*(16 - len(s2))
        else:
            s = s2
        with open("key") as f:
            key_str = f.read()
        with open("key_bak","w") as f:
            f.write(key_str)
        key_str = key_str.strip()
        key_list = key_str.split("\n")
        key_tmp = list(key_list[0].split(":"))
        key1 = key_tmp[0]
        key2 = key_tmp[1]
        encry = AES.new(key1,AES.MODE_CBC,key2)
        passwd = encry.encrypt(s)
        with open("key","a") as f:
            f.write(name + ":" + str(passwd) + "\n")

    def create_user_gui(self, name, passwd):

        if(len(passwd) < 16):
            s = passwd + "_"*(16 - len(passwd))
        with open("key") as f:
            key_str = f.read()
        with open("key_bak","w") as f:
            f.write(key_str)
        key_str = key_str.strip()
        key_list = key_str.split("\n")
        key_tmp = list(key_list[0].split(":"))
        key1 = key_tmp[0]
        key2 = key_tmp[1]
        encry = AES.new(key1,AES.MODE_CBC,key2)
        passwd = encry.encrypt(s)
        with open("key","a") as f:
            f.write(name + ":" + str(passwd) + "\n")

def num_generator(h):
    nums = []
    i = 0
    num_list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    while (i < h):
        t = randint(0, 9 - i)
        nums.append(num_list[t])
        nums[i] = str(nums[i])
        num_list.remove(num_list[t])
        i += 1
    num = "".join(nums)
    return num

    #begin to play
if __name__=="__main__":
    name = input("Please enter your name:")
    user = GuessNumbers(name)
    check = user.check_user
    profile_dic = user.get_user_dic()
    if(check == "new"):
        while(name in profile_dic):
            name = input("This name has been used, please enter another name:")
            user = GuessNumbers(name)
        user.create_user()
        print("\nlooks like it's your fist time here.\n")

    if(name in profile_dic):
        if(profile_dic[name][0] == "1"):
            s = "nd"
        elif(profile_dic[name][0] == "2"):
            s = "rd"
        else:
            s = "th"
        n = int(profile_dic[name][0]) + 1
        a = float(profile_dic[name][1])
        a = int(round(a))
        print("\n\nWelcome, " + name + "," + "this your " + str(n) + s + " play.")
        print("Your average score is " + str(a) + ", and your best score is "+ profile_dic[name][2] +"!\n")
    else:
        print("\n\nWelcome, " + name + ".")

    user_score = user.countdown()
    times = 1
    while(user.retry == 1):
        print("\n\nLet's play another round, note that the number will change!")
        tmp_score = user.countdown()
        times += 1
        if(tmp_score > user_score):
            user_score = tmp_score

    user.update_profile(times,user_score)

