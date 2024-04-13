# sdk-show
展示sdk以及相关的隐私政策信息
参考文档  https://dhtmlx.com/blog/create-javascript-mindmap-diagram-dhtmlx-library/

### 原始json文件结构说明：
sdk-name 第三方sdk名称
data 数据项 需要按照顿号进行分隔（在括号内的需要进行分叉）
ori-url： 原本爬下来的url
sdk-url：确定为sdk隐私政策的链接
url：ori-url规范化为列表的链接
url-judge：判断是否为隐私政策的链接 (是隐私政策)
sdk-url-judge：判断隐私政策链接是否适用于sdk（是sdk隐私政策）

### 修改的地方：
1. 换用新的模板 使得整体结构更加紧凑
2. 不显示purpose节点
3. URL链接仅展示三个之中的一个
4. 通过sdk名称进行检索展示
5. 对于数据项的拆分，使用parse_data函数进行拆分，思路是将{"位置信息、应用列表、剪切板信息、设备信息（IMSI、IMEI、MAC地址、BSSID、SSID、IDFA、MEID、AndroidID）、手机存储权限、音频"} 这种格式的先按照括号项进行拆分，比如设备信息和它的子内容作为一个节点，之后设备信息的这些子节点再从设备信息进行分支

### 缺陷
由于CROS限制 无法访问本地文件 如果想要生成新的afterTreeData.json进行展示，需要执行python changeJson.py，将转换后的json文件结果复制到example.html的dataset字段进行展示，该问题属于次要矛盾后续再进行解决，在开发过程中首先进行数据效果的展示和调整