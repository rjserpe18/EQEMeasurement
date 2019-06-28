import seaborn as sns
from tkinter import Frame, Button,Label,Entry,Checkbutton,IntVar, Scale
from tkinter.ttk import Notebook
from tkinter import LEFT, TOP, X, FLAT, RAISED,RIGHT, SUNKEN, GROOVE, RIDGE
import matplotlib
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
import math
matplotlib.use('TkAgg')

def linspace(start,stop,n):
    vector = []
    step = (stop-start)/n
    for i in range(n+1):
        val = start + step*i
        vector.append(val)

    return vector

try:
    from Tkinter import Canvas
    from Tkconstants import *
except ImportError:
    from tkinter import Canvas
    from tkinter.constants import *

from PIL import Image, ImageDraw, ImageTk

# Python 2/3 compatibility
try:
    basestring
except NameError:
    basestring = str

def hex2rgb(str_rgb):
    try:
        rgb = str_rgb[1:]

        if len(rgb) == 6:
            r, g, b = rgb[0:2], rgb[2:4], rgb[4:6]
        elif len(rgb) == 3:
            r, g, b = rgb[0] * 2, rgb[1] * 2, rgb[2] * 2
        else:
            raise ValueError()
    except:
        raise ValueError("Invalid value %r provided for rgb color." % str_rgb)

    return tuple(int(v, 16) for v in (r, g, b))

class GradientFrame(Canvas):

    def __init__(self, master, from_color, to_color, width=None, height=None, orient=HORIZONTAL, steps=None, **kwargs):
        Canvas.__init__(self, master, **kwargs)
        if steps is None:
            if orient == HORIZONTAL:
                steps = height
            else:
                steps = width

        if isinstance(from_color, basestring):
            from_color = hex2rgb(from_color)

        if isinstance(to_color, basestring):
            to_color = hex2rgb(to_color)

        r, g, b = from_color
        dr = float(to_color[0] - r) / steps
        dg = float(to_color[1] - g) / steps
        db = float(to_color[2] - b) / steps

        if orient == HORIZONTAL:
            if height is None:
                raise ValueError("height can not be None")

            self.configure(height=height)

            if width is not None:
                self.configure(width=width)

            img_height = height
            img_width = self.winfo_screenwidth()

            image = Image.new("RGB", (img_width, img_height), "#FFFFFF")
            draw = ImageDraw.Draw(image)

            for i in range(steps):
                r, g, b = r + dr, g + dg, b + db
                y0 = int(float(img_height * i) / steps)
                y1 = int(float(img_height * (i + 1)) / steps)

                draw.rectangle((0, y0, img_width, y1), fill=(int(r), int(g), int(b)))
        else:
            if width is None:
                raise ValueError("width can not be None")
            self.configure(width=width)

            if height is not None:
                self.configure(height=height)

            img_height = self.winfo_screenheight()
            img_width = width

            image = Image.new("RGB", (img_width, img_height), "#FFFFFF")
            draw = ImageDraw.Draw(image)

            for i in range(steps):
                r, g, b = r + dr, g + dg, b + db
                x0 = int(float(img_width * i) / steps)
                x1 = int(float(img_width * (i + 1)) / steps)

                draw.rectangle((x0, 0, x1, img_height), fill=(int(r), int(g), int(b)))

        self._gradient_photoimage = ImageTk.PhotoImage(image)

        self.create_image(0, 0, anchor=NW, image=self._gradient_photoimage)


class CustomToolbar(NavigationToolbar2Tk):
    def save_Figure(self):
        filename = filedialog.asksaveasfilename(initialdir="/", title="Select file", filetypes=(
        ('png files', '*.png'), ("jpeg files", "*.jpg"), ("all files", "*.*")))
        plt.savefig(filename)

    def __init__(self,canvas_,parent_):
        self.toolitems = (
            ('Home', 'Reset original view', 'home', 'home'),
            ('Back', 'Back to previous view', 'back', 'back'),('Forward', 'Forward to next view', 'forward', 'forward'),
            # TODO Get this poor thing a nice gif
            ('Pan', 'Pan axes with left mouse, zoom with right', 'move', 'pan'),('Zoom', 'Zoom to rectangle', 'zoom_to_rect', 'zoom'),
            ( 'save_fig', 'Save Figure', 'Filesave', 'save_Figure')
            )
        NavigationToolbar2Tk.__init__(self,canvas_,parent_)

