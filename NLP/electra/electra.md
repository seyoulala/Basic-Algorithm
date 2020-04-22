### ELECTRA: PRE-TRAINING TEXT ENCODERS AS DISCRIMINATORS RATHER THAN GENERATORS



### abstract

electra在pretraning的阶段不是和之前bert之类的model使用MLM来predict被mask掉的token,而是引入了GAN中的思想，首先使用一个小型的生成网络来生成一些token来替换掉原始的sentence中的一些token，然后不像MLM中去predict这个被mask掉的token，而是训练一个判别器去判断sentence中的token是否被生成器中生成的样本进行了替换。

