# Generated with SMOP  0.41-beta
from libsmop import *
# PF.m

    
@function
def PF(*args,**kwargs):
    varargin = PF.varargin
    nargin = PF.nargin

    # Just call PF (without any arguments) to run the animation
# 
# This is the matlab code behind the movie "Particle Filter Explained
# without Equations", which can be found at http://youtu.be/aUkBa1zMKv4
# Written by Andreas Svensson, October 2013
# Updated by Andreas Svensson, February 2013, fixing a coding error in the
# 'propagation-update' of the weights
# andreas.svensson@it.uu.se
# http://www.it.uu.se/katalog/andsv164
# 
# The code is provided as is, and I take no responsibility for what this
# code may do to you, your computer or someone else.
    
    # This code is licensed under a
# Creative Commons Attribution-ShareAlike 3.0 Unported License.
# http://creativecommons.org/licenses/by-sa/3.0/
    
    ################################
### Setup and initialization ###
################################
    
    # Setting the random seed, so the same example can be run several times
    s=RandStream('mt19937ar','Seed',1)
# PF.m:24
    RandStream.setGlobalStream(s)
    # Some unceratinty parameters
    measurementNoiseStdev=0.1
# PF.m:28
    speedStdev=1
# PF.m:28
    # Speed of the aircraft
    speed=1
# PF.m:31
    # Set starting position of aircraft
    planePosX=- 25
# PF.m:33
    planePosY=4
# PF.m:33
    # Some parameters for plotting the particles
    m=1000
# PF.m:36
    k=0.0001
# PF.m:36
    # Number of particles
    N=200
# PF.m:39
    # Some variables for plotting
    plotVectorSea=arange(- 10,10,0.01)
# PF.m:42
    plotVectorMountains=concat([arange(- 40,- 10.01,0.01),arange(10.01,40,0.01)])
# PF.m:43
    plotHeight=5
# PF.m:44
    # The function describing the ground
    ground=lambda x=None: multiply((x >= 10),(multiply((1 - (x - 10) / 30),sin(x - 10)) + multiply(((x - 10) / 30),sin(dot(1.5,(x - 10)))) + multiply(multiply(0.2,(x - 10)),(x <= 20)) + dot(2,(x > 20)))) + multiply((x <= - 10),(multiply((1 - (- x - 10) / 30),sin(- x - 10)) + multiply(((- x - 10) / 30),sin(dot(1.5,(- x - 10)))) + multiply(multiply(0.2,(- x - 10)),(x >= - 20)) + dot(2,(x < - 20))))
# PF.m:47
    # Plot the environment
    area(plotVectorMountains,ground(plotVectorMountains),- 1,'FaceColor',concat([0,0.6,0]))
    set(gca,'XTick',[])
    set(gca,'YTick',[])
    hold('on')
    area(plotVectorSea,ground(plotVectorSea),- 1,'FaceColor',concat([0,0,0.8]))
    axis(concat([- 40,40,- 1,10]))
    plane=plotPlane(planePosX,planePosY,1)
# PF.m:54
    measurementLine=line(concat([planePosX,planePosX]),concat([ground(planePosX),planePosY]),'Color',concat([1,0,0]),'LineStyle',':')
# PF.m:55
    pause(1)
    #######################
### Begin filtering ###
#######################
    
    # Generate particles
    particles=dot(rand(N,1),80) - 40
# PF.m:64
    # Plot particles
    particleHandle=scatter(particles,plotHeight(ones(size(particles))),dot(m,(dot(1 / N,ones(N,1)) + k)),'k','filled')
# PF.m:67
    pause(1)
    FirstRun=1
# PF.m:70
    # Initialize particle weights
    w=dot(1 / N,ones(N,1))
# PF.m:73
    for t in arange(1,60).reshape(-1):
        # Generate height measurements (with gaussian measurement noise)
        planeMeasDist=planePosY - ground(planePosX) + dot(randn,measurementNoiseStdev)
