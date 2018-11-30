import requests
import json
import csv
import time


class ZhiLianSpider(object):
	def __init__(self, f_name, file_headers):
		self.headers = {
			"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebK"
			              "it/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",

		}
		self.url = "https://fe-api.zhaopin.com/c/i/sou?pageSize=60&cityId=765&kw=python&kt=3&start={}"
		self.filename = f_name
		self.file_headers = file_headers

	def parse_url(self, url):
		response = requests.get(url, headers=self.headers)
		return response.content.decode()

	def get_data(self, json_data):
		dict_data = json.loads(json_data)
		temp_list = []

		# 取出来是个列表，列表里面是字典数据, 0: {number: "CC688998424J00201975003",…}
		data_list = dict_data["data"]["results"]
		# 判断获取的数据是否为空，如果为空，表示数据已经取完了
		if data_list is not None:
			for i in range(len(data_list)):
				temp = data_list[i]
				data = {}
				# print(temp)
				data["公司"] = temp["company"]["name"]
				data["职位"] = temp["jobName"]
				data["城市"] = temp["city"]["display"]
				data["经验"] = temp["workingExp"]["name"]
				data["学历"] = temp["eduLevel"]["name"]
				data["薪资"] = temp["salary"]
				data["福利"] = temp["welfare"]
				data["发布日期"] = temp["updateDate"].split(" ")[0]
				data["企业类型"] = temp["company"]["type"]["name"]
				data["企业规模"] = temp["company"]["size"]["name"]
				data["detail_url"] = temp["positionURL"]
				data["岗位"] = temp["jobType"]["items"][1]["name"]
				temp_list.append(data)
			return temp_list

	def save_data_to_csvfile(self, data_list):
		# 中文保存到CSV中编码格式要 gb18030
		with open(self.filename, "a", encoding="gb18030", newline="") as f:
			f_csv = csv.DictWriter(f, self.file_headers)
			f_csv.writerows(data_list)
			print("-"*10, "Done", "-"*10)

	def run(self):
		# 构造url地址
		page = 0
		while True:
			url = self.url.format(page)
			# 发送请求，获取响应
			json_data = self.parse_url(url)
			# 提取数据
			data_list = self.get_data(json_data)
			# 如果返回数据为空，则结束函数
			if not data_list:
				return
			# 保存数据到CSV文件中
			self.save_data_to_csvfile(data_list)
			page += 60
			time.sleep(0.5)


def write_csv_header(path, headers):
	with open(path, "a", encoding="gb18030", newline="") as f:
		f_csv = csv.DictWriter(f, headers)
		f_csv.writeheader()

if __name__ == '__main__':
	# 定义文件名
	filename = "深圳python岗位招聘信息.csv"
	# 定义CSV文件表头
	headers = ["公司", "职位", "岗位", "薪资", "学历", "经验", "福利", "城市", "企业类型", "企业规模", "detail_url", "发布日期"]
	# 写入表头
	write_csv_header(filename, headers)
	zl = ZhiLianSpider(filename, headers)
	zl.run()