import pdb

def rgb2hsl(r, g, b):
	cmax = max(r, g, b)
	cmin = min(r, g, b)
	pdb.set_trace()
	l = (cmax + cmin) / 2.0
	if cmax == cmin:
		h = s = 0
	else:
		d = float(cmax - cmin)
		if s > 0.5:
			s = d / (2 - cmax - cmin)
		else:
			s = d / (cmax - cmin)
		if cmax == r:
			if g < b:
				h = (g - b) / d + 6
			else:
				h = (g - b) / d
		elif cmax == g:
			h = (b - r) / d + 2
		elif cmax == b:
			h = (r - g) / d + 4
		h /= 6.0
	return h, s, l

def hsl2rgb(h, s, l):
	if(s == 0):
		r = g = b = l; # achromatic
	else:
		if l < 0.5:
			q = l * (1 + s)
		else:
			q = l + s - l * s
		p = 2 * l - q;
		r = hue2rgb(p, q, h + 1.0/3.0)
		g = hue2rgb(p, q, h);
		b = hue2rgb(p, q, h - 1.0/3.0)
	return (r, g, b);


def hue2rgb(p, q, t):
    if(t < 0.0):
    	t += 1.0
    if(t > 1.0):
     	t -= 1.0
    if(t < 1.0/6.0):
    	return p + (q - p) * 6.0 * t
    if(t < 1.0/2.0):
    	return q
    if(t < 2.0/3.0):
    	return p + (q - p) * (2.0/3.0 - t) * 6.0
    return p
