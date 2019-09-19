#!/usr/bin/env python
# coding:utf-8

"""
#iras数据定制监测绘图通用方法
"""

import os
from PIL import Image
import numpy as np
import matplotlib
import matplotlib.gridspec as gridspec

import netCDF4
import matplotlib.figure
from matplotlib.font_manager import FontProperties
from matplotlib.backends.backend_agg import FigureCanvasAgg


class Plot():
    def __init__(self,  debug=1):
        fontpath = os.path.join(os.path.dirname(__file__),'simsun.ttf')
        self.font = FontProperties(fname=fontpath, size=14)
        #self.sysarg = sysarg
        self.debug = 1

    def layout_style_5(self):
        width_ratios = [1,1,1]
        gs = gridspec.GridSpec(1, 3, width_ratios=width_ratios)
        gs.update(left=0.09, right=0.91, top=0.91, bottom=0.09,  wspace=0.2)

        ax1 = self.Figure.add_subplot(gs[0, 0])
        ax2 = self.Figure.add_subplot(gs[0, 1])
        ax3 = self.Figure.add_subplot(gs[0, 2])
        #ax1.set_adjustable('box-forced')
        #ax1.set_aspect('equal')
        return [ax1, ax2, ax3]

    def set_figure_size(self, w, h):
        '''
        w宽度，像素
        h高度，像素
        DPI像素每英寸
        '''
        #w_inches = (w*1.0)/self.Figure.get_dpi()
        #h_inches = (h*1.0)/self.Figure.get_dpi()
        w_inches = (w*1.0)/100
        h_inches = (h*1.0)/100
        self.Figure.set_size_inches(w_inches, h_inches)

    def set_xlim_average(self, axes, major_unit):
        axes.xaxis.set_major_locator(matplotlib.ticker.LinearLocator(major_unit + 1))

    def set_StrFormatter(self, axes, formatterstr):
        formatter   = matplotlib.ticker.FormatStrFormatter(formatterstr)
        axes.xaxis.set_major_formatter(formatter)

    def plot_line(self, axes, *args, **kwargs):
        '''#最常用的绘图命令plot '''
        axes.plot(*args, **kwargs)

    def ylabel(self, axes, YabelString="Y"):
        ''' # Add ylabel to the plotting '''
        axes.set_ylabel(YabelString, fontproperties=self.font)

    def xlabel(self, axes, XabelString="X"):
        ''' # Add xlabel to the plotting    '''
        axes.set_xlabel(XabelString, fontproperties=self.font)


    def xlim(self, axes, x_min, x_max):
        ''' # 设置x轴的显示范围  '''
        axes.set_xlim(x_min, x_max)

    def ylim(self, axes, x_min, x_max):
        ''' # 设置x轴的显示范围  '''
        axes.set_ylim(x_min, x_max)

    def setlegend(self, axes, *args, **kwargs):
        axes.legend(*args, prop=self.font, **kwargs)

    def process_plot_avp(self, AT_x, LD_x, AH_x, AO_x, l2a_AT_x, l2a_LD_x, l2a_AH_x, l2a_AO_x, pressure, clm, width, height, AH_xlim, AO_xlim, AT_xlim, out_file, i, thumbnail):

        #necp = self.getMplCb(cb['gradient'])
        #cmap = matplotlib.colors.LinearSegmentedColormap.from_list('mycmap', necp)
        self.Figure = matplotlib.figure.Figure()

        self.set_figure_size(width, height)
        self.axList = self.layout_style_5()
        #图一
        self.plot_line(self.axList[0], AT_x, pressure, color='r', label=u"温度廓线")
        #self.plot_line(self.axList[0], LD_x, pressure,  color='#9400D3', label=u"露点温度")
        self.plot_line(self.axList[0], l2a_AT_x, pressure, color='orange', ls='--', label=u"温度数值预报廓线")
        #self.plot_line(self.axList[0], l2a_LD_x, pressure,  color='pink', ls='--', label=u"数值预报露点温度")
        #图二
        self.plot_line(self.axList[1], AH_x, pressure, color='g', label=u"湿度廓线")
        self.plot_line(self.axList[1], l2a_AH_x, pressure, color='orange', ls='--', label=u"湿度数值预报廓线")
        #图三
        self.plot_line(self.axList[2], AO_x, pressure, color='b', label=u"臭氧廓线")
        self.plot_line(self.axList[2], l2a_AO_x, pressure, color='orange', ls='--', label=u"臭氧数值预报廓线")

        self.xlim(self.axList[0], AT_xlim[0], AT_xlim[1])
        self.xlim(self.axList[1], AH_xlim[0], AH_xlim[1])
        self.xlim(self.axList[2], AO_xlim[0], AO_xlim[1])

        self.set_StrFormatter(self.axList[1], '%d')
        # self.set_StrFormatter(self.axList[1], '%.3f')
        # self.set_StrFormatter(self.axList[1], '%d')

        #self.ylim(self.axList[0], 100, 1101)
        #self.ylim(self.axList[1], 100, 1101)
        #self.ylim(self.axList[2], 100, 1101)
        self.ylim(self.axList[0], 100, 1000)
        self.ylim(self.axList[1], 100, 1000)
        self.ylim(self.axList[2], 100, 1000)
        self.set_xlim_average(self.axList[0], 5)
        self.set_xlim_average(self.axList[1], 5)
        self.set_xlim_average(self.axList[2], 5)
        self.xlabel(self.axList[0], XabelString=u"温度廓线(K)")
        self.xlabel(self.axList[1], XabelString=u"湿度廓线(g/kg)")
        self.xlabel(self.axList[2], XabelString=u"臭氧廓线(ppmv)")

        self.setlegend(self.axList[0], loc='upper right')
        self.setlegend(self.axList[1], loc='upper right')
        self.setlegend(self.axList[2], loc='upper right')

        self.axList[0].set_yscale('log')#, nonposx='clip'
        self.axList[1].set_yscale('log')
        self.axList[2].set_yscale('log')
        self.axList[0].invert_yaxis()
        self.axList[1].invert_yaxis()
        self.axList[2].invert_yaxis()

        self.axList[0].xaxis.set_major_formatter(matplotlib.ticker.FormatStrFormatter("%d"))

        def log_10_product(x, pos):
            """The two args are the value and tick position.
            Label ticks with the product of the exponentiation"""
            if 10<x < 100:
                return ''
            else:
                return '%1i' % (x,)
        for ax_ind in range(3):
            #self.axList[ax_ind].yaxis.set_major_formatter(matplotlib.ticker.NullFormatter())
            #实际应显示 200, 500, 700, 850
            #self.axList[ax_ind].yaxis.set_minor_locator(matplotlib.ticker.LogLocator(subs=[150, 300, 500, 800]))
            #self.axList[ax_ind].yaxis.set_minor_locator(matplotlib.ticker.LogLocator(subs=[100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100]))
            self.axList[ax_ind].yaxis.set_minor_formatter(matplotlib.ticker.FuncFormatter(log_10_product))
            self.axList[ax_ind].yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(log_10_product))
            pass

        self.ylabel(self.axList[0], YabelString=u"气压(hPa)")

        new_out_file = ''
        # out_file = out_file.replace('AHProf', 'Prof')
        # out_file_list = out_file.split('.')
        # out_file_list.insert(-1, str(int(i)))
        # out_file_list.insert(-1, '.')
        # new_out_file = ''.join(out_file_list)
        # title = os.path.basename(new_out_file).split('.')[0]
        title = 'Prof%03d' %i

        if int(clm) == 0:
            title += ' clear'
        else:
            title += ' cloud'
        self.title_main(title)
        self.savefig(out_file)
        #imglist.append(new_out_file)

        if len(thumbnail) != 0:
            img = Image.open(new_out_file, mode='r')
            img = img.resize(thumbnail)
            filepathlist = new_out_file.split('.')
            newfilePath = []
            newfilePath.extend(filepathlist[:-1])
            newfilePath.append('_THUMB.')
            newfilePath.append(filepathlist[-1])
            newfilePath = ''.join(newfilePath)
            img.save(newfilePath)

            if self.debug:
                pass


    def getLDTemp(self, Temp, WV, pressure):
        '''
        获取露点温度数据
        '''

        LD_temp = np.ones(Temp.shape)
        LD_temp[LD_temp==1] = 0

        pressure.shape = WV.shape[0] ,1
        pressure = pressure.repeat(WV.shape[1], axis=1)
        Saturated_Vapor_Press = WV * pressure / 622.0
        DVP = np.log10(Saturated_Vapor_Press)
        for rownum, row in enumerate(Temp):
            for colnum, col in enumerate(row):
                if Temp[rownum][colnum] > 253.0:
                    if Saturated_Vapor_Press[rownum][colnum] > 123.3972 or Saturated_Vapor_Press[rownum][colnum] < 0.0636:
                        Temp_SVP_Water = 0
                    else:
                        Temp_SVP_Water= -22.5896152438 + DVP[rownum][colnum] *( 26.1012286592 + DVP[rownum][colnum]*( 3.0206720594+DVP[rownum][colnum]*( 0.370219024579+0.072838702401*DVP[rownum][colnum] ))) + 273.16
                else:
                    if Saturated_Vapor_Press[rownum][colnum] > 6.108 or Saturated_Vapor_Press[rownum][colnum] < 0.00001403:
                        Temp_SVP_Water = 0
                    else:
                        Temp_SVP_Water= -20.31888177+ DVP[rownum][colnum] *( 23.94167436+ DVP[rownum][colnum]*( 2.252719878+DVP[rownum][colnum]*( 0.1914055442+ 0.009636593860*DVP[rownum][colnum] ))) + 273.16

                if Temp_SVP_Water == 0:
                    Temp_SVP_Water = Temp[rownum][colnum] - 40

                LD_temp[rownum][colnum] = min([Temp_SVP_Water, Temp[rownum][colnum]])



        return LD_temp

    #--------------------------------------------------------------------------------
    def getMplCb(self, mpl_cb):
        '''
        将自定义的colorbar数据转换为matplotlib识别的数据。
        :param mpl_cb: 自定义colorbar数据
        :return: mpl 数据
        '''
        yl = 0.0
        yr = 1.0
        xl = mpl_cb[0][0]*1.0
        xr = mpl_cb[-1][0]*1.0
        necp = list()
        for item in mpl_cb:
            rgb = [i/255.0 for i in item[1]]
            k = (item[0] - xl)/(xr-xl)
            y = yl + (yr-yl)*k
            necp.append([k, rgb])

        return necp

    def title_main(self, mainTitle, size=16):
        self.Figure.suptitle(mainTitle, fontproperties=self.font, size=size)

    def savefig(self, *args, **kwargs):
        ''' #保存图形到文件 '''
        FigureCanvasAgg(self.Figure)
        self.Figure.savefig(*args,**kwargs)




