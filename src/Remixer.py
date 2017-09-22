import sys

from pydub import AudioSegment

class Remixer:
	
	def __init__(self, file, sample1_start, sample2_start, sample3_start):
		self.bg_music = AudioSegment.from_file("Funtastic_Power_-_300_This_is_Sparta_EXTENDED_instrumental.mp3")
		self.sample = AudioSegment.from_file(file)
		self.main_sounds = []
		self.long_sounds = []
		
		sample_starts = [sample1_start, sample2_start, sample3_start]
		
		for start in sample_starts:
			self.main_sounds.append(self.sample[start:start+107.1])
			self.long_sounds.append(self.sample[start:start+429])
		
		
	def remix(self, epicness=False, export=None):	
		song = AudioSegment.silent(60)
		song += self.generate_intro()
		song += self.generate_hook()*2
		song += self.generate_verse()*6
		song += self.generate_hook()*4
		if epicness:
			song += self.generate_epicness()
		song += self.generate_hook()*4
		song = self.bg_music.overlay(song)
		if export is not None:
			song.export(export, format="wav")
		
		return song.raw_data
		
		
	def generate_section(self, pattern, long=False):
		section = AudioSegment.empty()	
		silence = AudioSegment.silent(len(self.main_sounds[0]))
		if long:
			silence = AudioSegment.silent(len(self.long_sounds[0]))
		for c in pattern:
			if c == ' ':
				section += silence
			else:
				section += self.long_sounds[int(c)-1] if long else self.main_sounds[int(c)-1]
				
		return section
		
	
	def generate_intro(self):
		return self.generate_section('1 2 3   ', True)
	
	
	def generate_verse(self):
		return self.generate_section('1233', True)
		
		
	def generate_hook(self):
		return self.generate_section('11 11 111 1 1 11222 2 222 222 2 ')
	
	
	def generate_epicness(self):
		epicness1 = self.generate_section('1   1 332 1 1 11  1 1 113 3 22221 3 1 332 1 1 111 11111111111111')
		epicness2 = self.generate_section('                                            3 3     3  3 3333 33')
		
		return epicness1.overlay(epicness2)
		
			
def main():
	if len(sys.argv) == 1:
		print("Missing sample file. Ex: Remixer.py meme.wav")
		return
		
	sample1_start = 1000 * float(input("Enter the start position (in seconds) of the first sound to use from the sample: "))
	sample2_start = 1000 * float(input("Enter the start position of the second sound to use: "))
	sample3_start = 1000 * float(input("Enter the start position of the third sound to use: "))
	
	r = Remixer(sys.argv[1], sample1_start, sample2_start, sample3_start)
	r.remix(True, "song.wav")

if __name__ == '__main__':
	main()