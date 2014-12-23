#!/usr/bin/env python2.7

import time
import psutil
import sys
from progressbar import ProgressBar

bcolors = {
    'K' : '\033[90m',
    'R' : '\033[91m',
    'G' : '\033[92m',
    'B' : '\033[94m',
    'C' : '\033[96m',
    'M' : '\033[95m',
    'Y' : '\033[93m',
    'N' : '\033[0m'}

def main():
	cpus = []
	cores = psutil.cpu_count()

	mem = ProgressBar(1000, pos = 1, width = 0.5, ansi = True, fillchar = '#')
	mem.set_bar_color('G')
	mem.set_perc_color('B')
	mem.set_msg_color('Y')
	
	swp = ProgressBar(1000, pos = 2, width = 0.5, ansi = True, fillchar = '#')
	swp.set_bar_color('G')
	swp.set_perc_color('B')
	swp.set_msg_color('Y')
	
	tot = ProgressBar(1000, pos = (4 + cores), width = 0.5, ansi = True, fillchar = '#')
	tot.set_bar_color('G')
	tot.set_perc_color('B')
	tot.set_msg_color('M')
	
	start_alternate_screen()
	print '\033[?25l'

	mem.draw('RAM')
	swp.draw('Swap')
	
	for i in range(cores):
		cpus.append(ProgressBar(1000, pos = (4 + i), width = 0.5, ansi = True, fillchar = '#'))
		cpus[i].set_bar_color('G')
		cpus[i].set_perc_color('B')
		cpus[i].set_msg_color('M')
		cpus[i].draw('CPU #{}'.format(i + 1))
	
	tot.draw('Total CPU')
	
	start_alternate_screen()
	print '\033[?25l'
	
	try:
		while (True):
			mem.change_progress(psutil.virtual_memory().percent * 10)
			swp.change_progress(psutil.swap_memory().percent * 10)
	
			perc = psutil.cpu_percent(percpu = True)
			for i in range(cores):
				cpus[i].change_progress(perc[i] * 10)
	
			tot.change_progress(psutil.cpu_percent() * 10)

			print ''
			raw = psutil.boot_time()
			ut = conv_systime(time.time() - raw)
			print bcolors['G'] + 'System uptime: ' + bcolors['K'] + ut + bcolors['N']
	
			time.sleep(1)
	
	except KeyboardInterrupt:
		end_alternate_screen()
		print '\033[?25h'
		pass

def conv_systime(raw):
	m, s = divmod(raw, 60)
	h, m = divmod(m, 60)
	d, h = divmod(h, 24)
	return '{0:02d}d, {1:02d}:{2:02d}:{3:02d}'.format(int(d), int(h), int(m), int(s))

def start_alternate_screen():
    sys.stdout.write("\033[?1049h\033[H")
    sys.stdout.flush()

def end_alternate_screen():
    sys.stdout.write("\033[?1049l")
    sys.stdout.flush()

if __name__ == '__main__':
	main()