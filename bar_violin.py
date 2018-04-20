#Imports here for writefile magic only. Not Pythonic.
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
red = (1,0,0)
blue = (0,.475,1) #Same relative luminance as primary red (approx)

#now a plot analogous to above midcurve violin plots, for discrete vars.
#useful for later as well

#can remove a lot of these params for ordering. just wanna be able to flip 
#which goes to left vs right. could stick with color ordering (left is blue)

def bar_violin(y, data, hue='ds', y_label=None, colors = [blue, red],
               hue_labels=['My Library','Billboard Top'], order=None, 
               hue_order=['nix','top'], ax=None, int_labels=False, title=None):

    #Assumes binary variable with no missing values
    split_vals = data[hue].unique()
        
    #Count non-missing values for both sets, to normalize each barplot
    totals = ( data[y][ data[hue]==split_vals[0] ].count(), 
              data[y][ data[hue]==split_vals[1] ].count() )
    
    p = sns.barplot(x='', y=y, data=data[ data[hue]==split_vals[0] ], 
                    estimator=lambda x: -len(x)/totals[0], orient='h', ci=None,
                    color=colors[0], saturation=1, ax=ax )
    p = sns.barplot(x='', y=y, data=data[ data[hue]==split_vals[1] ], 
                    estimator=lambda x: len(x)/totals[1], orient='h', ci=None, 
                    color=colors[1], saturation=1, ax=ax )

    #Center plot
    xlim = p.get_xlim()
    xlim_max = max( np.abs( xlim ) )
    p.set_xlim( [-xlim_max, xlim_max] )

    #Plot vertical line
    ylim = p.get_ylim()
    p.plot( [0]*2, ylim, 'k-', lw=1.5)

    #Custom Y axis label
    if y_label is None:
        y_label = y.title() #Capitalize first letter
    p.set_ylabel(y_label)
        
    #Title, with default.
    if title is None:
        var = y.title() #Capitalize first letter
        title = 'Track ' + var + ' by Dataset'
    p.set_title(title)

    #This is necessary, othewise the ticklabels will not be populated 
    #until the entire cell has completed
    #Quirk of %matplotlib inline
    plt.draw() 

    #Remove x tick labels
    p.set_xticklabels([])

    #Integer formatting for y axis
    if int_labels:
        ylabels = [ item.get_text() for item in p.get_yticklabels() ]
        ylabels = [ str( int( float( label ) ) ) for label in ylabels ]
        p.set_yticklabels(ylabels);
     
    #Add redundant y axis
    p.tick_params(labelright=True)

    #Add colored split variable indicators to top of frame
    p.text(.25, -.04, hue_labels[0], horizontalalignment='center', 
           verticalalignment='center', transform = p.transAxes, 
           color=colors[0], size=16)
    p.text(.75, -.04, hue_labels[1], horizontalalignment='center', 
           verticalalignment='center', transform = p.transAxes, 
           color=colors[1], size=16)

    return p