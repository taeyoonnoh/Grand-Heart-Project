

##### 모순점(데이터의 부족시 발생할 수 있는) 예외 처리 방법 예시#####

User1_data = {
    '국':11,
    '구이':0,
    '밥':1   
}
User2_data = {
    '국':2,
    '구이':0,
    '밥':0   
}

class User():

  # def __init__(self):
  #   self.sum = 0

  def common(self, user1, user2):
      exception_category=[]
      sum=0
      for key, value in user1.items():
          if value == 0 :
              exception_category.append(key)
      
      for key,value in user2.items() : 
          if value == 0 :
              exception_category.append(key)
      exception_category = list(set(exception_category))
      return exception_category

exception = User()
exception.common(User2_data, User1_data)

######## filter(exception.common(User2_data, User1_data))#######



####   Weighted_sum_Algorithm 예시 #### 


User = {
    'User1':{'국':11, '구이':0, '밥':1},
    'User2':{'국':2, '구이':0, '밥':0}
}

user1 = [list(list(User.values())[0].values())[i] for i in range(len(list(User.values())[0].keys()))]
user2 = [list(list(User.values())[1].values())[i] for i in range(len(list(User.values())[0].keys()))]

result = [(x + y) * (1 / len(User)) for x, y in zip(user1, user2)]
result

####### User가 새로 추가 되더라도 적용가능한 class 생성 필요, 데이터셋이 어떻게 databse에 저장되어 불러올 수 있는지에 따라서 방법이 바뀔 수 있음. 

















#============================================================================================================================#
# def WSA(i, j):
#     abc = []
#     for i in User:
#         abc = []
#         hum = [list(User.values())[i].values()][i] * (1 / len(User)) + [list(User.values())[i+1].values()][i] * (1 / len(User))
#         abc.append(hum)
#     return abc





# User1_data = {
#     '국':11,
#     '구이':0,
#     '밥':1   
# }
# User2_data = {
#     '국':2,
#     '구이':0,
#     '밥':0   
# }



# def WS_algorithm(User):
#     WS_result = []    
#     WS_result.append({i:User[i] * (1 / len(User))})
#     return WS_result


# WS_result = []
# for i in result:
#     WS_result.append({i:User[i] * (1 / len(User))})

# for i in User:
#     WS_result = User[i]


