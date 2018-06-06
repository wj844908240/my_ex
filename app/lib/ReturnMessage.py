# -*- coding: utf-8 -*-

Code_Str = "code"
Status_Str = "status"
Error_Str = "error"
Info_Str = "info"
Message_Str = "message"
Success_Str = "success"
No_Data = "no data"

# 请求报错
def returnErrorMsg():
	resultDict = {Message_Str:{Code_Str: -1, Status_Str: Error_Str}}
	return resultDict

# 请求成功，有数据
def returnMsg(dataDict):
	resultDict = {Info_Str: dataDict, Message_Str: {Code_Str: 1, Status_Str: Success_Str}}
	return resultDict

# 请求成功，无数据
def returnNoneMsg(dataDict):
	resultDict = {Info_Str: dataDict, Message_Str: {Code_Str: 0, Status_Str: No_Data}}
	return resultDict

class RetrunMessage:

	def __init__(self, info_dict, code_status):
		self.info_dict = info_dict
		self.code_status = code_status
		self.code_status_dict = {-1:Error_Str,0:No_Data,1:Success_Str}

	def get_return_info(self):
		if self.code_status == -1:
			return {Message_Str:{Code_Str: -1, Status_Str: self.code_status_dict[self.code_status]}}
		return {Info_Str: self.info_dict, Message_Str: {Code_Str: self.code_status, Status_Str: self.code_status_dict[self.code_status]}}
