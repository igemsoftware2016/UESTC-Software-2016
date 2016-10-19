def simple(request):
    import random
    import django
    import datetime

    from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
    from matplotlib.figure import Figure

# to plot a function curve in web

    fig=Figure()

    ax=fig.add_subplot(111)
    x=[0,1,2,3,4,5,6]
    y=[]
    for i in range(len(x)):
        y.append(x[i]**2) 

   
    canvas=FigureCanvas(fig)
    response=django.http.HttpResponse(content_type='image/png')
    canvas.print_png(response)
    return response