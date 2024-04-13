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