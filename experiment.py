import matplotlib.pyplot as plt
import numpy as np

em_extra = 187
atk_extra = 0.466

e_db = 0.466+0.48
q_db = 0.466+0.12

b = 948
c = 1447*1.15

def pd_atk(value):
    em = value[1] + em_extra
    e = b*5.1192*(1+e_db+0.0015*em)
    q = b*22.7061*(1+q_db+0.0015*em)
    return 7*e+q

def pd_em(value):
    atk = value[0] + atk_extra
    em = value[1] + em_extra
    e = 0.0015*(5.1192*(b*(1+atk)+311)+c*(1+5*em/(1200+em)))+c*6000/((em+1200)**2)*(1+e_db+0.0015*em)
    q0 = 0.0015*(4.68*(b*(1+atk)+311)+c*(1+5*em/(1200+em)))+c*6000/((em+1200)**2)*(1+q_db+0.0015*em)
    q1 = 0.0015*(6.0087*(b*(1+atk)+311)+c*(1+5*em/(1200+em)))+c*6000/((em+1200)**2)*(1+q_db+0.0015*em)
    return 7*e+q0+q1*3

n = 30
x, y = np.meshgrid(np.arange(0, n*19.82), np.arange(0, n*0.0496, 0.0496/19.82))
w = x.shape[1]
h = x.shape[0]
x, y = x.flatten(), y.flatten()
print(h,w)

pa = pd_atk(np.vstack([y, x]))*0.0496
pe = pd_em(np.vstack([y, x]))*19.82
# print(pa-pe)
mask = (pa > pe).astype(int).reshape(h,w)
# mask = np.vstack((mask, np.zeros((h,w))))
# print(np.all(mask==1))
plt.imshow(np.flipud(mask.reshape(h,w)), cmap='gray')
plt.xlabel("em")
plt.ylabel("percentage ATK")
plt.show()

