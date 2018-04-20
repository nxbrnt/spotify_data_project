#Imports here for writefile magic only. Not Pythonic.
import seaborn as sns
import numpy as np
from scipy.interpolate import interp1d
red = (1,0,0)
blue = (0,.475,1) #Same relative luminance as primary red (approx)

#can remove a lot of these params for ordering. just wanna be able to flip 
#which goes to left vs right. could stick with color ordering (left is blue)

def extract_violin_curves(p):
    #Pull vertices from violin KDE estimate plot
    left_points = p.collections[0].get_paths()[0].vertices
    right_points = p.collections[1].get_paths()[0].vertices

    #Strip out points where x=0, corresponding to the vertical middle line.
    left_points = [ (a,b) for a,b in left_points if a!=0.0]
    right_points = [ (a,b) for a,b in right_points if a!=0.0]
    #left_points.sort(key=lambda x: x[1])
    #right_points.sort(key=lambda x: x[1])

    #Zip into separate x and y arrays
    x_left,y_left = zip(*left_points)
    x_right,y_right = zip(*right_points)

    #Interpolated function created from each kde which can be evaluated for 
    #arbitrary y values. Return 0 for out of range inputs.
    f_left = interp1d(y_left, x_left, bounds_error=False, fill_value=0.)
    f_right = interp1d(y_right, x_right, bounds_error=False, fill_value=0.)

    #Combine list of all y values
    y_all = np.concatenate((y_left,y_right))
    y_all.sort()
    
    return y_all, f_left, f_right

def violin_midcurve(y, data, hue='ds', y_label=None, 
                    hue_labels=['My Library','Billboard Top'],
                    order=None, hue_order=['nix','top'], bw='silverman',
                    colors=[ blue, red ], ax=None, 
                    ylim=None, title=None):

    """
    Generates a seaborn violin plot with a "midcurve" that indicates 
    difference in probability between two distributions.
    """
    
    #To do: Implement truncated KDE for distros with known, finite support 
    #(e.g. [0,1]). Also implement cross-validated bandwidth via sklearn.
    p = sns.violinplot('', y, hue, data, order, hue_order, bw=bw, cut=3, 
                       split=True, linewidth=0, palette=colors, color=(0,0,0), 
                       saturation=1, inner=None, showmedians=True, ax=ax,
                       gridsize=200)
    
    #Extract violin curves
    y_all, f_left, f_right = extract_violin_curves(p)

    #Create midpoint x values of the two KDE plots, and add to violinplot
    x_mid = ( f_left(y_all)+f_right(y_all) )
    p.plot(x_mid,y_all,c='k',lw=3)
    
    #Plot mean lines.
    #Use hue_order to determine which dataset is which
    if hue_order is None:
        hue_order = data[hue].unique()
    data_left = data[y][ data[hue]==hue_order[0] ]
    data_right = data[y][ data[hue]==hue_order[1] ]
    
    mean_left = data_left.mean()
    mean_right = data_right.mean()
    
    #Could set these to xlim values rather than +/- 100.
    p.plot( [-100, 0], [mean_left]*2, 'k-', lw=3)
    p.plot( [100, 0], [mean_right]*2, 'k-', lw=3)
    
    #Draw redundant y axis for mean line comparison
    p.tick_params(labelright=True)
    
    #Plot vertical line
    y_min = min(y_all)
    y_max = max(y_all)
    p.plot( [0]*2, [y_min,y_max], 'k-', lw=3)
    
    #Tight vertical axis
    p.autoscale(enable=True, axis='y', tight=True)
    
    #Custom vertical range
    if ylim is not None:
        p.set_ylim( [ ylim[0], ylim[1] ] )
    
    #Remove legend and add colored split variable indicators to top of frame
    if hue_labels is None:
        hue_labels = hue_order     
    p.legend_.remove()
    p.text(.25, -.04, hue_labels[0], horizontalalignment='center', 
           verticalalignment='center', transform = p.transAxes, 
           color=colors[0], size=16)
    p.text(.75, -.04, hue_labels[1], horizontalalignment='center', 
           verticalalignment='center', transform = p.transAxes, 
           color=colors[1], size=16)
    
    #Custom Y axis label. Simply capitalizes column name by default.
    if y_label is None:
        y_label = y.title() #Capitalize first letter
    p.set_ylabel(y_label)
        
    #Title, with default.
    if title is None:
        var = y.title() #Capitalize first letter
        title = 'Track ' + var + ' by Dataset'
    p.set_title(title)
     
    return p