def ReadNC(strFileName, strSDSName):
    if not os.path.isfile(strFileName):
        print("%s is exist, will be exist the code!!" %strFileName)
        exit(1)

    fi = netCDF4.Dataset(strFileName, 'r')
    data = fi.variables[strSDSName][:]
    fi.close()

    return np.array(data)


def DrawProf(L2AFileName, L2FileName):
    l2a_AT = ReadNC(L2AFileName, "tlev_nwp")
    l2a_AH = ReadNC(L2AFileName, "wlev_nwp")
    l2a_AO = ReadNC(L2AFileName, "o3lev_nwp")

    l2_AT = ReadNC(L2FileName, "AT_Prof")
    l2_AH = ReadNC(L2FileName, "AQ_Prof")
    l2_AO = ReadNC(L2FileName, "AO_Prof")
    Pressure = ReadNC(L2FileName, "Pressure")
    CLM = ReadNC(L2FileName, "CLM")

    print(l2_AT.shape)
    Level, Points = l2_AT.shape
    width = 1500
    height = 1000
    AH_xlim = [0, 30]
    AO_xlim = [-1.5, 3]
    AT_xlim = [180, 320]

    # l2a_AT[l2a_AT<AT_xlim[0]] = np.nan
    # l2a_AT[l2a_AT>AT_xlim[1]] = np.nan
    # l2a_AH[l2a_AH<AH_xlim[0]] = np.nan
    # l2a_AH[l2a_AH>AH_xlim[1]] = np.nan
    # l2a_AO[l2a_AO<AO_xlim[0]] = np.nan
    # l2a_AO[l2a_AO>AO_xlim[1]] = np.nan
    #
    # l2_AT[l2_AT<AT_xlim[0]] = np.nan
    # l2_AT[l2_AT>AT_xlim[1]] = np.nan
    # l2_AH[l2_AH<AH_xlim[0]] = np.nan
    # l2_AH[l2_AH>AH_xlim[1]] = np.nan
    # l2_AO[l2_AO<AO_xlim[0]] = np.nan
    # l2_AO[l2_AO>AO_xlim[1]] = np.nan

    l2a_AT[l2a_AT == -999999.0] = np.nan
    l2a_AH[l2a_AH == -999999.0] = np.nan
    l2a_AO[l2a_AO == -999999.0] = np.nan
    l2_AT[l2_AT == -999999.0] = np.nan
    l2_AH[l2_AH == -999999.0] = np.nan
    l2_AO[l2_AO == -999999.0] = np.nan

    myplot = Plot()
    for i in range(Points):
        outPicName = L2FileName.replace('.NC', "AHProf%03d.PNG" % (i + 1))
        # process_plot_avp(self, AT_x, LD_x, AH_x, AO_x, l2a_AT_x, l2a_LD_x, l2a_AH_x, l2a_AO_x, pressure, clm, width, height, AH_xlim, AO_xlim, AT_xlim, out_file, i, thumbnail)
        myplot.process_plot_avp(l2_AT[:, i], [], l2_AH[:, i], l2_AO[:, i], l2a_AT[:, i], [], l2a_AH[:, i], l2a_AO[:, i],
                                Pressure, CLM[i], width, height, AH_xlim, AO_xlim, AT_xlim,
                                outPicName, i, [])
        print(outPicName)


if __name__ == '__main__':
    L2AFileName = r'/WORK/home/qx-fy4/PGSDATA/FY4A/GIIRS/L2/L2A/FY4A-_GIIRS-_N_REGX_1047E_L2A_AVP-_MULT_NUL_20190505060000_20190505061044_016KM_030V1.NC'
    L2FileName = r'/WORK/home/qx-fy4/PGSDATA/FY4A/GIIRS/L2/COMB/FY4A-_GIIRS-_N_REGX_1047E_L2-_AVP-_MULT_NUL_20190505060000_20190505061044_016KM_030V1.NC'

    DrawProf(L2AFileName, L2FileName)



