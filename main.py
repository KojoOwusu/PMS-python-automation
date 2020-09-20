from selenium import webdriver
from enum import Enum
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
#import org.openqa.selenium.support.ui.Select
from selenium.webdriver.support.ui import Select
import selenium.common.exceptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

constEmail = "portal@caa.com.gh"
constPassword = "1Ct@@pms123!"
EmailFormElement = ""
PasswordFormElement = ""
BASE_URL = "http://172.16.0.21"

class WorkPlanDataObject:
	'the data object for a single performance objective'
	def __init__(self,employeeName,performanceObjective,dataObj):
		self.employeeName=employeeName
		self.performanceObjective=performanceObjective
		self.data=[]
		self.data.append(dataObj)

	def __str__(self):
		output = 'EmployeeName:{0} \n Performance objective: {1} \n'.format(self.employeeName,self.performanceObjective)
		for item in self.data:
			output += 'Key Activity:{} \n Completion time:{} \n Expected Outputs: {} \n Resource Constraints:{} \n Target:{} \n Weight:{}'.format(item["keyActivity"],item["completionTime"],item["expectedOutputs"],item["resourceConstraints"],item["target"],item["weight"])
		return output	

def initWeb():
	SWebDriver = webdriver.Chrome()
	return SWebDriver

def signIn(Browser):
	EmailFormElement = Browser.find_element_by_name('email')
	PasswordFormElement = Browser.find_element_by_name('password')
	SigninButton = Browser.find_element_by_xpath('/html/body/div[1]/div[2]/div/div/div/div[2]/form/div[4]/button')
	EmailFormElement.clear()
	PasswordFormElement.clear()
	EmailFormElement.send_keys(constEmail)
	PasswordFormElement.send_keys(constPassword)
	SigninButton.send_keys(Keys.RETURN)

def findElementby(type,value):
	if type == "xpath":
		return webbrowser.find_element_by_xpath(value)
	elif type == "classname":
		return webbrowser.find_element_by_class_name(value)
	elif type == "id":
		return webbrowser.find_element_by_id(value)
	elif type =="name":
		return webbrowser.find_element_by_name(value)
	elif type =="linktext":
		return webbrowser.find_element_by_link_text(value)

def createWorkPlan(dataObject):
	webbrowser.implicitly_wait(10)
	el = webbrowser.find_element_by_xpath('//*[@id="sidenav-collapse-main"]/ul[1]/li[5]/a')
	el.send_keys(Keys.RETURN)
	webbrowser.find_element_by_xpath('//*[@id="panel"]/div[2]/div/div/div/div[1]/div/div[2]/a').send_keys(Keys.RETURN)
	EmployeeSelect = Select(webbrowser.find_element_by_name('employee'))
	try:
		EmployeeSelect.select_by_visible_text(dataObject.employeeName)
	except:
		print("CANT FIND THIS EMPLOYEE SORRY")
	DeptObjSelect = Select(webbrowser.find_element_by_name('department_objective'))
	try:
		DeptObjSelect.select_by_visible_text(dataObject.performanceObjective)
	except:
		print("NO SUCH PERFORMANCE OBJECTIVE")
	#webbrowser.find_element_by_name("objective").send_keys(dataObject.performanceObjective)
	#findElementby('xpath','/html/body/div[1]/div[2]/div/div/div/div/div[2]/form/div[1]/div[1]/select').send_keys(dataObject.employeeName)
	findElementby('name','objective').send_keys(dataObject.performanceObjective)
	findElementby('name','department_objective').send_keys(dataObject.performanceObjective)
	findElementby('name',"activity[]").send_keys(dataObject.data[0].get("keyActivity"))
	findElementby('name','completion_time[]').send_keys(dataObject.data[0].get("completionTime"))
	findElementby('name','planned_weight[]').send_keys(dataObject.data[0].get('weight'))
	findElementby('name','expected_output[]').send_keys(dataObject.data[0].get('expectedOutputs'))
	findElementby('name','resource_constraint[]').send_keys(dataObject.data[0].get('resourceConstraints'))
	findElementby('name','target[]').send_keys(dataObject.data[0].get('target'))
	findElementby('xpath','/html/body/div[1]/div[2]/div/div/div/div/div[2]/form/div[5]/button')

def getInput():
	EmpName, PerM = input("enter information employeeName and Performance Measure").split(",")
	Output = {"keyActivity":"","completionTime":"","expectedOutputs":"","resourceConstraints":"","target":"","weight":""}
	datalist=list(input("enter key activities").split(","))
	for pos, ele in enumerate(Output):
		Output[ele] = str(datalist[pos])
	print(Output)
	return WorkPlanDataObject(EmpName,PerM,Output)

				

if __name__ == "__main__":
	webbrowser=initWeb()
	#webbrowser.implicitly_wait(10)
	webbrowser.get(BASE_URL)
	signIn(webbrowser)
	Data = getInput()
	print(Data)
	#element = WebDriverWait(webbrowser, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="navbar-search-main"]/div/div/input')))
	createWorkPlan(Data)
	

	#webbrowser.quit()
