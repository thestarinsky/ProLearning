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
scoreManagePath = "/study/"
while driver.title != "登录系统":
    pass 
driver.execute_script(js.format(localPath+scoreManagePath))
# key = input("继续请按1")
handle_all = driver.window_handles
for h in handle_all:
    if h != handle_study:
        handle_score = h
driver.switch_to.window(handle_study)
print("切换至学习系统")
driver.find_element_by_class_name("login-btn2").click()
driver.find_element_by_xpath("/html/body/div/div[2]/a[4]").click()
driver.find_element_by_xpath("//*[@id=\"coursetype_chosen\"]/a/span").click()
driver.find_element_by_xpath("//*[@id=\"coursetype_chosen\"]/div/ul/li[2]").click()
driver.find_element_by_xpath("//*[@id=\"search\"]/div[2]/div/button").click()




