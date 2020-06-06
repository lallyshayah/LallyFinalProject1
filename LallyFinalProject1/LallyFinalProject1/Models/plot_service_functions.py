import base64 #מביאה מבחוץ
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas #מביאה מהסביבה
from matplotlib.figure import Figure #מביאה מהסביבה
import pandas as pd #מביאה מבחוץ
import numpy as np #מביאה מבחוץ
import matplotlib.pyplot as plt #מביאה מבחוץ
import datetime #מביאה מבחוץ
from os import path #מביאה מבחוץ 
import io 

# פונקציה שלוקחת עצ והופכת אותו לתמונה (בשביל להציג באתר)
def plot_to_img(fig):
    pngImage = io.BytesIO()
    FigureCanvas(fig).print_png(pngImage)
    pngImageB64String = "data:image/png;base64,"
    pngImageB64String += base64.b64encode(pngImage.getvalue()).decode('utf8')
    return pngImageB64String


