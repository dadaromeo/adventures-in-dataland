def display_confusion_matrix(true, pred, labels=None, tablefmt="rst"):
    import tabulate
    from sklearn.metrics import confusion_matrix
    
    cm = confusion_matrix(true, pred, labels=labels)
    data = [[k]+list(v) for k,v in enumerate(cm)]
    data.insert(0, list(labels))
    return tabulate.tabulate(data, headers="firstrow", tablefmt=tablefmt)

def plot_misclass(x,true,pred,a=0,b=5):
    import matplotlib.pyplot as plt
    
    misclass = x[(true==a)&(pred==b)][:10]

    fig,axes = plt.subplots(nrows=2, ncols=5, figsize=(8,5))

    fig.suptitle("Some {} that were misclassified as {}".format(a,b), fontsize=15)
    for ax,d in zip(fig.axes,misclass):
        d = d.reshape((28,28))
        ax.imshow(d, cmap=plt.cm.Greys)

def count(arr):
    from numpy import array
    from collections import defaultdict
    
    tab = defaultdict(int)
    for elt in arr:
        tab[elt] += 1
    keys,vals = zip(*tab.items())    
    return array(keys), array(vals)