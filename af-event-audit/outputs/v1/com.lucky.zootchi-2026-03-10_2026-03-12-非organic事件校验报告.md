# com.lucky.zootchi - 2026-03-10_2026-03-12 - 非organic 事件校验报告

**数据范围**
- 文件：`data/events/problematic/com.lucky.zootchi_organic-in-app-events_2026-03-10_2026-03-12_Asia_Shanghai.csv`
- 行数：94

**问题概览（仅列出发现的问题）**
- Install Time 为空：12/94（12.77%）
- USD 事件金额超过 100：24/94（25.53%）
- IP 为空：93/94（98.94%）
- AppsFlyer ID 格式不合规：36/94（38.30%）

**比例指标**
- 未上报 IDFA 但上报了 IDFV 且上报了 IP 的数据占“未上报 IDFA”数据的比例：0/94（0.00%）

**问题示例（每类 1 条，包含完整行数据）**
- Install Time 为空（问题列：`Install Time`）
- 行号：21
```tsv
Attributed Touch Type	Attributed Touch Time	Install Time	Event Time	Event Name	Event Value	Event Revenue	Event Revenue Currency	Event Revenue USD	Cost Model	Cost Value	Cost Currency	Event Source	Partner	Media Source	Channel	Campaign	Campaign ID	Adset	Adset ID	Ad	Ad ID	Ad Type	Site ID	Region	Country Code	State	City	Postal Code	DMA	IP	Operator	Carrier	Language	AppsFlyer ID	Customer User ID	Android ID	Advertising ID	IMEI	IDFA	IDFV	Device Category	Platform	OS Version	App Version	SDK Version	App ID	App Name	Is Retargeting	Retargeting Conversion Type	Is Primary Attribution	Attribution Lookback	Reengagement Window	Match Type	User Agent	HTTP Referrer	Original URL	Device Model
			2026-03-11 22:15:07	af_co_active_60min	{"appVersion":"1.0.20","appsflyer_id":"78f87a209e6b3a7182c38aed55575406","cuid":"ryNZwZRnakuHcm0plfXIMqL Fwu/a/AJD8YS1RAqd g=","af_customer_user_id":"78f87a209e6b3a7182c38aed55575406"}		USD				S2S																				78f87a209e6b3a7182c38aed55575406	ryNZwZRnakuHcm0plfXIMqL+Fwu/a/AJD8YS1RAqd+g=		53ee6412-e448-4dba-9bfa-7fd2fe806ffa			unknown_device_category	android		1.0.20		com.lucky.zootchi		false		true				
```

- IP 为空（问题列：`IP`）
- 行号：2
```tsv
Attributed Touch Type	Attributed Touch Time	Install Time	Event Time	Event Name	Event Value	Event Revenue	Event Revenue Currency	Event Revenue USD	Cost Model	Cost Value	Cost Currency	Event Source	Partner	Media Source	Channel	Campaign	Campaign ID	Adset	Adset ID	Ad	Ad ID	Ad Type	Site ID	Region	Country Code	State	City	Postal Code	DMA	IP	Operator	Carrier	Language	AppsFlyer ID	Customer User ID	Android ID	Advertising ID	IMEI	IDFA	IDFV	Device Category	Platform	OS Version	App Version	SDK Version	App ID	App Name	Is Retargeting	Retargeting Conversion Type	Is Primary Attribution	Attribution Lookback	Reengagement Window	Match Type	User Agent	HTTP Referrer	Original URL	Device Model
		2026-01-21 19:12:35	2026-03-12 14:52:53	initiatecheckout	{"af_content_type":"gp-pre-month-9p9","af_order_id":"","appsflyer_id":"1773296695981-6781837853051499106","cuid":"qn8GmsA/bE Pc25 wqKaZfj/RAGxOvMIDMpGhxx4I70=","af_revenue":0,"af_currency":""}	0	USD	0.0				S2S								NA	US	AZ	Sierra Vista	85635	789					1773296695981-6781837853051499106	qn8GmsA/bE+Pc25+wqKaZfj/RAGxOvMIDMpGhxx4I70=		ea02cd39-fe47-4fc4-828b-a5c2da4be973			unknown_device_category	android				com.lucky.zootchi		false		true				
```