# PF.m:77
        w=multiply(w,(dot(1 / (dot(sqrt(dot(2,pi)),measurementNoiseStdev)),exp(- ((planePosY - ground(particles)) - planeMeasDist) ** 2 / (dot(2,measurementNoiseStdev ** 2))))))
# PF.m:80
        w=w / sum(w)
# PF.m:83
        if FirstRun:
            # Sort out some particles to evaluate them "in public" the first
        # run (as in the movie)
            __,order=sort(w,'descend',nargout=2)
# PF.m:89
            pmax=order(1)
# PF.m:90
            pmaxi=setdiff(arange(1,N),pmax)
# PF.m:91
            delete(particleHandle)
            particleHandle=scatter(concat([[particles(pmaxi)],[particles(pmax)]]),plotHeight(ones(size(particles))),dot(m,(concat([[ones(N - 1,1) / N],[w(pmax)]]) + k)),'k','filled')
# PF.m:93
            pause(1)
            pmax2=order(2)
# PF.m:96
            pmaxi2=setdiff(pmaxi,pmax2)
# PF.m:97
            delete(particleHandle)
            particleHandle=scatter(concat([[particles(pmaxi2)],[particles(pmax)],[particles(pmax2)]]),plotHeight(ones(size(particles))),dot(m,(concat([[ones(N - 2,1) / N],[w(pmax)],[w(pmax2)]]) + k)),'k','filled')
# PF.m:99
            pause(1)
            # Plot all weighted particles
            delete(particleHandle)
            particleHandle=scatter(particles,plotHeight(ones(size(particles))),dot(m,(w + k)),'k','filled')
# PF.m:104
            pause(1)
        # Resample the particles
        u=rand(N,1)
# PF.m:109
        wc=cumsum(w)
# PF.m:109
        __,ind1=sort(concat([[u],[wc]]),nargout=2)
# PF.m:110
        ind=find(ind1 <= N) - (arange(0,N - 1)).T
# PF.m:110
        particles=particles(ind,arange())
# PF.m:111
        w=ones(N,1) / N
# PF.m:111
        delete(particleHandle)
        particleHandle=scatter(particles,plotHeight(ones(size(particles))),dot(m,(w + k)),'k','filled')
# PF.m:114
        pause(1)
        # Time propagation
        speedNoise=dot(speedStdev,randn(size(particles)))
# PF.m:118
        particles=particles + speed + speedNoise
# PF.m:119
        # w = w, since the update in the previous step is done using our motion model, so the
    # information is already contained in that update.
        # Move and plot moved aircraft
        planePosX=planePosX + speed
# PF.m:126
        delete(plane)
        delete(measurementLine)
        plane=plotPlane(planePosX,planePosY,1)
# PF.m:128
        measurementLine=line(concat([planePosX,planePosX]),concat([ground(planePosX),planePosY]),'Color',concat([1,0,0]),'LineStyle',':')
# PF.m:129
        if FirstRun:
            # Plot updated particles
            delete(particleHandle)
            particleHandle=scatter(particles,plotHeight(ones(size(particles))),dot(m,(w + k)),'k','filled')
# PF.m:134
            pause(1)
        FirstRun=0
# PF.m:138
    
    return
    
if __name__ == '__main__':
    pass
    
    
@function
def plotPlane(xpos=None,ypos=None,fignr=None,*args,**kwargs):
    varargin = plotPlane.varargin
    nargin = plotPlane.nargin

    figure(fignr)
    X=xpos - 0.6 + concat([- 1,- 0.1,- 0.09,0.3,0.7,0.8,0.7,0.3,- 0.09,- 0.1,- 1])
# PF.m:145
    Y=ypos + concat([- 0.05,- 0.05,- 0.4,- 0.05,- 0.05,0,0.05,0.05,0.4,0.05,0.05])
# PF.m:146
    h=fill(X,Y,'k')
# PF.m:147
    return h
    
if __name__ == '__main__':
    pass
    