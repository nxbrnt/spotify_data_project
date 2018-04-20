#Imports here for writefile magic only. Not Pythonic.
import seaborn as sns

def decade_violinplot(df, col, ylabel=None, ylim=None, title=None):

    #Plot violins and points.
    colors = sns.color_palette( [(0,0,0)] )
    p = sns.violinplot(x='decade',y=col,data=df, split=False, palette=colors, 
                       saturation=1, scale='width', width=0.5, inner='point', 
                       cut=2, linewidth=0)
    p = sns.pointplot(x='decade',y=col,data=df, color='w', join=False, ci=None, 
                      scale=.5)
    
    #Set Y range
    if ylim is not None:
        p.set_ylim(ylim)
    
    #Labels
    #Capitalize column name for ylabel by default
    if ylabel is None:
        ylabel = col.title() #Capitalize first letter
    p.set_ylabel(ylabel)
    p.set_xlabel('Decade')
    p.set_xticklabels(['1960s', '1970s', '1980s', '1990s', '2000s', '2010s']);
    
    #Title, with default.
    if title is None:
        var = col.title() #Capitalize first letter
        title = 'Track ' + var + ' by Decade'
    p.set_title(title)
    
    return p