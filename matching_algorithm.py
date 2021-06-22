##### 초기 데이터 생성시, 두 유저간 저장된 음식 데이터 매칭 방법######

# 아이템기반(Item-based CF) 은 실제 데이터에서 유저 수가 적거나 겹치는 아이템이 적어 유효한 데이터를 뽑아내기 힘들 때 거꾸로 
# 아이템을 기반으로 유사도를 구하는 기법이다.

####오토인코더 모델로인하여 유저개인이 선호하여 선택한 이미지 데이터를 기반으로 이와 유사한 데이터 이미지반환 ex)냉면=>could be 국수 메뉴반환될 수 있음 

#AI_hub의 한국음식 이미지는 각 음식 종류별로 딕셔너리화 되어있음.
#각 유저의 음식종류 = key로 구분 , 해당 음식 종류의 숫자는 = value
#각 value 포인트는 각 사용자가 모아온 데이터의 축적양을 나타냄 => 숫자가 높은수록 해당 종류음식을 많이 선택(선호)하여 그 값이 축적됨.
recommended_food = {
    '국':{'User1':11, 'User2':2},
    '구이':{'User1':7, 'User2':8},
    '밥':{'User1':1, 'User2':12}   
}


dic = []
for i in recommended_food:
    num1 = recommended_food.get(i).get('User1')- recommended_food.get(i).get('User2')
 
    dic.append({i:abs(num1)})
print(dic)#각 음식종류를 튜플화 하여 리스트로 반환 / 문제는 min(dic) 으로 최소값의 key를 불러오질 못했음. 