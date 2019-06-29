####因子分析####

rm(list = ls())  #清理内存,对象
gc()

install.packages("psych")
install.packages("GPArotation")

#### 1. 函数介绍####

###R语言做因子分析主要介绍三个函数
##******************
# (1) 自带的factanal函数
#  factanal(x,factors,data=NULL,covmat=NUL,
#           n.obs=NA,subset,na.action,start=NULL,
#           score=c("none","regression","Bartlett"),
#           rotation="varimax",control=NULL,…) 
# x是公式或者用于因子分析的数据，可以是矩阵或数据框；
# factors表示要生成的因子个数；
# data指定数据集，当x为公式的时候使用；
# covmat是样本的协方差矩阵或者相关系数矩阵，x可以忽略；
# scores表示计算因子得分的方法；
# rotation表示因子旋转的方法，默认为"varimax"。
# 这个函数仅支持用极大似然估计方法做因子分析。
##*********************************************

##**************************
# (2) psych包里的fa函数
# fa(r，nfactors=，n.obs=，rotate=，scores=，fm=)
# r是相关系数矩阵或原始数据矩阵；
# nfactors设定提取的因子数（默认为1）；
# n.obs是观测数（输入相关系数矩阵时需要填写）；
# rotate设定放置的方法（"varimax",最大方差旋转正交法）；
# scores设定是否计算因子得分（默认不计算）；
# fm为估计解的方法（pa为主轴因子法,ml为极大似然法,wls加权最小二乘法，gls广义加权最小二乘法，minres最小残差法（默认））。

##***************************************

##***************************************
# (3) varimax()函数可完成因子载荷矩阵的旋转变换，其使用格式为：
# varimax(x, normalize = TRUE, eps = 1e-5)
# x是因子载荷矩阵;
# normalize是逻辑变量，是否对变量进行Kaiser正则化;
# eps是迭代终止精度。
##***************************************

#### 2. 因子分析的基本步骤####
##**************************
# 1.为避免各变量量纲的不利影响,用scale()函数数据标准化;
# 2.标准化数据的相关矩阵，用cor()函数;
# 3.求相关矩阵的特征值和单位特征向量，用eigen()函数，根据特征值大于1的个数，可以确定因子的个数;
# 4.因子分析，可以利用psych包中的fa()函数;
# 5.根据因子载荷矩阵进行解释;
# 6.因子旋转，如果不好解释，进行因子旋转,然后进行解释。解释可结合fa.diagram函数对载荷矩阵进行可视化
# 7.求因子得分

##**************************

#************************
#为研究某地区的综合发展状况，收集了该地区20年经济发展、社会状况等方#面的统计数据，包括总人口数（x1）、GDP（x2）、全社会固定资产投资额(x3)、城市化水平(x4)、人均居住面积(x5)、客运量(x6)共6个变量。
#********************************************

###### 3. 主成分分析#####

### (1) 变量间应具有较强的相关关系。
##经验地，若矩阵中大部分相关系数的绝对值大于0.3，则表示存在一定程度的相关性，可进一步依此构造因子变量。

EcoData <- read.table(file = "EcoData.txt", header = TRUE)
RMatrix <- cor(EcoData)

library(corrplot)
corrplot.mixed(RMatrix, upper = "ellipse")

### (2) 主成分分析法
##对x1,x2,x3,x4,x5,x6采用主成分分析法实施变量降维

RMatrix <- cor(EcoData)
Result <- eigen(RMatrix)#eigen函数计算指定矩阵的特征值和特征向量，结果分别存储在values和vectors的列表成分中。

##绘制各主成分的方差变化折线图
plot(Result$values, type = "b", 
     ylab = "特征值(主成分方差)", 
     xlab = "特征值编号(主成分编号)")
(U <- as.matrix(Result$vectors[, 1:2]))

##在原有变量经过标准化处理后计算主成分得分
Y <- as.matrix(scale(EcoData)) %*% U
plot(Y, xlab="第一主成分", ylab="第二主成分", 
     main="基于主成分的观测样本")

### (3) 利用函数进行主成分分析
EcoData <- read.table(file = "EcoData.txt", header = TRUE)
pca <- princomp(x = EcoData, cor = TRUE)
pca$loadings #loadings的成分中存储着主成分系数矩阵
pca$scores[, 1:2] #存储着各主成分上的得分


#### 4. 因子分析原理 ####
###不用包，一步步实现来解释(PCA法操作)

### (1) 利用主成分分析法计算因子载荷矩阵
EcoData <- read.table(file = "EcoData.txt", header = TRUE)
RMatrix <- cor(EcoData)
Result <- eigen(RMatrix)

lambda <- Result$values 
vectors <- Result$vectors

A <- NULL
for(i in 1:6){
  f <- sqrt(Result$values[i]) * Result$vectors[, i]
  A <- cbind(A, f)
}
colnames(A) <- paste("f", 1:6, sep = "")
A

### (2)判断因子变量个数k
Result$values
(cR <- cumsum(Result$values) / sum(Result$values))
#第一个因子变量的方差贡献(特征值)为5.57，方差贡献率为93%。

