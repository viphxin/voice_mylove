#coding=utf-8
from django.http import HttpResponse
from django.conf import settings
import random, StringIO, os
def initCheckCodeVal(length=4):
    """
    @des: 获取验证码的值
    """
    codes = ['0','2','3','4','5','6','7','8','9',
	    'a','b','c','d','e','f','g','h','i','j',
	    'k','m','n','o','p','q','r','s','t','u',
	    'v','w','x','y','z','A','B','C','D','E',
	    'F','G','H','I','J','K','L','M','N','O',
	    'P','Q','R','S','T','U','V','W','X','Y', 'Z']
    code_list = []
    code_str = ''
    for i in range(0,length):
        temp = codes[random.randint(0,59)]
        code_list.append(temp)
        code_str+=temp

    return {'clist':code_list, 'cstr':code_str}

def getCheckCodeImage(request):
	try:
		import Image
		import ImageDraw
		import ImageFont
	except ImportError:
		from PIL import Image, ImageDraw, ImageFont
	#验证码的长度
	clength = 4
	#获取到验证码的值
	code_dict = initCheckCodeVal(clength)
	#取出列表类型的验证码值
	rand_list = code_dict['clist']
	#取出字符串类型的验证码值
	rand_str = code_dict['cstr']
	#设置字体,需设置的字体包simsun.ttc与python源码同级目录

	font = ImageFont.truetype(os.path.join(settings.STATIC_ROOT, "code.ttf"),random.randint(18,25))
	#Image背景颜色
	bg_color = (255,255,255)
	#Image的长和宽
	i_width,i_height = clength*30,40
	#初始化Image对象
	im = Image.new('RGB',(i_width,i_height),bg_color)
	draw = ImageDraw.Draw(im)

	for i in range(0,clength):
		in_x = 40+i*10+random.randint(1+i,7+i*2)
		in_y = random.randint(2,15)
		draw.text((in_x,5), rand_list[i],font=font,fill=(0,0,0))

	#随机设置干扰线
	for i in range(0,3):
		linecolor = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
		#都是随机的
		x1 = random.randint(0,10)
		x2 = random.randint(i_width-10,i_width)
		y1 = random.randint(5,i_height-5)
		y2 = random.randint(5,i_height-5)
		draw.line([(x1, y1), (x2, y2)], linecolor)
	del draw
	#将验证码转换成小写的，并保存到session中
	request.session['checkcode'] = rand_str.lower()
	buf = StringIO.StringIO()
	#将image信息保存到StringIO流中
	im.save(buf, 'gif')
	return HttpResponse(buf.getvalue(),'image/gif')