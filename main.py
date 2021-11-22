from selenium import webdriver
import time 

# set login info
username = "18626886786"
password = "Yhblsqt2"
windows_handles = []#record all window handles,set new handle when new window opened , delete the handle which window is closed 
handle_study = 0
handle_score = 0
handle_video = 0
opt = webdriver.ChromeOptions()   
driver = webdriver.Chrome(options=opt)

"""
this is a program to finish yearly cources on https://learning.hzrs.hangzhou.gov.cn
setps:
1. Login
2. get lessons learned and compare the list to all lessons
3. according to the result open a new window to learn

Points:
1. windows need to be remembered to switch
"""
def login():
    localPath = "https://learning.hzrs.hangzhou.gov.cn"     
    driver.get(localPath)
    btn = driver.find_element_by_class_name("login-btn")
    btn.click()
    # Login page
    while driver.title != "浙江政务服务网 个人用户登录":
        time.sleep(1)
    uname_input = driver.find_element_by_id("loginname")
    pwd_input = driver.find_element_by_id("loginpwd")
    uname_input.send_keys(username)
    pwd_input.send_keys(password)
    driver.find_element_by_id("submit").click()
    # page select    
    learnPath = "/"
    scoreManagePath = "/study/?act=studyCourseList"
    js="window.open('{}','blank_');"
    while driver.title != "登录系统":
        pass 
    driver.execute_script(js.format(localPath+scoreManagePath))




# get score now
# input codes


# key = input("继续请按1")
def getHandle():
    global windows_handles
    handle_study = driver.current_window_handle #main windows handle
    handle_all = driver.window_handles
    for h in handle_all:
        if h != handle_study:
            h_new = h
    return h_new
    # swicth to lesson learned list
driver.switch_to.window(handle_score)
# get max page number
pages = int(driver.find_element_by_xpath("/html/body/div/div[2]/div[2]/div[2]/form/div[3]/div/div/span").get_attribute("innerHTML")[1:-1])
print("获取已学课程页面总数",pages)
lessons_learned = []
lessons_learned_ids= []
for p in range(0,pages):
    p_lessons = driver.find_elements_by_xpath("/html/body/div/div/div/div/form/div/table/tbody/tr/td[1]/a")    
    for l in p_lessons:
        obj = {}
        obj["title"]= l.get_attribute("innerHTML").split("]")[1]
        obj["id"] = l.get_attribute("href").split("courseid=")[1]
        # print("单课程",obj)
        lessons_learned.append(obj)
        lessons_learned_ids.append(obj["id"])
    driver.find_element_by_xpath("/html/body/div/div[2]/div[2]/div[2]/form/div[3]/div/div/a[4]").click()
print("已学课程：",lessons_learned,"已学课程ID：",lessons_learned_ids)
driver.switch_to.window(handle_study)



print("切换至学习系统")
driver.find_element_by_class_name("login-btn2").click()
driver.find_element_by_xpath("/html/body/div/div[2]/a[4]").click()
driver.find_element_by_xpath("//*[@id=\"coursetype_chosen\"]/a/span").click()
driver.find_element_by_xpath("//*[@id=\"coursetype_chosen\"]/div/ul/li[2]").click()
driver.find_element_by_xpath("//*[@id=\"search\"]/div[2]/div/button").click()



lesson_page_path= "https://learning.hzrs.hangzhou.gov.cn/course/index.php?act=detail&courseid="
lessons=[]
lessons_ids = []
learn_list = []
pages_to_learn = int(driver.find_element_by_xpath("/html/body/div[1]/div[3]/div[2]/div[4]/div/span").get_attribute("innerHTML")[1:-1])
for p in range(0,pages_to_learn):
    apool = driver.find_elements_by_xpath("/html/body/div/div/div/div/ul/li/div/p/a")
    for a in apool:
        title = str(a.get_attribute("innerHTML"))
        if title[0] != "[" and title[-1] != "]":
            obj = {}
            obj["title"] = title
            obj["href"] = a.get_attribute("href")
            obj["id"] = a.get_attribute("href").split("courseid=")[1]
            lessons.append(obj)
            lessons_ids.append(obj["id"])
    print(lessons_ids)
    if not set(lessons_ids).issubset(set(lessons_learned_ids)):#if lessons ids are not all in learned
        learn_list = set(lessons_ids) - set(lessons_learned_ids)
        if len(learn_list)>0:
            for li in learn_list:
                learn_page =  lesson_page_path + li
                driver.get(learn_page)
                driver.find_element_by_xpath("/html/body/div/div[3]/table[2]/tbody/tr[2]/td/div/button[1]").click()


    else:
        pass
        