##绘制累计方差贡献率的折线图
plot(cR, type = "b", 
     xlab = "因子变量编号",
     ylab = "累计方差贡献率",
     main = "因子变量的累计方差贡献率")
A[, 1:2] #取两个因子变量的因子载荷矩阵

### (3) 原有变量的变量共同度
h2 <- vector(length = 6)
for(i in 1:6){ 
  h2[i] = round(sum(A[i, 1:2] ^ 2), 2)
}
cbind(A[, 1:2], h2)
#两个因子变量对原有变量信息的解释程度都很高，信息丢失很少，因子分析 的效果很好。


##### 5. 构造因子变量#####

### (1) 利用函数principal()采用主成分分析法
### 对x1,x2,x3,x4,x5,x6基于主成分分析法计算因子载荷矩阵

## psych包提供的principal函数：
## principal(r=相关系数矩阵名,nfactors=因子变量个数,rotate="none")
## 返回结果为列表，主要包括三个名为values,loadings,communality的成分，分别存储特征值、因子载荷矩阵和各变量的共同度等计算结果。

library("psych")
EcoData <- read.table(file = "EcoData.txt", header = TRUE)
RMatrix <- cor(EcoData)
(pc <- principal(r = RMatrix, nfactors = 2, rotate = "none"))

## PC1，PC2两列分别为因子载荷矩阵的元素；h2列为各变量的共同度；u2列为特殊因子的方差。
## SS loadings行分别为第一、第二个因子变量的方差贡献；
## Proportion Var行为两个因子变量的方差贡献率;
## Cumulative Var为累计方差贡献率;
## Porportion Explained为两个因子变量的方差贡献占总方差贡献的比例；
## Cumulative Proportion为累计比率。

### (2) 利用函数fa()采用主轴因子法
### 对x1,x2,x3,x4,x5,x6基于主轴因子法计算因子载荷矩阵

fa <- fa(r = RMatrix, nfactors = 2, fm = "pa", rotate = "none")

##绘制碎石图（主成分法和主轴因子法的碎石图）
scree(rx = RMatrix, factors = TRUE, pc = TRUE, 
      main = "基于主成分法和主轴因子法的碎石图")
##factors = TRUE, pc = TRUE分别表示显示基于主成分法和主轴因子法的碎石图

#### 6. 因子变量的命名 ####

### (1) 绘制因子载荷图
### 利用包psych中的factor.plot函数对因子分析或主成分分析的结果绘制因子载荷图

EcoData <- read.table(file = "EcoData.txt", header = TRUE)
RMatrix <- cor(EcoData)
library("psych")
pc <- principal(RMatrix, nfactors = 2, rotate = "none")
fa <- fa(RMatrix, nfactors = 2, fm = "pa", rotate = "none")
par(mfrow = c(1, 2))
factor.plot(pc, label = rownames(pc$loadings))
factor.plot(fa, label = rownames(fa$loadings))


### (2) 实施因子旋转
varimax(x = pc$loadings)
varimax(x = fa$loadings)

#***************************
# Loadings:   #旋转后的因子载荷矩阵
#      RC1   RC2   
# X1 0.882 0.457
# X2 0.491 0.869
# X3 0.484 0.874
# X4 0.784 0.600
# X5 0.855 0.502
# X6 0.708 0.665
#
#                  RC1   RC2
# SS loadings    3.100 2.780 #旋转后的两因子的方差贡献,发生了变化
# Proportion Var 0.517 0.463
# Cumulative Var 0.517 0.980
#
#********************************************

library("GPArotation")
(pc <- principal(RMatrix, nfactors = 2, rotate = "varimax"))
library("MASS")
fa <- fa(RMatrix, nfactors = 2, fm = "pa", rotate = "varimax")
par(mfrow = c(2, 2))
factor.plot(pc, label = rownames(pc$loadings))
factor.plot(fa, label = rownames(fa$loadings))
fa.diagram(pc, simple = TRUE) #绘制因子结果图
fa.diagram(fa, simple = TRUE)
#simple=TRUE,表示只给出对原有变量有最大因子载荷的因子变量。

### (3) 计算因子得分
## principal函数中的参数：
## score=TRUE，表示计算因子得分;
## method = "regression",表示采用回归法估计因子值系数，返回到名为weight的列表成分中。

pc <- principal(RMatrix, nfactors = 2, rotate = "varimax",
                scores = TRUE, method = "regression")
pc$weight
fa <- fa(RMatrix, nfactors = 2, fm = "pa",
         rotate = "varimax", scores = "regression")
fa$weight

pcFS <- as.matrix(scale(EcoData)) %*% pc$weight
faFS <- as.matrix(scale(EcoData)) %*% fa$weight
par(mfrow = c(2, 1))
plot(pcFS, main = "基于主成分分析法的因子得分",
     xlab = "第一个因子变量", ylab = "第二个因子变量")
plot(faFS, main = "基于主轴因子法的因子得分",
     xlab = "第一个因子变量", ylab = "第二个因子变量")


library(psych)
EcoData <- read.csv(file = "fiance.csv", header = TRUE)
EcoData <- EcoData[, -13]
RMatrix <- cor(EcoData[, c(3:12)])
pc <- principal(RMatrix, nfactors = 3, rotate = "none")
