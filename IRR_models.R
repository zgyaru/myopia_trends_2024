library(lme4)


data$pre_covid$stage = 'PreCOVID'
data$post_covid_1$stage = 'PostCOVID-1'
data$post_covid_2$stage = 'PostCOVID-2'

pre_post_1 = rbind(data$pre_covid, data$post_covid_1)
all_data = rbind(rbind(data$pre_covid, data$post_covid_1), data$post_covid_2)
all_data$stage = factor(all_data$stage,
                        levels = c('PreCOVID',
                                   'PostCOVID-1',
                                   'PostCOVID-2'))

num_id = 1:length(unique(all_data$idcard))
names(num_id) = unique(all_data$idcard)
all_data$numer_idcard = num_id[all_data$idcard]


model <- glmer(event ~ stage + age +grade+ studentSex +key+district+
                 (1 | numer_idcard),
               family = poisson(link = "log"),
               offset = log(off_time),
               data = all_data)

# 
print(summary(model))

coeff_matrix <- as.matrix(coef(summary(model)))


# 
colnames(coeff_matrix) <- c("Estimate", "Std.Error", "z.value", "p.value")
coeff_matrix = as.data.frame(coeff_matrix)
# 
coeff_matrix$Lower_CI <- exp(coeff_matrix$Estimate) - 1.96 * coeff_matrix$Std.Error
coeff_matrix$Upper_CI <- exp(coeff_matrix$Estimate) + 1.96 * coeff_matrix$Std.Error
coeff_matrix$IRR = exp(coeff_matrix$Estimate)



## first-grade
grade1 = all_data[which(all_data$grade == 1),]

model <- glmer(event ~ stage + age + studentSex +key+district+
                 (1 | numer_idcard),
               family = poisson(link = "log"),
               offset = log(off_time),
               data = grade1)

# 
print(summary(model))

coeff_matrix <- as.matrix(coef(summary(model)))
# 
colnames(coeff_matrix) <- c("Estimate", "Std.Error", "z.value", "p.value")
coeff_matrix = as.data.frame(coeff_matrix)
# 
coeff_matrix$Lower_CI <- exp(coeff_matrix$Estimate) - 1.96 * coeff_matrix$Std.Error
coeff_matrix$Upper_CI <- exp(coeff_matrix$Estimate) + 1.96 * coeff_matrix$Std.Error
coeff_matrix$IRR = exp(coeff_matrix$Estimate)




## stage-specific IRR
model1 <- glmer(event ~ age + grade + studentSex +key+district+
                  (1 | idcard),
                family = poisson(link = "log"),
                offset = log(off_time),
                data = data$post_covid_1)

# 
print(summary(model1))

coeff_matrix <- as.matrix(coef(summary(model1)))
coeff_matrix = as.data.frame(coeff_matrix)
colnames(coeff_matrix) <- c("Estimate", "Std.Error", "z.value", "p.value")
# 
coeff_matrix$Lower_CI <- exp(coeff_matrix$Estimate) - 1.96 * coeff_matrix$Std.Error
coeff_matrix$Upper_CI <- exp(coeff_matrix$Estimate) + 1.96 * coeff_matrix$Std.Error
coeff_matrix$IRR = exp(coeff_matrix$Estimate)
write.csv(coeff_matrix, 'E:/zyr/myopia/coef_myopiaRate_GLMER_stage1_20250107.csv')

model2 <- glmer(event ~ age + grade + studentSex +key+district+
                  (1 | idcard),
                family = poisson(link = "log"),
                offset = log(off_time),
                data = data$post_covid_2)

# 
print(summary(model2))
coeff_matrix <- as.matrix(coef(summary(model2)))
coeff_matrix = as.data.frame(coeff_matrix)
colnames(coeff_matrix) <- c("Estimate", "Std.Error", "z.value", "p.value")
#
coeff_matrix$Lower_CI <- exp(coeff_matrix$Estimate) - 1.96 * coeff_matrix$Std.Error
coeff_matrix$Upper_CI <- exp(coeff_matrix$Estimate) + 1.96 * coeff_matrix$Std.Error
coeff_matrix$IRR = exp(coeff_matrix$Estimate)



