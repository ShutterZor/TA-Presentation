* =============================================================
/* Author Information */
* Name:        Shutter Zor（左祥太）
* Email:       Shutter_Z@outlook.com
* Affiliation: School of Management, Xiamen University
* Date:        2023/7/24
* Version:     V1.0
* =============================================================


/* Reference: 

[1]姚加权,冯绪,王赞钧等.语调、情绪及市场影响:基于金融情绪词典[J].管理科学学报,2021,24(05):26-46.
[2]拿铁一定要加冰(左祥太).「Stata」遍历文件夹与批量追加合并[EB/OL].(2023-3-28)[2023-7-24].https://www.bilibili.com/video/BV1ZL411Q7v6.
[3]拿铁一定要加冰(左祥太).「Stata」词频统计下的数字化转型[EB/OL].(2023-6-18)[2023-7-24].https://www.bilibili.com/video/BV1qk4y1M7AM.
[4]OneStata(左祥太).「Stata」词频统计下的数字化转型[EB/OL].(2023-6-18)[2023-7-24].https://mp.weixin.qq.com/s/f3S0uszvDPALtXk425FWBg.

*/



/* Code */
*- 读入文本
local txtFiles : dir "resources/files" files "*.txt"

local N = 1
foreach singleFile in `txtFiles' {

	import delimited "resources/files/`singleFile'", delimiter("shutterzor", asstring) varnames(nonames) encoding(UTF-8) clear
	
	gen stkcd = ustrregexs(0) if ustrregexm("`singleFile'", "\d+")
	gen year = ustrregexs(0) if ustrregexm("`singleFile'", "_\d+-")
	replace year = substr(year, 2, 4)
	
	tempfile file`N'
	save "`file`N''"
	local N = `N' + 1
}

use "`file1'", clear
forvalues fileNum = 2/5 {
	append using "`file`fileNum''"
}
rename v1 content
save "MDAText.dta", replace


*- 统计情绪词频
use MDAText.dta, clear

	*- 积极词汇
	preserve
		import delimited "resources/PosDict.txt", encoding(UTF-8) clear
		levelsof v1, local(posWords)
		local posNum = _N
	restore

	local tempCount = 1
	foreach posWord of local posWords{
		quietly onetext content, k("`posWord'") m(count) g(posWord`tempCount')
		local tempCount = `tempCount' + 1
		dis %4.2f (`tempCount'-1)/`posNum'*100
	}
	
		*- 计算积极情绪，并删除无用变量
		egen posSentiment = rowtotal(pos*)
		keep stkcd year content posSentiment

	*- 消极词汇
	preserve
		import delimited "resources/negDict.txt", encoding(UTF-8) clear
		levelsof v1, local(negWords)
		local negNum = _N
	restore

	local tempCount = 1
	foreach negWord of local negWords{
		quietly onetext content, k("`negWord'") m(count) g(negWord`tempCount')
		local tempCount = `tempCount' + 1
		dis %4.2f (`tempCount'-1)/`negNum'*100
	}	
	
		*- 计算积极情绪，并删除无用变量
		egen negSentiment = rowtotal(neg*)
		keep stkcd year posSentiment negSentiment
	
	*- 保存结果
	save "sentimentResult.dta", replace


