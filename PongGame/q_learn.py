# import torch
# from torch import nn
# from torch.utils.data import DataLoader
# from torchvision import datasets
# from torchvision.transforms import ToTensor

# device = "cuda" if torch.cuda.is_available() else "cpu"
# print(f"Using {device} device")

# # Define model
# class QN(nn.Module):
#     def __init__(self):
#         super(QN, self).__init__()
#         self.flatten = nn.Flatten()
#         self.relu = nn.ReLU()
#         self.conv = nn.Conv2d(1,200,3,padding=1)

#     def forward(self, x):
#         x = self.flatten(x)
#         logits = self.linear_relu_stack(x)
#         return logits

# model = QN().to(device)
# print(model)













from random import *
# b_pos = [b_x,b_y] //小球的位置坐标
# iter=1000 迭代次数
# bar_pos = [x, center_y] 挡条中心坐标
# l 挡条长度
# up_pos = [x,center_y+l/2] 挡条上端坐标
# down_pos = [x,center_y-l/2] 挡条下端坐标
# w1=1.0,w2=1.0 近似函数参数，
# f1 -> 上端据小球距离，特征方程1
# f2 -> 上端据小球距离，特征方程1
# lr=0.1 学习率
# eplse = 0.8 探索（与利用率） （随学习过程降低）
# gamma=0.9 损失参数
class Q_Agent:
    w1 = -1.0
    w2 = 1.0
    iters = 10000
    lr = 0.1
    elpase = 0.8
    gamma = 1.0
    thresh = .001
    l = 200 #板长
    b_pos= []
    new_b_pos = []
    bar_pos = []
    new_bar_pos = []
    boundray = 1000
    def q_learn(self,rwd:float):
        # while self.iters>0:
        # print("rws:",rwd)
        # self.iters-=1
        Q_r = rwd+self.gamma*self.getQval(self.new_bar_pos)
        Q_appx = self.getQval(self.bar_pos)
        diff = Q_r - Q_appx
        # print('diff',diff,Q_r,Q_appx)
        # print("w1,w2:",self.w1,self.w2)
        if abs(diff) > self.thresh:
            # print("!!!!yes!!!!")
            self.w1 = self.w1 + self.lr*diff*self.f1([self.new_bar_pos[0],self.new_bar_pos[1]+self.l/2])
            self.w2 = self.w2 + self.lr*diff*self.f2([self.new_bar_pos[0],self.new_bar_pos[1]-self.l/2])
    def getAction(self):
        ind = random()
        if ind*10000<=self.iters+10:
            res = choice([-5,5,0])
            if res == 5:
                if self.bar_pos[1]+5+self.l/2 >=self.boundray:
                    self.new_bar_pos = [self.bar_pos[0],self.bar_pos[1]-5]
                    return -5
                else:
                    self.new_bar_pos = [self.bar_pos[0],self.bar_pos[1]+5]
            else:
                if self.bar_pos[1]-5-self.l/2 <=0:
                    self.new_bar_pos = [self.bar_pos[0],self.bar_pos[1]+5]
                    return 5
            self.new_bar_pos = [self.bar_pos[0],self.bar_pos[1]+res]
            return res
        else:
            # print("view:",self.boundray,self.bar_pos[1])
            if self.bar_pos[1]+5> self.boundray:
                # print("point1")
                self.new_bar_pos = [self.bar_pos[0],self.bar_pos[1]-5]
                return -5
            # print("view2:",self.boundray,self.bar_pos[1])
            if self.bar_pos[1]-5< 0:
                # print("point2")
                self.new_bar_pos = [self.bar_pos[0],self.bar_pos[1]+5]
                return 5
            tmp_up = [self.bar_pos[0],self.bar_pos[1]+5]
            tmp_down = [self.bar_pos[0],self.bar_pos[1]-5]
            up = self.getQval(tmp_up)
            down = self.getQval(tmp_down)
            still = self.getQval(self.bar_pos)
            # print("up&down:", up,down)
            if up > down and up > still:
                # print("point3")
                self.new_bar_pos = tmp_up
                return 5
            elif down > up and down > still:
                # print("point4")
                self.new_bar_pos = tmp_down
                return -5
            elif still > up and still > down:
                self.new_bar_pos = self.bar_pos
                return 0
            else:
                return choice([5,-5,0])
            
    
    def getQval(self,bar_pos:list):
        up_pos = [bar_pos[0],bar_pos[1]+self.l/2]
        down_pos = [bar_pos[0],bar_pos[1]-self.l/2]
        # if up_pos[1]>self.boundray or down_pos[1] <=0:
        #     return -10
        # else:
        return self.w1*self.f1(up_pos)+self.w2*self.f2(down_pos)
    def f1(self,up_pos:list):
        return pow(sum([(up_pos[i]-self.new_b_pos[i])**2 for i in range(2)]),0.5)/1000
    def f2(self,down_pos:list):
        return pow(sum([(down_pos[i]-self.new_b_pos[i])**2 for i in range(2)]),0.5)/1000
    def b_pos_update(self,b_pos:list):
        self.new_b_pos = b_pos
    # def bar_pos_update(self,bar_pos:list):
    #     self.bar_pos = bar_pos
# if __name__ == '__main__':
#     Q_Agent().q_learn()