from selenium import webdriver

js="window.open('{}','blank_');"

localPath = "https://learning.hzrs.hangzhou.gov.cn"
opt = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=opt)
driver.get(localPath)
btn = driver.find_element_by_class_name("login-btn")
btn.click()

# set login info
username = "18626886786"
password = "Yhblsqt2"

# Login page
uname_input = driver.find_element_by_id("loginname")
pwd_input = driver.find_element_by_id("loginpwd")
uname_input.send_keys(username)
pwd_input.send_keys(password)
driver.find_element_by_id("submit").click()

# page select
handle_study = driver.current_window_handle #main windows handle
learnPath = "/"
scoreManagePath = "/study/?act=studyCourseList"
while driver.title != "登录系统":
    pass 
driver.execute_script(js.format(localPath+scoreManagePath))




# get score now
# input codes


# key = input("继续请按1")
handle_all = driver.window_handles
for h in handle_all:
    if h != handle_study:
        handle_score = h
# swicth to lesson learned list
driver.switch_to.window(handle_score)
# get max page number
pages = int(driver.find_element_by_xpath("/html/body/div/div[2]/div[2]/div[2]/form/div[3]/div/div/span").get_attribute("innerHTML")[1:-1])
print("获取已有课程页面总数",pages)
lessons_learned = []
for p in range(0,pages):
    p_lessons = driver.find_elements_by_xpath("/html/body/div/div/div/div/form/div/table/tbody/tr/td[1]/a")    
    for l in p_lessons:
        obj = {}
        obj["title"]= l.get_attribute("innerHTML").split("]")[1]
        obj["id"] = l.get_attribute("href").split("courseid=")[1]
        print("单课程",obj)
        lessons_learned.append(obj)
    driver.find_element_by_xpath("/html/body/div/div[2]/div[2]/div[2]/form/div[3]/div/div/a[4]").click()
print("已学课程：",lessons_learned)
driver.switch_to.window(handle_study)



print("切换至学习系统")
driver.find_element_by_class_name("login-btn2").click()
driver.find_element_by_xpath("/html/body/div/div[2]/a[4]").click()
driver.find_element_by_xpath("//*[@id=\"coursetype_chosen\"]/a/span").click()
driver.find_element_by_xpath("//*[@id=\"coursetype_chosen\"]/div/ul/li[2]").click()
driver.find_element_by_xpath("//*[@id=\"search\"]/div[2]/div/button").click()




lessons=[]
apool = driver.find_elements_by_xpath("/html/body/div/div/div/div/ul/li/div/p/a")
for a in apool:
    obj = {}
    title = str(a.get_attribute("innerHTML"))
    if title[0] != "[" and title[-1]!="]":
        obj["title"] = title
        obj["href"] = a.get_attribute("href")
        lessons.append(obj)
print(lessons)





