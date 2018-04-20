#Imports here for writefile magic only. Not Pythonic.
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt
red = (1,0,0)
blue = (0,.475,1) #Same relative luminance as primary red (approx)

def ds_ratio(group):
    """Returns the fraction of rows that are in 'nix' dataset."""
    nix_count = (group=='nix').sum()
    top_count = (group=='top').sum()
    ratio = nix_count/(nix_count+top_count) #could smooth this
    return ratio

def extremes_plot(grouped, by, col, title=None, xlabel=None, min_tracks=4, 
                  xlim=None, axes=None):
    
    #Filter groupby object and re-group
    grouped_filtered = grouped.filter(lambda x: x[by].count()>=min_tracks
                                   ).groupby(by)
    
    #Aggregate over "col" to obtain mean column and dataset ratio column
    df_temp = grouped_filtered[col].mean().reset_index()
    df_temp['ds_ratio'] = grouped_filtered.ds.agg(ds_ratio).values
    
    #Sort, and store head and tail
    df_temp.sort_values(by=col, inplace=True, ascending=False)
    df_temp_head = df_temp.head(5)
    df_temp_tail = df_temp.tail(5)

    #Set colormap to visualize dataset ratio. 
    #'top'=red, 'nix'=blue, mixed=black
    c1 = red
    c2 = (0,0,0)
    c3 = blue
    cm_list = [ (0, c1), (0.5, c2), (1, c3) ]
    cmap = mpl.colors.LinearSegmentedColormap.from_list(
        'mymap', cm_list, N=256, gamma=1.0)
    colors_head = [cmap(ratio) for ratio in df_temp_head.ds_ratio.values]
    colors_tail = [cmap(ratio) for ratio in df_temp_tail.ds_ratio.values]

    #Make axes if none passed in
    if axes is None:
        fig, axes = plt.subplots(2,1)
        fig.set_size_inches(2, 4)
    (ax1,ax2) = axes
    
    #Ensure that x axes are shared
    ax1.get_shared_x_axes().join(ax1, ax2)

    #Get figure from subplot
    fig = plt.gcf()

    #Top pointplot
    sns.pointplot(y=by, x=col, data=df_temp_head, palette=colors_head,
                  join=False, scale=1.4, ax=ax1)
    
    #Remove labels from top plot
    ax1.set_ylabel('')
    ax1.set_xlabel('', visible=False)
    plt.setp(ax1.get_xticklabels(), visible=False)

    #Bottom pointplot
    sns.pointplot( y=by, x=col, data=df_temp_tail, palette=colors_tail, 
                join=False, scale=1.4, ax=ax2)
    ax2.set_ylabel('')
       
    #Capitalize column name for xlabel by default
    if xlabel is None:
        xlabel = col.title() #Capitalize first letter
    ax2.set_xlabel(xlabel)

    #Set title and title position
    ax1.set_title(title)
    ax1.title.set_position([.5, 1.07])

    #Position tweaks and x limits
    plt.subplots_adjust(hspace=.1);
    if xlim is not None:
        ax1.set_xlim(xlim)
    
    return fig


def extreme_artists_plot(df, col, title=None, xlabel=None, min_tracks=4, 
                         xlim=None, axes=None):
    
    grouped = df.groupby('name_artist')
    by = 'name_artist'
    
    #Title, with default.
    if title is None:
        var = col.title() #Capitalize first letter
        title = 'Artists with Highest and Lowest ' + var
    
    fig = extremes_plot(grouped, by, col, title=title, xlabel=xlabel,
                         min_tracks=min_tracks, xlim=xlim, axes=axes)
    
    return fig


def extreme_genres_plot(by_genre, col, title=None, xlabel=None, min_tracks=16, 
                        xlim=None, axes=None):
    grouped = by_genre
    by = 'genre'
    
    #Title, with default.
    if title is None:
        var = col.title() #Capitalize first letter
        title = 'Genres with Highest and Lowest ' + var
    
    fig = extremes_plot(grouped, by, col, title=title, xlabel=xlabel, 
                         min_tracks=min_tracks, xlim=xlim, axes=axes)
    
    return fig