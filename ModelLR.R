setwd("D:/โปรเจค")

############################################
data <- read.csv("output1.csv")
head(data)
attach(data)

############################################
#แปลงข้อมูลให้เป็น dummy
SEX.f <- factor(SEX)
Injp.f <- factor(Injp)
Risk1.f <- factor(Risk1)
Risk2.f <- factor(Risk2)
Risk4.f <- factor(Risk4)
Risk5.f <- factor(Risk5)


############################################
#ตรวจสอบความเหมาะสมของดมเดล
library(lmtest)

fit <- glm(Dead ~ I(SEX.f==1) + AGE + I(Injp.f==2) + I(Injp.f==3) + I(Risk1.f==1) + I(Risk1.f==2) + I(Risk2.f==1) + I(Risk2.f==2) + I(Risk4.f==1) + I(Risk4.f==2) + I(Risk5.f==1) + I(Risk5.f==2) + Ais1 + Ais2 + Ais3 + Ais4 + Ais5 + Ais6 + GCS + SBP + RR + PR + Time + ISS + RTS + SBP_group + RR_group , data=data , family=binomial)
lrtest(fit) 
############################################
#หาสมการแรกที่ได้แบบตัดตัว
summary(fit)

############################################
fit2 <- glm(Dead ~ I(SEX.f==1) + AGE + I(Injp.f==2) + I(Risk1.f==1) + Ais2 + SBP + RR  + Time + ISS , data=data , family=binomial)
summary(fit2)

############################################
#สมการสุดท้าย
fit3 <- glm(Dead ~ I(SEX.f==1) + AGE + I(Risk1.f==1) + Ais2 + SBP + RR  + Time + ISS , data=data , family=binomial)
summary(fit3)

############################################
##หาค่า OR เพื่ออธิบายผล
exp(coef(fit3))

############################################
##ประเมินความแม่นยำ
pred = predict(fit3,data,type ="response")
pred = ifelse(pred >0.5 ,1,0)

table(data$Dead,pred)

acc = mean(pred == data$Dead)
print(paste('Accuracy = ' ,acc))
############################################
############################################
##ลองตัดทีล่ะตัว

fitt <- glm(Dead ~ I(SEX.f==1) + AGE + I(Injp.f==2) + I(Injp.f==3) + I(Risk1.f==1) + I(Risk1.f==2) + I(Risk2.f==1) + I(Risk2.f==2) + I(Risk4.f==1) + I(Risk4.f==2) + I(Risk5.f==1) + I(Risk5.f==2) + Ais1 + Ais2 + Ais3 + Ais4 + Ais5 + Ais6 + GCS + SBP + RR + PR + Time + ISS + RTS + SBP_group + RR_group , data=data , family=binomial)
summary(fitt)

##############################################
fitt2 <- glm(Dead ~ I(SEX.f==1) + AGE + I(Injp.f==2) + I(Injp.f==3) + I(Risk1.f==1) + I(Risk1.f==2) + I(Risk2.f==1) + I(Risk4.f==1) + I(Risk4.f==2) + I(Risk5.f==1) + I(Risk5.f==2) + Ais1 + Ais2 + Ais3 + Ais4 + Ais5 + Ais6 + GCS + SBP + RR + PR + Time + ISS + RTS + SBP_group + RR_group , data=data , family=binomial)
summary(fitt2)

##############################################
fitt3 <- glm(Dead ~ I(SEX.f==1) + AGE + I(Injp.f==2) + I(Injp.f==3) + I(Risk1.f==1) + I(Risk1.f==2) + I(Risk2.f==1) + I(Risk4.f==1) + I(Risk4.f==2) + I(Risk5.f==1) + I(Risk5.f==2) + Ais1 + Ais2 + Ais4 + Ais5 + Ais6 + GCS + SBP + RR + PR + Time + ISS + RTS + SBP_group + RR_group , data=data , family=binomial)
summary(fitt3)

##############################################
fitt4 <- glm(Dead ~ I(SEX.f==1) + AGE + I(Injp.f==2) + I(Injp.f==3) + I(Risk1.f==1) + I(Risk1.f==2) + I(Risk2.f==1) + I(Risk4.f==1) + I(Risk5.f==1) + I(Risk5.f==2) + Ais1 + Ais2 + Ais4 + Ais5 + Ais6 + GCS + SBP + RR + PR + Time + ISS + RTS + SBP_group + RR_group , data=data , family=binomial)
summary(fitt4)

