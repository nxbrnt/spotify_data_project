#Imports here for writefile magic only. Not Pythonic.
import seaborn as sns
import matplotlib.pyplot as plt

#explain blurred markers lets markers blend without weird edge artifacts
#looks very similar to a kde spikeplot with gaussian kernel and very small
#kernel bandwidth. implemented that with nearly identical results but a
#factor of 30 slower.

def smooth_scatterplot(data, xcol, ycol, color=True, alpha=.03, size=1, 
                       ax=None, xlabel=None, ylabel=None, title=None):
    """Generates a simple scatter plot with blurred markers 
    and alpha blended colors."""
    
    if ax is None:
        ax = plt.gca()
    
    #Shuffle rows so different colored points are layered at random
    df_temp = data[ [xcol, ycol, 'ds'] ].dropna().sample(frac=1)

    #Color via dataset: 'nix'=blue, 'top'=red.
    df_temp['color'] = df_temp.ds.map( { 'nix':(0,.475,1), 'top':(1,0,0) } )
    
    #Base size
    s0 = size

    if color:
        c=df_temp.color
    else:
        c = (0,0,0)

    for i in reversed( range(5) ):
        #Marker size
        s=(s0*(i+1))**2
        ax.scatter(df_temp[xcol], df_temp[ycol], c=c, s=s, alpha=alpha,
                        linewidths=0)
    if xlabel is None:
        xlabel = xcol.title()
    if ylabel is None:
        ylabel = ycol.title()
    if title is None:
        title = xcol.title() + ' vs. ' + ycol.title()
        
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    
    return ax