- AppsFlyer ID 格式不合规（问题列：`AppsFlyer ID`）
- 行号：5
```tsv
Attributed Touch Type	Attributed Touch Time	Install Time	Event Time	Event Name	Event Value	Event Revenue	Event Revenue Currency	Event Revenue USD	Cost Model	Cost Value	Cost Currency	Event Source	Partner	Media Source	Channel	Campaign	Campaign ID	Adset	Adset ID	Ad	Ad ID	Ad Type	Site ID	Region	Country Code	State	City	Postal Code	DMA	IP	Operator	Carrier	Language	AppsFlyer ID	Customer User ID	Android ID	Advertising ID	IMEI	IDFA	IDFV	Device Category	Platform	OS Version	App Version	SDK Version	App ID	App Name	Is Retargeting	Retargeting Conversion Type	Is Primary Attribution	Attribution Lookback	Reengagement Window	Match Type	User Agent	HTTP Referrer	Original URL	Device Model
		2026-02-02 18:20:36	2026-03-12 13:51:02	af_key_action_D0_2	{"appVersion":"1.0.20","appsflyer_id":"10d14940556fc204e68630ee7c9dbf91","cuid":"qStbyJc/bEuLIm0txabPN//6TA60OvAIDZAehkd4fu8=","af_customer_user_id":"10d14940556fc204e68630ee7c9dbf91"}		USD				S2S								AS	CN	BJ	Daxing	100010	156001					10d14940556fc204e68630ee7c9dbf91	qStbyJc/bEuLIm0txabPN//6TA60OvAIDZAehkd4fu8=		ef6df6c2-1402-4448-a7d0-2baf7b09720f			unknown_device_category	android		1.0.20		com.lucky.zootchi		false		true				
```

- USD 事件金额超过 100（问题列：`Event Revenue` + `Event Revenue Currency`）
- 行号：15
```tsv
Attributed Touch Type	Attributed Touch Time	Install Time	Event Time	Event Name	Event Value	Event Revenue	Event Revenue Currency	Event Revenue USD	Cost Model	Cost Value	Cost Currency	Event Source	Partner	Media Source	Channel	Campaign	Campaign ID	Adset	Adset ID	Ad	Ad ID	Ad Type	Site ID	Region	Country Code	State	City	Postal Code	DMA	IP	Operator	Carrier	Language	AppsFlyer ID	Customer User ID	Android ID	Advertising ID	IMEI	IDFA	IDFV	Device Category	Platform	OS Version	App Version	SDK Version	App ID	App Name	Is Retargeting	Retargeting Conversion Type	Is Primary Attribution	Attribution Lookback	Reengagement Window	Match Type	User Agent	HTTP Referrer	Original URL	Device Model
		2026-01-21 19:12:35	2026-03-12 11:10:28	af_pay	{"af_content_type":"dootchi_platinum","af_order_id":"2441121358718466327","appsflyer_id":"1773052859848-3028740892582215440","cuid":"qn8GmsA/bE Pc25 wqKaZfj/RAGxOvMIDMpGhxx4I70=","af_revenue":1050,"af_currency":"USD"}	1050	USD	1050.0				S2S								NA	US	AZ	Sierra Vista	85635	789					1773052859848-3028740892582215440	qn8GmsA/bE+Pc25+wqKaZfj/RAGxOvMIDMpGhxx4I70=		ea02cd39-fe47-4fc4-828b-a5c2da4be973			unknown_device_category	android				com.lucky.zootchi		false		true				
```

**说明**
- 本报告仅列出检测到的问题类型与示例，不包含解决方案。
- 如需排查/解决方案，请以 `event_eval/af_event_checks.md` 中的说明为准。