##############################################
fitt5 <- glm(Dead ~ I(SEX.f==1) + AGE + I(Injp.f==2) + I(Injp.f==3) + I(Risk1.f==1) + I(Risk1.f==2) + I(Risk2.f==1) + I(Risk4.f==1) + I(Risk5.f==1) + I(Risk5.f==2) + Ais1 + Ais2 + Ais4 + Ais5 + Ais6 + GCS + SBP + RR + PR + Time + ISS + RTS + RR_group , data=data , family=binomial)
summary(fitt5)

##############################################
fitt6 <- glm(Dead ~ I(SEX.f==1) + AGE + I(Injp.f==2) + I(Injp.f==3) + I(Risk1.f==1) + I(Risk1.f==2) + I(Risk2.f==1) + I(Risk4.f==1) + I(Risk5.f==1) + Ais1 + Ais2 + Ais4 + Ais5 + Ais6 + GCS + SBP + RR + PR + Time + ISS + RTS + RR_group , data=data , family=binomial)
summary(fitt6)

##############################################
fitt7 <- glm(Dead ~ I(SEX.f==1) + AGE + I(Injp.f==2) + I(Injp.f==3) + I(Risk1.f==1) + I(Risk2.f==1) + I(Risk4.f==1) + I(Risk5.f==1) + Ais1 + Ais2 + Ais4 + Ais5 + Ais6 + GCS + SBP + RR + PR + Time + ISS + RTS + RR_group , data=data , family=binomial)
summary(fitt7)

##############################################
fitt8 <- glm(Dead ~ I(SEX.f==1) + AGE + I(Injp.f==2) + I(Injp.f==3) + I(Risk1.f==1) + I(Risk2.f==1) + I(Risk4.f==1) + I(Risk5.f==1) + Ais1 + Ais2 + Ais4 + Ais5 + GCS + SBP + RR + PR + Time + ISS + RTS + RR_group , data=data , family=binomial)
summary(fitt8)

##############################################
fitt9 <- glm(Dead ~ I(SEX.f==1) + AGE + I(Injp.f==2) + I(Injp.f==3) + I(Risk1.f==1) + I(Risk4.f==1) + I(Risk5.f==1) + Ais1 + Ais2 + GCS + SBP + RR + PR + Time + ISS + RTS + RR_group , data=data , family=binomial)
summary(fitt9)

##############################################
fitt10 <- glm(Dead ~ I(SEX.f==1) + AGE + I(Injp.f==2) + I(Injp.f==3) + I(Risk1.f==1) + I(Risk5.f==1) + Ais1 + Ais2 + GCS + SBP + RR + PR + Time + ISS + RTS + RR_group , data=data , family=binomial)
summary(fitt10)

##############################################
fitt11 <- glm(Dead ~ I(SEX.f==1) + AGE + I(Injp.f==2) + I(Injp.f==3) + I(Risk1.f==1) + I(Risk5.f==1) + Ais2 + GCS + SBP + RR + PR + Time + ISS + RTS + RR_group , data=data , family=binomial)
summary(fitt11)

##############################################
fitt12 <- glm(Dead ~ I(SEX.f==1) + AGE + I(Injp.f==2) + I(Injp.f==3) + I(Risk1.f==1) + I(Risk5.f==1) + Ais2 + SBP + RR + PR + Time + ISS + RTS + RR_group , data=data , family=binomial)
summary(fitt12)

##############################################
fitt13 <- glm(Dead ~ I(SEX.f==1) + AGE + I(Injp.f==2) + I(Injp.f==3) + I(Risk1.f==1) + Ais2 + SBP + RR + PR + Time + ISS + RTS + RR_group , data=data , family=binomial)
summary(fitt13)

##############################################
##หาค่า OR เพื่ออธิบายผล
exp(coef(fitt13))

##############################################
##ประเมินความแม่นยำ
pred2 = predict(fitt13,data,type ="response")
pred2 = ifelse(pred2 >0.5 ,1,0)

table(data$Dead,pred2)

acc = mean(pred2 == data$Dead)
print(paste('Accuracy = ' ,acc))























