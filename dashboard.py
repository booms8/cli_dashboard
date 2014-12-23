#!/usr/bin/env python2.7

import time
import psutil
import sys
from progressbar import ProgressBar

mem = ProgressBar(1000, pos = 1, width = 0.5, ansi = True, fillchar = '#')
mem.set_bar_color('G')
mem.set_perc_color('B')
mem.set_msg_color('Y')

swp = ProgressBar(1000, pos = 2, width = 0.5, ansi = True, fillchar = '#')
swp.set_bar_color('G')
swp.set_perc_color('B')
swp.set_msg_color('Y')

cpus = []
cores = psutil.cpu_count()
for i in range(cores):
	cpus.append(ProgressBar(1000, pos = (3 + i), width = 0.5, ansi = True, fillchar = '#'))
	cpus[i].set_bar_color('G')
	cpus[i].set_perc_color('B')
	cpus[i].set_msg_color('M')
	cpus[i].draw('CPU #{}'.format(i + 1))

mem.draw('RAM')
swp.draw('Swap')

print '\033[?25l'

try:
	while (True):
		for i in range(cores):
			cpus[i].change_progress(psutil.cpu_percent(percpu = True)[i] * 10)

		mem.change_progress(psutil.virtual_memory().percent * 10)
		swp.change_progress(psutil.swap_memory().percent * 10)
		time.sleep(1)

except KeyboardInterrupt:
	print '\033[?25h'
	pass
