import csv
from matplotlib import pyplot as plt
import pygal

path = "F:\Python\爬虫\Myspider\Myspider\spiders\深圳python岗位招聘信息.csv"


# 获取平均薪酬
def get_avg_salary(salary_str_list):
	# 把"15K-25K" 变为 ["15", "25"]的格式，并把第一行的数据过滤掉
	salary = [i.replace("K", "").split("-") for i in salary_str_list[1:] if i != "薪资面议" and i != "校招" and i != "1K以下"]
	# print(salary)
	# 求范围之间平均薪资
	avg_salary = [(float(i[0]) * 1000 + float(i[1]) * 1000) // 2 for i in salary]
	return avg_salary


# 绘制薪资范围直方图
def salary_analysis():
	# 读取数据
	with open(path, "r", encoding="gb18030", newline="") as f:
		reader = csv.reader(f)
		salary = [row[3] for row in reader]
	avg_salary = get_avg_salary(salary)
	# 统计一定范围内薪资出现的频数
	counts = [0] * 6
	for i in avg_salary:
		if 5000 >= i > 0:
			counts[0] += 1
		elif 13000 >= i > 5000:
			counts[1] += 1
		elif 20000 >= i > 13000:
			counts[2] += 1
		elif 30000 >= i > 20000:
			counts[3] += 1
		elif 40000 >= i > 30000:
			counts[4] += 1
		elif 80000 >= i > 40000:
			counts[5] += 1
	# 绘制直方图
	hist = pygal.Bar()

	hist.x_labels = ["0-5K", "5-13K", "13-20K", "20-30K", "30-40K", "40-80K"]

	hist.add("深圳python工程师薪资分布", counts)
	hist.x_title = "薪资范围"
	hist.y_title = "频数"
	hist.render_to_file("123.svg")


# 绘制经验与薪资的关系图
def experience_salary():
	# 读取数据
	exp_list = []
	salary_list = []
	with open(path, "r", encoding="gb18030", newline="") as f:
		reader = csv.reader(f)

		for row in reader:
			if row[3] != "薪资面议" and row[3] != "校招" and row[3] != "1K以下":
				exp_list.append(row[5])
				salary_list.append(row[3])

	# 求得平均薪资
	avg_salary = get_avg_salary(salary_list)

	# 获得X轴坐标轴，对exp_list去重,  {'1-3年', '5-10年', '3-5年', '经验', '无经验', '不限', '10年以上', '1年以下'}
	exp_set = set(exp_list)
	# 定义一个临时二维数组 记录 不同经验的 工资总数  数量  工作经验
	# temp = [[0, 0]] * len(exp_set) 不能这样生成二维数组,因为改变一个， 会改变所有
	temp = [[0, 0, 0] for i in range(len(exp_set))]

	exp_list = exp_list[1:]

	for i in range(len(exp_list)):
		if exp_list[i] == "1年以下":
			temp[0][0] += avg_salary[i]
			temp[0][1] += 1
			temp[0][2] = "1年以下"

		elif exp_list[i] == "1-3年":
			temp[1][0] += avg_salary[i]
			temp[1][1] += 1
			temp[1][2] = "1-3年"

		elif exp_list[i] == "3-5年":
			temp[2][0] += avg_salary[i]
			temp[2][1] += 1
			temp[2][2] = "3-5年"

		elif exp_list[i] == "5-10年":
			temp[3][0] += avg_salary[i]
			temp[3][1] += 1
			temp[3][2] = "5-10年"

		elif exp_list[i] == "10年以上":
			temp[4][0] += avg_salary[i]
			temp[4][1] += 1
			temp[4][2] = "10年以上"

		elif exp_list[i] == "无经验":
			temp[5][0] += avg_salary[i]
			temp[5][1] += 1
			temp[5][2] = "无经验"

		elif exp_list[i] == "不限":
			temp[6][0] += avg_salary[i]
			temp[6][1] += 1
			temp[6][2] = "不限"
	# print(temp)

	# 绘图
	hist = pygal.Bar()

	hist.x_labels = [i[2] for i in temp]

	hist.add("深圳python工程师工作经验与薪资分布图", [i[0]//i[1] for i in temp if i[1] != 0])
	hist.x_title = "工作经验"
	hist.y_title = "平均薪资(元)"
	hist.render_to_file("深圳python工程师工作经验与薪资分布图.svg")

if __name__ == '__main__':
	experience_salary()
	print("hhhhhhhh")