class interface(Frame):

    def __init__(self,sets):
        super().__init__()

        self.initUI(sets)
        self.mainloop()

    def initUI(self, sets):

        self.current_palette = sns.cubehelix_palette(len(sets), start=2, rot=0, dark=.2, light=.85, reverse=True)
        self.sets = sets

        outer_options_frame = Frame(self.master)
        outer_options_frame.pack(side=LEFT, expand = True, fill='both')

        self.fig = plt.figure()
        self.fig.patch.set_alpha(1)
        self.fig.set_facecolor((.95,.95,.95))
        matplotlib.style.use('seaborn-darkgrid')

        self.ax = self.fig.add_subplot(1,1,1)
        self.ax.set_facecolor((210/255,210/255,210/255))
        self.ax.set_alpha(0.0)
        self.ax.spines['left'].set_visible(True)


        GradientFrame(outer_options_frame, from_color="#FCFCFC", to_color="#404040", height=1200, width=800).place(anchor='nw',
                                                                                                 bordermode=INSIDE)
        # w, h = self.master.winfo_screenwidth(), self.master.winfo_screenheight()
        # if self.master.winfo_screenwidth() != w or self.master.winfo_screenheight()
        options_frame = Frame(outer_options_frame)
        options_frame.pack(side=LEFT)

        self.canvas_frame = Frame(outer_options_frame, bg='')
        self.canvas_frame.pack(side=LEFT, expand = True, fill = 'both')
        self.canvas = FigureCanvasTkAgg(self.fig, self.canvas_frame)
        self.toolbar = CustomToolbar(self.canvas, self.canvas_frame)
        self.canvas.get_tk_widget().pack(side=LEFT, expand = True, fill = 'both')

        self.drop = Notebook(options_frame)
        self.drop.pack(expand=True, fill='x')

        title_frame = Frame(options_frame)
        title_frame.pack(expand = True,fill='x')
        title_label = Label(title_frame, text='Title', fg='#009999', bg = '#C0C0C0')
        title_label.pack(expand=True, fill='x')
        self.title_box = Entry(title_frame, fg='#009999')
        self.title_box.pack(side=LEFT, expand=True, fill='both')

        x_ax_frame = Frame(options_frame)
        x_ax_frame.pack(expand=True, fill='x')
        x_axlabel = Label(x_ax_frame, text='X Axis Label', fg='#009999', bg = '#C0C0C0')
        x_axlabel.pack(expand=True, fill='x')
        self.x_ax_box = Entry(x_ax_frame, fg='#009999')
        self.x_ax_box.pack(side=LEFT, expand=True, fill='x')

        y_ax_frame = Frame(options_frame)
        y_ax_frame.pack(expand=True, fill='x')
        y_axlabel = Label(y_ax_frame, text='Y Axis Label', fg='#009999', bg = '#C0C0C0')
        y_axlabel.pack(expand=True, fill='x')
        self.y_ax_box = Entry(y_ax_frame, fg='#009999')
        self.y_ax_box.pack(side=LEFT, expand=True, fill='x')

        self.integrate_onoffs = []
        self.max_points = []
        self.min_points = []
        self.min_boxes = []
        self.max_boxes = []
        self.max_texts = []
        self.min_texts = []
        self.max_lower_boxes = []
        self.min_lower_boxes = []
        self.max_higher_boxes = []
        self.min_higher_boxes = []
        self.min_onoffs = []
        self.max_onoffs = []
        self.lines = []
        self.fills = []
        self.area_boxes = []
        self.data_titles = []
        self.lines = []
        self.x_maxmax = -999999999
        self.x_minmin = 99999999999
        self.y_maxmax = -999999999
        self.y_minmin = 99999999999
        self.data_checks = []
        self.data_check_onoffs = []
        self.lines_onoffs = []
        self.linewidths = []

        for set in sets:
            current_frame = Frame(self.drop)
            max_point = 0
            self.fills.append(0)
            self.linewidths.append(3)
            min_point = 0
            max_text = ''
            min_text = ''
            self.max_texts.append(max_text)
            self.min_texts.append(min_text)
            self.max_points.append(max_point)
            self.min_points.append(min_point)
            x = set[0]
            y = set[1]
            if max(x) > self.x_maxmax:
                self.x_maxmax = max(x)
            if min(x) < self.x_minmin:
                self.x_minmin = min(x)
            if max(y) > self.y_maxmax:
                self.y_maxmax = max(y)
            if min(y) < self.y_minmin:
                self.y_minmin = min(y)
            line, = self.ax.plot(x, y, linewidth=3, color=self.current_palette[sets.index(set)])
            self.lines.append(line)
            self.lines_onoffs.append(1)
            # self.ax.scatter(x, y, linewidth=3, color=self.current_palette[sets.index(set)])
            dataset_frame = Frame(current_frame)
            dataset_frame.pack()
            data_check_onoff = IntVar()
            data_check = Checkbutton(dataset_frame, bg = '#C0C0C0', fg = '#009999', variable = data_check_onoff, command = self.toggle_line, activebackground = '#C0C0C0', activeforeground ='#009999')
            data_check.pack(side=LEFT, expand = True, fill = 'x')
            self.data_checks.append(data_check)
            self.data_check_onoffs.append(data_check_onoff)

            dataset_box = Entry(dataset_frame, fg='#009999', bg = '#C0C0C0', justify = 'center')
            dataset_box.insert(0,'Dataset ' + str(sets.index(set)+1))
            self.data_titles.append(dataset_box)
            dataset_box.pack(expand=True, fill = 'both', side=LEFT)
            max_frame = Frame(current_frame, bg='#C0C0C0')
            max_frame.pack(expand = True, fill='x')
            max_OnOff = IntVar()
            max_checkbox = Checkbutton(max_frame,text='Max:',variable= max_OnOff, command= self.maximum, fg='#009999', bg = '#C0C0C0',activebackground = '#C0C0C0', activeforeground ='#009999')
            self.max_onoffs.append(max_OnOff)
            max_checkbox.pack(side=LEFT)
            self.max_boxes.append(max_checkbox)
            max_lower_label = Label(max_frame,text='Between', fg='#009999', bg = '#C0C0C0')
            max_lower_label.pack(side=LEFT)
            max_lower_box = Entry(max_frame,width=7, fg='#009999')
            max_lower_box.insert(0,str(float(min(x))))
            max_lower_box.pack(side=LEFT, expand = True, fill = 'x')
            max_higher_label = Label(max_frame, text='and', fg='#009999', bg = '#C0C0C0')
            max_higher_label.pack(side=LEFT)
            max_higher_box = Entry(max_frame, width=7, fg='#009999')
            max_higher_box.insert(0, str(float(max(x))))
            max_higher_box.pack(side=LEFT, expand = True, fill = 'x')
            self.max_higher_boxes.append(max_higher_box)
            self.max_lower_boxes.append(max_lower_box)


            min_frame = Frame(current_frame, bg='#C0C0C0')
            min_frame.pack( expand = True, fill = 'x')
            min_OnOff = IntVar()
            min_checkbox = Checkbutton(min_frame, text='Min:', variable=min_OnOff, command=self.minimum, fg='#009999', bg = '#C0C0C0',activebackground = '#C0C0C0', activeforeground ='#009999')
            self.min_onoffs.append(min_OnOff)
            min_checkbox.pack(side=LEFT)
            self.min_boxes.append(min_checkbox)
            min_lower_label = Label(min_frame, text='Between', fg='#009999', bg = '#C0C0C0')
            min_lower_label.pack(side=LEFT)
            min_lower_box = Entry(min_frame, width=7, fg='#009999')
            min_lower_box.insert(0, str(float(min(x))))

            min_lower_box.pack(side=LEFT, expand = True, fill = 'x')
            min_higher_label = Label(min_frame, text='and', fg='#009999', bg = '#C0C0C0')
            min_higher_label.pack(side=LEFT)
            min_higher_box = Entry(min_frame, width=7, fg='#009999')
            min_higher_box.insert(0, str(float(max(x))))
            min_higher_box.pack(side=LEFT, expand = True, fill = 'x')
            self.min_higher_boxes.append(min_higher_box)
            self.min_lower_boxes.append(min_lower_box)

            integrate_frame = Frame(current_frame)
            integrate_frame.pack(expand=True, fill='x')
            integrate_ofonn = IntVar()
            self.integrate_check = Checkbutton(integrate_frame, bg = '#C0C0C0', variable = integrate_ofonn, fg = '#009999', activebackground = '#C0C0C0', activeforeground = '#009999', text = 'Integrate, Area = ', command = self.integral)
            self.integrate_check.pack(expand=True, fill = 'x', side=LEFT)
            area_box = Entry(integrate_frame, fg = '#009999')
            area_box.pack(side=LEFT, expand= True, fill = 'x')
            self.area_boxes.append(area_box)
            self.integrate_onoffs.append(integrate_ofonn)

            # line_width_frame = Frame(current_frame)
            # line_width_frame.pack(expand=True, fill = 'x')
            # line_width_box = Entry(line_width_frame, width=7, fg='#009999', text ='Linewidth')
            # line_width_box.insert('3')
            # line_width_box.pack(expand=True, fill = 'x')

            # linear_frame = Frame(current_frame)
            # linear_frame.pack(expand=True, fill='x')
            # linear_ofonn = IntVar()
            # linear_checkbox = Checkbutton(linear_frame, text='Linear Regression', variable=linear_ofonn, fg='#009999', activebackground='#C0C0C0', activeforeground='#009999', command=self.lin_reg, bg = '#C0C0C0')
            # linear_checkbox.pack(expand=True, fill='x')
            # equation_box = Entry(linear_frame)

            self.drop.add(current_frame, text=str(1+sets.index(set)))

        self.xlow, self.xhigh, self.ylow, self.yhigh = plt.axis()

        xlimit_frame = Frame(options_frame)
        xlimit_frame.pack(expand=True, fill='x')
        xlim_label = Label(xlimit_frame, text='X Limit', fg='#009999', bg='#C0C0C0')
        xlim_label.pack(side=LEFT)
        self.xlim_lower_box = Entry(xlimit_frame, width=7, fg='#009999')
        self.xlim_lower_box.insert(0, self.xlow)
        self.xlim_lower_box.pack(side=LEFT, expand=True, fill='x')
        xlim_higher_label = Label(xlimit_frame, text='to', fg='#009999', bg='#C0C0C0')
        xlim_higher_label.pack(side=LEFT)
        self.xlim_higher_box = Entry(xlimit_frame, width=7, fg='#009999')
        self.xlim_higher_box.insert(0, self.xhigh)
        self.xlim_higher_box.pack(side=LEFT, expand=True, fill='x')

        ylimit_frame = Frame(options_frame)
        ylimit_frame.pack(expand=True, fill='x')
        ylim_label = Label(ylimit_frame, text='Y Limit', fg='#009999', bg='#C0C0C0')
        ylim_label.pack(side=LEFT)
        self.ylim_lower_box = Entry(ylimit_frame, width=7, fg='#009999')
        self.ylim_lower_box.insert(0, self.ylow)
        self.ylim_lower_box.pack(side=LEFT, expand=True, fill='x')
        ylim_higher_label = Label(ylimit_frame, text='to', fg='#009999', bg='#C0C0C0')
        ylim_higher_label.pack(side=LEFT)
        self.ylim_higher_box = Entry(ylimit_frame, width=7, fg='#009999')
        self.ylim_higher_box.insert(0, self.yhigh)
        self.ylim_higher_box.pack(side=LEFT, expand=True, fill='x')

        bg_slider_frame = Frame(options_frame)
        bg_slider_frame.pack(expand = True, fill = 'x')
        bg_slider_label = Label(bg_slider_frame, text = 'Background Color', fg = '#009999', bg = '#C0C0C0')
        bg_slider_label.pack(expand = True, fill = 'x')
        self.bg_slider = Scale(bg_slider_frame, from_=0, to=255, orient='horizontal', bg = '#C0C0C0')
        self.bg_slider.set(210)
        self.bg_slider.pack(expand = True, fill = 'x')

        legend_frame = Frame(options_frame)
        legend_frame.pack(expand=True, fill = 'x')
        self.legend_onoff = IntVar()
        self.legend_check = Checkbutton(legend_frame, bg = '#C0C0C0',fg = '#009999', variable = self.legend_onoff, command = self.add_legend, text='Legend', activebackground = '#C0C0C0', activeforeground = '#009999')
        self.legend_check.pack(expand = True, fill = 'x')

        apply_button_frame = Frame(options_frame, bg='#C0C0C0')
        apply_button_frame.pack()

        self.apply_button = Button(apply_button_frame, text='Apply', command=self.apply, bg='#C0C0C0')
        self.apply_button.grid(row=0, column=0)

        for chk in self.data_checks:
            chk.toggle()

        def close(self):
            self.master.destroy()
            self.master.quit()

        self.master.protocol("WM_DELETE_WINDOW", lambda: close(self))

    def xlimit(self):
        if self.xlim_lower_box.get() != self.xlow:

            lower_text = self.xlim_lower_box.get()
            self.ax.set_xlim(xmin=float(lower_text))
            self.ax.set_xticks(linspace(float(lower_text), self.ax.get_xlim()[1], 20))
            self.canvas.get_tk_widget().update()
            self.canvas.draw()

        if self.xlim_higher_box.get() != self.xhigh:
            higher_text = self.xlim_higher_box.get()
            self.ax.set_xlim( xmax = float(higher_text))
            self.ax.set_xticks(linspace(self.ax.get_xlim()[0], float(higher_text), 20))
            self.canvas.get_tk_widget().update()
            self.canvas.draw()


    def ylimit(self):
        if self.ylim_lower_box.get() != self.ylow:
            lower_text = self.ylim_lower_box.get()
            self.ax.set_ylim(ymin=float(lower_text))
            self.ax.set_yticks(linspace(float(lower_text), self.ax.get_ylim()[1], 20))
            self.canvas.get_tk_widget().update()
            self.canvas.draw()

        if self.ylim_higher_box.get() != self.yhigh:
            higher_text = self.ylim_higher_box.get()
            self.ax.set_ylim(ymax=float(higher_text))
            self.ax.set_yticks(linspace(self.ax.get_ylim()[0], float(higher_text), 20))
            self.canvas.get_tk_widget().update()
            self.canvas.draw()
    # def linewidth(self):
    #
    def title(self):
        title_text = self.title_box.get()
        self.title_box.delete(0, len(title_text))
        self.ax.set_title(title_text)
        self.canvas.get_tk_widget().update()
        self.canvas.draw()

    def background(self):
        color = self.bg_slider.get()
        self.ax.set_facecolor((color / 255, color / 255, color / 255))
        self.canvas.get_tk_widget().update()
        self.canvas.draw()

    def x_ax(self):
        x_ax_text = self.x_ax_box.get()
        self.x_ax_box.delete(0, len(x_ax_text))
        self.ax.set_xlabel(x_ax_text)
        self.canvas.get_tk_widget().update()
        self.canvas.draw()

    def y_ax(self):
        y_ax_text = self.y_ax_box.get()
        self.y_ax_box.delete(0, len(y_ax_text))
        self.ax.set_ylabel(y_ax_text)
        self.canvas.get_tk_widget().update()
        self.canvas.draw()

    def maximum(self):
        for box in self.max_boxes:
            x = self.sets[self.max_boxes.index(box)][0]
            y = self.sets[self.max_boxes.index(box)][1]
            if self.max_onoffs[self.max_boxes.index(box)].get() == 0 and self.max_points[self.max_boxes.index(box)]!= 0:
                try:
                    self.max_points[self.max_boxes.index(box)].remove()
                    self.max_texts[self.max_boxes.index(box)].remove()
                    self.canvas.get_tk_widget().update()
                    self.canvas.draw()
                except:
                    pass
            if self.max_onoffs[self.max_boxes.index(box)].get() == 1:
                try:
                    self.max_points[self.max_boxes.index(box)].remove()
                    self.max_texts[self.max_boxes.index(box)].remove()
                except:
                    pass
                try:
                    lower_val = float(self.max_lower_boxes[self.max_boxes.index(box)].get())
                except:
                    lower_val = min(x)
                    self.max_lower_boxes[self.max_boxes.index(box)].insert(0,str(min(x)))
                try:
                    higher_val = float(self.max_higher_boxes[self.max_boxes.index(box)].get())
                except:
                    higher_val = max(x)
                    self.max_higher_boxes[self.max_boxes.index(box)].insert(0, str(max(x)))

                if lower_val not in x:
                    closest = x[0]
                    for val in x:
                        if abs(lower_val - val) < abs(lower_val - closest):
                            closest = val
                    lower_val = closest
                if higher_val not in x:
                    closest = x[0]
                    for val in x:
                        if abs(higher_val - val) < abs(higher_val - closest):
                            closest = val
                    higher_val = closest
                if lower_val != min(x) or higher_val != max(x):
                    try:
                        self.max_points[self.max_boxes.index(box)].remove()
                        self.max_texts[self.max_boxes.index(box)].remove()
                        self.canvas.get_tk_widget().update()
                        self.canvas.draw()
                    except:
                        pass
                self.max_higher_boxes[self.max_boxes.index(box)].delete(0,len(self.max_higher_boxes[self.max_boxes.index(box)].get()))
                self.max_lower_boxes[self.max_boxes.index(box)].delete(0,len(self.max_lower_boxes[self.max_boxes.index(box)].get()))
                self.max_lower_boxes[self.max_boxes.index(box)].insert(0,str(lower_val))
                self.max_higher_boxes[self.max_boxes.index(box)].insert(0,str(higher_val))
                max_y_range = y[x.index(lower_val):x.index(higher_val)+1]
                ymax = max(max_y_range)
                xmax = x[y.index(ymax)]
                max_point, = self.ax.plot(xmax, ymax, 'ko')
                self.max_points[self.max_boxes.index(box)] = max_point
                max_str = 'Max: (' + str(round(xmax,2)) + ',' + str(round(ymax,2)) + ')'
                max_text = self.ax.annotate(max_str,(xmax,ymax + ymax/100), annotation_clip = False)

                self.max_texts[self.max_boxes.index(box)] = max_text
                self.canvas.get_tk_widget().update()
                self.canvas.draw()

    def minimum(self):
        for box in self.min_boxes:
            x = self.sets[self.min_boxes.index(box)][0]
            y = self.sets[self.min_boxes.index(box)][1]

            if self.min_onoffs[self.min_boxes.index(box)].get() == 0 and self.min_points[
                self.min_boxes.index(box)] != 0:
                try:
                    self.min_points[self.min_boxes.index(box)].remove()
                    self.min_texts[self.min_boxes.index(box)].remove()
                    self.canvas.get_tk_widget().update()
                    self.canvas.draw()
                except:
                    pass
            if self.min_onoffs[self.min_boxes.index(box)].get() == 1:
                try:
                    self.min_points[self.min_boxes.index(box)].remove()
                    self.min_texts[self.min_boxes.index(box)].remove()
                except:
                    pass
                try:
                    lower_val = float(self.min_lower_boxes[self.min_boxes.index(box)].get())
                except:
                    lower_val = min(x)
                    self.min_lower_boxes[self.min_boxes.index(box)].insert(0, str(min(x)))
                try:
                    higher_val = float(self.min_higher_boxes[self.min_boxes.index(box)].get())
                except:
                    higher_val = max(x)
                    self.min_higher_boxes[self.min_boxes.index(box)].insert(0, str(max(x)))
                if lower_val not in x:
                    closest = x[0]
                    for val in x:
                        if abs(lower_val - val) < abs(lower_val - closest):
                            closest = val
                    lower_val = closest
                if higher_val not in x:
                    closest = x[0]
                    for val in x:
                        if abs(higher_val - val) < abs(higher_val - closest):
                            closest = val
                    higher_val = closest
                if lower_val != min(x) or higher_val != max(x):
                    try:
                        self.min_points[self.min_boxes.index(box)].remove()
                        self.min_texts[self.min_boxes.index(box)].remove()
                        self.canvas.get_tk_widget().update()
                        self.canvas.draw()
                    except:
                        pass
                self.min_higher_boxes[self.min_boxes.index(box)].delete(0, len(
                    self.min_higher_boxes[self.min_boxes.index(box)].get()))
                self.min_lower_boxes[self.min_boxes.index(box)].delete(0, len(
                    self.min_lower_boxes[self.min_boxes.index(box)].get()))
                self.min_lower_boxes[self.min_boxes.index(box)].insert(0, str(lower_val))
                self.min_higher_boxes[self.min_boxes.index(box)].insert(0, str(higher_val))
                min_y_range = y[x.index(lower_val):x.index(higher_val) + 1]
                ymin = min(min_y_range)
                xmin = x[y.index(ymin)]
                min_point, = self.ax.plot(xmin, ymin, 'ko')
                self.min_points[self.min_boxes.index(box)] = min_point
                min_str = 'Min: (' + str(round(xmin,2)) + ',' + str(round(ymin,2)) + ')'
                min_text = self.ax.annotate(min_str, (xmin, ymin + ymin / 100), annotation_clip=False)

                self.min_texts[self.min_boxes.index(box)] = min_text
                self.canvas.get_tk_widget().update()
                self.canvas.draw()
    def apply(self):
        if self.title_box.get() != '':
            self.title()
        if (self.x_ax_box.get() != ''):
            self.x_ax()
        if (self.y_ax_box.get() != ''):
            self.y_ax()

        self.xlimit()
        self.ylimit()
        self.maximum()
        self.minimum()
        self.background()
        self.integral()
        self.add_legend()

    def integral(self):
        for box in self.integrate_onoffs:
            ind = self.integrate_onoffs.index(box)
            if box.get() == 1 and self.fills[ind] == 0:
                area_box = self.area_boxes[ind]
                set = self.sets[ind]
                x = set[0]
                y = set[1]
                color = self.current_palette[ind]
                fill = self.ax.fill_between(x,0,y, alpha=.35, color=color)
                self.fills[ind] = fill
                self.canvas.get_tk_widget().update()
                self.canvas.draw()
                area = 0
                x = self.sets[ind][0]
                y = self.sets[ind][1]
                last_x = x[0]
                last_y = y[0]
                for i in range(len(x)):
                    x_val = x[i]
                    y_val = y[i]
                    low_da = (x_val - last_x)*last_y
                    high_da = (x_val - last_x)* y_val
                    da = (low_da + high_da)/2
                    area += da
                    last_x = x_val
                    last_y = y_val
                area_box.insert(0,str(round(area,4)))
                area_box.update()

            if box.get() == 0:
                area_box = self.area_boxes[ind]
                try:
                    area_box.delete(0, len(area_box.get()))
                    area_box.update()
                    self.fills[ind].remove()
                    self.fills[ind] = 0
                    self.canvas.get_tk_widget().update()
                    self.canvas.draw()

                except:
                    pass
    def add_legend(self):
        if self.legend_onoff.get() ==1:
            labels = ()
            lines = ()
            for i in range(len(self.sets)):
                label = self.data_titles[i].get()
                labels += (label,)
                line = self.ax.lines[i]
                lines += (line,)
            self.leg = self.ax.legend(lines, labels, frameon=True, loc=4)
            self.canvas.get_tk_widget().update()
            self.canvas.draw()
        if self.legend_onoff.get() == 0:
            try:
                self.leg.remove()
                self.canvas.get_tk_widget().update()
                self.canvas.draw()
            except:
                pass
    def toggle_line(self):
        for chk in self.data_check_onoffs:
            if chk.get() == 0:
                if self.lines_onoffs[self.data_check_onoffs.index(chk)] == 1:
                    self.lines_onoffs[self.data_check_onoffs.index(chk)] = 0
                    self.lines[self.data_check_onoffs.index(chk)].remove()
                    self.canvas.get_tk_widget().update()
                    self.canvas.draw()

                    try:
                        self.min_points[self.data_check_onoffs.index(chk)].remove()
                        self.min_texts[self.data_check_onoffs.index(chk)].remove()
                        self.canvas.get_tk_widget().update()
                        self.canvas.draw()
                    except:
                        pass
                    try:
                        self.max_points[self.data_check_onoffs.index(chk)].remove()
                        self.max_texts[self.data_check_onoffs.index(chk)].remove()
                        self.canvas.get_tk_widget().update()
                        self.canvas.draw()
                    except:
                        pass
                    try:
                        ind = self.data_check_onoffs.index(chk)
                        area_box = self.area_boxes[ind]
                        area_box.delete(0, len(area_box.get()))
                        area_box.update()
                        self.fills[ind].remove()
                        self.fills[ind] = 0
                        self.canvas.get_tk_widget().update()
                        self.canvas.draw()
                    except:
                        pass

            if chk.get() == 1:
                if self.lines_onoffs[self.data_check_onoffs.index(chk)] == 0:
                    x = self.sets[self.data_check_onoffs.index(chk)][0]
                    y = self.sets[self.data_check_onoffs.index(chk)][1]
                    line, = self.ax.plot(x, y, linewidth=3, color=self.current_palette[self.data_check_onoffs.index(chk)])
                    self.lines[self.data_check_onoffs.index(chk)] = line
                    self.canvas.get_tk_widget().update()
                    self.canvas.draw()
                    self.lines_onoffs[self.data_check_onoffs.index(chk)] = 1
                    if self.integrate_onoffs[self.data_check_onoffs.index(chk)].get() == 1:
                        try:
                            ind = self.data_check_onoffs.index(chk)
                            area_box = self.area_boxes[ind]
                            set = self.sets[ind]
                            x = set[0]
                            y = set[1]
                            color = self.current_palette[ind]
                            fill = self.ax.fill_between(x, 0, y, alpha=.35, color=color)
                            self.fills[ind] = fill
                            self.canvas.get_tk_widget().update()
                            self.canvas.draw()
                            area = 0
                            x = self.sets[ind][0]
                            y = self.sets[ind][1]
                            last_x = x[0]
                            last_y = y[0]
                            for i in range(len(x)):
                                x_val = x[i]
                                y_val = y[i]
                                low_da = (x_val - last_x) * last_y
                                high_da = (x_val - last_x) * y_val
                                da = (low_da + high_da) / 2
                                area += da
                                last_x = x_val
                                last_y = y_val
                            area_box.insert(0, str(round(area, 4)))
                            area_box.update()
                        except:
                            pass
                    if self.min_onoffs[self.data_check_onoffs.index(chk)].get() == 1:
                        try:
                            try:
                                self.min_points[self.data_check_onoffs.index(chk)].remove()
                                self.min_texts[self.data_check_onoffs.index(chk)].remove()
                            except:
                                pass
                            try:
                                lower_val = float(self.min_lower_boxes[self.data_check_onoffs.index(chk)].get())
                            except:
                                lower_val = min(x)
                                self.min_lower_boxes[self.data_check_onoffs.index(chk)].insert(0, str(min(x)))
                            try:
                                higher_val = float(self.min_higher_boxes[self.data_check_onoffs.index(chk)].get())
                            except:
                                higher_val = max(x)
                                self.min_higher_boxes[self.data_check_onoffs.index(chk)].insert(0, str(max(x)))
                            if lower_val not in x:
                                closest = x[0]
                                for val in x:
                                    if abs(lower_val - val) < abs(lower_val - closest):
                                        closest = val
                                lower_val = closest
                            if higher_val not in x:
                                closest = x[0]
                                for val in x:
                                    if abs(higher_val - val) < abs(higher_val - closest):
                                        closest = val
                                higher_val = closest
                            if lower_val != min(x) or higher_val != max(x):
                                try:
                                    self.min_points[self.data_check_onoffs.index(chk)].remove()
                                    self.min_texts[self.data_check_onoffs.index(chk)].remove()
                                    self.canvas.get_tk_widget().update()
                                    self.canvas.draw()
                                except:
                                    pass
                            self.min_higher_boxes[self.data_check_onoffs.index(chk)].delete(0, len(
                                self.min_higher_boxes[self.data_check_onoffs.index(chk)].get()))
                            self.min_lower_boxes[self.data_check_onoffs.index(chk)].delete(0, len(
                                self.min_lower_boxes[self.data_check_onoffs.index(chk)].get()))
                            self.min_lower_boxes[self.data_check_onoffs.index(chk)].insert(0, str(lower_val))
                            self.min_higher_boxes[self.data_check_onoffs.index(chk)].insert(0, str(higher_val))
                            min_y_range = y[x.index(lower_val):x.index(higher_val) + 1]
                            ymin = min(min_y_range)
                            xmin = x[y.index(ymin)]
                            min_point, = self.ax.plot(xmin, ymin, 'ko')
                            self.min_points[self.data_check_onoffs.index(chk)] = min_point
                            min_str = 'Min: (' + str(round(xmin, 2)) + ',' + str(round(ymin, 2)) + ')'
                            min_text = self.ax.annotate(min_str, (xmin, ymin + ymin / 100), annotation_clip=False)

                            self.min_texts[self.data_check_onoffs.index(chk)] = min_text
                            self.canvas.get_tk_widget().update()
                            self.canvas.draw()
                        except:
                            pass
                    if self.max_onoffs[self.data_check_onoffs.index(chk)].get() == 1:
                        try:
                            self.max_points[self.data_check_onoffs.index(chk)].remove()
                            self.max_texts[self.data_check_onoffs.index(chk)].remove()
                        except:
                            pass
                        try:
                            lower_val = float(self.max_lower_boxes[self.data_check_onoffs.index(chk)].get())
                        except:
                            lower_val = min(x)
                            self.max_lower_boxes[self.data_check_onoffs.index(chk)].insert(0, str(min(x)))
                        try:
                            higher_val = float(self.max_higher_boxes[self.data_check_onoffs.index(chk)].get())
                        except:
                            higher_val = max(x)
                            self.max_higher_boxes[self.data_check_onoffs.index(chk)].insert(0, str(max(x)))

                        if lower_val not in x:
                            closest = x[0]
                            for val in x:
                                if abs(lower_val - val) < abs(lower_val - closest):
                                    closest = val
                            lower_val = closest
                        if higher_val not in x:
                            closest = x[0]
                            for val in x:
                                if abs(higher_val - val) < abs(higher_val - closest):
                                    closest = val
                            higher_val = closest
                        if lower_val != min(x) or higher_val != max(x):
                            try:
                                self.max_points[self.data_check_onoffs.index(chk)].remove()
                                self.max_texts[self.data_check_onoffs.index(chk)].remove()
                                self.canvas.get_tk_widget().update()
                                self.canvas.draw()
                            except:
                                pass
                        self.max_higher_boxes[self.data_check_onoffs.index(chk)].delete(0, len(
                            self.max_higher_boxes[self.data_check_onoffs.index(chk)].get()))
                        self.max_lower_boxes[self.data_check_onoffs.index(chk)].delete(0, len(
                            self.max_lower_boxes[self.data_check_onoffs.index(chk)].get()))
                        self.max_lower_boxes[self.data_check_onoffs.index(chk)].insert(0, str(lower_val))
                        self.max_higher_boxes[self.data_check_onoffs.index(chk)].insert(0, str(higher_val))
                        max_y_range = y[x.index(lower_val):x.index(higher_val) + 1]
                        ymax = max(max_y_range)
                        xmax = x[y.index(ymax)]
                        max_point, = self.ax.plot(xmax, ymax, 'ko')
                        self.max_points[self.data_check_onoffs.index(chk)] = max_point
                        max_str = 'Max: (' + str(round(xmax, 2)) + ',' + str(round(ymax, 2)) + ')'
                        max_text = self.ax.annotate(max_str, (xmax, ymax + ymax / 100), annotation_clip=False)

                        self.max_texts[self.data_check_onoffs.index(chk)] = max_text
                        self.canvas.get_tk_widget().update()
                        self.canvas.draw()


    def lin_reg(self):
        ...



