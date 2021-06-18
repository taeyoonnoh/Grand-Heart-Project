from selenium import webdriver
 
path = "chromedriver"    #ex. C:/downloads/chromedriver.exe
 
#조금만 기다리면 selenium으로 제어할 수 있는 브라우저 새창이 뜬다
driver = webdriver.Chrome(path)


driver.get('https://www.google.com/maps/search/')
#페이지의 제목을 체크하여 'Google'에 제대로 접속했는지 확인한다
assert "Google" in driver.title

 
#검색 입력 부분에 커서를 올리고
#검색 입력 부분에 다양한 명령을 내리기 위해 elem 변수에 할당한다
elem = driver.find_element_by_name("q")
 
#입력 부분에 default로 값이 있을 수 있어 비운다
elem.clear()

food = '파스타'# 반환된 값 food 변수에 할당

#검색어를 입력한다
elem.send_keys(food)
 
#검색을 실행한다
elem.submit()
 
#검색이 제대로 됐는지 확인한다
assert "No results found." not in driver.page_source
 
#브라우저를 종료한다
# driver.close()
