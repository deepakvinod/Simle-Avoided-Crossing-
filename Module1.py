import numpy as np
import RK4
import InitPos as guass
import Dual_avoided_crossing as PE
import Verlet_Velocity as vv
import matplotlib.pyplot as plt


mp =1                                                       #mass of particle
dt = 1                                                      # time step
alpha = 0.25; sigr = np.sqrt(1/(2*alpha)); r0 =-7; n = 10   # gauss distrubution 
g = 0                                                       # ground state
e =1
                                                            # excited state
V = PE.Vmatrix
H = PE.dHmatrix
d = PE.dmatrix

P0av =[]
P1av =[]
for j in range (n):                                       # loop for each trajectory  
     x = []
     v = []
     a = []
     t = []
     P0 =[]
     P1 =[]
     norm =[]
# itial conditions
     Co = np.array([1,0])
     
     x.append(np.random.choice(guass.ipos(r0,sigr,n)))     
     v.append(10/2000)
     P0.append(1)
     P1.append(0)
     surface = e                                                      
     KE = 0.5*mp*(v[0]**2)
     a.append(vv.accel(x[0],surface,V,H))
     t.append(0)
     k =0
     norm.append(1)

#loop will be replaced/scrapped later
     
     for m in range(1,3000):
          xi = x[m-1] 
          vi = v[m-1]
          ti = t[m-1]

# final conditiona
          tf = t[m-1]+dt
          xf =vv.verlet_pos(xi,vi,dt,k,V,H)
          vf =vv.verlet_vel(xi,xf,vi,dt,k,V,H)
          x1_2 = vv.verlet_pos(xi,vi,dt/2,k,V,H)
          v1_2 =vv.verlet_vel(xi,x1_2,vi,dt/2,k,V,H)
          C0 = RK4.Ck(Co,xi,x1_2,xf,vi,v1_2,vf,0,dt,V,d)
          C1 = RK4.Ck(Co,xi,x1_2,xf,vi,v1_2,vf,1,dt,V,d)
          Co = np.array([C0,C1])
          p0 = C0.real**2+C0.imag**2
          p1 = C1.real**2+C1.imag**2
          norm.append( p0+p1)
          P0.append(p0)
          P1.append(p1)
          x.append(xf)
          v.append(vf)
          t.append(tf)

     # here I have v and d so I can calculate electronic dynamics and then hoping
     #     RK4.RK4()
     
     
          #if x[m] > 10:
               #break
          #elif x[m] < -10:
               #break
     #plt.figure(1)
     #plt.subplot(212)
     #plt.plot(x,t,label='x_%i' % j)
     #plt.xlabel('x')
     #plt.ylabel('t')
     #plt.figure(1)
     #plt.subplot(211)
     
     if j == 0:
          P0av = P0
          P1av = P1
     else:
          for i in range(len(P0)):
               P0av[i] = P0av[i]+P0[i]
               P1av[i]=P1av[i]+P1[i]
for i in range(len(P0av)):
     P0av[i]=P0av[i]/n
     P1av[i] = P1av[i]/n

     
plt.plot(t,P0av,label='P0')
plt.plot(t,P1av,label ='P1')
#plt.plot(t,norm)
#plt.legend()
plt.ylabel('Probability')
    
     





plt.show()
    



