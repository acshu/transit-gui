# -*- coding: utf-8 -*-
#Python 2.7.3
#

from numpy import radians,degrees,pi,sin,cos,arcsin,arctan,inf,zeros,log
from numpy import arccos as acos
from numpy import arcsin as asin
from scipy import sqrt
from scipy.integrate import quad
from copy import copy

# Calculates lightcurve using the input parameters(see below); default number of dots(iterations) on the LC is 150;

def transit(A,Rs,Rp,Tp,Ts,i,u,iterations=150):

        #Preliminary calculations
    rs=Rs/A             #Relative stelar radius
    rp=Rp/A             #Relative planetary radius
    n=rp/rs             #radius ratio
    k=(Tp/Ts)**4

    print '---------------------------------------------------------'
    print 'rs= ', rs
    print 'rp= ', rp
    print ''
        #Inclination limits
    i1=acos(rs+rp)
    print 'i1= ',i1*180/pi
    i2=acos(rs-rp)
    print 'i2= ',i2*180/pi
    i5=acos(rp)
    print 'i5= ',i5*180/pi
    print ''
        #Phase limits
    f1= (1/(2*pi))*arcsin(sqrt((rs+rp)**2 -cos(i)**2)/sin(i))
    print 'f1= ',f1
    f2= (1/(2*pi))*arcsin(sqrt((rs-rp)**2 - cos(i)**2)/sin(i))
    print 'f2= ',f2
    f4= (1/(2*pi))*acos( rp/cos(i) )
    print 'f4= ',f4
    f6= (1/(2*pi))*arcsin(sqrt(rp**2 - cos(i)**2)/sin(i))
    print 'f6= ',f6
    f5= (1/(2*pi))*arctan(cos(i))
    print 'f5= ',f5
    print ''

    #Defining phases btw 0 and f1
    phases=[]
    phases.append(float(0))
    count=1
    while count <= iterations:
        phases.append(count*(f1-f1/iterations)/iterations)
        count=count+1
    phases.append(f1)
    phases.append(f1+f1/iterations)

    #print phases
    #print mag

    int1 = lambda q,rs,b,x0,y0,rp : (1-u+u*sqrt(1-(q/rs)**2))*q*(acos((x0*(b**2 + q**2 - rp**2) - y0*sqrt(4*b**2*q**2 - (b**2 + q**2 - rp**2)**2))/(2*b**2*q)) - acos((x0*(b**2 + q**2 - rp**2) + y0*sqrt(4*b**2*q**2 - (b**2 + q**2 - rp**2)**2))/(2*b**2*q)))
    int2 = lambda q,rs,b,x0,y0,rp : (1-u+u*sqrt(1-(q/rs)**2))*q*(acos((x0*(b**2 + q**2 - rp**2) - y0*sqrt(4*b**2*q**2 - (b**2 + q**2 - rp**2)**2))/(2*b**2*q)) + acos((x0*(b**2 + q**2 - rp**2) + y0*sqrt(4*b**2*q**2 - (b**2 + q**2 - rp**2)**2))/(2*b**2*q)))
    int3 = lambda q,rs,b,x0,y0,rp : (1-u+u*sqrt(1-(q/rs)**2))*q*( ((2)*pi) - acos(abs((x0*(b**2 + q**2 - rp**2) + y0*sqrt(4*b**2*q**2 - (b**2 + q**2 - rp**2)**2))/(2*b**2))/q ) + acos(abs((x0*(b**2 + q**2 - rp**2) - y0*sqrt(4*b**2*q**2 - (b**2 + q**2 - rp**2)**2))/(2*b**2))/q ) )
    int4 = lambda q,rs,b,x0,y0,rp : (1-u+u*sqrt(1-(q/rs)**2))*q*( pi + acos(abs((x0*(b**2 + q**2 - rp**2) + y0*sqrt(4*b**2*q**2 - (b**2 + q**2 - rp**2)**2))/(2*b**2))/q ) + acos(abs((x0*(b**2 + q**2 - rp**2) - y0*sqrt(4*b**2*q**2 - (b**2 + q**2 - rp**2)**2))/(2*b**2))/q ) )
    #int5 = lambda q,rs,b,x0,y0,rp : (1-u+u*sqrt(1-(q/rs)**2))*q*( ((2)*pi) - acos(abs((x0*(b**2 + q**2 - rp**2) + y0*sqrt(4*b**2*q**2 - (b**2 + q**2 - rp**2)**2))/(2*b**2))/q ) - acos(abs((x0*(b**2 + q**2 - rp**2) - y0*sqrt(4*b**2*q**2 - (b**2 + q**2 - rp**2)**2))/(2*b**2))/q ) )

    intResults=[]
    mag=[]

    if i > i1 and i <= i2:
        print '   Using Cycle 1',' i= ',degrees(i)
        for ph in phases:
            if ph >= 0 and ph < f1:
                #calculating variable coefficients
                x0=sin(2*pi*ph)
                y0=cos(i)*cos(2*pi*ph)
                b=sqrt(x0**2 + y0**2) 
                qmin=b-rp
                qmax=rs                    
                #print x0,' ',y0,' ',b,' ',qmin,qmax
                if y0 >= rp: 
                    integr=int1
                else:
                    integr=int2

                intResult,err=quad(integr,qmin,qmax,args=(rs,b,x0,y0,rp,))
                mag.append( 1-(-2.5 *log(1-intResult/(pi*(k*rp**2 +rs**2 *(1-u/3) ) ) ))   )
            else:
                mag.append(float(1))


    if i>i2 and i <= i5:
        print '   Using Cycle 2',' i= ',degrees(i)
        for ph in phases:
            if ph >= 0 and ph < f1:
                #calculating variable coefficients
                x0=sin(2*pi*ph)
                y0=cos(i)*cos(2*pi*ph)
                b=sqrt(x0**2 + y0**2) 
                if ph <= f2: 
                    qmin=b-rp
                    qmax=b+rp
                    if y0 >= rp: 
                        integr=int1
                        intResult,err=quad(integr,qmin,qmax,args=(rs,b,x0,y0,rp,))
                    else:
                        q1=x0+sqrt(rp**2 - y0**2)
                        q2=x0-sqrt(rp**2 - y0**2)
                        print 'qmin= ',qmin, ' qmax= ',qmax                   
                        print 'q2= ',q2, ' q1= ',q1                    
                        j1,err=quad(int1,qmin,q2,args=(rs,b,x0,y0,rp,))
                        j2,err=quad(int2,q2,q1,args=(rs,b,x0,y0,rp,))
                        j3,err=quad(int1,q1,qmax,args=(rs,b,x0,y0,rp,))
                        intResult=(j1+j2+j3)
                        print 'ph= ',ph
                        #print j1,j2,j3, intResult
                        #print ''
                else:
                    qmin=b-rp
                    qmax=rs
                    #q2=x0-sqrt(rp**2 - y0**2)
                    #if q2 >= rs: 
                    integr=int1
                    intResult,err=quad(integr,qmin,qmax,args=(rs,b,x0,y0,rp,))
                    #print x0,' ',y0,' ',b,' ',qmin,qmax
                    #print intResult

                mag.append( 1-(-2.5 *log(1-intResult/(pi*(k*rp**2 +rs**2 *(1-u/3) ) ) ))   )
            else:
                mag.append(float(1))
                 
    if i > i5 and i <= radians(90):
        print '   Using Cycle 3','i= ',degrees(i)#    for ph in phases:
        if f5 < f6:
            limit1=f5
            limit2=f6
        else:
            limit1=f6
            limit2=0          
        print 'limit1= ', limit1,'limit2= ', limit2
        print ''  
        for ph in phases:
            if ph >= 0 and ph < f1:
                x0=sin(2*pi*ph)
                y0=cos(i)*cos(2*pi*ph)
                b=sqrt(x0**2 + y0**2)

                if ph< limit1:
                    q1=sqrt(rp**2 - y0**2)+x0
                    q4=sqrt(rp**2 - y0**2)-x0                                
                    q2=sqrt(rp**2 - x0**2)+y0
                    q3=sqrt(rp**2 - x0**2)-y0
                    #print 'ph = ',ph
                    #print 'b= ',b
                    #print 'x0= ',x0,'  y0= ',y0
                    #print 'rp= ',rp, ' b= ',b
                    #print 'rp-b= ',(rp-b)
                    #print 'q3= ',q3, ' q4= ',q4
                    #print 'q2= ',q2, ' q1= ',q1
                    j1,err=quad(lambda q : 2*pi*q*(1-u+u*sqrt(1-(q/rs)**2)) ,0,(rp-b))
                    j2,err=quad(int3,(rp-b),q3,args=(rs,b,x0,y0,rp,))
                    j3,err=quad(int4,q3,q4,args=(rs,b,x0,y0,rp,))                
                    j4,err=quad(int2,q4,q1,args=(rs,b,x0,y0,rp,))
                    j5,err=quad(int1,q1,(rp+b),args=(rs,b,x0,y0,rp,))
                    intResult=(j1+j2+j3+j4+j5)
                    #print 'rp-b= ', rp-b
                    #print '_ph= ',ph
                    #print j1,j2,j3,j4,j5, intResult
                    #print ''

                elif ph < limit2:
                    q1=sqrt(rp**2 - y0**2)+x0
                    q3=sqrt(rp**2 - x0**2)-y0
                    q4=sqrt(rp**2 - y0**2)-x0
     
                    j1,err=quad(lambda q : 2*pi*q*(1-u+u*sqrt(1-(q/rs)**2)) ,0,(rp-b))
                    j2,err=quad(int3,(rp-b),q4,args=(rs,b,x0,y0,rp,))
                    #j3,err=quad(int5,q4,q3,args=(rs,b,x0,y0,rp,))
                    j4,err=quad(int2,q4,q1,args=(rs,b,x0,y0,rp,))
                    j5,err=quad(int1,q1,(rp+b),args=(rs,b,x0,y0,rp,))
                    intResult=(j1+j2+j4+j5)
                    #print 'ph= ',ph
                    #print j1,j2,j4,j5, intResult
                    #print 'x0= ',x0
                    #print 'y0= ',y0 
                    #print 'b=  ',b                   
                    #print 'rp-b= ', rp-b
                    #print ''

                else: # f6<= ph <f1
                    qmin=b-rp
                    if ph <=f2: #f6<= ph <=f2
                        qmin=b-rp
                        qmax=b+rp
                        if y0 >= rp: 
                            integr=int1
                            intResult,err=quad(integr,qmin,qmax,args=(rs,b,x0,y0,rp,))
                        else:
                            q1=x0+sqrt(rp**2 - y0**2)
                            q2=x0-sqrt(rp**2 - y0**2)
                            #print 'qmin= ',qmin, ' qmax= ',qmax                   
                            #print 'q2= ',q2, ' q1= ',q1                    
                            j1,err=quad(int1,qmin,q2,args=(rs,b,x0,y0,rp,))
                            j2,err=quad(int2,q2,q1,args=(rs,b,x0,y0,rp,))
                            j3,err=quad(int1,q1,qmax,args=(rs,b,x0,y0,rp,))
                            intResult=(j1+j2+j3)
                            #print 'ph= ',ph
                            #print j1,j2,j3, intResult
                            #print ''
                    else:   #f2 < ph < f1
                        qmin=b-rp
                        qmax=rs
                        if y0 >= rp:
                            integr=int1
                            intResult,err=quad(integr,qmin,qmax,args=(rs,b,x0,y0,rp,))
                        else:                            
                            q2=x0-sqrt(rp**2 - y0**2)
                            if q2 >= rs:
                                #print '_ph= ',ph
                                #print 'x0= ',x0,'  y0= ',y0,                             
                                integr=int1
                                intResult,err=quad(integr,qmin,qmax,args=(rs,b,x0,y0,rp,))
                            else:
                                q1=x0+sqrt(rp**2 - y0**2)
                                if q1 < qmax:
                                    q1=x0+sqrt(rp**2 - y0**2)
                                    q2=x0-sqrt(rp**2 - y0**2)
                                    #print 'qmin= ',qmin, ' qmax= ',qmax                   
                                    #print 'q2= ',q2, ' q1= ',q1                    
                                    j1,err=quad(int1,qmin,q2,args=(rs,b,x0,y0,rp,))
                                    j2,err=quad(int2,q2,q1,args=(rs,b,x0,y0,rp,))
                                    j3,err=quad(int1,q1,qmax,args=(rs,b,x0,y0,rp,))
                                    intResult=(j1+j2+j3)
                                    #print 'ph= ',ph
                                    #print j1,j2,j3, intResult
                                    #print ''
                                else:                                
                                    #print 'ph= ',ph
                                    #print 'x0= ',x0,'  y0= ',y0,
                                    #print 'qmin(b-rp)= ',qmin, ' qmax(rs)= ',qmax                   
                                    #print 'q2= ',q2, ' q1= ',q1  
                                    #print 'q2( x0-sqrt(rp**2 - y0**2) )= ',q2
                                    #print ''
                                    j1,err=quad(int1,qmin,q2,args=(rs,b,x0,y0,rp,))
                                    j2,err=quad(int2,q2,qmax,args=(rs,b,x0,y0,rp,))
                                    intResult=(j1+j2)
                                    #print j1,j2, intResult
                                    #print ''                                                           

                mag.append( 1-(-2.5 *log(1-intResult/(pi*(k*rp**2 +rs**2 *(1-u/3) ) ) ))   )
            else:
                mag.append(float(1))

    rev_mag=copy(mag)
    rev_mag.reverse()
    rev_phases=copy(phases)
    count=0
    while count < len(rev_phases):
        rev_phases[count]= -rev_phases[count]
        count=count+1
    rev_phases.reverse()

    all_phases=rev_phases+phases
    all_mag=rev_mag+mag

    return all_phases, all_mag